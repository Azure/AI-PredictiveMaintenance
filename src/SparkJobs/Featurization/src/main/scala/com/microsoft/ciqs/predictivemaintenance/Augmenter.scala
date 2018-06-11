package com.microsoft.ciqs.predictivemaintenance

import com.microsoft.azure.storage.CloudStorageAccount
import com.microsoft.azure.storage.table.{DynamicTableEntity, TableOperation, TableQuery}
import com.microsoft.azure.storage.table.TableQuery.QueryComparisons
import com.microsoft.ciqs.predictivemaintenance.Definitions.{CycleAggregates, Features}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import com.microsoft.ciqs.predictivemaintenance.Definitions._

import scala.collection.JavaConverters._
import scala.collection.mutable
import scala.util.parsing.json.JSON

// Scheduling jobs from separate threads within the same Spark application is allowed:
// http://spark.apache.org/docs/latest/job-scheduling.html#scheduling-within-an-application
class Augmenter(spark: SparkSession, storageAccountConnectionString: String) extends Runnable {
  val sc = spark.sparkContext
  import spark.implicits._

  val storageAccount =  CloudStorageAccount.parse(storageAccountConnectionString)
  val tableClient = storageAccount.createCloudTableClient
  val cyclesTableReference = tableClient.getTableReference("cycles")
  val featuresTableReference = tableClient.getTableReference("features")
  val w = Window.partitionBy("machineID").rowsBetween(-LOOKBACK, Window.currentRow).orderBy("CycleStart")

  def augment(l: Iterable[CycleAggregates]) = {
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

  def run: Unit = {

    val partitionFilter = TableQuery.generateFilterCondition(
      PARTITION_KEY,
      QueryComparisons.EQUAL,
      INDEX_KEY)

    val indexQuery = TableQuery.from(classOf[DynamicTableEntity]).where(partitionFilter)

    var lastModified = mutable.HashMap[String, java.util.Date]()

    while (true) {
      val indices = cyclesTableReference.execute(indexQuery).asScala

      val indicesMap = indices.map(x => x.getRowKey -> x).toMap
        .filter(x => lastModified.contains(x._1) && lastModified(x._1).before(x._2.getTimestamp) || !lastModified.contains(x._1))

      indicesMap foreach {
        case (machineID, index) => {
          val rollingWindowJson = index.getProperties.get("RollingWindow").getValueAsString

          val currentWindow = JSON.parseFull(rollingWindowJson) match {
            case Some(l: List[Any]) => l.map(_.toString)
            case _ => List[String]()
          }

          val timestampTo = currentWindow.head
          val timestampFrom = currentWindow.last

          val partitionFilter = TableQuery.generateFilterCondition(
            PARTITION_KEY,
            QueryComparisons.EQUAL,
            machineID)

          val rangeFrom = TableQuery.generateFilterCondition(ROW_KEY, QueryComparisons.GREATER_THAN_OR_EQUAL, timestampFrom)
          val rangeTo = TableQuery.generateFilterCondition(ROW_KEY, QueryComparisons.LESS_THAN_OR_EQUAL, timestampTo)
          val combinedRowFilter = TableQuery.combineFilters(rangeFrom, TableQuery.Operators.AND, rangeTo)
          val filter = TableQuery.combineFilters(partitionFilter, TableQuery.Operators.AND, combinedRowFilter)

          val partitionQuery = TableQuery.from(classOf[CycleAggregates]).where(filter)

          val l = cyclesTableReference.execute(partitionQuery).asScala

          if (l.size >= LOOKBACK + 1) {
            if (l.size > LOOKBACK + 1) {
              // log warning
            }
            augment(l)
            lastModified += machineID -> index.getTimestamp
          }
        }
      }
      Thread.sleep(1000)
    }
  }
}
