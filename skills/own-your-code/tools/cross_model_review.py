#!/usr/bin/env python3
"""Cross-model onboarding review for own-your-code docs.

Feeds an ownership doc (TEXT ONLY, never the source) to a DIFFERENT model and asks it to
onboard cold: run the success test + emit reader-side "Least confident / loose ends".
The point is to validate the doc against its actual use case — can a fresh reader take the
project over from the doc alone? Its cold-read confusion is the signal.

Providers, in fallback order (a genuinely different architecture beats a same-family model):
  1. OpenRouter  (OPENROUTER_API_KEY)  — one key, real model diversity (Qwen/DeepSeek/Llama/...)
  2. Gemini      (GEMINI_API_KEY)       — different family, reliable free `flash`

Keys are read from the environment, or parsed from ~/.secrets/llm.env if not already set.
Stdlib only — no pip install.

Usage:
  python tools/cross_model_review.py <doc.md> [--provider auto|openrouter|gemini]
         [--model <slug>] [--out <path>] [--prompt <promptfile>]

Prints the review to stdout (and to --out if given), prefixed with a provenance line
(provider + model) so a run is always traceable to who reviewed it.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

SECRETS = Path.home() / ".secrets" / "llm.env"
# Free-tier models rate-limit per model/upstream, so rotate across several strong,
# different-lineage ones before falling back to Gemini. Override with OYC_REVIEW_MODELS (csv).
DEFAULT_OPENROUTER_MODELS = [
    m.strip() for m in os.environ.get(
        # Fast, reliable, different-lineage mid-size models. The giant reasoning models
        # (nemotron-120b, hermes-405b) are slow and sometimes emit empty completions —
        # available via --model, but not in the default rotation. Gemini is the backstop.
        "OYC_REVIEW_MODELS",
        "meta-llama/llama-3.3-70b-instruct:free,"
        "qwen/qwen3-next-80b-a3b-instruct:free",
    ).split(",") if m.strip()
]
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

REVIEW_PROMPT = """You are reviewing DOCUMENTATION, not code. Below is an "ownership wiki" meant to let a
fresh engineer take over a repo WITHOUT reading the source first — well enough to explain its
architecture, defend its key decisions on maintainability / UX / cost, and actually locate and
shape the fix for a bug, from the doc alone.

You have NOT seen this repo or its source. Read it COLD, as that fresh engineer. Then answer:

1. SUCCESS TEST — from the doc alone: (a) what is this project, in 2 sentences? (b) describe the
   component map and how data flows through it. (c) pick the single most important decision and
   defend it as if in an interview. (d) pick one named bug/gap and describe the SHAPE of the fix
   (you have no source — just say where you'd go and what you'd change).
2. LEAST CONFIDENT / LOOSE ENDS — the specific places you lost the thread, had to guess, or could
   not follow. Cite the section. Be concrete; "I don't know X" is preferred over inventing.
3. MOST NEEDED — the few additions that would let you fully onboard.

Be direct, not diplomatic — the goal is to find real gaps. Call out anything that reads as padding
or as assumed context.

=== THE DOCUMENT ===
"""


def load_secrets():
    if not SECRETS.exists():
        return
    for line in SECRETS.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _post(url, headers, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=75) as r:
        return json.loads(r.read().decode())


def _openrouter_once(prompt, model, key):
    data = _post(
        "https://openrouter.ai/api/v1/chat/completions",
        {
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "https://github.com/chzylee/own-your-code-skill",
            "X-Title": "own-your-code cross-model review",
        },
        {"model": model, "messages": [{"role": "user", "content": prompt}]},
    )
    msg = data["choices"][0]["message"]
    content = msg.get("content")
    if not (content and content.strip()):
        content = msg.get("reasoning")  # some reasoning models emit only a reasoning field
    if not (content and content.strip()):
        raise RuntimeError(f"empty completion from {model}")  # rotate past it
    return content


def review_openrouter(prompt, models):
    """Try each free model once (free tiers rate-limit per model/upstream); rotate, then caller falls back."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    last = None
    for model in models:
        try:
            return _openrouter_once(prompt, model, key), f"openrouter:{model}"
        except Exception as e:  # noqa: BLE001 — rate-limit / unavailable → rotate to the next model
            last = e
            sys.stderr.write(f"[openrouter] {model} failed ({getattr(e, 'code', '?')}); trying next\n")
    raise last or RuntimeError("all OpenRouter models failed")


def review_gemini(prompt, model):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    data = _post(url, {}, {"contents": [{"parts": [{"text": prompt}]}]})
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    if not (text and text.strip()):
        raise RuntimeError(f"empty completion from gemini:{model}")
    return text, f"gemini:{model}"


def main():
    ap = argparse.ArgumentParser(description="Cross-model cold onboarding review of an ownership doc.")
    ap.add_argument("doc", help="Path to the ownership doc (markdown). The reviewer sees this ONLY, never the source.")
    ap.add_argument("--provider", default="auto", choices=["auto", "openrouter", "gemini"])
    ap.add_argument("--model", default=None, help="Override the model slug for the chosen provider.")
    ap.add_argument("--out", default=None, help="Also write the review to this path.")
    ap.add_argument("--prompt", default=None, help="Override the built-in review prompt with a file.")
    args = ap.parse_args()

    load_secrets()
    doc = Path(args.doc).read_text(encoding="utf-8")
    preamble = Path(args.prompt).read_text(encoding="utf-8") if args.prompt else REVIEW_PROMPT
    prompt = preamble + "\n" + doc

    order = {"auto": ["openrouter", "gemini"], "openrouter": ["openrouter"], "gemini": ["gemini"]}[args.provider]
    last_err = None
    for prov in order:
        try:
            if prov == "openrouter":
                text, used = review_openrouter(prompt, [args.model] if args.model else DEFAULT_OPENROUTER_MODELS)
            else:
                text, used = review_gemini(prompt, args.model or DEFAULT_GEMINI_MODEL)
            out = f"<!-- cross-model review · via {used} -->\n\n{text}\n"
            if args.out:
                Path(args.out).write_text(out, encoding="utf-8")
            sys.stdout.buffer.write(out.encode("utf-8", errors="replace"))
            return 0
        except Exception as e:  # noqa: BLE001 — surface any provider failure, then fall back
            last_err = e
            sys.stderr.write(f"[{prov}] failed: {e}\n")
            if isinstance(e, urllib.error.HTTPError):
                try:
                    sys.stderr.write(e.read().decode()[:600] + "\n")
                except Exception:
                    pass
    sys.stderr.write(f"All providers failed. Last error: {last_err}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
