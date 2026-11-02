# PySpark Data Pipeline Optimization

## 1. About the Project

This project is about building and improving a data processing pipeline using PySpark.

I created synthetic transaction and product datasets and used them to build two pipelines: a baseline version and an optimized version.

The pipeline checks data quality, removes invalid records, joins transaction data with product information, and calculates customer-level results.

I also compared the execution time of both pipelines to understand how Spark optimization techniques affect performance.

## 2. Project Objectives

- Generate transaction and product datasets.
- Find missing values and invalid records.
- Identify duplicate transaction IDs.
- Clean the data before processing.
- Join transaction and product datasets.
- Calculate total transaction amounts and other customer-level details.
- Improve performance using Spark optimization techniques.
- Compare both pipeline outputs and execution times.

## 3. Technologies Used

- Python
- PySpark 3.5.6
- Apache Spark
- Pandas
- Java JDK 17
- CSV files
- Visual Studio Code

## 4. Project Structure

```text
pyspark-data-pipeline/
│
├── data/
│   ├── transactions.csv
│   └── products.csv
│
├── output/
│   ├── valid_records.csv
│   ├── invalid_records.csv
│   ├── baseline_result.csv
│   ├── optimized_result.csv
│   └── benchmark_report.csv
│
├── src/
│   ├── generate_data.py
│   ├── data_quality.py
│   ├── baseline.py
│   ├── optimized.py
│   ├── compare.py
│   └── benchmark.py
│
├── tests/
│   └── test_pipeline.py
│
├── PROMPT_HISTORY.md
├── TECHNICAL_DECISIONS.md
├── README.md
├── requirements.txt
└── .gitignore
```

## 5. Dataset Information

I generated two datasets for this project.

### Transactions Dataset

Contains 100,000 transaction records with details such as:

- Transaction ID
- Customer ID
- Product ID
- Amount
- Quantity
- Transaction status

### Products Dataset

Contains 500 product records with:

- Product ID
- Product name
- Category

To test data cleaning, I also introduced some invalid records into the transaction dataset:

- Negative transaction amounts
- Zero quantities
- Missing customer IDs
- Missing product IDs
- Duplicate transaction IDs

## 6. Data Quality Results

After running the data quality checks, the results were:

| Metric | Result |
|---|---:|
| Total records | 100,000 |
| Valid records | 99,500 |
| Invalid records | 500 |
| Duplicate ID groups | 1 |
| Rows sharing duplicate IDs | 101 |

The valid and invalid records are saved separately in the output folder.

## 7. Pipeline Implementation

### Baseline Pipeline

The baseline pipeline performs the following operations:

1. Reads the transaction and product datasets.
2. Checks and removes invalid records.
3. Joins both datasets using a regular Spark join.
4. Groups the records by customer ID.
5. Calculates total amount, transaction count, and product category count.
6. Saves the results.

### Optimized Pipeline

I applied a few Spark optimization techniques to improve the pipeline:

- **Broadcast Join:** Used the small product dataset as a broadcast table to avoid a regular shuffle-based join.
- **Repartitioning:** Repartitioned the cleaned transaction data using customer ID.
- **Shuffle Partitions:** Reduced the configured shuffle partitions from 200 to 8.
- **Adaptive Query Execution:** Enabled AQE to allow Spark to optimize execution at runtime.

The optimized pipeline performs the same calculations as the baseline pipeline.

## 8. Performance Comparison

I executed both pipelines three times and compared their average execution times.

| Metric | Baseline | Optimized |
|---|---:|---:|
| Average execution time | 55.98 seconds | 11.31 seconds |
| Join strategy | SortMergeJoin | BroadcastHashJoin |
| Configured shuffle partitions | 200 | 8 |

### Results

- Average speedup: **4.95x**
- Execution time reduction: **79.8%**
- Customer records generated: **10,000**
- Mismatched customer records: **0**

These results were measured on my local Windows environment. Actual execution times may change depending on the system and Spark configuration.

The benchmark compares the combined effect of the optimization changes. It does not measure the individual contribution of each optimization technique separately.

## 9. Execution Plan Comparison

I used Spark's `explain("formatted")` method to inspect the execution plans.

The baseline pipeline uses `SortMergeJoin`, which involves shuffle and sorting operations.

The optimized pipeline uses `BroadcastHashJoin` because the product dataset is small enough to broadcast.

This reduces the join-related shuffle work and helps improve execution time.

## 10. How to Run the Project

### Requirements

- Python 3
- Java JDK 17
- Visual Studio Code

### Step 1: Clone the Repository

```powershell
git clone https://github.com/tamiriDhanalakshmi15/pyspark-data-pipeline.git
cd pyspark-data-pipeline
```

### Step 2: Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Generate Datasets

```powershell
python src/generate_data.py
```

### Step 6: Run Data Quality Checks

```powershell
python src/data_quality.py
```

### Step 7: Run Baseline Pipeline

```powershell
python src/baseline.py
```

### Step 8: Run Optimized Pipeline

```powershell
python src/optimized.py
```

### Step 9: Compare Both Pipelines

```powershell
python src/compare.py
```

### Step 10: Run Performance Benchmark

```powershell
python src/benchmark.py
```

### Step 11: Run Automated Tests

```powershell
python -m unittest discover -s tests -v
```

The automated tests check data quality counts, customer record counts, and whether both pipeline outputs match.

## 11. What I Learned

While working on this project, I got practical experience with:

- Reading and processing datasets using PySpark.
- Identifying and handling data quality issues.
- Joining datasets using Spark.
- Understanding broadcast joins and repartitioning.
- Reading Spark execution plans.
- Measuring and comparing execution times.
- Writing basic automated tests.

## 12. Future Improvements

Some improvements I would like to work on next:

- Test the pipeline with larger datasets.
- Add more detailed data quality reports.
- Improve the automated test coverage.
- Run the pipeline on a distributed Spark cluster.
- Explore more Spark performance optimization techniques.

## 13. Conclusion

Through this project, I built a PySpark pipeline that processes transaction data, checks data quality, and generates customer-level results.

I also created an optimized version and compared it with the baseline pipeline. In my local benchmark, the optimized version achieved a 4.95x speedup, while both versions produced matching results.

This project helped me understand how data processing, data quality checks, and Spark optimization techniques work in practice.

## 14. Additional Documentation

- [AI Usage and Prompt History](PROMPT_HISTORY.md)
- [Technical Decisions and Project Reasoning](TECHNICAL_DECISIONS.md)