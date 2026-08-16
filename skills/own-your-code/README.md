# own-your-code

A Claude skill that turns an **AI-built (or inherited) repo into an onboarding that confers
ownership** — the internal engineering wiki a fresh teammate reads to *own* the project
without reading the code first. After AI compresses a week (or months) of building into hours,
the code exists but the ownership doesn't: you can't yet justify or evolve its key decisions,
because you never read every line or weighed the options. This gives that back — not by
re-reading every line (that re-spends the week you saved), but by reconstructing the project
top-down and re-deriving only the decisions that aren't already yours.

It is the **ownership pass of [Ship Pipeline](../../README.md)** — run after an increment the
acceptance gate has proven, not as a numbered step of the S1-S7 loop — and works standalone on any
repo.

## Who it's for
Write-target is **an engineer who inherited the repo from someone no longer on the team** and
has to adopt it as their own. Future-you, cold months later, is a subset of that reader. If a
stranger can own it from the doc, so can you.

## What "own" means
Not 100% line-level recall — that's the acceptable cost of not typing every line. Ownership =
**enough mastery to justify and evolve the key decisions**, where *key* means the decision
moves **maintainability, user experience, or cost**. Defend and grow the project on those
three axes and you own it well enough to ship, support, and scale it.

## What makes it different from "explain my repo"
- **Onboarding, not a catalogue** — top-down (what it is → core-component map → each component
  broken down, decisions nested inside their component), so you can own it before reading source.
- **Decisions tiered by the lens that matters** — full treatment for calls that move
  maintainability / UX / cost, confirm-form (one line) for the rest, trivia omitted.
- **Drift check** — reconciles what was *built* against the design doc / decision ledger and
  flags where the AI build silently diverged (the top corroder of AI-built ownership).
- **Certainty markers** — every rationale tagged `[code]` / `[doc]` / `[likely-why]` /
  `[reconsider]`; a reconstructed "why" is never dressed up as confirmed history.
- **Cognitive-load contract** — cockpit-first, progressive disclosure, disposable: regenerate
  after any change, never hand-edit (so multiple output targets can't drift).

## Success test
A fresh engineer — or you, cold, months later — reads it and can, **without opening the
code**: say what the project is and where it stands, hold its core-component map, and justify
(and know how to evolve) each key decision on maintainability / UX / cost.

## Output
One regenerable guide — **`docs/own_your_code.md`** in the target repo, in version control — in this
order: **cockpit** (one screen: what-it-is + current state + component map + decisions index +
where-to-spend) → **the system** (components + how they connect + run/debug cold) → **data pipeline**
(first input → final output — the data flow the component map doesn't show) → **each component
broken down** (decisions nested and justified) → **drift** (built vs design) →
**ranked gaps** → **drills**. A real handoff doc then gets a **cross-model onboarding read** (a fresh
reader validates it) folded back before it ships.

**The repo is canonical**, and the file is overwritten in place on each run — version history is
git's job. A wiki may hold a dated, non-editable snapshot that names `<repo>/docs/own_your_code.md`
as its source; an editable copy anywhere else is the exact thing that makes a later run read the
wrong file.

This is the **engineering wiki**, distinct from the project's own README: the README is the
user/public front door; this is the internal onboarding that confers ownership of the build.

## Scope (held line)
Owns the **built artifact** — what it is, how it's structured, why each part is built that way,
and where it drifted from design. It does NOT own the upstream idea/problem decisions; those
belong to the design phase and a decision/Judgment Ledger, which this skill *consumes* to
detect drift, not reproduces.

## Install
Installed as part of **[ship-pipeline](../../README.md#install)** — this directory is the
skill's canonical home. (The old standalone `own-your-code-skill` repo is retired; if you
installed from it, remove that copy so a name-trigger can't grab a stale version.)

## Requirements & setup
- **Nothing required to run.** The cross-model onboarding read defaults to a fresh sub-agent (built
  into the agent harness) — no dependencies, no keys, no paid tools; it works the moment the skill
  is installed, on any machine.
- **Optional — a different-*lineage* review.** For the opportunistic upgrade (a genuinely different
  model reads the doc, not just a fresh same-model sub-agent), drop a free key into `~/.secrets/llm.env`
  (one `KEY=value` per line): `OPENROUTER_API_KEY` and/or `GEMINI_API_KEY`. The bundled
  `tools/cross_model_review.py` (Python 3, stdlib only — no `pip install`) is then used automatically.

## Use
Invoke on a built repo: "own my code for X" / "onboard me to X" / "step into this build".
Read-only on your code — never modifies code or data. Re-runnable; regenerate after any change.

## Status
See [`VERSION`](VERSION). Onboarding/top-down form; the data-pipeline section; and the
portable-first cross-model onboarding read (fresh sub-agent by default, different lineage when a
free key is present). The v1 roster rework moved the output home into the repo, made retraces and
conformance reports its raw material, and replaced the old maintainability/UX/cost ranking with the
**re-entry lens** — reconstruct, reach, surprise — so nothing here computes how much a decision
ought to matter to you.

`SKILL.md` is the canonical instruction set; the version lives in `VERSION`.
