# Python for AI-ML

Course files for **Python for AI-ML**, a three-module course by **Emmanuel Naweji** ([Here2ServeU](https://github.com/Here2ServeU)).

From a raw CSV, to a model you can trust, to a plain-English summary with the cost written down.

| Module | Phrase | You build | Script | Saves |
|---|---|---|---|---|
| 1 · Python That Runs Anywhere | *Box it. Pin it. Rebuild it.* | A dataset inspector in plain Python | [`modules/module-1/scripts/inspect_data.py`](modules/module-1/scripts/inspect_data.py) | `summary.json` |
| 2 · A Model You Can Trust | *Don't trust the Desert Forecaster.* | Two fraud models, scored honestly | [`modules/module-2/scripts/train.py`](modules/module-2/scripts/train.py) | `metrics.json` |
| 3 · Make It Explain Itself | *Check the meter.* | An AI explanation, with tokens and cost | [`modules/module-3/scripts/explain.py`](modules/module-3/scripts/explain.py) | `summary.md` |

The same dataset is used in all three modules: `data/transactions.csv`, 5,000 card transactions (made up, but messy like real data).

---

## What's in the box

```
python-for-ai-ml/
├── data/
│   ├── transactions.csv      # 5,000 rows: txn_id, amount, merchant, hour, is_fraud
│   └── make_data.py          # rebuilds transactions.csv exactly (fixed seed)
├── modules/
│   ├── module-1/  README.md + scripts/inspect_data.py
│   ├── module-2/  README.md + scripts/train.py
│   └── module-3/  README.md + scripts/explain.py
├── tests/test_course.py      # checks every number the slides promise
├── requirements.txt          # the recipe card: every tool + exact version
├── .env.example              # where your API key goes (never in code)
└── .gitignore                # keeps .venv, outputs and secrets out of Git
```

## Before you start (once, about 10 minutes)

You need **Python 3.11+**, **Git** and a **terminal**.

| macOS · Terminal | Windows · PowerShell |
|---|---|
| `brew install python git` | `winget install Python.Python.3.12` |
| `brew install --cask visual-studio-code` | `winget install Git.Git` |
| `python3 --version && git --version` | `py --version; git --version` |

Official pages: [python.org/downloads](https://www.python.org/downloads/) · [git-scm.com/downloads](https://git-scm.com/downloads) · [venv docs](https://docs.python.org/3/library/venv.html)

## Quick start: box it, pin it, rebuild it

**macOS / Linux**

```bash
git clone https://github.com/Here2ServeU/python-for-ai-ml && cd python-for-ai-ml
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/Here2ServeU/python-for-ai-ml; cd python-for-ai-ml
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Your prompt now starts with `(.venv)`. That's how you know you're inside the box.

> **Windows tip:** if `Activate.ps1` is blocked, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again. Use `py` wherever the slides say `python3`.

## Run the whole course in one line

```bash
python3 modules/module-1/scripts/inspect_data.py && \
python3 modules/module-2/scripts/train.py && \
python3 modules/module-3/scripts/explain.py --offline
```

You should see three files saved, in order: `summary.json` → `metrics.json` → `summary.md`. If a step fails, `&&` stops the rest, so you never pay to explain broken data.

### What you should see

Everyone has the same data file and the same versions, so everyone gets the same numbers.

**Module 1**
```
rows                       5000
missing_amount             83
fraud_rows                 137
fraud_rate_pct             2.74
fraud_rate_by_merchant_pct {'electronics': 4.6, 'fuel': 2.1, 'grocery': 2.1, 'online': 3.2, 'travel': 1.7}
saved -> summary.json
```

**Module 2**
```
loaded 5000 rows; 83 missing amounts
3933 train rows · 984 test rows
always_not_fraud       accuracy 0.973   f1 0.000
logistic_regression    accuracy 0.887   f1 0.302
random_forest          accuracy 0.921   f1 0.381
saved -> metrics.json
```

**Module 3 (offline)**
```
usage: input_tokens=88 output_tokens=77 · cost $0.00142  (offline estimate)
saved -> summary.md
```

## When something goes wrong

| You see | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | You're outside the box. Activate `.venv`, then `pip install -r requirements.txt`. |
| `error: data/transactions.csv not found. Are you in the repo root?` | `cd` into the `python-for-ai-ml` folder (`pwd` must end in `python-for-ai-ml`). |
| `error: metrics.json not found` | Run Module 2 first: `python3 modules/module-2/scripts/train.py`. |
| `error: ANTHROPIC_API_KEY is not set` | Use `--offline`, or set your key (see Module 3). |
| Numbers differ slightly from the slides | Reinstall inside the box: `pip install -r requirements.txt`. |
| `transactions.csv` got changed or deleted | Rebuild it: `python3 data/make_data.py`. |

## Check everything works

```bash
python3 -m unittest discover -s tests -v
```

This runs all three modules in a temporary folder and checks every number the slides promise.

## Capstone

Pick any CSV with a yes/no column you care about (churn, loan approval, spam). Make it:

- **Reproducible:** venv + `requirements.txt`; a stranger can rebuild it.
- **Honest:** a fair quiz (train/test split); F1 beats the do-nothing model.
- **Explained:** a plain-English summary from an AI, with its cost written down.

---

Created by Emmanuel Naweji · [Here2ServeU](https://github.com/Here2ServeU) · Transformed2Succeed (T2S)
