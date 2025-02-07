import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType, TimestampType

def calculate_sum(input_uri: str, output_uri: str):
    """ Calculates the total taxi fares in USD per vendor

    Args:
        input_uri (str): Input parquet file S3 URI
        output_uri (str): Output folder S3 URI
    """

    spark = SparkSession.builder.appName("Calculate Average Trip Distance").getOrCreate()

    # Define the schema for better performance
    schema = StructType([
    StructField("VendorID", IntegerType(), True),
    StructField("tpep_pickup_datetime", TimestampType(), True),
    StructField("tpep_dropoff_datetime", TimestampType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", DoubleType(), True),
    StructField("pickup_longitude", DoubleType(), True),
    StructField("pickup_latitude", DoubleType(), True),
    StructField("RatecodeID", IntegerType(), True),
    StructField("store_and_fwd_flag", StringType(), True),
    StructField("dropoff_longitude", DoubleType(), True),
    StructField("dropoff_latitude", DoubleType(), True),
    StructField("payment_type", IntegerType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("extra", DoubleType(), True),
    StructField("mta_tax", DoubleType(), True),
    StructField("tip_amount", DoubleType(), True),
    StructField("tolls_amount", DoubleType(), True),
    StructField("improvement_surcharge", DoubleType(), True),
    StructField("total_amount", DoubleType(), True)
])

    df = spark.read.schema(schema).parquet(input_uri)

    # Compute average trip_distance per VendorID
    result = df.groupBy("VendorID").agg(sum("total_amount").alias("Total USD"))

    # Write the result to the specified output_uri
    result.write.mode("overwrite").csv(output_uri, header=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_uri')
    parser.add_argument('--output_uri')
    args = parser.parse_args()

    calculate_sum(args.input_uri, args.output_uri)