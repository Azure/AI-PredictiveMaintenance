import sys
import json

from functools import reduce
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import udf, mean, lit, stddev
from pyspark.sql.types import DoubleType
import pandas as pd
from collections import OrderedDict
from datetime import date

from pyspark.ml.feature import StringIndexer, VectorAssembler, VectorIndexer
from pyspark.ml import PipelineModel

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("AvroKeyInputFormat")\
        .getOrCreate()

    wasbUrlInput = sys.argv[1]
    wasbUrlOutput = sys.argv[2]
    storageAccountName = sys.argv[3]
    storageAccountKey = sys.argv[4]

    sc = spark.sparkContext

    hc = sc._jsc.hadoopConfiguration()
    hc.set("avro.mapred.ignore.inputs.without.extension", "false")
    hc.set("fs.azure.account.key.{}.blob.core.windows.net".format(storageAccountName), storageAccountKey)
    
    sql = SQLContext(sc)

    df = sql.read.format("com.databricks.spark.avro").load(wasbUrlInput)
        
    def g(c):
        return udf(lambda x: float(json.loads(bytes(x).decode("utf-8"))[c]), DoubleType())
    
    # WARNING: this is a very crude approximation of the feature data for demo purposes only.
    # As of right now, this code demonstrates how to access the input dataset in AVRO format,
    # transform it, perform batch scoring, and publish final results to a storage blob.
    features_df = (df
        .withColumn('machineID', df.SystemProperties['connectionDeviceId'])
        .withColumn('volt', g('volt')(df.Body))
        .withColumn('rotate', g('rotate')(df.Body))
        .withColumn('pressure', g('pressure')(df.Body))
        .withColumn('vibration', g('vibration')(df.Body))
        .drop('Properties', 'SystemProperties', 'Body')
        .groupBy('machineID')
        .agg(
            mean('volt').alias('volt_rollingmean_12'),
            mean('rotate').alias('rotate_rollingmean_12'),
            mean('pressure').alias('pressure_rollingmean_12'),
            mean('vibration').alias('vibration_rollingmean_12'),
            mean('volt').alias('volt_rollingmean_24'),
            mean('rotate').alias('rotate_rollingmean_24'),
            mean('pressure').alias('pressure_rollingmean_24'),
            mean('vibration').alias('vibration_rollingmean_24'),
            mean('volt').alias('volt_rollingmean_36'),
            mean('rotate').alias('rotate_rollingmean_36'),
            mean('pressure').alias('pressure_rollingmean_36'),
            mean('vibration').alias('vibration_rollingmean_36'),
            stddev('volt').alias('volt_rollingstd_12'),
            stddev('rotate').alias('rotate_rollingstd_12'),
            stddev('pressure').alias('pressure_rollingstd_12'),
            stddev('vibration').alias('vibration_rollingstd_12'),
            stddev('volt').alias('volt_rollingstd_24'),
            stddev('rotate').alias('rotate_rollingstd_24'),
            stddev('pressure').alias('pressure_rollingstd_24'),
            stddev('vibration').alias('vibration_rollingstd_24'),
            stddev('volt').alias('volt_rollingstd_36'),
            stddev('rotate').alias('rotate_rollingstd_36'),
            stddev('pressure').alias('pressure_rollingstd_36'),
            stddev('vibration').alias('vibration_rollingstd_36'),
        )
        .withColumn('age', lit(9))
        .withColumn('comp1sum', lit(0.0))
        .withColumn('comp2sum', lit(0.0))
        .withColumn('comp3sum', lit(0.0))
        .withColumn('comp4sum', lit(0.0))
        .withColumn('error1sum_rollingmean_24', lit(0.0))
        .withColumn('error2sum_rollingmean_24', lit(0.0))
        .withColumn('error3sum_rollingmean_24', lit(0.0))
        .withColumn('error4sum_rollingmean_24', lit(0.0))
        .withColumn('error5sum_rollingmean_24', lit(0.0))
    )

    pipeline = PipelineModel.load('/mnt/model')

    key_cols =['label_e','machineID','dt_truncated', 'failure','model_encoded','model' ]

    input_features = features_df.columns

    # Remove the extra stuff if it's in the input_df
    input_features = [x for x in input_features if x not in set(key_cols)]
    va = VectorAssembler(inputCols=(input_features), outputCol='features')
    data = va.transform(features_df).select('machineID','features')
    scores_df = pipeline.transform(data).select('machineID', 'prediction')    

    scores_df\
        .orderBy('machineID')\
        .coalesce(1)\
        .write.format("com.databricks.spark.csv")\
        .option("header", "true")\
        .mode('overwrite')\
        .save(wasbUrlOutput)
