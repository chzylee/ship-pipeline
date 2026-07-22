# Ship Pipeline

**A guided build process that keeps senior-engineer ownership in LLM-speed development.**

LLMs hand you build velocity; what they quietly take is the act of coding itself — and with
it the things seniority is made of: knowing why every decision was made, what "done" actually
means, whether the build honors the design, and being able to defend and evolve the result.
Skip those and you ship faster right up until you can't support, explain, or grow what you
shipped.

Ship Pipeline is that seniority, put back in as **process**. It guides a build from design
through shipping with clarity on what's going on at every stage, and it generates the
documentation as it goes — so you (or anyone below staff-level expertise, or anyone who just
didn't type the code) can build at LLM speed **and own the result**: every deliverable is
paired with a verifier that binds it to its source, "done" is a command that passes rather
than a feeling, and the trail it leaves is the onboarding a teammate could pick up cold.

## The pipeline

| # | Stage | What it produces | What verifies it |
|---|-------|------------------|------------------|
| 0 | Sourcing & Scope Gate — find what to build, harden it (methods: Scout · Sidequest · office-hours) | a Build Brief + lane declaration, hardened into the one job / definition of done / not-in-v0 list | method-matched: Reality Probe (main lane) · black-box test + greenlight (sidequest lane); the segment / one-job / kill checklist |
| 1 | Design Doc | **the truth** — the canonical spec everything traces to | design review |
| 2 | Build Plan | a **recommendation**: shared whole-design context + a proposed increment ordering with per-increment build prompts, sized to the owner's prediction span | anchor coverage (increments' union = the whole design) + cross-model cold read (or a two-build bake-off) |
| 3 | ⟳ Build Loop | the code, one increment at a time — the increment you judge is next, which need not be the plan's: build → `/test-spec` slice → tests made real (reds = decisions still owed) → `/finish-build` drives reds green → ratify gate → commit; WIP 1 | per increment: slice tests green + the owner's verify act (predict-then-run · break-it-on-purpose · change-one-thing), logged |
| 4 | Build Review | code ↔ design reconciliation of the assembled whole; the plan is reconciled to what was actually built | fresh judge: six checks → judgment + blockers |
| 5 | Test Sweep | version-level Test Spec: the seams between increments, the end-to-end scenario, the gap audit vs. the whole design; unmet MUSTs parked `xfail(strict)` | every item anchored to the design, bounded by not-in-scope |
| 6 | Acceptance Gate | the verdict that the build is DONE: the one command green on a clean checkout | leg-checklist administered by `/acceptance-gate` — `/finish-build` discharges parked `xfail` legs; failure paths, documented path, the owner's evidence-read, the human legs |
| 7 | Own Your Code | onboarding that confers ownership | re-derive a decision cold |

**Gates are leg-checklists, not single events.** A gate passes leg by leg; a leg that can't pass
now is *deferred* and must name the later step that discharges it. The Acceptance Gate's
automated-suite leg is discharged by `/finish-build`, which drives the ratified-but-deferred
behaviors (committed as `xfail(strict)`) to green. So **"build complete" is not "suite green"** — a
suite can be green while MUST behaviors sit parked under `xfail`. Build complete = every MUST leg
built-and-green *or* consciously demoted-and-logged (a demotion is a ratified decision, never a
quiet edit), every deferred marker removed, nothing regressed. That is the exit criterion into Own
Your Code.

**The design is truth; the plan is a recommendation.** Only the Design Doc is binding — it is the
comprehensive statement of what you actually want built, and every test, review, and gate traces to
it. The Build Plan is one viable *way* to get there, written before the build taught you anything.
Building changes what you know, so the plan is expected to go stale: **deviating from it is not a
violation and needs no permission.** Build the increment that makes sense to you next, in the shape
that makes sense once you're in the code. What the pipeline asks is not "does this fit the plan?"
but **"does this serve the design?"** — the only question a gate is allowed to block on.

The plan is settled up *after* the fact, not defended during it:

- **In the loop (stage 3)** — build uninhibited. Note deviations in passing; don't stop to re-plan,
  and never re-shape the code to fit a stale increment boundary.
- **At Build Review (stage 4)** — **reconcile**: walk the plan against what exists, mark each
  increment built / built-differently / dropped / still-owed, and rewrite the remaining ordering to
  start from reality. Only two things are real findings here: work the **design** requires that
  nothing built covers, and work built that the **design** doesn't ask for. A plan/code mismatch
  where the design is satisfied is bookkeeping, not a defect.
- **After reconciliation** — the owner optionally reworks the forward plan. Optional: a reconciled
  plan whose remainder still reads sensibly needs no rewrite.

