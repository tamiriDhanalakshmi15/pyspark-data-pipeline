import csv
import os

def read_csv(file_path):
    data = {}
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            data[row["customer_id"]] = row
    return data

baseline = read_csv("output/baseline_result.csv")
optimized = read_csv("output/optimized_result.csv")

print("--------------------------------")
print("PIPELINE COMPARISON")
print("--------------------------------")

print("Baseline customers:", len(baseline))
print("Optimized customers:", len(optimized))

mismatches = []

for customer_id in baseline:
    if customer_id not in optimized:
        mismatches.append(customer_id)
        continue

    b = baseline[customer_id]
    o = optimized[customer_id]

    if (
        abs(float(b["total_amount"]) - float(o["total_amount"])) >= 0.01
        or int(b["total_transactions"]) != int(o["total_transactions"])
        or int(b["product_categories"]) != int(o["product_categories"])
    ):
        mismatches.append(customer_id)

print("Mismatched customers:", len(mismatches))

if not mismatches and baseline.keys() == optimized.keys():
    print("RESULT: BOTH PIPELINES MATCH")
else:
    print("RESULT: PIPELINES DO NOT MATCH")

print("--------------------------------")