# AI Usage and Prompt History

## 1. AI Tools Used

I used ChatGPT as an AI assistant during the development of this PySpark Data Pipeline Optimization project.

I used it mainly to understand PySpark concepts, get beginner-friendly coding guidance, troubleshoot errors, and improve project documentation.

## 2. How I Used AI

I used ChatGPT for the following tasks:

- Understanding the project requirements and breaking the work into smaller steps.
- Setting up Python, Java, PySpark, and the virtual environment on Windows.
- Understanding how to generate synthetic transaction and product datasets.
- Developing data quality checks for missing values, invalid amounts, zero quantities, and duplicate transaction IDs.
- Understanding baseline and optimized PySpark pipelines.
- Learning about BroadcastHashJoin, repartitioning, shuffle partitions, and Adaptive Query Execution.
- Troubleshooting execution and testing errors.
- Preparing the README and GitHub documentation.
- Setting up Git and uploading the project to GitHub.

## 3. Representative Prompts Used

Some of the prompts and requests used during development included:

1. Help me build the PySpark data pipeline project step by step.
2. Explain how to install and configure PySpark on Windows.
3. Help me generate synthetic transaction and product datasets.
4. Help me identify invalid records and duplicate transaction IDs.
5. Help me create a baseline and optimized PySpark pipeline.
6. Explain broadcast joins, repartitioning, and shuffle optimization.
7. Help me compare baseline and optimized pipeline results.
8. Help me create automated tests for the project.
9. Help me troubleshoot Python and Git errors.
10. Help me prepare the README and GitHub repository.

This is a summary of representative prompts, not a complete verbatim transcript.

## 4. Where AI Helped

ChatGPT provided significant assistance with initial code structure, implementation guidance, debugging, explanations of Spark concepts, and documentation.

I relied on AI suggestions for several parts of the code and reviewed the suggested changes while building the project.

## 5. My Work and Validation

I personally worked through the project setup and execution using my Windows laptop and VS Code.

I:
- Created and configured the project environment.
- Created the project files and ran the Python scripts.
- Generated the synthetic datasets.
- Executed the data quality checks.
- Ran both baseline and optimized pipelines.
- Ran the performance benchmark.
- Executed the automated tests.
- Compared the outputs of both pipelines.
- Created the public GitHub repository and uploaded the project.

I verified that:
- The generated transaction dataset contains 100,000 records.
- The data quality checks identified 99,500 valid records and 500 invalid records.
- Both pipelines generated 10,000 customer records.
- The comparison reported zero mismatched customers.
- All three automated tests passed.
- The three-run local benchmark reported an average of 55.98 seconds for the baseline and 11.31 seconds for the optimized pipeline.

## 6. What I Learned

Through this project, I improved my understanding of PySpark, data cleaning, joins, partitioning, execution plans, performance benchmarking, automated testing, and GitHub.

I also learned that AI-generated suggestions need to be reviewed and tested before using them in a project.

## 7. Limitations

The project was developed and tested on a local Windows environment. The benchmark results may vary depending on hardware and execution conditions.

The synthetic dataset and local benchmark do not represent a production-scale distributed Spark environment.