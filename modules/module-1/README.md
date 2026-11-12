# Module 1 · Python That Runs Anywhere

**Module 1 of 3 · The environment problem** · about 55 minutes · 5 sections + practice

> Most Python failures are not code bugs. They are setup problems.

**Today's phrase:** *Box it. Pin it. Rebuild it.*
**Big idea:** make it run anywhere; then make it right.

📊 Slides: Google Drive › *Module 01 - Python That Runs Anywhere* (`PyAIML_Module_1_Presenter.pptx` / `PyAIML_Module_1_Student.pptx`)

---

## Start here: a story

Friday, 5 p.m.: the notebook runs. Monday, 9 a.m.: `ModuleNotFoundError`.

**"Nobody touched the code. So what broke?"**

By the end of this module you'll know the answer, and you'll never lose a Monday morning to it again.

---

## What is Python?

**Python is a programming language: a way to give a computer instructions in words that look almost like English.**

```python
amount = 42.5
if amount > 300:
    print("big purchase")
else:
    print("normal purchase")
```

You can read that out loud and understand it, even if you have never coded. That is Python's superpower.

- You write steps in a text file that ends in `.py` (a **script**).
- You run it with `python3` (Mac/Linux) or `py` (Windows).
- Python reads the steps **from top to bottom** and does them in order.

## Why do we use Python for AI and ML?

| Reason | What it means for you |
|---|---|
| **Easy to read** | Code looks like plain English, so beginners learn fast and teams can read each other's work. |
| **Free tools for everything** | Thousands of free **packages** (add-on tools): `pandas` for tables, `scikit-learn` for models, `anthropic` to talk to Claude. |
| **The language of AI** | Almost every AI course, paper and code example online is written in Python. Learn it once, follow them all. |
| **Runs anywhere** | Same code on Mac, Windows and Linux, *if* you set it up the right way. That's this module. |

## The big idea, in one line: make it run anywhere; then make it right

| | Idea | In plain words |
|---|---|---|
| 01 | **One box per project** | A private folder of tools for each project, plus a written list of them. No more "it works on my machine". |
| 02 | **The 20% you use daily** | Lists, dictionaries, functions and loops: the few building blocks all AI data uses. |
| 03 | **Fail loudly** | Real files are messy. Check them, and when something is wrong, say so in plain words. |

## Today's phrase: Box it. Pin it. Rebuild it.

Think of a **recipe card**. A dish tastes the same in any kitchen only if the recipe lists exact amounts.
Your project's box (`.venv`) is a clean kitchen; `requirements.txt` is the recipe card.

---

## New words

**Part 1: three words you'll hear in the first ten minutes**

| Word | Meaning | Everyday comparison |
|---|---|---|
| **Terminal** | A window where you type commands instead of clicking. | Like texting your computer. |
| **Command** | One instruction you type and run with Enter. | You can copy every command from this page. |
| **Folder path** | A file's address. `data/transactions.csv` is a file inside `data`. | Like a street address. |

Try it now: open a terminal and type `python3 --version` (Windows: `py --version`), then Enter. It just prints a version number. Nothing scary happened.

> **Where's my terminal?** Mac: Spotlight → type *Terminal*. Windows: Start menu → *PowerShell*. VS Code: menu *Terminal → New Terminal*.

**Part 2: three more words, then we build**

| Word | Meaning | Everyday comparison |
|---|---|---|
| **Package** | Free code someone else wrote that you install. | Like an app, but for Python. |
| **pip** | The tool that installs packages. | Python's app store. |
| **Script (`.py` file)** | A text file of Python steps. When you run it, Python does the steps in order. | A recipe the computer follows. |

---

## Sections at a glance

