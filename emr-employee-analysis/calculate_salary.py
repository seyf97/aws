import argparse
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, BooleanType

def calculate_salary(input_uri: str, output_uri: str) -> None:
    """Finds the youngest active employee with the highest salary among 1B employees

    Args:
        input_uri (str): S3 URI for input parquet files
        output_uri (str): S3 URI for the output
    """
    spark = SparkSession.builder.appName("Calculate Average Salary").getOrCreate()

    # Define schema for better performance
    schema = StructType([
    StructField("id", IntegerType(), False),      # Unique ID, required
    StructField("name", StringType(), True),      # Name, nullable
    StructField("age", IntegerType(), True),      # Age, nullable
    StructField("salary", DoubleType(), True),    # Salary with decimal precision
    StructField("is_active", BooleanType(), True) # Boolean flag for active status
])
    
    df = spark.read.schema(schema).parquet(input_uri)

    # Filter for active employees
    df_filtered = df.filter(df.is_active == True)

    # Get the youngest employee with the highest salary
    result = df_filtered.orderBy(df_filtered.salary.desc(), df_filtered.age.asc()).limit(1)

    # Write the result to the specified output URI
    result.write.mode("overwrite").csv(output_uri, header=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_uri')
    parser.add_argument('--output_uri')
    args = parser.parse_args()

    calculate_salary(args.input_uri, args.output_uri)