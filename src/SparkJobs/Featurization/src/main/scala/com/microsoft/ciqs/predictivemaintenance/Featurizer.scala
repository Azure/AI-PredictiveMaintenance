package com.microsoft.ciqs.predictivemaintenance

import org.apache.spark.eventhubs.ConnectionStringBuilder
import org.apache.spark.sql.SparkSession

object Featurizer {
  def main(args: Array[String]) {
    val endpoint = args(0)
    val eventHubName = args(1)
    val storageAccountConnectionString = args(2)

    val spark = SparkSession
      .builder
      .appName("PredictiveMaintenanceFeaturizer") //.master("local[2]")
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
    augmenterThread.interrupt
  }
}
