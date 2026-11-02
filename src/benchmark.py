
import subprocess
import statistics
import re
import csv
import os
import sys

def run_pipeline(script):
    print(f"\nRunning {script}...")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"{script} failed")

    match = re.search(
        r"Execution time:\s*([\d.]+)\s*seconds",
        result.stdout
    )

    if not match:
        raise RuntimeError("Execution time not found")

    return float(match.group(1))


baseline_times = []
optimized_times = []

runs = 3

for i in range(runs):
    print(f"\n========== RUN {i + 1} ==========")

    baseline_times.append(
        run_pipeline("src/baseline.py")
    )

    optimized_times.append(
        run_pipeline("src/optimized.py")
    )

baseline_avg = statistics.mean(baseline_times)
optimized_avg = statistics.mean(optimized_times)

speedup = baseline_avg / optimized_avg
improvement = (
    (baseline_avg - optimized_avg) / baseline_avg
) * 100

os.makedirs("output", exist_ok=True)

with open("output/benchmark_report.csv", "w", newline="",
          encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Pipeline", "Run 1", "Run 2", "Run 3", "Average Seconds"
    ])

    writer.writerow([
        "Baseline", *baseline_times, round(baseline_avg, 2)
    ])

    writer.writerow([
        "Optimized", *optimized_times, round(optimized_avg, 2)
    ])

print("\n========== FINAL BENCHMARK ==========")
print("Baseline average:", round(baseline_avg, 2), "seconds")
print("Optimized average:", round(optimized_avg, 2), "seconds")
print("Speedup:", round(speedup, 2), "x")
print("Time reduction:", round(improvement, 2), "%")
print("Report saved: output/benchmark_report.csv")