A deviation that changes *what gets built* rather than *the order it's built in* is a design
change, not a plan deviation — that goes back to the Design Doc through `/ratify` and is logged in
`docs/decision_log.md`. This is the one line the doctrine holds: the plan bends freely, the design
bends only on the record.

You can enter at any stage — each skill establishes the handshake with the stage before it. The
sourcing methods are optional front doors within stage 0: `/scout` when you don't have an idea yet
(main lane) · `/sidequest` to source low-ownership builds for autonomous runs (sidequest lane);
with an idea already in hand, begin at the Scope Gate half of stage 0.

## What each run carries in-repo

The pipeline's state, decisions, and provenance live in the **project's own repo**, so a cold clone
is self-describing — no one reconstructs "where is this and how did it get here" from chat, memory,
or a wiki. Each fact has one home and is handed forward to the stage that consumes it:

| Artifact | Lives at | Source of truth for | Handed forward to |
|----------|----------|---------------------|-------------------|
| Position + stage map + gate legs | `docs/build_status.md` | where this project is in the pipeline | anyone cloning · `/own-your-code`'s current-state · advanced by `/finish-build` |
| Build Plan (advisory) | `docs/build_plan.md` | the *recommended* route through the design — never what's binding | the build loop as a suggestion · reconciled to reality at Build Review |
| Ratified test contract | `TEST_SPEC.md` | what must be true to trust the build | `/finish-build` (its legs) · Acceptance Gate |
| Code/build decisions (each fork + why) | `docs/decision_log.md` | why the build is the way it is | `/own-your-code` drift check · `/finish-build` logs forks here |
| Ownership record (`predicted`/`surprised`/`no-opinion`) | `RATIFICATION_LOG.md` | demonstrated judgment + blind spots | `/own-your-code` study guide |
| Driving prompt per step | `docs/prompts/NN-<step>.md` | provenance / retrace of each step | audit of a fast or back-filled build |

**Repo owns run-state; the wiki owns the process.** The repo is the single source of truth for
*this build* — position, decisions, provenance, ratification. The Ship Pipeline wiki is the single
source of truth for the *generic process* — stage definitions and how-tos — and holds no project's
position; skill maturity lives in the Skills table below, not restated on the wiki. Two homes for
one fact is drift: retire any per-project "current state" wiki page in favor of `build_status.md`.

**Changelog boundary:** the Notion Changelog records changes to the pipeline's *stage documents*;
the repo's `decision_log.md` records decisions about the *code/build itself*.

The `docs/build_status.md` skeleton — the one place "where am I" is answered:

```markdown
# Build Status — <project>

Pipeline: 0 Sourcing & Scope · 1 Design · 2 Build Plan · 3 ⟳ Build Loop · 4 Review · 5 Test Sweep · 6 Acceptance Gate · 7 Own Your Code
Position: **6 · Acceptance Gate** (in progress)

## Gate legs — 6 · Acceptance Gate
- [x] Scenario A — human pass, <date>
- [x] Scenario B — human pass, <date>
- [ ] Automated-suite leg — deferred → /finish-build (N MUST behaviors parked as xfail-strict)

## Log
- <date> — advanced to <stage>: <one line>
```

## Skills

Skills are forged from real ships and land here as they prove out — this repo is harvested,
not built ahead.

| Skill | Status |
|-------|--------|
| `/scout` | **Available** (v2.0) — the front door: inverted office-hours that discovers what to build from a person + their real work → a Build Brief |
| `/own-your-code` | **Available** (v2.1.0) — turn an AI-built repo into an onboarding that confers ownership |
| `/test-spec` | **Available** (v0.5.0) — dialogue-driven skill producing a Test Spec: what must be tested to trust a build; slice mode per increment, sweep mode per version; ratifies via `/ratify` |
| `/ratify` | **Available** (v0.4.0) — cross-stage ratification protocol: prediction-before-reveal at blocking stops, logging `predicted`/`surprised`/`no-opinion` into a measurable ownership record + blind-spot reading list. Also emits a sanitized, plugin-owned telemetry corpus (`~/.claude/ship-pipeline/sends.jsonl`) that compounds across builds into presentable proof — see [telemetry schema](skills/ratify/telemetry/README.md) |
| `/finish-build` | **Available** (v0.1.0) — the execution-stage **driver**: drives committed-failing (`xfail`-strict) tests to green through a predict-then-reveal loop, escalating design forks to `/ratify` — in-loop for an increment's reds, canonically for the sweep's parked legs |
| `/acceptance-gate` | **Available** (v0.1.0) — the **criterion** to `/finish-build`'s driver: administers the gate that decides DONE — runs the mechanical legs (clean-checkout command, failure paths, documented path), presents the evidence and human legs as blocking stops, records the verdict. Never fixes code; never passes a human leg on the human's behalf |
| `/sidequest` | **Experimental** (v0.1.0) — the ▸ stage's autonomous second method: mines friction, screens with the black-box test (low ownership requirement, not low maintenance), emits launch-ready autonomous build briefs into the Sidequest Projects stockpile. Drafted ahead of first proven run; graduates on the first sourced-and-shipped sidequest |
| `/build-plan` | Next up — turn a design doc into a Build Plan: shared context + a *recommended* increment ordering with build prompts sized to the owner's verification bandwidth. Advisory by construction: it must be re-runnable against a part-built repo to reconcile the plan to reality, and must never ask the builder to justify a deviation the design already covers |
| `/build-review`, `/bake-off`, `/current-state` | Being harvested |

