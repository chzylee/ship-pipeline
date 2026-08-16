---
name: own-your-code
description: 'Turn an AI-built repo into an onboarding that confers ownership: a doc a fresh team member (or the original author, returning cold) reads to OWN the project — what it is and its current state, the core-component map, and each key decision justified so they can defend and evolve it. Organized top-down (what it is → core components → each component broken down, decisions nested and contextualized, never a flat catalogue). The bar is stepping back in comfortably: someone returns cold and can pick the project up and own it without re-deriving how it came to be. Decisions are selected and ranked by the RE-ENTRY lens — can the why be reconstructed from the source alone, how much else assumes it, and would a competent reader guess wrong — all readable properties, never a significance label, because how much a decision matters is the owner''s to judge and is never computed here. Works on ANY project: retraces and conformance reports are inputs if present, never prerequisites, and the same doc to the same bar must be producible from a codebase and nothing else. Includes the full data pipeline (first input → final output), a runtime/operational model, and a design→build drift check, in a compact, cockpit-first, low-cognitive-load format; real handoff docs get a final cross-model cold onboarding read (a fresh model validates the doc against its actual use case). Tier 1: one of the five skills that make up using Ship Pipeline, run after an increment the acceptance gate has proven rather than as a numbered step of the loop. Consumes docs/retrace/*.md for the why behind each decision, and the conformance reports for drift, rather than re-deriving either. Triggers on "own my code for X", "onboard me to X", "study guide for X project", "interview-prep my code", "help me own X", or after pushing updates. Re-runnable; disposable — regenerate after any change.'
---

# Own Your Code

Turn an AI-built repo into an **onboarding that confers ownership**. After AI compresses a
week (or months) of building into hours, the code exists but the ownership doesn't — you
can't yet justify or evolve its key decisions, because you never read every line or weighed
the options. This skill produces the document a **fresh team member would need to own the
project**, and it treats even the original author as fresh, because after an AI build (and
while juggling many projects) you are. The reader should come out able to **own** it, not
just read about it. The experience should feel like onboarding to a well-documented
codebase, not consulting a catalogue that assumes you've already read the source.

## What "own" means here (calibration — read this first)

Not 100% line-level recall. That's the unrecoverable cost of not typing every line, and it
is acceptable. Ownership = **enough mastery to justify and evolve the key decisions.**

**The bar is stepping back in comfortably.** Someone returns to this project cold — a new
teammate, or you six months later — and can pick it up and own it without re-deriving how it
came to be. Everything in this doc is judged against that, and nothing else.

**Success test.** A fresh engineer — or you, cold, months later — reads this and can: say
what the project is and where it stands, hold its core-component map, and justify (and know
how to evolve) each key decision — all **without reading the code first.**

**It must work on any project.** A repo built through Ship Pipeline hands you retraces and
conformance reports; most repos won't. Those are inputs *if present*, never prerequisites. The
same doc, to the same bar, has to be producible from a codebase and nothing else — that is the
test of whether this skill actually reconstructs ownership or merely transcribes a paper trail.

## Who it's for — write for a fresh teammate
Calibrate to **an engineer who joined the team and inherited this repo from someone who has
left** — they must read it and adopt it as their own. Future-you, returning cold months later,
is a *subset* of that reader, not the primary target: build it so a stranger can own it and it
will serve you too. Assume zero context; assume senior (don't re-explain fundamentals).

**Write for the maintainer, not the end user.** Refer to users generically ("the user"); keep the
end-user's name/identity and product-strategy asides (positioning, segment-vs-tester, is-it-well-aimed)
out of the doc. A maintainer needs how it works and how to run it — over-specific targeting is a
product judgment, not build ownership, and is out of scope here.

**This is not the README.** The project's `README` is the user/public front door (what it is, how
to use it). This is the **internal onboarding** that confers ownership of what was built. Different
readers, different jobs — don't collapse them, and don't restate the README. Assume the reader can
read the README for usage; spend this doc on why the code is the way it is and how to evolve it.
Where it lives is settled below under *Output target*: the repo.

