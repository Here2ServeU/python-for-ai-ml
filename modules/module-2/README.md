# Module 2 · A Model You Can Trust

**Phrase:** *Don't trust the Desert Forecaster.* · **Big idea:** accuracy is easy; honesty is hard.

## Back into your environment

```bash
cd python-for-ai-ml
source .venv/bin/activate                # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python3 -c "import pandas, sklearn"      # silence is success
```

## Build it: train a fraud model

```bash
# 1. Look before you train
python3 -c "import pandas as pd; df = pd.read_csv('data/transactions.csv'); print(df.groupby('merchant')['is_fraud'].mean().round(3))"

# 2. Train both models
python3 modules/module-2/scripts/train.py

# 3. Find the three verbs in the code        (Windows: use VS Code search, Ctrl+F)
grep -n "fit\|predict\|f1_score" modules/module-2/scripts/train.py

# 4. Read the scoreboard like a skeptic      (Windows: type metrics.json)
cat metrics.json

# 5. Write down the number to beat
python3 -c "import json; print(json.load(open('metrics.json'))['models']['random_forest'])"
```

Expected output of step 2:

```
loaded 5000 rows; 83 missing amounts
3933 train rows · 984 test rows
always_not_fraud       accuracy 0.973   f1 0.000
logistic_regression    accuracy 0.887   f1 0.302
random_forest          accuracy 0.921   f1 0.381
saved -> metrics.json
```

The random forest caught 24 of 27 frauds and flagged 75 honest customers. **0.381 is the score to beat.**

## Exercises (do these before Module 3)

1. **Explore with groupby:** fraud rate by hour. Which hours are riskiest?
2. **Fill, don't drop:** fill missing amounts with the median. Did F1 move?
3. **Remove stratify:** re-run without `stratify=y`. Count fraud in the test set.
4. **Change the seed:** try `random_state=7`. How stable is F1?
5. **Add a feature:** add `is_night` (late-night hours). Retrain and compare.
6. **Try a third model:** add a `GradientBoostingClassifier`. Same three verbs.
7. **Print precision and recall:** use `classification_report`. Which one is weak?
8. **Beat 0.381:** record your best F1 and the change that got it.
