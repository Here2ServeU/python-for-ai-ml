# Module 2 · A Model You Can Trust

**Module 2 of 3 · Data to model** · about 60 minutes · 5 sections + practice

> A model learns from examples. Trust comes from how you test it.

**Today's phrase:** *Don't trust the Desert Forecaster.*
**Big idea:** accuracy is easy; honesty is hard.

📊 Slides: Google Drive › *Module 02 - A Model You Can Trust* (`PyAIML_Module_2_Presenter.pptx` / `PyAIML_Module_2_Student.pptx`)

---

## Start here: a choice

Two fraud models, tested on the same 984 transactions.

**"97.3% or 92.1% accurate. Which one do you ship?"**

Most people pick 97.3%. It catches zero fraud. Today you'll see why, and learn the score that can't be fooled.

## The big idea, in one line: accuracy is easy; honesty is hard

| | Idea | In plain words |
|---|---|---|
| 01 | **Clean before you train** | Fix the data first: blanks, wrong types, words. Messy data ruins even a good model. |
| 02 | **Hold data back** | Test on examples the model never saw. Anything else is grading your own homework. |
| 03 | **Score what matters** | For rare things like fraud, a score called F1 tells the truth when accuracy lies. |

## Today's phrase: Don't trust the Desert Forecaster

A forecaster in the desert who says "no rain" every day is right almost every day, and useless the one day you need an umbrella. A model that always says "not fraud" is the same forecaster.

---

## New words

**Part 1: three words that explain machine learning**

| Word | Meaning | Everyday comparison |
|---|---|---|
| **Model** | A recipe the computer writes for itself by studying examples. | A student's notes. |
| **Training** | Showing the model many examples with the answers, so it learns the pattern. | Studying with the answer key. |
| **Testing** | A quiz on examples it has never seen. This shows if it really learned. | The final exam, with new questions. |

**Part 2: three things we'll use today**

| Word | Meaning |
|---|---|
| **pandas** | A Python package for tables. Like Excel, but you give the orders in code. |
| **scikit-learn** | A package full of ready-made models. Pick one and train it in a few lines. |
| **Fraud** | A purchase the real card owner didn't make. In our data, those rows have `is_fraud` set to 1. |

## Sections at a glance