## Scope — hold this line
Owns the **built artifact**: what it is, how it's structured, why each part is built that
way, and where the build drifted from its design. It does NOT own the upstream idea/problem
decisions — those belong to the design phase (`/design-doc`) and a decision/Judgment
Ledger, which this skill *consumes* (to confirm rationale and detect drift), not reproduces.

## The re-entry lens — threads through everything

A decision is **key** when not knowing it would **obstruct someone stepping back in**. Rank on
three properties, all readable from the code and the repo:

- **Reconstruct** — can the *why* be re-derived from the source alone? If it cannot, the doc
  must carry it. This is the highest-value axis, because it is precisely what a returning owner
  lacks and cannot get anywhere else.
- **Reach** — how much else assumes this choice. A decision three other things are built on
  has to be understood before any of them can be touched.
- **Surprise** — would a competent reader's first guess be wrong? A counter-intuitive choice
  left unexplained gets "corrected" by whoever comes next.

**This ranks what the DOC must carry, not what matters to users.** Impact on how the thing gets
used is the owner's to judge and is never computed here. All three properties above are
readable; whether the owner cares is not, and is not yours to assert.

Use the lens three ways:
- **Selection:** full treatment for decisions that score on any of the three; confirm-form (one
  line) for the rest; omit true trivia. The filter is not "chose over an alternative," it is
  "would someone coming back cold get stuck here."
- **Justification:** every key decision's "why" ties to its component's role and to what a
  returning owner would otherwise have to reconstruct.
- **Growth:** for each, note what it constrains or enables (load-bearing vs cheap-to-change) —
  ownership includes knowing how to grow it, not just how it works.

**The doc's own usability is part of the bar.** A complete document nobody can navigate has
failed the same test as an incomplete one. Cognitive load is a correctness property here, not a
polish item — see the format contract below.

## When to run
On demand, and again after any code change. **Disposable — regenerate, never hand-maintain.**
(Regeneration overwrites `docs/own_your_code.md` in place, refreshing its "current state" block.)

## Output format — the cognitive-load contract
High-volume ownership, delivered compact. Structure over prose:
- **Lead with a one-screen orientation (the cockpit).** Everything after is drill-down; the
  reader navigates from the map, never a wall of text.
- **Structure-first:** tables, a component map, flow diagrams, checklists, status markers.
  Prose only for genuine reasoning; no unbroken prose block beyond ~4 sentences.
- **Progressive disclosure:** Markdown top summary + collapsible `<details>` per section;
  Skim to orient, expand to own.
- **Markers:** per decision — `OWNED`/`REVISIT`, a **re-entry** tag (`reconstruct` / `reach` /
  `surprise`, whichever apply), and certainty
  `[code]` (verified in source) / `[doc]` (rationale confirmed in a decision log/ADR) /
  `[likely-why]` (reconstructed, verify) / `[reconsider]` (judgment). Never present a
  reconstructed rationale as confirmed history.
