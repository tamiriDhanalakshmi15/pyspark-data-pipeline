# Technical Decisions and Project Reasoning

## 1. Problem Understanding

The goal of this project is to build a PySpark pipeline that processes transaction data, identifies data quality issues, joins transaction records with product information, and produces customer-level results.

I created two versions of the pipeline to compare normal Spark processing with an optimized approach.

## 2. Dataset Design

I generated two synthetic datasets:

- Transactions: 100,000 records.
- Products: 500 records.

I intentionally introduced invalid records to test the data quality checks.

These included negative amounts, zero quantities, missing customer IDs, missing product IDs, and duplicate transaction IDs.

**Reason:** A dataset containing only clean records would not properly test the validation logic.

## 3. Data Quality Decisions

I used PySpark DataFrame operations to identify invalid records.

The validation checks include:

- Missing required fields.
- Amounts less than or equal to zero.
- Quantities less than or equal to zero.
- Duplicate transaction IDs.

A window function groups records by transaction ID and identifies IDs that occur more than once.

Invalid records are separated from valid records so that they can be inspected independently.

## 4. Baseline Pipeline

The baseline pipeline uses a regular Spark join and the default shuffle partition configuration.

I disabled automatic broadcast joins and Adaptive Query Execution in the baseline configuration to make the comparison with the optimized pipeline clearer.

The execution plan showed a SortMergeJoin.

## 5. Optimization Decisions

### Broadcast Join

The product dataset contains only 500 records, while the transaction dataset contains 100,000 records.

I used a broadcast join to distribute the small product dataset to the workers instead of performing a regular shuffle-based join.

**Trade-off:** Broadcasting is useful for small datasets, but broadcasting a very large table can increase memory pressure.

### Repartitioning

I repartitioned the cleaned transaction data into 8 partitions using customer ID.

**Reason:** The final aggregation is performed using customer ID, so this partitioning is intended to support the customer-level processing.

**Trade-off:** Repartitioning itself involves data movement and may not improve performance in every workload.

### Shuffle Partitions

I configured the optimized pipeline to use 8 shuffle partitions instead of the default 200.

**Reason:** The local dataset and execution environment did not require 200 shuffle partitions.

**Trade-off:** Too few partitions can reduce parallelism for larger datasets. The appropriate number depends on data size and cluster resources.

### Adaptive Query Execution

I enabled Adaptive Query Execution in the optimized pipeline so Spark can adjust parts of the execution plan at runtime.

## 6. Benchmarking Approach

I executed the baseline and optimized pipelines three times each.

I calculated the average execution time for both versions.

| Metric | Baseline | Optimized |
|---|---:|---:|
| Average execution time | 55.98 seconds | 11.31 seconds |
| Join strategy | SortMergeJoin | BroadcastHashJoin |
| Configured shuffle partitions | 200 | 8 |

The measured results were:

- Speedup: 4.95x
- Execution time reduction: 79.8%

These results represent the combined effect of the optimization changes. They do not measure the independent contribution of each optimization.

The benchmark was performed locally on Windows, and execution times can vary depending on system resources and run conditions.

## 7. Testing and Validation

I used an automated Python unittest script to check the pipeline outputs.

The tests verify:

1. The number of valid and invalid records.
2. The number of customer records produced by both pipelines.
3. Whether customer-level amounts, transaction counts, and category counts match.

**Observed results:**

- Valid records: 99,500.
- Invalid records: 500.
- Baseline customer records: 10,000.
- Optimized customer records: 10,000.
- Mismatched customers: 0.
- Automated tests passed: 3 out of 3.

## 8. Limitations

- The datasets are synthetic and may not represent real-world transaction patterns.
- The project was tested on a local Windows environment, not on a distributed Spark cluster.
- Only a limited set of Spark optimization techniques was evaluated.
- The benchmark used three sequential runs and did not include a separate warm-up or randomized execution order.
- Performance may change with different dataset sizes, hardware, and Spark configurations.

## 9. Possible Improvements

- Test with larger datasets.
- Compare different partition counts.
- Measure the impact of each optimization separately.
- Add more detailed invalid-record reason reporting.
- Test on a distributed Spark cluster.
- Improve benchmark repeatability and reporting.

## 10. Conclusion

This project helped me understand how Spark join strategies, partitioning, and execution settings affect data processing.

The optimized pipeline produced matching customer-level results and achieved a measured 4.95x speedup in my local benchmark.