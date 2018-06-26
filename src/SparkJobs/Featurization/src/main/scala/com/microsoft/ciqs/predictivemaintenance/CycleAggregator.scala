package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.azure.storage.table._
import com.microsoft.ciqs.predictivemaintenance.Definitions._
import org.apache.spark.eventhubs.{EventHubsConf, EventPosition}
import org.apache.spark.sql.{ForeachWriter, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.{GroupState, GroupStateTimeout, OutputMode}
import org.apache.spark.sql.types._
import scala.util.parsing.json._

// Companion object
object CycleAggregator {
  def getIntervalsFromTimeSeries(timestamps: Iterator[Timestamp], cycleGapMs: Int) = {
    val first = timestamps.next()
    val augmented = Seq(first) ++ timestamps ++ Seq(FAR_FUTURE_TIMESTAMP)

    ((first, first) :: augmented.sliding(2)
      .map(x => (x(0), x(1), x(1).getTime - x(0).getTime))
      .filter(_._3 > cycleGapMs).map(x => (x._1, x._2)).toList)
      .sliding(2).map(x => List(x(0)._2, x(1)._1)).toList.reverse
  }

  def getCycleIntervalsStateful(machineID: String,
                                inputs: Iterator[TelemetryEvent],
                                groupState: GroupState[CycleInterval]): Iterator[CycleInterval] = {
    if (groupState.hasTimedOut) {
      assert(inputs.isEmpty)
      val state = groupState.get
      groupState.remove()
      Iterator(state)
    } else {
      // According to https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c,
      // IoT Hub partitions messages by deviceId;
      // https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-programming-guide suggests that
      // message order is maintained within one partition. Therefore, it is assumed that messages are
      // in the order they were sent to the Event Hub.
      val timestamps = inputs.map(x => x.timestamp) //.toSeq.sortWith(_.before(_)).iterator

      val latest :: tail = getIntervalsFromTimeSeries(timestamps, DEFAULT_CYCLE_GAP_MS)

      groupState.setTimeoutTimestamp(latest(1).getTime, "15 minutes")

      if (groupState.exists) {
        val state = groupState.get
        if (latest(0).getTime - state.end.getTime < DEFAULT_CYCLE_GAP_MS) {
          groupState.update(CycleInterval(state.start, latest(1), machineID))
          Iterator(groupState.get)
        } else {
          groupState.update(CycleInterval(latest(0), latest(1), machineID))
          Iterator(state)
        }
      } else {
        groupState.update(CycleInterval(latest(0), latest(1), machineID))
        tail.map(x => CycleInterval(x(0), x(1), machineID)).iterator
      }
    }
  }

  def getUpdatedRollingWindow(windowJson: String, newTimestamp: String, windowLength: Int) = {
    val currentWindow = JSON.parseFull(windowJson) match {
      case Some(l: List[Any]) => l.map(_.toString)
      case _ => List[String]()
    }

    if (currentWindow.contains(newTimestamp)) {
      (true, currentWindow)
    } else {
      val newWindow = (newTimestamp::currentWindow).sorted(Ordering.String.reverse).take(windowLength)
      (currentWindow != newWindow, newWindow)
    }
  }
}


class CycleAggregator(spark: SparkSession,
                      storageAccountConnectionString: String,
                      eventHubConnectionString: String) extends Runnable with Serializable {
  def run: Unit = {
    val sc = spark.sparkContext
    sc.setLogLevel("WARN")

    import spark.implicits._

    val ehConf = EventHubsConf(eventHubConnectionString)
      .setConsumerGroup("sparkconsumergroup")
      .setStartingPosition(EventPosition.fromStartOfStream)

    val schemaTyped = new StructType()
      .add("ambient_pressure", DoubleType)
      .add("ambient_temperature", DoubleType)
      .add("machineID", StringType)
      .add("timestamp", TimestampType)
      .add("pressure", DoubleType)
      .add("speed", DoubleType)
      .add("speed_desired", LongType)
      .add("temperature", DoubleType)

    val telemetry = spark
      .readStream
      .format("eventhubs")
      .options(ehConf.toMap)
      .load()
      //.withColumn("timestamp", col("enqueuedTime"))
      .withColumn("BodyJ", from_json($"body".cast(StringType), schemaTyped))
      .select("*", "BodyJ.*")
      .withWatermark("timestamp", "2 hours")
      .as[TelemetryEvent]

    val telemetryByDevice = telemetry.groupByKey(_.machineID)

    val cycleIntervals = telemetryByDevice
      .flatMapGroupsWithState(
        outputMode = OutputMode.Append,
        timeoutConf = GroupStateTimeout.EventTimeTimeout)(func = CycleAggregator.getCycleIntervalsStateful)
      .withColumnRenamed("machineID", "renamed_machineID")
      //.withWatermark("start", "1 days")
      //.withWatermark("end", "1 days")

    var cycleAggregates = cycleIntervals.
      join(telemetry,
        $"renamed_machineID" === $"machineID" &&
          $"start" <= $"timestamp" &&
          $"end" >= $"timestamp", "leftOuter").
      groupBy("machineID", "start", "end").
      agg(
        max("speed_desired").alias("SpeedDesiredMax"),
        avg("speed").alias("SpeedAvg"),
        avg("temperature").alias("TemperatureAvg"),
        max("temperature").alias("TemperatureMax"),
        avg("pressure").alias("PressureAvg"),
        max("pressure").alias("PressureMax"),
        min("timestamp").alias("CycleStart"),
        max("timestamp").alias("CycleEnd"),
        count(lit(1)).alias("RawCount")
      )

    val writer = new ForeachWriter[CycleAggregates] {
      var tableReference: CloudTable = _

      override def open(partitionId: Long, version: Long) = {
        val storageAccount =  CloudStorageAccount.parse(storageAccountConnectionString)
        val tableClient = storageAccount.createCloudTableClient
        tableReference = tableClient.getTableReference("cycles")
        true
      }

      override def process(value: CycleAggregates) = {
        try {
          val retrieveIndexOperation = TableOperation.retrieve(INDEX_KEY, value.getPartitionKey, classOf[DynamicTableEntity])
          val existingIndex = tableReference.execute(retrieveIndexOperation).getResultAsType[DynamicTableEntity]

          val (index, updateIndexOperation) = Option(existingIndex) match {
            case Some(entity) => (entity, TableOperation.replace(entity))
            case None => {
              val newIndex = new DynamicTableEntity(INDEX_KEY, value.getPartitionKey)
              (newIndex, TableOperation.insert(newIndex))
            }
          }

          val currentWindowJson = Option(index.getProperties.get("RollingWindow")) match {
            case Some(entity) => entity.getValueAsString
            case None => "[]"
          }

          val (isWindowUpdated, newWindow) = CycleAggregator.getUpdatedRollingWindow(currentWindowJson, value.CycleStart, LOOKBACK + 1)

          if (isWindowUpdated) {
            val newWindowJson = JSONArray(newWindow).toString()
            index.getProperties.put("RollingWindow", new EntityProperty(newWindowJson))

            val insertCycleAggregates = TableOperation.insertOrReplace(value)
            tableReference.execute(insertCycleAggregates)

            tableReference.execute(updateIndexOperation)
          }
        } catch {
          case e: TableServiceException => {
            if (e.getHttpStatusCode == 412 || e.getHttpStatusCode == 409) {
              process(value)
            }
          }
          case e: Exception => throw e
        }
      }

      override def close(errorOrNull: Throwable) = {}
    }

    val sq = cycleAggregates.
      as[CycleAggregates].
      writeStream.
      outputMode("update").
      foreach(writer).
      start()

    sq.awaitTermination()
  }
}
