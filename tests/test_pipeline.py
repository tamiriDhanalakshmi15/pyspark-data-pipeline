
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_csv(filename):
    with open(
        ROOT / "output" / filename,
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


class TestPipeline(unittest.TestCase):

    def test_data_quality(self):
        valid = read_csv("valid_records.csv")
        invalid = read_csv("invalid_records.csv")

        self.assertEqual(len(valid), 99500)
        self.assertEqual(len(invalid), 500)
        self.assertEqual(len(valid) + len(invalid), 100000)

    def test_customer_count(self):
        baseline = read_csv("baseline_result.csv")
        optimized = read_csv("optimized_result.csv")

        self.assertEqual(len(baseline), 10000)
        self.assertEqual(len(optimized), 10000)

    def test_pipeline_match(self):
        baseline = read_csv("baseline_result.csv")
        optimized = read_csv("optimized_result.csv")

        baseline = {
            row["customer_id"]: row for row in baseline
        }

        optimized = {
            row["customer_id"]: row for row in optimized
        }

        self.assertEqual(baseline.keys(), optimized.keys())

        for customer_id in baseline:
            b = baseline[customer_id]
            o = optimized[customer_id]

            self.assertAlmostEqual(
                float(b["total_amount"]),
                float(o["total_amount"]),
                delta=0.01
            )

            self.assertEqual(
                int(b["total_transactions"]),
                int(o["total_transactions"])
            )

            self.assertEqual(
                int(b["product_categories"]),
                int(o["product_categories"])
            )


if __name__ == "__main__":
    unittest.main()
