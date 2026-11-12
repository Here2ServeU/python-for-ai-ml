"""Module 3: ask an AI to explain Module 2's scores, and check the meter.

Reads metrics.json (from Module 2), sends a short prompt to Claude, prints the
reply plus its token usage and cost, and saves the reply to summary.md.

Run from the repo root:
    python3 modules/module-3/scripts/explain.py --offline        # free: no key, no cost
    export ANTHROPIC_API_KEY=your-key-here                         # Windows: $env:ANTHROPIC_API_KEY="..."
    python3 modules/module-3/scripts/explain.py                  # a real call (real money)

Prices are dollars per MILLION tokens. Check your provider's pricing page.
"""
import argparse
import json
import math
import os
import sys
import time

PROMPT = """You are explaining a fraud model to a non-technical manager.
Results on {test_rows} held-out transactions ({fraud_in_test} were fraud):
{table}
In 4 short sentences: which model to trust, why accuracy is misleading here,
and one next step. No jargon."""

# Offline mode: a canned reply, so every step can be practised for free.
OFFLINE_REPLY = (
    "Trust the random forest: it has the highest F1, so it catches the most real\n"
    "fraud. Accuracy looks great for every model because almost nothing is fraud, "
    "so a model that never says fraud still scores 97%. The forest also flags "
    "many honest customers. Next step: reduce those false alarms, then test it again."
)


def estimate_tokens(text):
    """Rough rule for English: about 4 characters per token."""
    return math.ceil(len(text) / 4)


def load_metrics(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"error: {path} not found. Run Module 2 first:"
                 " python3 modules/module-2/scripts/train.py")


def build_prompt(metrics):
    table = "\n".join(
        f"{name}: accuracy {s['accuracy']:.3f}, F1 {s['f1']:.3f}"
        for name, s in metrics["models"].items()
    )
    return PROMPT.format(test_rows=metrics["test_rows"],
                         fraud_in_test=metrics["fraud_in_test"], table=table)


def call_claude(prompt, model, max_tokens, retries=3):
    """One real API call. Retry short-term problems only, with a limit."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("error: ANTHROPIC_API_KEY is not set. Set it, or use --offline.")
    try:
        import anthropic
    except ImportError:
        sys.exit("error: the anthropic package is missing. Run: pip install -r requirements.txt")

    client = anthropic.Anthropic()  # reads the key from the environment, never from code
    for attempt in range(1, retries + 1):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            text = "".join(block.text for block in msg.content if block.type == "text")
            return text, msg.usage.input_tokens, msg.usage.output_tokens
        except (anthropic.RateLimitError, anthropic.APIConnectionError) as err:
            if attempt == retries:
                break
            wait = 2 ** attempt  # 2s, 4s, 8s
            print(f"attempt {attempt} failed ({type(err).__name__}); retrying in {wait}s")
            time.sleep(wait)
        except anthropic.AuthenticationError:
            sys.exit("error: the API key was rejected. A wrong key won't fix itself, so no retry.")
    sys.exit(f"error: gave up after {retries} retries")


def offline_reply(prompt, max_tokens):
    """Fake reply + estimated tokens. The reply is cut to max_tokens, like a real one."""
    reply = OFFLINE_REPLY
    output_tokens = estimate_tokens(reply)
    if output_tokens > max_tokens:
        reply = reply[: max_tokens * 4]
        output_tokens = max_tokens
    return reply, estimate_tokens(prompt), output_tokens


def main():
    parser = argparse.ArgumentParser(description="Explain the model scores in plain English.")
    parser.add_argument("--input", default="metrics.json", help="scores from Module 2")
    parser.add_argument("--out", default="summary.md", help="where to save the explanation")
    parser.add_argument("--offline", action="store_true", help="fake reply: no key, no cost")
    parser.add_argument("--model", default="claude-sonnet-4-5", help="which AI model to use")
    parser.add_argument("--max-tokens", type=int, default=300, help="longest reply allowed")
    parser.add_argument("--input-rate", type=float, default=3.0, help="$ per million input tokens")
    parser.add_argument("--output-rate", type=float, default=15.0, help="$ per million output tokens")
    args = parser.parse_args()

    prompt = build_prompt(load_metrics(args.input))
    if args.offline:
        reply, tokens_in, tokens_out = offline_reply(prompt, args.max_tokens)
    else:
        reply, tokens_in, tokens_out = call_claude(prompt, args.model, args.max_tokens)

    cost = tokens_in * args.input_rate / 1e6 + tokens_out * args.output_rate / 1e6
    print(reply)
    note = "  (offline estimate)" if args.offline else ""
    print(f"usage: input_tokens={tokens_in} output_tokens={tokens_out} · cost ${cost:.5f}{note}")

    with open(args.out, "w") as f:
        f.write("# Fraud model: plain-English summary\n\n")
        f.write(reply.strip() + "\n\n")
        f.write(f"_model: {'offline' if args.offline else args.model} · "
                f"input_tokens={tokens_in} · output_tokens={tokens_out} · cost ${cost:.5f}_\n")
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