- **Plain language over coined shorthand.** Domain jargon → the primer. *Project-coined* terms
  (a build's pet names for a check, a phase, a component — "kill-test," "gap-read," "the altitude
  split") get defined in plain words on **first use** and are never stacked. Teach-test: a
  newcomer follows each sentence without already knowing the project's vocabulary — if you can't
  say it without the insider term, you haven't shown you own it. Worst offenders are coined terms
  that *look* like real jargon but aren't (a reader who googles them gets nothing) — replace them
  with a plain description plus the file/symbol they refer to.

## Output target — the repo, single source
**The repo is canonical.** Write `docs/own_your_code.md` in the target repo, in version control,
alongside every other pipeline artifact. Spec, tests, decisions, and ownership share one home and one
history, so they cannot drift.

- **One living, top-level doc, regenerated in place.** This is *the current ownership of the whole
  project* — disposable, always-current, one meaningful read. It is a **single file**, a
  project-level deliverable and **not one per increment**, overwritten on each regenerate. Do not
  stack per-run archive files; version history is git's job.
- **A wiki is a derived surface, never a second canonical.** If a project wants a teammate-readable
  copy, publish a dated snapshot that names `<repo>/docs/own_your_code.md` as its source. An
  *editable* copy anywhere else is the exact thing that makes a later run read the wrong file. Do not
  create one.
- **Stamp every output** — put `own-your-code v{VERSION} · {YYYY-MM-DD}` in the generated header, so
  a doc always declares which skill version produced it.

## Step 1 — Read to ONBOARD, not to catalogue

**Start with the retraces.** `docs/retrace/*.md` holds per-increment accounts of how the work
actually went and why the moves were made — including the wrong turns. That is the raw material this
skill consolidates, and reading it beats re-deriving the same history from the diff. Retraces are
**non-binding**: they report what happened, they never establish a requirement, and nothing here may
cite one as authority for a behavior. Use them for *why*, and confirm every *what* in the source.

Then read enough to reconstruct the project for someone with zero context:
- **What it is / does / current state:** purpose, the user, what stage it's at, what's in flight.
- **Domain jargon:** collect the acronyms, proper nouns, and external systems a newcomer won't
  know (especially in a domain you delegated to the AI) — they become the domain primer.
- **Component decomposition:** identify the 3-7 **core components** and what each is responsible for.
- **Runtime:** trace at least one execution path end to end; how components connect; how you
  run it cold; every artifact written to disk.
- **Data provenance:** trace every data input from its origin — what it is, where it comes from,
  in what *form* (file type, format, size) — through each transformation to the final output. The
  full data pipeline, distinct from the control flow.
- **Decisions per component:** for each component, the calls made inside it; flag the
  AI-defaulted / undocumented ones and, via the lens, the ones a returning owner would trip on.
- **Drift inputs (if present):** design doc, decision/Judgment Ledger, ADRs, CLAUDE.md —
  prefer these over older specs.
- **No access:** ask for the key files; don't guess.

## The output, in order

### 1. Orientation — one screen (the cockpit)
- **Domain primer (only if the domain has non-obvious jargon).** A compact glossary — the
  acronyms, proper nouns, external systems, and core concepts a reader needs *before* the lines
  below parse (expand every initialism once). A **bulleted definition list**, not a table (tables
  compress and render poorly) — a handful of entries, one line each. Skip for
  plain/familiar domains; don't gloss a generic CRUD app.
- **What it is + does + who for** (≤5 sentences).
- **Current state / what you're returning to:** stage, what's done, what's in flight, last
  major moves. (Stale by nature — regenerate to refresh.)
- **Component map:** the core components + how they connect, laid out so it *answers "how does
  what-it-is actually work?"* in the orientation's own plain terms (not just file/function names)
  — and preempts the obvious next question a reader would ask (for a product, the user-facing
  logic: how it finds X, what it does with my input, what it's judging). Keep it **legible**:
  favor a top-down / two-track flow over fragile 2-D ASCII (misaligned monospace art is worse
  than a clean vertical list). Label each box with what it does; tag components so §2/§4 anchor.
- **Decisions index:** compact table — `# | decision | component | re-entry (reconstruct/reach/surprise) | your call | cert`. Navigation only; full treatment lives under each component. **No significance column** — the lens says why a decision is in the doc, never how much it ought to matter to you.
- **Where to spend attention:** the top gaps — the decisions most likely to strand someone coming back cold.

### 2. The system — core components + how they connect
Assembled **whole** (do NOT scatter this across the decision sections):
- **Component roles:** each core component — what it owns, library vs entrypoint.
- **How it runs:** control + data flow between components (the artifact graph, cache /
  only-if branches, shared state); the cold-start sequence (empty clone → working output);
  prereqs / inputs / outputs; "is it working?" signals; human-in-the-loop steps;
  failure/debug first-moves; runtime state (what persists, how to invalidate).

### 3. Data pipeline — first input to final output
Trace the **data**, not the code. For every data input: what it is, where it comes from, in what
*form* (file type, format, size), and how each stage transforms it into the next — to the final
output. A **table** works well: *stage · data + form · source · → becomes · by which code.* Mark
**automated vs. manual** inputs and **public vs. private** data. This answers the maintainer's first
question — *"where does the data come from and what happens to it?"* — which the component map
(control flow) does **not**. Skip only for a project with no meaningful data flow.

### 4. Each core component — broken down
This is where decisions live: **nested under their component and contextualized**, never a
flat catalogue. For every core component:
- **Role** — what it does and which part of "what the app is/does" it serves.
- **How it works** — the local mechanism, first-principles (not API).
- **Key decisions inside it** — each: the call (file/symbol ref) · **why**, tied to the
  component's role AND **what a returning owner would otherwise have to reconstruct** · for the ones you don't
  yet own: the option landscape (real alternatives on the axes; a table) + a rebuild path;
  for the ones you do: confirm-form (one line) · **would I make this call again** — framed as
  what a returning owner runs into if it was wrong.
- **Growth** — what this component's shape constrains or enables for future evolution
  (load-bearing vs cheap-to-change).
Vary the depth via the lens: spend it where the why cannot be reconstructed, where reach is wide, where
a reader would guess wrong — and wherever an agent made the call and nobody ruled on it.

### 5. Drift — built vs design (only if drift inputs exist)
**Read the conformance reports first if they exist.** An independent fresh-context agent already
checked each increment against its design doc in both directions — creep (built but never specced)
and gap (specced but never built). Consolidate what it found; do not re-derive it here, where you
have neither its isolation nor its focus. Re-deriving it produces a second, weaker answer to a
question already answered.

Where no conformance report exists, flag divergence yourself: a swapped approach, a dropped guard,
unplanned scope. Drift is the top ownership-corroder — you can't own "as if I built it" if it
quietly diverged and you never saw it. If no design artifact exists, skip and say so.
**Drift means built-vs-design, and nothing else.** The design doc is the only binding artifact;
ordering and grouping are planning activity nobody records. Work that was sequenced or split
differently than anyone imagined, while still satisfying the design, has not drifted — do not report
it. Only report divergence from what the design requires.

### 6. Gaps ranked
Where ownership is thinnest, ranked on the axes that matter: which key decisions you cannot
yet justify, and which runtime behaviors you couldn't debug
cold. Both decision and operational gaps.

### 7. Own it — the active pass
Reading the doc gives reading-ownership; this section converts it to owned. Three moves, in order:
- **Code to review (targeted reading list).** Not the whole repo — the bounded set (≈5–10) of
  spots where reading the *actual source* earns the most ownership: load-bearing decisions you
  can't yet justify, agent-defaulted calls nobody ruled on, drift sites, and the
  golden-path core. Rank them; per spot give the file/symbol and **what to look for**. State
  explicitly what you can trust from this doc and skip — the point is a short list of where
  your own eyes are worth it, not "read everything."
- **First changes to make it yours.** 2–3 small, real edits to make by hand in this repo —
  e.g. close the #1 ranked gap, add one test to the load-bearing component, one minimal
  extension. Per change: the edit and **the ownership it buys**. This is doing-ownership — it
  closes what reading alone can't.
- **Drills.** Onboarding check (from this doc alone, could a stranger say what it is, draw the
  component map, and justify the top 3 decisions?); runtime cold-trace (trace
  one input end to end naming each component — "it broke here, first check?"); one run-it-cold.

## Final step — the cross-model onboarding read (default for real handoff docs; T2–T3)
This doc's success test *is* a fresh reader onboarding from it — so validate it with the reader
it's for: **a model that has never seen this doc or its source reads it cold.** This is the one
review where a fresh perspective is unambiguously right — the whole goal is "a cold stranger can
onboard," so the reviewer's goal-blindness *is* the acceptance criterion, not a liability. (Contrast
most reviews, where a memory-carrying reviewer is needed to preserve the goal.)

- **When.** Default-on for a doc you'll actually hand someone (T2–T3). Skip on a quick throwaway
  pass or a routine re-run.
- **Who reviews — *check for the different-lineage tier first, then fall back*. The sub-agent is the
  portable floor, not a reason to skip the check. Reviewer gets the doc TEXT ONLY, never the source.**
  - **Step 0 — always look for a reviewer key (one quick read).** Is `OPENROUTER_API_KEY` or
    `GEMINI_API_KEY` in `~/.secrets/llm.env`? **Do this every run; never default past it.** The whole
    point of this step is a *different* perspective, and a genuinely different *lineage* is often one
    file-read away — going straight to a same-family sub-agent without looking wastes it.
  - **Key present → different lineage (preferred).** Route the cold read through that model
    (OpenRouter / Gemini) using the bundled `tools/cross_model_review.py`, resolved relative to
    **this skill's own base directory** (it ships beside this `SKILL.md`; never the target repo's cwd,
    never a hardcoded path). Can't locate the runner? The call is a plain stdlib HTTP POST — make it
    from a **temp/scratch script, never by writing tooling into the *target* repo**. A different
    lineage escapes the model-family blind spots a same-family reviewer shares — that's *why* you checked.
  - **No key → a fresh blind sub-agent (the portable floor).** Spawn a sub-agent with **no memory of
    this session**, doc text only, framed as a *skeptical incoming engineer onboarding cold*. Free,
    instant, ships with nothing — so the step never blocks. Then surface the upgrade in one line:
    *add `OPENROUTER_API_KEY` or `GEMINI_API_KEY` to `~/.secrets/llm.env` for a different-lineage read.*
  **Guarantee vs. laziness:** the sub-agent floor means the step never *fails* — it does **not** mean
  skip Step 0 and go straight to same-model. Never depend on a paid tool or a hard-required key; but
  when a different lineage is one key-check away, take it.
