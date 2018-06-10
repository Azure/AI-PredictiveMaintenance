package com.microsoft.ciqs.predictivemaintenance

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.ciqs.predictivemaintenance.Definitions._
import org.apache.spark.eventhubs.{ConnectionStringBuilder, EventHubsConf, EventPosition}
import org.apache.spark.sql.{ForeachWriter, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.{GroupState, GroupStateTimeout, OutputMode}
import org.apache.spark.sql.types._
import com.microsoft.azure.storage.table.{TableOperation, CloudTable}

object Featurizer {
  def main(args: Array[String]) {
    val endpoint = args(0)
    val eventHubName = args(1)
    val storageAccountConnectionString = args(2)

    val spark = SparkSession
      .builder
      .appName("PredictiveMaintenanceFeaturizer").master("local[2]")
      .getOrCreate()

    val sc = spark.sparkContext
    sc.setLogLevel("WARN")

    val eventHubConnectionString = ConnectionStringBuilder(endpoint)
      .setEventHubName(eventHubName)
      .build

    val cycleAggregator = new CycleAggregator(spark, storageAccountConnectionString, eventHubConnectionString)
    val augmenterThread = new Thread(new Augmenter(spark, storageAccountConnectionString))
    augmenterThread.start()

    cycleAggregator.run
    augmenterThread.join()
  }
}
