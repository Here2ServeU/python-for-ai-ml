"""Module 1: inspect the dataset with plain Python (no extra packages).

Loads data/transactions.csv, counts rows, blanks and fraud, and saves a
summary to summary.json.

Run from the repo root:
    python3 modules/module-1/scripts/inspect_data.py
    python3 modules/module-1/scripts/inspect_data.py --input data/transactions.csv --out summary.json
"""
import argparse
import csv
import json
import sys


def load_rows(path):
    """Read the CSV into a list of dicts. Fail loudly, in plain words."""
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        sys.exit(f"error: {path} not found."
                 " Are you in the repo root?")


def fraud_rate(rows):
    """Share of rows where is_fraud is 1."""
    frauds = sum(int(r["is_fraud"]) for r in rows)
    return frauds / len(rows)


def summarize(rows):
    missing = [r for r in rows if r["amount"] == ""]   # blank cells come in as ""
    fraud_rows = [r for r in rows if r["is_fraud"] == "1"]

    by_merchant = {}
    for r in rows:
        by_merchant.setdefault(r["merchant"], []).append(r)

    rate = fraud_rate(rows)
    return {
        "rows": len(rows),
        "missing_amount": len(missing),
        "fraud_rows": len(fraud_rows),
        "fraud_rate_pct": round(100 * rate, 2),
        "fraud_rate_by_merchant_pct": {
            m: round(100 * fraud_rate(group), 1) for m, group in sorted(by_merchant.items())
        },
        # what a model that always says "not fraud" would score
        "always_not_fraud_accuracy_pct": round(100 * (1 - rate), 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Inspect the course dataset.")
    parser.add_argument("--input", default="data/transactions.csv", help="CSV file to inspect")
    parser.add_argument("--out", default="summary.json", help="where to save the summary")
    args = parser.parse_args()

    rows = load_rows(args.input)
    if not rows:
        sys.exit(f"error: {args.input} has no data rows.")
    needed = {"amount", "merchant", "hour", "is_fraud"}
    missing_cols = needed - set(rows[0])
    if missing_cols:
        sys.exit(f"error: {args.input} is missing column(s): {', '.join(sorted(missing_cols))}")

    summary = summarize(rows)
    for key in ("rows", "missing_amount", "fraud_rows", "fraud_rate_pct", "fraud_rate_by_merchant_pct"):
        print(f"{key:<27}{summary[key]}")

    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
