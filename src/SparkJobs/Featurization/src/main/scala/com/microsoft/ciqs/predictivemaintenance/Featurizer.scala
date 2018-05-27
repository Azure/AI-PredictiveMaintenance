package com.microsoft.ciqs.predictivemaintenance

import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql
import com.microsoft.azure.eventhubs._
import org.apache.spark.eventhubs.ConnectionStringBuilder
import org.apache.spark.eventhubs._
import scala.util.parsing.json._
import java.sql.Timestamp
import org.apache.spark.sql.streaming.{GroupState, GroupStateTimeout, OutputMode}
import Definitions._
import org.apache.spark.sql.streaming.{OutputMode, Trigger}
import scala.concurrent.duration._
import java.time.{LocalDate, LocalDateTime}
import org.apache.spark.sql.types._

object Featurizer {
  val futureTimestamp = new Timestamp(6284160000000L)
  val cycleGapMs = 30 * 1000;
    
  def main(args: Array[String]) {
      
      def findOperationalCycles(
        deviceId: DeviceId,
        inputs: Iterator[Signal],
        groupState: GroupState[CycleState]): Iterator[CycleInterval] = {
/*
      val state = if (groupState.exists) groupState.get else CycleState(new Timestamp(6284160000000L), new Timestamp(0), deviceId)

      val range = inputs.map(i => i.timestamp).foldLeft(
        (state.cycle_start, state.cycle_end))((acc, i) =>
        (if (i.before(acc._1)) i else acc._1, if (i.after(acc._2)) i else acc._2))

      if (groupState.hasTimedOut) {
        val state = groupState.get
        groupState.remove()
        Iterator(CycleInterval(range._1, range._2, deviceId)) //emit
      } else {
        groupState.update(CycleState(range._1, range._2, deviceId))
        groupState.setTimeoutTimestamp(range._2.getTime(), "30 seconds")
        Iterator(CycleInterval(range._1, range._2, deviceId))
        //Iterator()
      }
*/
        val timestamps = inputs.map(x => x.timestamp)
        val first = timestamps.next()
        val augmented = Seq(first) ++ timestamps ++ Seq(futureTimestamp)
        
        val intervals = (first :: augmented.sliding(2)
                         .map(x => (x(0), x(1).getTime() - x(0).getTime()))
                         .filter(_._2 > cycleGapMs).map(_._1).toList
                        ).sliding(2).toList.reverse

        val head :: tail = intervals
        
        tail.map(x => CycleInterval(x(0), x(1), deviceId)).iterator ++ Seq(CycleInterval(head(0), head(1), deviceId))
    }

    //     val without = "Endpoint=sb://iothub-ns-iothub-5tt-480165-0519bed52d.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=zkfIryYrIWjMqwfL8oOYadV71i6hfe/p+lQJuconBUU="
    //     var eventHubName = "iothub-5tto36p3klduc"

    //     val connectionString = ConnectionStringBuilder(without)
    //       .setEventHubName(eventHubName)
    //       .build

    val spark = SparkSession
      .builder
      .appName("StructuredNetworkWordCount").master("local[2]")
      .getOrCreate()

    val sqlContext = spark.sqlContext
    import sqlContext.implicits._ //sqlContext OR spark implicits

    //     val ehConf = EventHubsConf(connectionString)

    // val telemetry = spark.
    //     readStream.
    //     format("rate").
    //     option("rowsPerSecond", 1).
    //     load.
    //     withColumn("value", $"value" % 10).  // <-- randomize the values (just for fun)
    //     withColumn("deviceId", rint(rand() * 10) cast "int"). // <-- 10 devices randomly assigned to values
    //     as[Signal] // <-- convert to our type (from "unpleasant" Row)


    val schemaTyped = new StructType()
      .add("timestamp", TimestampType)
      .add("ambient_pressure", DoubleType)
      .add("ambient_temperature", DoubleType)
      .add("machineID", StringType)
      .add("pressure", DoubleType)
      .add("speed", DoubleType)
      .add("speed_desired", LongType)
      .add("temperature", DoubleType)


    val telemetry = spark.
      readStream.
      format("parquet").
      schema(schemaTyped).
      load("/home/andrew/work/streaming/input").
      withColumnRenamed("machineID", "deviceId").
      as[Signal]


    val telemetryByDevice = telemetry.withWatermark("timestamp", "30 seconds").
      groupByKey(_.deviceId)

    val cycleIntervals = telemetryByDevice.
      flatMapGroupsWithState(
        outputMode = OutputMode.Append,
        timeoutConf = GroupStateTimeout.EventTimeTimeout)(func = findOperationalCycles).withWatermark("cycle_end", "1 minutes")

    var cycleAggregates = cycleIntervals.as("a").
      join(telemetry.as("b"),
        $"a.deviceId" === $"b.deviceId" &&
          $"a.cycle_start" <= $"b.timestamp" &&
          $"a.cycle_end" >= $"b.timestamp").
      groupBy("a.deviceId", "a.cycle_start", "a.cycle_end").
      agg(
        max("b.speed_desired").alias("speed_desired_max"),
        avg("b.speed").alias("speed_avg"),
        avg("b.temperature").alias("temperature_avg"),
        max("b.temperature").alias("temperature_max"),
        avg("b.pressure").alias("pressure_avg"),
        max("b.pressure").alias("pressure_max"))


    val sq = cycleAggregates.
      writeStream.
      format("json").
      option("path", "/home/andrew/work/streaming/output").
      option("checkpointLocation", "/home/andrew/work/streaming/checkpoint").
      start()


    //val telemetry = spark.readStream.format("eventhubs").options(ehConf.toMap).load()


    //     val wordCounts = lines.withColumnRenamed("enqueuedTime", "timestamp").withColumn("machineID", lit("test")).as[InputRow].groupByKey(_.machineID) //.mapGroupsWithState()

    //     val query = wordCounts.writeStream
    //       .outputMode("append")
    //       .format("console")
    //       .start()

    sq.awaitTermination()
  }
}
