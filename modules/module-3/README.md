# Module 3 · Make It Explain Itself

**Module 3 of 3 · LLMs are APIs** · about 60 minutes · practice + capstone

> Asking an AI is a request with a key, a message and a price. Write it down.

**Today's phrase:** *Check the meter.*
**Big idea:** every call has a price; write it down.

📊 Slides: Google Drive › *Module 03 - Make It Explain Itself* (`PyAIML_Module_3_Presenter.pptx` / `PyAIML_Module_3_Student.pptx`)

---

## Start here: a money surprise

One call to explain your model costs about **$0.0014**. A seventh of a cent.

**"How does a fraction of a cent become a $426 bill?"**

$0.0014 × 10,000 calls a day × 30 days ≈ **$426 a month**. Today you'll learn to read the meter before the bill arrives.

## The big idea, in one line: every call has a price; write it down

| | Idea | In plain words |
|---|---|---|
| 01 | **Keys stay secret** | Keep your key in a hidden setting, never in your code. A leaked key means a stranger's bill on your card. |
| 02 | **Tokens are the bill** | AI charges by tokens: small word pieces you send and get back. Count both. |
| 03 | **Networks fail** | If a request fails, wait and try again, but only a few times. Each try costs. |

## Today's phrase: Check the meter

A taxi meter ticks for every mile. An AI meter ticks for every **token**: the words you send and the words that come back. Your API key is the card that pays the fare, so it never sits in your code.

---

## New words

**Part 1: three words before we talk to an AI**

| Word | Meaning | Everyday comparison |
|---|---|---|
| **LLM** | Large Language Model: an AI that reads and writes text, like Claude. | — |
| **API** | A way for your code to ask another computer for something. | A waiter taking your order to the kitchen. |
| **API key** | A secret password: it says who you are, and who pays the bill. | Your credit card. |

**Part 2: three more words, then we build**

| Word | Meaning |
|---|---|
| **Token** | A small piece of a word, about 4 letters. AI reads, writes and charges by tokens. |
| **Prompt** | The message you send to the AI. Clear prompts get better answers. |
| **Offline mode** | A practice mode in our script: a fake reply, no key, no cost. **You can do this whole module for free.** |

## Sections at a glance

