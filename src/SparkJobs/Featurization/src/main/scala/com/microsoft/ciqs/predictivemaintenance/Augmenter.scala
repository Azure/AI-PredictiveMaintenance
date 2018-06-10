package com.microsoft.ciqs.predictivemaintenance

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.azure.storage.table.{TableOperation, TableQuery}
import com.microsoft.azure.storage.table.TableQuery.QueryComparisons
import com.microsoft.ciqs.predictivemaintenance.Definitions.{CycleAggregates, Features}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

import scala.collection.JavaConverters._

// Scheduling jobs from separate threads within the same Spark application is allowed:
// http://spark.apache.org/docs/latest/job-scheduling.html#scheduling-within-an-application
class Augmenter(spark: SparkSession, storageAccountConnectionString: String) extends Runnable {
  val PARTITION_KEY = "PartitionKey"

  def run: Unit = {
    val sc = spark.sparkContext
    import spark.implicits._

    val storageAccount =  CloudStorageAccount.parse(storageAccountConnectionString)
    val tableClient = storageAccount.createCloudTableClient
    val cyclesTableReference = tableClient.getTableReference("cycles")
    val featuresTableReference = tableClient.getTableReference("features")
    val lookback = 5
    val w = Window.partitionBy("machineID").rowsBetween(-lookback, Window.currentRow).orderBy("CycleStart")

    while (true) {
      val machineID = "MACHINE-000"

      val partitionFilter = TableQuery.generateFilterCondition(
        PARTITION_KEY,
        QueryComparisons.EQUAL,
        machineID)

      val partitionQuery = TableQuery.from(classOf[CycleAggregates]).where(partitionFilter)

      val l = cyclesTableReference.execute(partitionQuery).asScala

      val df = sc.parallelize(l.toSeq).toDF

      val rollingAverages = Seq("TemperatureAvg", "TemperatureMax", "PressureAvg", "PressureMax")

      val augmented_labeled_cycles_df = rollingAverages.foldLeft(df) {
        (_df, colName) => _df.withColumn(colName.concat("RollingAvg"), avg(colName).over(w))
      }.orderBy(desc("CycleStart")).limit(1).drop("RawCount")

      var nonFeatureColumns = Set("MachineID", "CycleStart", "CycleEnd")
      val featureColumns = augmented_labeled_cycles_df.columns.filterNot(c => nonFeatureColumns.contains(c))

      val obfuscateColumns = featureColumns zip (1 to featureColumns.length + 1)

      val features_df = obfuscateColumns.foldLeft(augmented_labeled_cycles_df) {
        (_df, c) => _df.withColumnRenamed(c._1, "s".concat(c._2.toString))
      }.as[Features]

      if (features_df.count() > 0) {
        val featuresJson = features_df.drop(nonFeatureColumns.toList: _*).toJSON.first()

        val features = features_df.first()
        features.FeaturesJson = featuresJson

        val insertFeatures = TableOperation.insertOrReplace(features)
        featuresTableReference.execute(insertFeatures)
      }
    }
  }
}
