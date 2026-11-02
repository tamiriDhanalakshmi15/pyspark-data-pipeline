
import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

random.seed(42)

rows = 100000

# Generate transactions
data = {
    "transaction_id": list(range(1, rows + 1)),
    "customer_id": [random.randint(1, 10000) for _ in range(rows)],
    "product_id": [random.randint(1, 500) for _ in range(rows)],
    "amount": [round(random.uniform(10, 5000), 2) for _ in range(rows)],
    "quantity": [random.randint(1, 10) for _ in range(rows)],
    "status": [random.choice(["SUCCESS", "FAILED", "PENDING"]) for _ in range(rows)]
}

df = pd.DataFrame(data)

# Inject data quality issues
df.loc[0:99, "amount"] = -100
df.loc[100:199, "quantity"] = 0
df.loc[200:299, "customer_id"] = None
df.loc[300:399, "product_id"] = None

# Add duplicate transaction IDs
df.loc[400:499, "transaction_id"] = 1

df.to_csv("data/transactions.csv", index=False)

# Generate product dimension dataset
products = {
    "product_id": list(range(1, 501)),
    "product_name": [f"Product_{i}" for i in range(1, 501)],
    "category": [
        random.choice(["Electronics", "Clothing", "Food", "Books", "Home"])
        for _ in range(500)
    ]
}

product_df = pd.DataFrame(products)

product_df.to_csv("data/products.csv", index=False)

print("--------------------------------")
print("DATASETS GENERATED SUCCESSFULLY")
print("--------------------------------")
print("Transactions:", len(df))
print("Products:", len(product_df))
print("Negative amounts:", (df["amount"] <= 0).sum())
print("Zero quantities:", (df["quantity"] <= 0).sum())
print("Missing customer IDs:", df["customer_id"].isna().sum())
print("Missing product IDs:", df["product_id"].isna().sum())
print("Duplicate transaction IDs:", df["transaction_id"].duplicated().sum())
print("--------------------------------")
