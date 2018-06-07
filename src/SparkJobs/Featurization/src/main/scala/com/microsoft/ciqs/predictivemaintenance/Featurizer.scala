package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.ciqs.predictivemaintenance.Definitions._
import org.apache.spark.eventhubs.{ConnectionStringBuilder, EventHubsConf, EventPosition}
import org.apache.spark.sql.{ForeachWriter, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.{GroupState, GroupStateTimeout, OutputMode}
import org.apache.spark.sql.types._
import org.apache.spark.sql.Row
import com.microsoft.azure.storage.table.{CloudTableClient, TableOperation, CloudTable}

object Featurizer {
  val futureTimestamp = new Timestamp(6284160000000L)
  val cycleGapMs = 30 * 1000;

  def main(args: Array[String]) {
    val endpoint = args(0)
    val eventHubName = args(1)
    val storageAccountConnectionString = args(2)

    def getCycleIntervalsStateful(machineID: DeviceId,
                                  inputs: Iterator[Signal],
                                  groupState: GroupState[CycleInterval]): Iterator[CycleInterval] = {
      if (groupState.hasTimedOut) {
        assert(inputs.isEmpty)
        val state = groupState.get
        groupState.remove()
        Iterator(state)
      } else {
        val timestamps = inputs.map(x => x.timestamp)
        val first = timestamps.next()
        val augmented = Seq(first) ++ timestamps ++ Seq(futureTimestamp)

        val intervals = (first :: augmented.sliding(2)
          .map(x => (x(0), x(1).getTime - x(0).getTime))
          .filter(_._2 > cycleGapMs).map(_._1).toList
          ).sliding(2).toList.reverse

        val latest :: tail = intervals

        groupState.setTimeoutTimestamp(latest(1).getTime, "30 seconds")
        //groupState.setTimeoutDuration("30 seconds")

        if (groupState.exists) {
          val state = groupState.get
          if (latest(0).getTime - state.end.getTime < cycleGapMs) {
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

   val connectionString = ConnectionStringBuilder(endpoint)
     .setEventHubName(eventHubName)
     .build

    val spark = SparkSession
      .builder
      .appName("StructuredNetworkWordCount").master("local[2]")
      .getOrCreate()

    import spark.implicits._

    val ehConf = EventHubsConf(connectionString)
      .setStartingPosition(EventPosition.fromStartOfStream)

    val schemaTyped = new StructType()
      //.add("timestamp", TimestampType)
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
      .withWatermark("timestamp", "1 days")
      .as[Signal]

    val telemetryByDevice = telemetry.withWatermark("timestamp", "30 seconds").groupByKey(_.machineID)

    val cycleIntervals = telemetryByDevice.
      flatMapGroupsWithState(
        outputMode = OutputMode.Append,
        timeoutConf = GroupStateTimeout.EventTimeTimeout)(func = getCycleIntervalsStateful).
      withColumnRenamed("machineID", "renamed_machineID").
      withWatermark("start", "1 days").
      withWatermark("end", "1 days")

    var cycleAggregates = cycleIntervals.
      join(telemetry,
        $"renamed_machineID" === $"machineID" &&
          $"start" < $"timestamp" &&
          $"end" >= $"timestamp", "leftOuter").
      groupBy("machineID", "start", "end").
      agg(
        max("speed_desired").alias("speed_desired_max"),
        avg("speed").alias("speed_avg"),
        avg("temperature").alias("temperature_avg"),
        max("temperature").alias("temperature_max"),
        avg("pressure").alias("pressure_avg"),
        max("pressure").alias("pressure_max"),
        min("timestamp").alias("cycle_start"),
        max("timestamp").alias("cycle_end"),
        count(lit(1)).alias("raw_count")
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
        if (value.getPartitionKey != null) {
          val insertCycleAggregates = TableOperation.insertOrReplace(value)
          tableReference.execute(insertCycleAggregates)
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
