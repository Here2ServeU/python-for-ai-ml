# Module 1 · Python That Runs Anywhere

**Phrase:** *Box it. Pin it. Rebuild it.* · **Big idea:** make it run anywhere; then make it right.

## Build it: inspect a real dataset (plain Python, no extra tools)

```bash
# 1. Download the course files
git clone https://github.com/Here2ServeU/python-for-ai-ml && cd python-for-ai-ml

# 2. Create the box and step inside            (Windows: py -m venv .venv ; .venv\Scripts\Activate.ps1)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install the tools on the list             (Windows: pip freeze | findstr pandas)
pip install -r requirements.txt
pip freeze | grep -i pandas                    # pandas==3.0.5

# 4. Run the inspector
python3 modules/module-1/scripts/inspect_data.py

# 5. Break it on purpose
python3 modules/module-1/scripts/inspect_data.py --input data/missing.csv
# error: data/missing.csv not found. Are you in the repo root?

# 6. Read what the numbers are telling you      (Windows: type summary.json)
cat summary.json
```

Expected output of step 4:

```
rows                       5000
missing_amount             83
fraud_rows                 137
fraud_rate_pct             2.74
fraud_rate_by_merchant_pct {'electronics': 4.6, 'fuel': 2.1, 'grocery': 2.1, 'online': 3.2, 'travel': 1.7}
saved -> summary.json
```

Only 2.74% is fraud, so a model that always says "not fraud" is **97.3% accurate** and useless. Module 2 shows a better score.

## Your turn (3 minutes)

1. **Delete it:** `deactivate`, then delete the `.venv` folder.
2. **Rebuild it:** recreate `.venv`, activate it, `pip install -r requirements.txt`.
3. **Prove it:** run `inspect_data.py` again. Same 5,000 rows and 2.74%?

## Exercises (do these before Module 2)

1. **Rebuild your venv:** delete `.venv`, recreate it, reinstall from `requirements.txt`.
2. **Spot the difference:** `pip freeze` before and after installing one package.
3. **Write a list of dicts:** three transactions by hand, then compute the fraud rate.
4. **Rewrite a loop:** turn a loop into the one-line version. Then back.
5. **Count by hour:** extend `inspect_data.py`: fraud rate for hours 0-4 vs the rest.
6. **Fix text numbers:** compute the average amount. Handle the blank strings.
7. **Improve an error:** add a clear message when the CSV is missing a column.
8. **Answer the question:** what accuracy does "always not fraud" get? Show your math.
