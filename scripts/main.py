# Copyright 2022 Google LLC.
# SPDX-License-Identifier: Apache-2.0
import sys
from pyspark.sql import SparkSession
from delta import *


#pip install delta-spark

def main():
    #input = sys.argv[1]
    OUTPUT = f"gs://output-dataproc-serveless"
    print("Starting job: GCS Bucket: ")
    builder = SparkSession\
        .builder\
        .appName("DeltaTest")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    
    data = spark.range(0, 500)
    data.write.format("delta").mode("append").save()
    df = spark.read \
    .format("delta") \
    .load(input)
    df.show()
    spark.stop()

if __name__ == "__main__":
    main()