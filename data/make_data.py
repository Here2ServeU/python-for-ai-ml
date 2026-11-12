"""Rebuild data/transactions.csv: 5,000 synthetic card transactions.

The data is made up, but it behaves like the real thing:
  * fraud is rare (137 of 5,000 rows, 2.74%)
  * fraud skews toward bigger amounts, late-night hours and electronics/online
  * 83 rows have a blank amount, because real files are messy

The same SEED always gives the same file, so every learner gets the same numbers.

Run from the repo root:
    python3 data/make_data.py
"""
import argparse
import csv
import random
from pathlib import Path

SEED = 8917
ROWS = 5000
MISSING_AMOUNTS = 83

# merchant -> (number of rows, number of fraud rows)
MERCHANTS = {
    "electronics": (900, 41),
    "fuel": (900, 19),
    "grocery": (1300, 27),
    "online": (1200, 38),
    "travel": (700, 12),
}

# typical (median) purchase size per merchant, in dollars
TYPICAL_AMOUNT = {"electronics": 180, "fuel": 45, "grocery": 60, "online": 75, "travel": 320}

NIGHT_HOURS = [21, 22, 23, 0, 1, 2]   # 9 p.m. - 3 a.m.
DAY_HOURS = list(range(3, 21))      # 3 a.m. - 9 p.m.


# how often purchases happen late at night
NIGHT_SHARE = {"fraud": 0.77, "normal": 0.06}
# fraud amounts run about e^1.2 (roughly 3x) bigger than normal ones
FRAUD_AMOUNT_SHIFT = 1.2


def pick_hour(rng, is_fraud):
    night_share = NIGHT_SHARE["fraud"] if is_fraud else NIGHT_SHARE["normal"]
    return rng.choice(NIGHT_HOURS if rng.random() < night_share else DAY_HOURS)


def pick_amount(rng, merchant, is_fraud):
    typical = TYPICAL_AMOUNT[merchant]
    if is_fraud:
        amount = typical * rng.lognormvariate(FRAUD_AMOUNT_SHIFT, 0.6)
    else:
        amount = typical * rng.lognormvariate(0.0, 0.6)
    return round(max(amount, 1.0), 2)


def build_rows(seed=SEED):
    rng = random.Random(seed)
    rows = []
    for merchant, (count, fraud_count) in MERCHANTS.items():
        labels = [1] * fraud_count + [0] * (count - fraud_count)
        rng.shuffle(labels)
        for is_fraud in labels:
            rows.append({
                "amount": pick_amount(rng, merchant, is_fraud),
                "merchant": merchant,
                "hour": pick_hour(rng, is_fraud),
                "is_fraud": is_fraud,
            })
    rng.shuffle(rows)
    for i in rng.sample(range(len(rows)), MISSING_AMOUNTS):
        rows[i]["amount"] = ""  # a blank cell, like a real export
    for i, row in enumerate(rows, start=1):
        row["txn_id"] = f"T{i:05d}"
    assert len(rows) == ROWS
    return rows


def main():
    parser = argparse.ArgumentParser(description="Rebuild the course dataset.")
    parser.add_argument("--out", default="data/transactions.csv")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    rows = build_rows(args.seed)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["txn_id", "amount", "merchant", "hour", "is_fraud"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