- **What the reviewer does.** Give it the **doc text only, never the source** (the point is "can you
  onboard *from the doc*"). Have it (a) run the success test — say what it is, draw the component
  map, justify the top 3 decisions, and from the doc alone *locate and describe the
  shape of the fix* for one named bug — and (b) emit `/sharpen`-style reader-side reflection:
  **Least confident / loose ends** (where it lost the thread, guessed, or couldn't follow) +
  **Most needed** (what would let it fully onboard).
- **Fold back — a round-trip, like a PR review.** Hand the reviewer's *Least confident / loose ends*
  to the producing agent, which **revises**: apply fixable gaps to the doc, list the rest under
  **Gaps ranked** tagged `[reader-side]` (distinct from the author-side certainty tags), and
  re-review if the changes were substantial. This is the engineer-gets-review-then-updates loop, not
  a one-shot list. Keep the honest ceiling explicit: the doc gets a reader to *locate + explain +
  know the fix's shape*; the edit still opens the file.
- **It feeds the calibration log** (not just per-doc QA): the fresh reader's loose-ends, clustered
  across runs, show where this skill *systematically* under-serves — the input that improves the
  skill itself. **Two confidence signals now:** author-side (certainty tags in the doc) + reader-side
  (this step).

## Notes
- **Read-only** on code and data. Never modify either.
- **Calibrate to senior** — don't re-explain fundamentals; spend depth on the key
  and AI-defaulted calls.
- **Disposable** — regenerate after any change; regeneration writes every target, so targets never drift.
- The bar for every section: could the reader now **own** this — justify and evolve it on
  — without the code in front of them?
