
# PySpark Data Pipeline Optimization

## Project Overview

This project implements a scalable data processing pipeline using PySpark. It processes synthetic transaction data, identifies data-quality issues, joins transaction records with product information, and generates customer-level analytics.

The project compares a baseline pipeline with an optimized pipeline using Spark optimization techniques.

## Objectives

- Process a large synthetic transaction dataset.
- Identify and handle invalid records.
- Detect duplicate transaction IDs.
- Perform transaction and product data joins.
- Calculate customer-level transaction metrics.
- Optimize Spark execution using partitioning and broadcast joins.
- Compare baseline and optimized performance.
- Verify that both pipelines produce identical results.

## Technology Stack

- Python
- Apache Spark (PySpark 3.5.6)
- Pandas
- Java JDK 17
- CSV datasets
- Visual Studio Code

## Project Structure

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
│
├── README.md
└── requirements.txt
```

## Dataset Details

The project generates two synthetic datasets.

### Transactions Dataset

- 100,000 transaction records.
- Transaction ID
- Customer ID
- Product ID
- Amount
- Quantity
- Transaction status

### Products Dataset

- 500 product records.
- Product ID
- Product name
- Category

The dataset includes intentionally injected data-quality issues:

- Negative transaction amounts.
- Zero quantities.
- Missing customer IDs.
- Missing product IDs.
- Duplicate transaction IDs.

## Data Quality Results

| Metric | Result |
|---|---:|
| Total records | 100,000 |
| Valid records | 99,500 |
| Invalid records | 500 |
| Duplicate ID groups | 1 |
| Rows sharing duplicate IDs | 101 |

Invalid records are separated from valid records for further inspection.

## Pipeline Architecture

### 1. Data Generation

Generates synthetic transaction and product datasets.

### 2. Data Quality Validation

Checks missing values, negative amounts, zero quantities, and duplicate transaction IDs.

### 3. Baseline Pipeline

- Reads transaction and product datasets.
- Cleans invalid records.
- Performs a regular Spark join.
- Aggregates transaction data by customer.
- Saves customer-level results.

### 4. Optimized Pipeline

Uses the following optimization techniques:

- Broadcast Join for the small product dataset.
- Repartitioning using customer ID.
- Reduced shuffle partitions from 200 to 8.
- Adaptive Query Execution (AQE).
- Customer-level aggregation.

### 5. Output Validation

Compares baseline and optimized results to ensure that both pipelines produce identical customer-level metrics.

## Performance Benchmark

Three runs were performed for each pipeline.

| Metric | Baseline | Optimized |
|---|---:|---:|
| Average execution time | 55.98 sec | 11.31 sec |
| Join strategy | SortMergeJoin | BroadcastHashJoin |
| Shuffle partitions | 200 | 8 |

### Performance Improvement

- Speedup: 4.95x
- Execution time reduction: 79.8%
- Customer records: 10,000
- Mismatched customers: 0

These are observed results from a local Windows environment. Performance may vary with hardware and execution conditions.

## Execution Plan Analysis

The baseline pipeline uses:

`SortMergeJoin`

The optimized pipeline uses:

`BroadcastHashJoin`

The optimized plan broadcasts the small product dataset, avoiding the regular shuffle-based join of the baseline plan.

## Installation and Setup

Requirements:

- Python 3
- Java JDK 17
- VS Code

Install dependencies:

```bash
pip install -r requirements.txt
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

## How to Run

Generate datasets:

```bash
python src/generate_data.py
```

Run data-quality checks:

```bash
python src/data_quality.py
```

Run baseline pipeline:

```bash
python src/baseline.py
```

Run optimized pipeline:

```bash
python src/optimized.py
```

Compare pipeline outputs:

```bash
python src/compare.py
```

Run three-run performance benchmark:

```bash
python src/benchmark.py
```

## Conclusion

This project demonstrates how PySpark optimization techniques can improve data-processing performance while preserving output correctness.

The optimized pipeline achieved an observed 4.95x speedup compared with the baseline pipeline in a three-run local benchmark.

The project demonstrates practical experience with distributed data processing concepts, data-quality validation, join optimization, partitioning, performance measurement, and result verification.

## Future Improvements

- Test with larger datasets.
- Add automated unit tests.
- Add detailed data-quality error categories.
- Evaluate performance on a distributed Spark cluster.
- Explore additional Spark optimization techniques.
