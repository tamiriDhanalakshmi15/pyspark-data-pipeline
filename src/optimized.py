
import csv
import os
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as spark_sum, count, countDistinct, broadcast
)
from pyspark.sql.window import Window

start_time = time.time()

spark = SparkSession.builder \
    .appName("Optimized Pipeline") \
    .master("local[*]") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# 1. Read datasets
df = spark.read.csv(
    "data/transactions.csv",
    header=True,
    inferSchema=True
)

products = spark.read.csv(
    "data/products.csv",
    header=True,
    inferSchema=True
)

# 2. Identify duplicate transaction IDs
window = Window.partitionBy("transaction_id")

checked_df = df.withColumn(
    "id_count", count("*").over(window)
)

# 3. Clean invalid records
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

# 4. Repartition by customer ID
partitioned_df = clean_df.repartition(8, "customer_id")

# 5. Broadcast join with small product dataset
joined_df = partitioned_df.join(
    broadcast(products),
    on="product_id",
    how="inner"
)

# 6. Display optimized execution plan
print("\n========== OPTIMIZED EXECUTION PLAN ==========")
joined_df.explain("formatted")

# 7. Aggregate customer transactions
result = joined_df.groupBy("customer_id").agg(
    spark_sum("amount").alias("total_amount"),
    count("transaction_id").alias("total_transactions"),
    countDistinct("category").alias("product_categories")
)

# 8. Save output
os.makedirs("output", exist_ok=True)

output_file = "output/optimized_result.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(result.columns)

    for row in result.toLocalIterator():
        writer.writerow(row)

execution_time = time.time() - start_time

# 9. Display pipeline metrics
print("\n--------------------------------")
print("OPTIMIZED PIPELINE COMPLETED")
print("--------------------------------")

print("Total input records:", df.count())
print("Valid records:", clean_df.count())
print("Customer records:", result.count())
print("Execution time:", round(execution_time, 2), "seconds")
print("Join strategy: BROADCAST JOIN")
print("Partitions: 8")
print("Output saved:", output_file)

print("--------------------------------")

spark.stop()