## The public page — `/record`

A self-contained static page that presents what `/ratify` is and the ownership data behind it, as a
shareable explainer. Plain HTML — no build step, no dependencies, no JavaScript framework — served
from the repo root by GitHub Pages (light + dark, responsive).

**What it is.** It leads with what `/ratify` does and why it matters (evaluating an AI's output vs.
merely accepting it), then shows the evidence: the telemetry corpus
(`~/.claude/ship-pipeline/sends.jsonl`) aggregated across five delegated deliverables — most of them
*not* code — with the calibration read, the gap-nature finding, the code case (the first build it
ran on), and two worked moments. Numbers are recomputed from the raw corpus, never stored derived;
the page fetches nothing at runtime.
**Served at** https://chzylee.github.io/ship-pipeline/record/ · source: [`record/index.html`](record/index.html)

### Viewing it locally

Static, so any file server over the repo root works:

```bash
# from the repo root
python -m http.server 8000
# then open http://localhost:8000/record/ in a browser
```

Opening `record/index.html` directly via `file://` also works for a quick look.

For hot reload while editing `record/index.html` or `record/styles.css`:

```bash
# from the repo root
npx live-server --port=8000
# then open http://localhost:8000/record/ in a browser — edits auto-reload
```

## Install

Two ways to install. The **default gives skills their bare names** (`/own-your-code`) —
cleaner to use day to day. Plugin mode namespaces them (`/ship-pipeline:own-your-code`) —
choose it if you prefer skills indexed under the suite's name or want plugin-manager
updates.

### Default — bare skill names (30-second install)

Paste this into Claude Code:

```text
Install ship-pipeline: run
  git clone https://github.com/chzylee/ship-pipeline.git ~/repos/ship-pipeline
(or `git -C ~/repos/ship-pipeline pull` if it already exists), then symlink every
directory under ~/repos/ship-pipeline/skills/ into ~/.claude/skills/ (macOS/Linux:
`ln -sfn <skill-dir> ~/.claude/skills/<name>`; Windows: copy the folders instead and
note that updating means re-copying). If a name already exists in ~/.claude/skills/,
replace it only if it is a symlink or an older copy of the same skill — otherwise
list the conflict and skip it. Finish by listing what was installed and remind me to
restart Claude Code so the skills load.
```

Or do it by hand:

```bash
git clone https://github.com/chzylee/ship-pipeline.git ~/repos/ship-pipeline
for s in ~/repos/ship-pipeline/skills/*/; do
  ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"
done
```

Symlinks mean a `git pull` updates every installed skill in place.

### Plugin mode — namespaced `/ship-pipeline:*`

Paste this into Claude Code:

```text
Install the ship-pipeline plugin: run
  claude plugin marketplace add chzylee/ship-pipeline
then
  claude plugin install ship-pipeline@ship-pipeline
and confirm the skills are available (namespaced, e.g. /ship-pipeline:own-your-code).
```

Or by hand:

```bash
claude plugin marketplace add chzylee/ship-pipeline
claude plugin install ship-pipeline@ship-pipeline
```

## Update

- **Bare-name install:** `git -C ~/repos/ship-pipeline pull` — symlinked skills update
  instantly. Or paste: *"Update ship-pipeline: git -C ~/repos/ship-pipeline pull, then tell
  me what changed."*
- **Plugin install:** `claude plugin update ship-pipeline` (every push to this repo is a
  release — versions track commits).

## Uninstall

- **Bare-name install:** remove the symlinks and the clone:
  `for s in ~/repos/ship-pipeline/skills/*/; do rm ~/.claude/skills/"$(basename "$s")"; done && rm -rf ~/repos/ship-pipeline`
- **Plugin install:** `claude plugin uninstall ship-pipeline`

## Requirements

Nothing to run: the skills work with a stock Claude Code install, no dependencies or keys.
Optional: `/own-your-code`'s cross-model onboarding read can use a genuinely
different-lineage model if a free `OPENROUTER_API_KEY` or `GEMINI_API_KEY` is present in
`~/.secrets/llm.env` — see [skills/own-your-code/README.md](skills/own-your-code/README.md).