| # | Section | Time |
|---|---|---|
| 01 | [Works on My Machine](#01--works-on-my-machine) | ~7 min |
| 02 | [Virtual Environments](#02--virtual-environments) | ~9 min |
| 03 | [The 20% of Python](#03--the-20-of-python) | ~10 min |
| 04 | [Files, Data and Errors](#04--files-data-and-errors) | ~8 min |
| 05 | [Build It: Inspect a Real Dataset](#05--build-it-inspect-a-real-dataset) | ~11 min |

---

## Before you start (once, about 10 minutes)

**What Module 1 needs:** Python 3.11+ (`python3`, or `py` on Windows) · Git (to download the course files) · a terminal.

**macOS · Terminal**

```bash
# install Homebrew first: brew.sh
brew install python git
brew install --cask visual-studio-code
python3 --version && git --version
```

**Windows · PowerShell**

```powershell
# winget ships with Windows 11
winget install Python.Python.3.12
winget install Git.Git
winget install Microsoft.VisualStudioCode
py --version; git --version
```

The last line checks it worked: you should see Python 3.11 or newer, plus a git version.

> **Stuck?** Mac `brew: command not found` → install Homebrew first from [brew.sh](https://brew.sh). Windows `py is not recognized` → close and reopen PowerShell after installing.

**Prefer a video?**

- macOS: [Install Git, Python and VS Code on a Mac](https://www.youtube.com/watch?v=8ZIiXg4XOY0&t=6s)
- Windows: [Install Git, Python and VS Code on Windows](https://www.youtube.com/watch?v=f091sbQSv7I)

**Official pages:** [python.org/downloads](https://python.org/downloads) · [git-scm.com/downloads](https://git-scm.com/downloads) · [Python tutorial](https://docs.python.org/3/tutorial) · [venv docs](https://docs.python.org/3/library/venv.html)

### One repo for all three modules

Everything this course uses lives here: the data, one script per module, and a README with every command from the slides.

| Script | Module | Saves |
|---|---|---|
| `inspect_data.py` | 1 | `summary.json` |
| `train.py` | 2 | `metrics.json` |
| `explain.py` | 3 | `summary.md` |

---

## 01 · Works on My Machine

**It ran on Friday. It broke on Monday.**

| Fri 17:00 | `pip install` | Mon 09:00 | 3 hours |
|---|---|---|---|
| the code works | a teammate updates one tool everyone shares | same code, new laptop, new Python | lost before anyone finds the cause |

**The code was fine.** Nobody wrote down which tools it needed, so nobody could rebuild it.

### Don't blame the code

Python projects use **packages**: free add-on tools other people wrote. Put them all in one shared place, and every project shares, and breaks, the same pile. The project had no written record of what it needed.

The fix has three parts, and each one matches today's phrase:

| Fix | What it means | Phrase |
|---|---|---|
| **1. Separate** | Each project gets its own packages. One upgrade can't break another project. | **Box it** |
| **2. Written down** | Each tool and its exact version, listed in a file called `requirements.txt`. | **Pin it** |
| **3. Rebuildable** | Anyone rebuilds the same setup with one command. | **Rebuild it** |

---

## 02 · Virtual Environments

That's the official name for **the box**. Think separate lunchboxes, not one shared fridge everyone grabs from.

**One shared install changes every project at once.**

- ❌ **Shared (risky):** `pip install pandas` → every project changes. Breaks easily; hard to see.
- ✅ **One box per project (safe):** `project/` → `.venv/` → `requirements.txt`

| Step | Command | What it does |
|---|---|---|
| **Box it** | `python3 -m venv .venv` | A private copy of Python inside the project folder. |
| **Pin it** | `pip freeze` | Lists every tool and exact version, so you can save it. |
| **Rebuild it** | `pip install -r requirements.txt` | Recreates the exact same box on any machine. |

### The commands you'll type in every project

A **virtual environment** is a private box of Python packages that belongs to one project. Nothing you install there touches the rest of your computer, and you can delete it and rebuild it in seconds.

**macOS · Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
pip freeze > requirements.txt
```

**Windows · PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install pandas
pip freeze > requirements.txt
```

Your prompt now starts with **`(.venv)`**. That is how you know you are inside the box.

> **Why does `.venv` start with a dot?** A dot just hides the folder in normal file views. It's still there.
>
> **Stuck?** Windows *"running scripts is disabled"* → run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, and activate again. Mac *"command not found: python3"* → Python isn't installed yet; go back to [Before you start](#before-you-start-once-about-10-minutes).

---

## 03 · The 20% of Python

You don't need all of Python. You need **four building blocks and one loop**.

### Four shapes hold almost all AI data

**A list:** items in order, counted from 0

```python
scores = [0.2, 0.9, 0.4]
scores[0]          # 0.2
```

**A dictionary (dict):** labels with values, one record

```python
txn = {"amount": 42.5, "merchant": "fuel"}
txn["amount"]      # 42.5
```

**A list of dicts:** a table, one dict per row

```python
rows = [
    {"amount": 42.5,  "is_fraud": 0},
    {"amount": 910.0, "is_fraud": 1},
]
```

**A function:** a named step you can reuse

```python
def fraud_rate(rows):
    f = sum(r["is_fraud"] for r in rows)
    return f / len(rows)

fraud_rate(rows)   # 0.5
```

| Shape | Everyday comparison |
|---|---|
| List | A shopping list. Python starts counting at **0**, so `scores[0]` is the first item. |
| Dict | One row of a form: *amount* is 42.5, *merchant* is fuel. |
| List of dicts | A whole spreadsheet: one dict per row. |
| Function | A saved recipe you can use again and again. |

### A loop does one thing for every item

**A loop**

```python
big = []
for r in rows:
    if r["amount"] > 300:
        big.append(r)
```

**The same loop, in one line** (called a *comprehension*)

```python
big = [r for r in rows if r["amount"] > 300]
```

- **Read it as English:** "Give me each row `r` whose amount is over 300."
- **Use it for:** picking items. Keep it simple; if it gets confusing, use the normal loop.
- **You'll see it everywhere:** this style is in almost every AI code example.

---

## 04 · Files, Data and Errors

### Real files are messy, every time

| Problem | What happens | How you check for it |
|---|---|---|
| ⚠️ **Blank cells** | An empty cell comes in as empty text (`""`), not as 0. | `r["amount"] == ""` |
| ⚠️ **Numbers stored as text** | CSV files give you text. Text `'42.5'` is not the number 42.5. | `float(r["amount"])` |
| ⚠️ **Missing files** | Wrong folder or wrong file name: the most common beginner error. | `FileNotFoundError` |

These happen all the time. Write code that checks for them.

### Fail loudly, in a sentence a human can act on

```python
def load_rows(path):
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        sys.exit(f"error: {path} not found."
                 " Are you in the repo root?")
```

| Piece | What it does |
|---|---|
| `with open(...)` | Opens the file and always closes it, even if something fails. |
| `try / except` | Try something. If a known error happens, handle it calmly. |
| `sys.exit("...")` | Stop with a message that says what to do next. |
| `Traceback (most recent…` | A wall of red error text scares people. One clear sentence helps. |

**Good errors save more time than clever code.**

---

## 05 · Build It: Inspect a Real Dataset

**Do it with plain Python, once.** No extra tools yet; those come in Module 2. Plain Python can load, count and summarize a real dataset. Doing it by hand once makes the shortcuts make sense later.

- **5,000 card transactions:** `amount`, `merchant`, `hour`, `is_fraud` (1 = fraud, 0 = not)
- **Some of it is messy:** blank amounts, like real data
- The same repo and dataset are used for all three modules.

> The first three steps are today's phrase: **Box it. Pin it. Rebuild it.**

### Step 1 of 6 · Download the course files (clone)

```bash
git clone https://github.com/Here2ServeU/python-for-ai-ml && cd python-for-ai-ml
ls          # Windows: dir
```

Look before you run anything:

| You'll see | What it is |
|---|---|
| `data/` | `transactions.csv` + `make_data.py` |
| `modules/` | one `scripts/` folder per module |
| `requirements.txt` | the list of tools + versions |

> **Stuck?** `git: command not found` → Git isn't installed. `destination path already exists` → you already cloned it; just `cd python-for-ai-ml`.

### Step 2 of 6 · Create the box, and step inside it

```bash
pwd                         # must end in python-for-ai-ml
```

| macOS · Linux | Windows · PowerShell |
|---|---|
| `python3 -m venv .venv` | `py -m venv .venv` |
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |

Your prompt now starts with `(.venv)`. Every command from here runs inside it.

> **Stuck?** Wrong folder is the number one problem here: `cd python-for-ai-ml` and try again.

### Step 3 of 6 · Install the tools on the list

```bash
pip install -r requirements.txt
pip freeze | grep -i pandas       # Windows: pip freeze | findstr pandas
```

One command installs the exact tools and versions this course uses. That's why we write the list down.

**You should see:** some downloading, then `pandas==3.0.5`. Same version as everyone else.

> **Stuck?** If pip errors or installs to the wrong place, check for `(.venv)` at the start of the line. If it's missing, activate again.

### Step 4 of 6 · Run the inspector script

```bash
python3 modules/module-1/scripts/inspect_data.py
```

**You should see exactly these numbers.** Everyone has the same data file, so everyone gets the same answers.

```
rows                       5000
missing_amount             83
fraud_rows                 137
fraud_rate_pct             2.74
fraud_rate_by_merchant_pct {'electronics': 4.6, 'fuel': 2.1, 'grocery': 2.1, 'online': 3.2, 'travel': 1.7}
saved -> summary.json
```

| Line | Meaning |
|---|---|
| `rows` | the file loaded: 5,000 records |
| `missing_amount` | 83 blanks we must deal with |
| `fraud_rate_pct` | only 2.74% are fraud. **Remember this number.** |

> **Stuck?** `No such file or directory` → wrong folder: `pwd`, then `cd python-for-ai-ml`. `No module named ...` → you're outside the box; activate again.

### Step 5 of 6 · Break it on purpose

```bash
python3 modules/module-1/scripts/inspect_data.py --input data/missing.csv
```

That file doesn't exist, on purpose. Instead of a wall of red error text, you get one sentence that says what to check:

```
error: data/missing.csv not found. Are you in the repo root?
```

Open [`scripts/inspect_data.py`](scripts/inspect_data.py) and find the `try` / `except`. That's the pattern from Section 04, in real code.

### Step 6 of 6 · Read what the numbers are telling you

```bash
cat summary.json        # Windows: type summary.json
```

| 5,000 | 137 | 2.74% | 97.3% |
|---|---|---|---|
| transactions | are fraud | fraud rate | accuracy of a model that always says "not fraud" |

When something is rare, **"accuracy" can fool you:** a useless model scores 97%. Module 2 shows a better score.

### Commands explained: every command, piece by piece

```bash
python3 modules/module-1/scripts/inspect_data.py --input data/transactions.csv --out summary.json
```

| Piece | Meaning |
|---|---|
| `$` / `>` | The prompt sign. `$` on Mac, `>` on Windows. Don't type it. |
| `# comment` | A note for you. The computer ignores everything after `#`. |
| `python3` / `py` | Start Python. Mac and Linux use `python3`; Windows uses `py`. |
| `modules/.../inspect_data.py` | The file to run, written as its folder address. |
| `--input data/transactions.csv` | Which file to inspect. This is the default, so it's optional. |
| `--out summary.json` | Where to save the summary. Also optional. |
| `A \| B` | Pipe: send what A prints into B. |
| `A && B` | Run B only if A succeeded. |

**Windows · PowerShell:** `py modules\module-1\scripts\inspect_data.py --input data\transactions.csv`

**You should see:** the same six lines as step 4. The `--options` only change which files it uses.

---

## Your turn (3 minutes): delete your box, then rebuild it

1. **Delete it:** `deactivate`, then delete the `.venv` folder. It's safe: nothing in it is precious.
   Mac/Linux: `rm -rf .venv` · Windows: `Remove-Item -Recurse .venv`
2. **Rebuild it:** recreate `.venv`, activate it, then `pip install -r requirements.txt`.
3. **Prove it:** run `inspect_data.py` again. Same 5,000 rows and 2.74%? You rebuilt a project from its recipe.

## Self-check, from memory

Close your notes. Answer out loud:

**"What three steps let a stranger run your project?"**

<details>
<summary>Check yourself</summary>

- **Box it:** `python3 -m venv .venv`
- **Pin it:** `pip freeze > requirements.txt`
- **Rebuild it:** `pip install -r requirements.txt`

Two out of three is great for day one.
</details>

## Recap · your win: four new skills

- ✅ **Box it. Pin it. Rebuild it.** venv, freeze, install -r. A stranger can now rebuild and run your project.
- ✅ **Four data shapes.** List, dictionary, list of dictionaries, function. Most AI data fits one.
- ✅ **Expect messy files.** Blanks, wrong types, missing files. Check for them before you trust anything.
- ✅ **Read the numbers.** Only 2.74% is fraud, so "accuracy" can fool you. Remember 97.3%.

## Before Module 2

Look at your `summary.json` and ask one question:

**"If only 2.7% is fraud, what does a useless model score?"**

The answer is 97.3%, and most people would trust it. Module 2 shows a score that can't be fooled by a model that never says yes.

**Next · Module 2 of 3: Data to a model.** Load the same data with pandas, clean it, and teach the computer to spot fraud. Then test it fairly. Keep your `summary.json`; we start right there. → [Module 2](../module-2/README.md)

---

## Appendix A · Exercises (do these before Module 2)

Everyone: do at least **01** and **08**. The rest are bonus.

| # | Exercise | Task |
|---|---|---|
| 01 | **Rebuild your venv** | Delete `.venv`, recreate it, reinstall from `requirements.txt`. |
| 02 | **Spot the difference** | `pip freeze` before and after installing one package. Spot the change. |
| 03 | **Write a list of dicts** | Three transactions by hand, then compute the fraud rate. |
| 04 | **Rewrite a loop** | Turn a loop into the one-line version. Then back. |
| 05 | **Count by hour** | Extend `inspect_data.py`: fraud rate for hours 0-4 vs the rest. |
| 06 | **Fix text numbers** | Compute the average amount. Handle the blank strings. |
| 07 | **Improve an error** | Add a clear message when the CSV is missing a column. |
| 08 | **Answer the question** | What accuracy does "always not fraud" get? Show your math. |

Stuck on an exercise? Post the exact error message. Copying the error is a skill, too.

## Appendix B · Glossary: every term from Module 1

| Term | Meaning |
|---|---|
| **Python** | A programming language that reads almost like English; the main language of AI. |
| **Terminal** | A window where you type commands instead of clicking. |
| **Package** | Free code someone else wrote that you install. |
| **pip** | Python's app store for tools. Use it inside your venv. |
| **Script** | A `.py` text file of Python steps, run top to bottom. |
| **Virtual environment** | A private toolbox for one project, kept in a `.venv` folder. |
| **requirements.txt** | The recipe card: every tool and exact version a project needs. |
| **List** | Items in order, counted from 0: `[0.2, 0.9, 0.4]`. |
| **Dict** | Labels with values, like one row of a table: `{"amount": 42.5}`. |
| **Function** | A named step you can reuse: `def fraud_rate(rows): ...` |
| **Comprehension** | A loop written in one line, to pick or change items. |
| **Fraud rate** | Fraud rows ÷ all rows. Here 2.74%: a rare event. |
