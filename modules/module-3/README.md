# Module 3 · Make It Explain Itself

**Phrase:** *Check the meter.* · **Big idea:** every call has a price; write it down.

## Before you start

```bash
source .venv/bin/activate                # Windows: .venv\Scripts\Activate.ps1
python3 -c "import anthropic"            # silence is success
```

An API key is **optional**: every step works with `--offline` (a fake reply, no key, no cost).
For real calls, create a key at [console.anthropic.com](https://console.anthropic.com) → API keys.

## Keep your key out of your code

```bash
export ANTHROPIC_API_KEY=your-key-here           # macOS / Linux
$env:ANTHROPIC_API_KEY="your-key-here"           # Windows PowerShell
```

`.gitignore` already keeps `.env` files out of Git. Leaked a key? Delete it on the Anthropic website and make a new one.

## Build it: explain your model

```bash
# 1. Run it offline: no key, no cost
python3 modules/module-3/scripts/explain.py --offline

# 2. Read the prompt you're paying for
grep -n "PROMPT" -A 6 modules/module-3/scripts/explain.py

# 3. Set your key, then make a real call (real money: fractions of a cent)
python3 modules/module-3/scripts/explain.py

# 4. Price it with your model's real rates ($ per million tokens)
python3 modules/module-3/scripts/explain.py --offline --input-rate 1.00 --output-rate 5.00

# 5. Run the whole pipeline, end to end
python3 modules/module-1/scripts/inspect_data.py && \
python3 modules/module-2/scripts/train.py && \
python3 modules/module-3/scripts/explain.py --offline
```

Expected usage lines (offline):

| Command | Usage line |
|---|---|
| `--offline` | `input_tokens=88 output_tokens=77 · cost $0.00142` |
| `--offline --input-rate 1.00 --output-rate 5.00` | `input_tokens=88 output_tokens=77 · cost $0.00047` |
| `--offline --max-tokens 60` | `input_tokens=88 output_tokens=60 · cost $0.00116` |

$0.0014 × 10,000 calls a day × 30 days ≈ **$426 a month**. Check the meter before the bill arrives.

## All the options

| Option | What it does |
|---|---|
| `--offline` | A fake reply and estimated tokens. No key, no cost. |
| `--model claude-sonnet-4-5` | Which AI model to use. Check the provider's current list. |
| `--max-tokens 300` | Longest reply allowed, which also caps its cost. |
| `--input-rate 3 --output-rate 15` | Your model's prices, in dollars per million tokens. |
| `--input metrics.json --out summary.md` | Which scores to read, and where to save the explanation. |

Retries: only short-term problems (rate limits, dropped connections) are retried, waiting 2s then 4s, and the script stops after 3 tries. A wrong key is never retried.

## Exercises (do these before the capstone)

1. **Run it offline:** get a `summary.md` with no key at all.
2. **Shorten the prompt:** cut it by half. Did input tokens drop? Did quality?
3. **Cap the reply:** run with `--max-tokens 60`. What breaks first?
4. **Change the audience:** rewrite the prompt for an engineer. Compare.
5. **Price three models:** same tokens, three rate pairs. Make a small table.
6. **Log every call:** append each usage line to `calls.log` with a timestamp.
7. **Break the key:** set a wrong key. Read the error. Is it retried? Should it be?
8. **Answer the question:** cost per month at 10,000 calls a day, for your model.
