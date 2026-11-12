"""Checks that every module produces the numbers the slides promise.

Run from the repo root:
    python3 -m unittest discover -s tests -v
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "transactions.csv"
M1 = ROOT / "modules" / "module-1" / "scripts" / "inspect_data.py"
M2 = ROOT / "modules" / "module-2" / "scripts" / "train.py"
M3 = ROOT / "modules" / "module-3" / "scripts" / "explain.py"


def run(*args, cwd):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd,
                          capture_output=True, text=True)


class CourseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_0_dataset_rebuilds_exactly(self):
        out = self.dir / "rebuilt.csv"
        r = run(ROOT / "data" / "make_data.py", "--out", out, cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(out.read_text(), DATA.read_text())

    def test_1_inspect(self):
        r = run(M1, "--input", DATA, "--out", "summary.json", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        s = json.loads((self.dir / "summary.json").read_text())
        self.assertEqual(s["rows"], 5000)
        self.assertEqual(s["missing_amount"], 83)
        self.assertEqual(s["fraud_rows"], 137)
        self.assertEqual(s["fraud_rate_pct"], 2.74)
        self.assertEqual(s["fraud_rate_by_merchant_pct"],
                         {"electronics": 4.6, "fuel": 2.1, "grocery": 2.1, "online": 3.2, "travel": 1.7})
        self.assertEqual(s["always_not_fraud_accuracy_pct"], 97.3)

    def test_1_missing_file_fails_loudly(self):
        r = run(M1, "--input", "data/missing.csv", cwd=self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("error: data/missing.csv not found. Are you in the repo root?", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_2_train(self):
        r = run(M2, "--input", DATA, "--out", "metrics.json", cwd=self.dir)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("loaded 5000 rows; 83 missing amounts", r.stdout)
        self.assertIn("3933 train rows · 984 test rows", r.stdout)
        m = json.loads((self.dir / "metrics.json").read_text())
        self.assertEqual((m["test_rows"], m["fraud_in_test"]), (984, 27))
        self.assertEqual(m["models"], {
            "always_not_fraud": {"accuracy": 0.973, "f1": 0.0},
            "logistic_regression": {"accuracy": 0.887, "f1": 0.302},
            "random_forest": {"accuracy": 0.921, "f1": 0.381},
        })

    def test_3_explain_offline(self):
        if not (self.dir / "metrics.json").exists():
            self.test_2_train()
        cases = [
            ([], "input_tokens=88 output_tokens=77 · cost $0.00142"),
            (["--input-rate", "1.00", "--output-rate", "5.00"], "input_tokens=88 output_tokens=77 · cost $0.00047"),
            (["--max-tokens", "60"], "input_tokens=88 output_tokens=60 · cost $0.00116"),
        ]
        for extra, expected in cases:
            r = run(M3, "--offline", *extra, cwd=self.dir)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn(expected, r.stdout)
        self.assertTrue((self.dir / "summary.md").exists())

    def test_3_no_key_fails_loudly(self):
        if not (self.dir / "metrics.json").exists():
            self.test_2_train()
        import os
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        r = subprocess.run([sys.executable, str(M3)], cwd=self.dir, env=env,
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ANTHROPIC_API_KEY is not set", r.stderr)


if __name__ == "__main__":
    unittest.main()
