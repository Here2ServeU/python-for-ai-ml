"""Module 2: clean the data, train two models, and score them honestly.

Run from the repo root:
    python3 modules/module-2/scripts/train.py
    python3 modules/module-2/scripts/train.py --input data/transactions.csv --out metrics.json
"""
import argparse
import json
import sys

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description="Train and score fraud models.")
parser.add_argument("--input", default="data/transactions.csv")
parser.add_argument("--out", default="metrics.json")
args = parser.parse_args()

# 1. Load (fail loudly, like Module 1)
try:
    df = pd.read_csv(args.input)
except FileNotFoundError:
    sys.exit(f"error: {args.input} not found. Are you in the repo root?")
print(f"loaded {len(df)} rows; {df['amount'].isna().sum()} missing amounts")

# 2. Clean: three decisions, always in the same order
df = df.dropna(subset=["amount"])                              # blank cells: drop the row
df["amount"] = pd.to_numeric(df["amount"])                     # numbers as numbers
X = pd.get_dummies(df[["amount", "hour", "merchant"]], columns=["merchant"])  # words -> 1/0
y = df["is_fraud"]

# 3. Split BEFORE training: hide 20% as the quiz
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"{len(X_tr)} train rows · {len(X_te)} test rows")

# 4. Fit, predict, score: the same three verbs for every model
models = {
    "always_not_fraud": DummyClassifier(strategy="constant", constant=0),
    "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "random_forest": RandomForestClassifier(
        n_estimators=67, max_depth=6, min_samples_leaf=5, class_weight="balanced", random_state=42),
}
scores = {}
for name, m in models.items():
    m.fit(X_tr, y_tr)
    pred = m.predict(X_te)
    scores[name] = {
        "accuracy": round(accuracy_score(y_te, pred), 3),
        "f1": round(f1_score(y_te, pred, zero_division=0), 3),
    }
    print(f"{name:<22} accuracy {scores[name]['accuracy']:.3f}   f1 {scores[name]['f1']:.3f}")

# 5. Save the scoreboard for Module 3
with open(args.out, "w") as f:
    json.dump({"test_rows": len(X_te), "fraud_in_test": int(y_te.sum()), "models": scores}, f, indent=2)
print(f"saved -> {args.out}")
