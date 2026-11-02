
import csv
import os
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, countDistinct
from pyspark.sql.window import Window

start_time = time.time()

spark = SparkSession.builder \
    .appName("Baseline Pipeline") \
    .master("local[*]") \
    .config("spark.sql.autoBroadcastJoinThreshold", "-1") \
    .config("spark.sql.adaptive.enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read transactions and products
df = spark.read.csv("data/transactions.csv", header=True, inferSchema=True)
products = spark.read.csv("data/products.csv", header=True, inferSchema=True)

# Detect duplicate transactions
window = Window.partitionBy("transaction_id")

checked_df = df.withColumn(
    "id_count", count("*").over(window)
)

# Clean invalid records
clean_df = checked_df.filter(
    col("transaction_id").isNotNull() &
    col("customer_id").isNotNull() &
    col("product_id").isNotNull() &
    col("amount").isNotNull() &
    col("quantity").isNotNull() &
    (col("amount") > 0) &
    (col("quantity") > 0) &
    (col("id_count") == 1)
).drop("id_count")

# Normal join
joined_df = clean_df.join(products, on="product_id", how="inner")
print("\n========== BASELINE EXECUTION PLAN ==========")
joined_df.explain("formatted")

# Customer aggregation
result = joined_df.groupBy("customer_id").agg(
    sum("amount").alias("total_amount"),
    count("transaction_id").alias("total_transactions"),
    countDistinct("category").alias("product_categories")
)

# Save output
os.makedirs("output", exist_ok=True)

output_file = "output/baseline_result.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(result.columns)

    for row in result.toLocalIterator():
        writer.writerow(row)

execution_time = time.time() - start_time

print("--------------------------------")
print("BASELINE PIPELINE COMPLETED")
print("Total input records:", df.count())
print("Valid records:", clean_df.count())
print("Customer records:", result.count())
print("Execution time:", round(execution_time, 2), "seconds")
print("Join strategy: Normal join")
print("Output saved:", output_file)
print("--------------------------------")

spark.stop()