| # | Section | Time |
|---|---|---|
| 01 | [An LLM Is an API](#01--an-llm-is-an-api) | ~7 min |
| 02 | [Keys and Secrets](#02--keys-and-secrets) | ~7 min |
| 03 | [Tokens Are the Bill](#03--tokens-are-the-bill) | ~9 min |
| 04 | [When the Call Fails](#04--when-the-call-fails) | ~8 min |
| 05 | [Build It: Explain Your Model](#05--build-it-explain-your-model) | ~15 min |

---

## Before you start: everything is already installed

Same files, same box. The `anthropic` package (to talk to Claude) is already installed by `requirements.txt`. A key is optional: offline mode is free.

**What Module 3 needs:** `metrics.json` (from Module 2's `train.py`) · the `anthropic` package · an API key (optional).

| macOS · Terminal | Windows · PowerShell |
|---|---|
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| `python3 -c "import anthropic"` | `py -c "import anthropic"` |

If the import line prints nothing, it worked. For real calls (optional): [console.anthropic.com](https://console.anthropic.com) → API keys.

> **Stuck?** `No module named anthropic` → activate the box, then `pip install -r requirements.txt`.

### Get the latest course files

```bash
git pull                         # run inside python-for-ai-ml
ls modules/module-3/scripts      # explain.py   (Windows: dir)
cat .env.example                 # where your key goes, never in code
```

| Module | Script | Saves |
|---|---|---|
| M1 | `inspect_data.py` | `summary.json` |
| M2 | `train.py` | `metrics.json` |
| M3 | [`explain.py`](scripts/explain.py) | `summary.md` |

`.gitignore` already keeps `.env` and your key out of Git.

> No `metrics.json`? Run Module 2 first: `python3 modules/module-2/scripts/train.py`.

---

## 01 · An LLM Is an API

**Three things in, two things back.**

```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    messages=[{"role": "user", "content": prompt}])
msg.content[0].text    # the reply
msg.usage              # the bill
```

| | Part | Meaning |
|---|---|---|
| IN | `model` | Which AI to use. Bigger ones cost more. |
| IN | `max_tokens` | The longest reply allowed. A limit on cost, too. |
| IN | `messages` | Your message to the AI. |
| BACK | `content` + `usage` | The reply text, plus how many tokens were used. |

Like a function: things go in, a result comes out. The difference: it runs on someone else's computer, and they charge by the token.

---

## 02 · Keys and Secrets

**Never paste a key into your code.**

**macOS · Linux**

```bash
export ANTHROPIC_API_KEY=your-key-here
echo ${ANTHROPIC_API_KEY:0:7}               # sk-ant-
```

**Windows · PowerShell**

```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
$env:ANTHROPIC_API_KEY.Substring(0,7)
```

The second line shows only the first 7 characters, to check the key is set without revealing it.

| Rule | Meaning |
|---|---|
| **1. A hidden setting** | Your terminal holds the key as `ANTHROPIC_API_KEY`. The code finds it. No key in the file. |
| **2. `.gitignore`** | A list of files Git must never upload. Our repo already hides secret files. |
| **3. Leaked? Replace it** | Delete the key on the Anthropic website and make a new one. Assume someone found it. |

---

## 03 · Tokens Are the Bill

**One call costs nothing. Ten thousand don't.**

| ~4 | 88 | 77 | $0.0014 |
|---|---|---|---|
| letters per token, in English | tokens we send (input) | tokens we get back (output) | one call, at $3 in / $15 out per million |

**Now multiply:** $0.0014 × 10,000 calls/day × 30 days = **~$426 / month**

Output tokens cost 5× input here. `max_tokens` limits the expensive part. Short messages and short answers save real money.

---

## 04 · When the Call Fails

**If it fails: wait, try again, then stop.**

```python
for attempt in range(1, retries + 1):
    try:
        return client.messages.create(...)
    except (anthropic.RateLimitError,
            anthropic.APIConnectionError):
        time.sleep(2 ** attempt)       # 2s, 4s, 8s
sys.exit("error: gave up after retries")
```

| Rule | Meaning |
|---|---|
| **Retry only short-term problems** | Busy servers and dropped internet. A wrong key won't fix itself, so don't retry it. |
| **Wait longer each time** | Wait 2, then 4, then 8 seconds. Rushing a busy server makes it worse. |
| **Stop at a limit** | Three tries, then fail loudly. Module 1's rule again. |
| **retry = bill** | Every retry that reaches the model is charged again. |

**A retry loop without a limit is a spending loop without a limit.**

> In the real [`explain.py`](scripts/explain.py), the third failure stops right away instead of sleeping again, so the actual waits are 2s, then 4s, then stop.

---

## 05 · Build It: Explain Your Model

**Offline first, then for real.** [`scripts/explain.py`](scripts/explain.py) reads Module 2's scores, writes a message to the AI, and prints the reply with its tokens and cost. `--offline` fakes the reply so every step is free.

- Input: `metrics.json` from Module 2's `train.py`
- Output: `summary.md`, a plain-English explanation

> No key yet? Use `--offline` for every step and skip step 3.

### Step 1 of 5 · Run it offline: no key, no cost

```bash
python3 modules/module-3/scripts/explain.py --offline
```

```
Trust the random forest: it has the highest F1, so it catches the most real
fraud. Accuracy looks great for every model because almost nothing is fraud ...
usage: input_tokens=88 output_tokens=77 · cost $0.00142  (offline estimate)
saved -> summary.md
```

**You should see:** a plain-English summary, a usage line, and `summary.md` saved. **The usage line is the meter.** Reading it is the habit we're building.

### Step 2 of 5 · Read the prompt you're paying for

```bash
grep -n "PROMPT" -A 6 modules/module-3/scripts/explain.py
```

```python
PROMPT = """You are explaining a fraud model to a non-technical manager.
Results on {test_rows} held-out transactions ({fraud_in_test} were fraud):
{table}
In 4 short sentences: which model to trust, why accuracy is misleading here,
and one next step. No jargon."""
```

The prompt is plain English with your scores filled in. It says **who it's for**, **the data**, **how long**, and **what to skip**. (It asks why accuracy is misleading: that's the Desert Forecaster from Module 2.)

### Step 3 of 5 · Set your key, then make a real call (optional)

```bash
export ANTHROPIC_API_KEY=your-key-here      # Windows: $env:ANTHROPIC_API_KEY="..."
python3 modules/module-3/scripts/explain.py
```

Same script, without `--offline`. Now a real AI writes the reply, and the usage line shows real counts:

```
usage: input_tokens=1xx output_tokens=1xx · cost $0.00xxx
```

> ⚠️ **This one is real money.** Fractions of a cent, but real. Your numbers will differ from the offline estimate; that's the point of measuring.
>
> `ANTHROPIC_API_KEY is not set` → the key wasn't saved in this terminal window. It resets when you close the window.

### Step 4 of 5 · Price it with your model's real rates

```bash
python3 modules/module-3/scripts/explain.py --offline --input-rate 1.00 --output-rate 5.00
```

```
usage: input_tokens=88 output_tokens=77 · cost $0.00047  (offline estimate)
```

Prices are dollars per million tokens. Find your model's prices on the provider's pricing page; the script redoes the math. Same tokens, a cheaper model, a third of the cost. **Picking the model is your biggest money saver.**

### Step 5 of 5 · Run the whole pipeline, end to end

```bash
python3 modules/module-1/scripts/inspect_data.py && \
python3 modules/module-2/scripts/train.py && \
python3 modules/module-3/scripts/explain.py --offline
```

| M1 | M2 | M3 | = |
|---|---|---|---|
| `summary.json`: rows, blanks, fraud rate | `metrics.json`: two models, scored | `summary.md`: plain-English summary | **A pipeline:** raw CSV to explanation |

**You should see:** three files saved, in order. If a step fails, `&&` stops the rest, so you never pay to explain broken data.

> The backslash `\` at the end of a line means "this command continues on the next line". On Windows, run the three commands one at a time.

### Commands explained: every command, piece by piece

```bash
python3 modules/module-3/scripts/explain.py --model claude-sonnet-4-5 --max-tokens 300 \
    --input-rate 3 --output-rate 15
```

| Piece | Meaning |
|---|---|
| `--offline` | A fake reply and estimated tokens. No key, no cost. |
| `--model` | Which AI model to use. Check the provider's current list. |
| `--max-tokens 300` | Longest reply allowed, which also caps its cost. |
| `--input-rate` / `--output-rate` | Your model's prices, in dollars per million tokens. |
| `--input metrics.json --out summary.md` | Which scores to read, and where to save the explanation. |
| `export NAME=value` | Save a hidden setting for this terminal window. |
| `A && \` | Run the next line only if this one worked. `\` means "continued". |

**Windows · PowerShell:** `py modules\module-3\scripts\explain.py --offline`

**You should see:** a summary, a usage line with both token counts, and a cost. Write the cost down every time.

| Command | Usage line (offline) |
|---|---|
| `--offline` | `input_tokens=88 output_tokens=77 · cost $0.00142` |
| `--offline --input-rate 1.00 --output-rate 5.00` | `input_tokens=88 output_tokens=77 · cost $0.00047` |
| `--offline --max-tokens 60` | `input_tokens=88 output_tokens=60 · cost $0.00116` |

---

## Capstone: data in, prediction out, summary back

Pick any spreadsheet (CSV) with a yes/no column you care about (customer churn, loan approvals, spam). Run the same three steps, and hand in something anyone can understand. Free public datasets exist on sites like Kaggle; or reuse `transactions.csv` with one change, like a new feature.

**Done means:**

- **Reproducible:** venv + `requirements.txt`; a stranger can rebuild it.
- **Honest:** a fair quiz; F1 beats the do-nothing model.
- **Explained:** a plain-English summary from an AI, with its cost written down.

**Tools you now use:** Python · venv · pip · pandas · scikit-learn · the Anthropic SDK · Git

**Where this leads:** GPU Optimization for AI-ML Systems, AI Agent Operations, and Agent Cost Control: all in the AI-ML Membership.

## Your turn (3 minutes): read your own meter, for free

1. **Run it:** run `explain.py --offline`. Find the usage line: 88 in, 77 out, $0.00142.
2. **Cap it:** add `--max-tokens 60`. Output tokens drop to 60; cost drops to $0.00116.
3. **Scale it:** multiply your cost by 10,000 calls × 30 days. Would you sign that bill?

## Self-check, from memory

Close your notes. Answer out loud:

**"Which two numbers decide what an AI request costs?"** Bonus: which of the two costs more per token?

<details>
<summary>Check yourself</summary>

Input tokens and output tokens, each times its own price. Bonus: output tokens. At our script's prices, they cost 5× more.
</details>

## Recap · your win: four new skills

- ✅ **An LLM is a function.** Your message goes in; a reply and a token count come back.
- ✅ **Keys stay hidden.** Never in code or online. Leaked? Make a new one.
- ✅ **Check the meter.** Input and output, priced separately, logged on every call.
- ✅ **Retries need a limit.** Wait longer each try, stop at three. Every retry costs money.

## Before you ship

Look at your usage line and ask one question:

**"What does this cost at 10,000 calls a day?"**

If you can answer that before you launch, you're ahead of most teams. Agent Cost Control picks up right here.

**You can do this.** From a raw CSV to a trusted model to a plain-English summary, with the cost written down.

*Box it · Beat the forecaster · Check the meter*

---

## Appendix A · Exercises (do these before the capstone)

Everyone: do **01**, **06** and **08**.

| # | Exercise | Task |
|---|---|---|
| 01 | **Run it offline** | Get a `summary.md` with no key at all. |
| 02 | **Shorten the prompt** | Cut it by half. Did input tokens drop? Did quality? |
| 03 | **Cap the reply** | Run with `--max-tokens 60`. What breaks first? |
| 04 | **Change the audience** | Rewrite the prompt for an engineer. Compare. |
| 05 | **Price three models** | Same tokens, three rate pairs. Make a small table. |
| 06 | **Log every call** | Append each usage line to `calls.log` with a timestamp. |
| 07 | **Break the key** | Set a wrong key. Read the error. Is it retried? Should it be? |
| 08 | **Answer the question** | Cost per month at 10,000 calls a day, for your model. |

## Appendix B · Glossary: every term from Module 3

| Term | Meaning |
|---|---|
| **API key** | A secret that proves who you are, and who pays. |
| **Environment variable** | A hidden setting your terminal gives to programs. Where keys belong. |
| **Token** | A small piece of a word, about 4 letters. AI bills by tokens. |
| **Input vs output tokens** | What you send vs what comes back. Priced separately. |
| **max_tokens** | The ceiling on a reply's length and output cost. |
| **Exponential backoff** | Retrying with waits that double: 2s, 4s, 8s, then stop. |
