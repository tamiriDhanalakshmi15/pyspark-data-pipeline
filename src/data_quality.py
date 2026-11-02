
import os
import csv

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Data Quality Checks") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read dataset
df = spark.read.csv(
    "data/transactions.csv",
    header=True,
    inferSchema=True
)

# Detect duplicate transaction IDs
window = Window.partitionBy("transaction_id")

checked_df = df.withColumn(
    "id_count",
    count("*").over(window)
)

# Identify all invalid records
invalid_condition = (
    col("transaction_id").isNull() |
    col("customer_id").isNull() |
    col("product_id").isNull() |
    col("amount").isNull() |
    col("quantity").isNull() |
    (col("amount") <= 0) |
    (col("quantity") <= 0) |
    (col("id_count") > 1)
)

invalid_df = checked_df.filter(invalid_condition).drop("id_count")
valid_df = checked_df.filter(~invalid_condition).drop("id_count")

# Count records
total_records = df.count()
valid_records = valid_df.count()
invalid_records = invalid_df.count()

duplicate_groups = checked_df.filter(
    col("id_count") > 1
).select("transaction_id").distinct().count()

duplicate_rows = checked_df.filter(
    col("id_count") > 1
).count()

# Save records
os.makedirs("output", exist_ok=True)

def save_csv(dataframe, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(dataframe.columns)

        for row in dataframe.toLocalIterator():
            writer.writerow(row)

save_csv(valid_df, "output/valid_records.csv")
save_csv(invalid_df, "output/invalid_records.csv")

# Quality report
print("--------------------------------")
print("DATA QUALITY REPORT")
print("--------------------------------")
print("Total records:", total_records)
print("Valid records:", valid_records)
print("Invalid records:", invalid_records)
print("Duplicate transaction ID groups:", duplicate_groups)
print("Rows with duplicate IDs:", duplicate_rows)
print("--------------------------------")
print("Valid records saved successfully")
print("Invalid records saved successfully")
print("--------------------------------")

spark.stop()