| # | Section | Time |
|---|---|---|
| 01 | [DataFrames](#01--dataframes) | ~8 min |
| 02 | [Cleaning Decisions](#02--cleaning-decisions) | ~8 min |
| 03 | [Fit, Predict, Score](#03--fit-predict-score) | ~9 min |
| 04 | [The Accuracy Trap](#04--the-accuracy-trap) | ~9 min |
| 05 | [Build It: Train a Fraud Model](#05--build-it-train-a-fraud-model) | ~14 min |

---

## Before you start: back into your environment

You already have the course files and your box (`.venv`) from Module 1. Step back inside and check the two tools load.

**What Module 2 needs:** your Module 1 venv with requirements installed · pandas (tables) · scikit-learn (ready-made models).

| macOS · Terminal | Windows · PowerShell |
|---|---|
| `cd python-for-ai-ml` | `cd python-for-ai-ml` |
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| `python3 -c "import pandas, sklearn"` | `py -c "import pandas, sklearn"` |

If the last line prints nothing at all, it worked. **In Python, silence is success.**

> **Stuck?** `No module named pandas` or `sklearn` → you're outside the box. Activate again, then `pip install -r requirements.txt`. New here? Do [Module 1](../module-1/README.md), steps 1-3 first.

### Get the latest course files

```bash
git pull          # inside python-for-ai-ml. New here? Module 1, step 1 clones it.
```

| Today's script | Reads | Saves |
|---|---|---|
| [`scripts/train.py`](scripts/train.py): load, clean, split, train, score | `data/transactions.csv` (5,000 rows, same as Module 1) | `metrics.json`: the scoreboard, used in Module 3 |

> `not a git repository` means you're in the wrong folder: `cd python-for-ai-ml` first.

---

## 01 · DataFrames

**A DataFrame is a spreadsheet you can program.**

```python
import pandas as pd
df = pd.read_csv("data/transactions.csv")
df.shape                                   # (5000, 5)
df.head()                                  # first 5 rows
df["amount"].isna().sum()                  # 83
df.groupby("merchant")["is_fraud"].mean()
```

| Idea | Meaning |
|---|---|
| **Rows and columns** | Each row is one purchase; each column is one detail. |
| **One column** | `df["amount"]` grabs one column to sum, average or filter. |
| **groupby** | Group rows by a category, then compute each group: fraud rate per store type. |

Module 1's inspector was about 40 lines of plain Python. The same answers in pandas are four lines; and now you know what those four lines are doing.

> `pd` is just a short nickname for pandas, so we type less.

---

## 02 · Cleaning Decisions

**Three decisions, every dataset, every time.** Each one changes what the model learns.

| Decision | What to do | Code |
|---|---|---|
| **Blank cells** | Drop the row, or fill it. Dropping 83 of 5,000 is safe; dropping 40% is not. | `df.dropna(subset=["amount"])` |
| **Numbers as numbers** | Make sure numbers are real numbers, not text that looks like numbers. | `pd.to_numeric(df["amount"])` |
| **Words into numbers** | Models only read numbers. "One-hot" turns `fuel` into a yes/no (1/0) column. | `pd.get_dummies(df, columns=["merchant"])` |

Write each decision down. Next month's data needs the same three, in the same order.

---

## 03 · Fit, Predict, Score

**Every model, the same three verbs.** Think: study, take the exam, get graded.

```
fit(X_train, y_train)  →  predict(X_test)  →  score(y_test, pred)
```

| Term | Meaning |
|---|---|
| **X** (features) | The clues the model looks at: amount, hour, store type. |
| **y** (label) | The answer it must guess: `is_fraud` (1 = fraud). |
| **test set** | Examples we hide. The model only sees them at quiz time. |
| **any model** | Two models we'll try. Same three steps for both. |

Learn these three steps once and you can follow almost any machine learning example online.

### Leakage: the exam answers left in the textbook

```python
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

| Rule | Why |
|---|---|
| **1. Split before you look** | Hide the quiz rows first (`test_size=0.2` = 20%). If you peek at them, the test is no longer fair. |
| **2. Same shuffle for everyone** | `random_state=42` shuffles the same way on every computer, every time. |
| **3. Share the rare cases fairly** | `stratify=y` puts fraud in both piles at the same 2.7%. Without it, the quiz might have almost none. |

---

## 04 · The Accuracy Trap

**Same test set. Same rows. Two stories.**

| 984 | 27 | 957 | 0 |
|---|---|---|---|
| test rows held back | of them are fraud | are not | fraud caught by "always no" |

| Model | Accuracy | F1 | Result |
|---|---|---|---|
| Always "not fraud" | **97.3%** | 0.00 | catches nothing |
| Random forest | **92.1%** | 0.38 | catches real fraud |

**Why it matters:** the model with lower accuracy is the only one catching fraud. With rare events, accuracy rewards doing nothing.

### Two questions, and one score for both

| Score | Question it answers | When it's low |
|---|---|---|
| **Precision** | When it says fraud, is it right? | Blocking good customers' cards. |
| **Recall** | Of all real fraud, how much did it catch? | Fraud slips through. |
| **F1** | One number that needs both to be good. 0 = useless · 1 = perfect. | Can't be gamed by saying "no" to everything. |

```python
from sklearn.metrics import f1_score
f1_score(y_test, pred)
```

> Airport security: precision = not stopping innocent travelers; recall = not letting threats through.

---

## 05 · Build It: Train a Fraud Model

**One script, the whole pattern.** [`scripts/train.py`](scripts/train.py) does everything from this module in about 40 lines: load, clean, split, train two models, compare them with a do-nothing model, and save the scores.

- Same dataset as Module 1: `data/transactions.csv`, 5,000 rows
- Saves `metrics.json`: the scores, used in Module 3

Read it top to bottom before you run it. Every line maps to a section of this module.

### Step 1 of 5 · Look before you train

```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/transactions.csv'); print(df.groupby('merchant')['is_fraud'].mean().round(3))"
```

```
merchant
electronics    0.046
fuel           0.021
grocery        0.021
online         0.032
travel         0.017
Name: is_fraud, dtype: float64
```

Look first: electronics (4.6%) and online (3.2%) have the most fraud. A good model should notice that too.

> Copy the command exactly; the single and double quotes matter.

### Step 2 of 5 · Train both models

```bash
python3 modules/module-2/scripts/train.py
```

**You should see exactly these numbers:** 83 blank rows removed, 80% to learn, 20% for the quiz, and the forest wins on F1.

```
loaded 5000 rows; 83 missing amounts
3933 train rows · 984 test rows
always_not_fraud       accuracy 0.973   f1 0.000
logistic_regression    accuracy 0.887   f1 0.302
random_forest          accuracy 0.921   f1 0.381
saved -> metrics.json
```

> Numbers differ slightly? Reinstall inside the box: `pip install -r requirements.txt`.

### Step 3 of 5 · Find the three verbs in the code

```bash
grep -n "fit\|predict\|f1_score" modules/module-2/scripts/train.py      # Windows: VS Code search (Ctrl+F)
```

A loop runs both models, and each one does the same three steps:

| Verb | Code | Meaning |
|---|---|---|
| **FIT** | `m.fit(X_tr, y_tr)` | study the examples |
| **PREDICT** | `pred = m.predict(X_te)` | answer the exam |
| **SCORE** | `f1_score(y_te, pred)` | mark the exam |

### Step 4 of 5 · Read the scoreboard like a skeptic

```bash
cat metrics.json        # Windows: type metrics.json
```

| Model | F1 | Verdict |
|---|---|---|
| Baseline | 0.000 | 97.3% accurate and completely useless. |
| Logistic regression | 0.302 | Simple, fast, explainable. A fair start. |
| Random forest | 0.381 | The best of three; but too many false alarms. |

It caught **24 of 27** frauds and flagged **75** honest customers. 0.38 is a start, not a finish.

### Step 5 of 5 · Write down the number to beat

```bash
python3 -c "import json; print(json.load(open('metrics.json'))['models']['random_forest'])"
```

```
{'accuracy': 0.921, 'f1': 0.381}
```

**0.381 is now the score to beat.** Every change you try in the exercises is compared to it.

### Commands explained: every command, piece by piece

```bash
python3 modules/module-2/scripts/train.py --input data/transactions.csv --out metrics.json
python3 -c "import pandas as pd; print(pd.__version__)"
```

| Piece | Meaning |
|---|---|
| `train.py` | Load, clean, split, train two models, score, save. |
| `--input` / `--out` | Which CSV to read and where to save. Both have defaults. |
| `python3 -c "..."` | Run one line of Python without making a file. Great for a quick look. |
| `import pandas as pd` | Load pandas under its usual short name, `pd`. |
| `metrics.json` | The scoreboard. Module 3 sends it to an AI. |
| `cat` / `type` | Print a file. `cat` on Mac and Linux, `type` on Windows. |

**Windows · PowerShell:** `py modules\module-2\scripts\train.py`

**You should see:** the scoreboard from step 2, and pandas `3.0.5` from the second line.

---

## Your turn (3 minutes): catch the Desert Forecaster yourself

1. **Run it:** run `train.py`. Find the `always_not_fraud` line in the output.
2. **Compare it:** write its accuracy and F1 next to the random forest's. Which number lied?
3. **Explain it:** tell a friend in one sentence why the 97.3% model is useless. Use the desert.

## Self-check, from memory

Close your notes. Answer out loud:

**"How can a model that never says 'fraud' score 97%?"**

<details>
<summary>Check yourself</summary>

Because only 2.7% of purchases are fraud, saying "not fraud" every time is right 97.3% of the time, while catching nothing. That's the Desert Forecaster.
</details>

## Recap · your win: four new skills

- ✅ **pandas does the heavy lifting.** `read_csv`, `dropna`, `get_dummies`, `groupby`: four commands do most cleaning.
- ✅ **Fit, predict, score.** Study, quiz, grade. The same three steps for every model.
- ✅ **Hold data back.** Keep 20% as a quiz the model never saw. Same shuffle every time.
- ✅ **Spot the Desert Forecaster.** On rare events, 97% accuracy can mean zero fraud caught. F1 can't be fooled.

## Before Module 3

Look at your scoreboard and ask one question:

**"Could I explain this F1 to my manager in plain English?"**

Most people can't, and that's where projects get stuck. In Module 3, an AI writes that plain-English summary for you, and you track what it costs.

**Next · Module 3 of 3: Make it explain itself.** Ask an AI (like Claude) to explain your results, from Python, and know exactly what each request costs. Keep your `metrics.json`. → [Module 3](../module-3/README.md)

---

## Appendix A · Exercises (do these before Module 3)

Everyone: do at least **01** and **08**. It's fine if your change makes F1 worse; that's still learning. Write it down.

| # | Exercise | Task |
|---|---|---|
| 01 | **Explore with groupby** | Fraud rate by hour. Which hours are riskiest? |
| 02 | **Fill, don't drop** | Fill missing amounts with the median. Did F1 move? |
| 03 | **Remove stratify** | Re-run without `stratify=y`. Count fraud in the test set. |
| 04 | **Change the seed** | Try `random_state=7`. How stable is F1? |
| 05 | **Add a feature** | Add `is_night = hour < 5`. Retrain and compare. |
| 06 | **Try a third model** | Add a `GradientBoostingClassifier`. Same three verbs. |
| 07 | **Print precision and recall** | Use `classification_report`. Which one is weak? |
| 08 | **Beat 0.381** | Record your best F1 and the change that got it. |

## Appendix B · Glossary: every term from Module 2

| Term | Meaning |
|---|---|
| **DataFrame** | A table in pandas, like a spreadsheet you control with code. |
| **One-hot encoding** | Turning words like `"fuel"` into 1/0 columns a model can read. |
| **Features (X) / label (y)** | What the model looks at, and what it must predict. |
| **Train / test split** | Hiding some examples as a fair quiz for the model. |
| **Leakage** | Quiz answers sneaking into study time. Makes a model look better than it is. |
| **F1 score** | One score for two questions: is it right, and did it catch it? 0 to 1. |
