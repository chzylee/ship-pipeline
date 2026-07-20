# Ship Pipeline — Telemetry Corpus (`sends.jsonl`)

> **What this is.** A plugin-owned, user-global, append-only event log that ship-pipeline skills
> write to as you build. `/ratify` is its first writer: one JSON line per ratified judgment item.
> The per-project `RATIFICATION_LOG.md` is the human record of a single build; this corpus is the
> **machine record across every build**, sanitized by construction so it is fit to present.
> Sourcing convention: this document specifies the format; the emitting behavior is defined in
> [`skills/ratify/SKILL.md`](../../skills/ratify/SKILL.md).

## Why it exists

The pipeline's claim is that you can build at LLM speed **and own the result**. `/ratify` is where
that claim is tested — you predict before the reveal, and the gap is the proof of understanding.
A single `RATIFICATION_LOG.md` shows that for one project. This corpus turns a scattered pile of
per-project logs into **one body of evidence** you can aggregate and show: *across N sittings on M
projects, here is how often I predicted correctly, how well-calibrated I was, and how often I
actively steered the design instead of approving it.*

That is the presentable artifact behind "quickly generated, genuinely owned."

## Where it lives

| | |
|---|---|
| **Path** | `~/.claude/ship-pipeline/sends.jsonl` |
| **Resolution** | `$HOME` resolved at runtime — never a hardcoded absolute path. Honor `$SHIP_PIPELINE_DATA_DIR` if set (default `~/.claude/ship-pipeline`). |
| **Ownership** | The ship-pipeline skillset owns this directory. Future skills append their own event types to the same file (disambiguated by `source_skill`). |
| **Not in any repo** | User-global, so it aggregates across projects — and so it survives `git pull` / `claude plugin update`, which would clobber anything written into the plugin's own install dir. Never commit it to a project repo. |

Standard app-data pattern: mutable, user-scoped state lives under the app's config home
(`~/.claude/…`), not in the distributed source tree.

## The record — schema v2

One JSON object per line, one line per judgment item:

```json
{"schema_version":2,"source_skill":"ratify","timestamp":"2026-07-15T18:44:17Z","project":"ratify-schema-v2","development_stage":"standalone","baseline":"partial","pre_confidence":"high","prediction_outcome":"surprised","decision_origin":"human","gap":"authored","decision_type":"amend"}
```

| Field | Type | Values | Role |
|-------|------|--------|------|
| `schema_version` | int | `2` | **Stamp.** The version of *this record format*, so older records still parse after the schema grows. v1 records keep `1`; the v2 fields are simply absent on them. Unrelated to your build's version. |
| `source_skill` | string | `"ratify"` | **Stamp.** Which ship-pipeline skill emitted the row. |
| `timestamp` | string | ISO-8601 UTC (`YYYY-MM-DDThh:mm:ssZ`) | **Stamp.** When the item was ratified. |
| `project` | string | repo/dir name, or a stable alias if the project is sensitive | **Context.** Which build the judgment belongs to. |
| `development_stage` | enum | `test-spec` · `finish-build` · `acceptance-gate` · `build-loop` · `standalone` | **Context.** Where in the pipeline the judgment happened. `standalone` when `/ratify` is run directly on a doc. |
| `baseline` *(v2)* | enum | `documented` · `emergent` · `partial` | **Context.** The regime the prediction was graded in — a spec of the design existed (`documented`), was articulated in-session (`emergent`, the native mode of non-code work), or a document *informed* but did not *specify* it (`partial`). This is what licenses a `judgment` verdict. |
| `pre_confidence` | enum | `low` · `med` · `high` | **Proof.** Strength of the expectation, stated **before** the reveal. |
| `prediction_outcome` | enum | `predicted` · `surprised` · `no-opinion` | **Proof.** Was that expectation right — the foresight grade. |
| `decision_origin` *(v2)* | enum | `human` · `ai` · `human+ai` | **Proof.** Who originated the decision's substance — the authorship axis, present on every record. |
| `gap` *(v2)* | enum | `authored` · `missing-info` · `judgment` | **Proof.** On a divergence, its *nature* (not a human-deficiency label); **omitted when `predicted`**. Only `judgment` is a true blind spot. |
| `decision_type` | enum | `build` · `demote` · `amend` | **Proof.** What you decided to *do*: accept as-is / drop or defer / accept with changes. |

The five `pre_confidence` → `decision_type` fields are the measurement; the rest is stamp and context.

## What the data proves

The proof is not any single field — it is the cross-tabs a reader takes off the corpus:

- **`pre_confidence:high` × `prediction_outcome:predicted`** — you knew what was coming before you
  saw it. The design→build→realization throughline held: owned code, not rubber-stamped.
- **`decision_type` in `{amend, demote}`** — you steered the design (changed or cut the proposal)
  rather than approving it. The strongest ownership signal: authorship, not consent.
- **`prediction_outcome:surprised` / `no-opinion` trending down over time** — a visible learning
  curve; blind spots converting to mastery.
- **`pre_confidence` × `prediction_outcome` together** — calibration: not just whether you were
  right, but whether you *knew when you knew*. Well-calibrated judgment is what deep ownership
  looks like on a chart.
- **`surprised` × `decision_origin:human` × `gap:authored`** — you were "surprised" only because
  you overrode the recommendation and authored the better call. The pattern v1 mislabeled as a
  whiff; v2 records it as ownership.
- **`gap:judgment` rate** — the *true* blind-spot rate, isolated from `missing-info` (facts you
  couldn't have had) and `authored` (calls you drove). This, not the raw `surprised` count, is the
  number that should trend down as you master a domain.
- **`gap:judgment` × `baseline`** — a `judgment` miss is only fairly charged when the dots existed
  to connect (`documented` / `partial`). Reading `gap` against `baseline` keeps the blind-spot
  count honest across code (usually `documented`) and non-code (usually `emergent`) work.

Reading examples — `jq` shown for brevity, but the corpus is plain JSON Lines that any language
reads (a five-line Python loop does the same); nothing here is a dependency of the pipeline:

```bash
CORPUS=~/.claude/ship-pipeline/sends.jsonl

# Prediction accuracy on high-confidence calls
jq -s '[.[]|select(.pre_confidence=="high")] | (map(select(.prediction_outcome=="predicted"))|length) as $hit
        | "\($hit)/\(length) high-confidence calls predicted"' "$CORPUS"

# Authorship rate — how often you actively steered
jq -s '(map(select(.decision_type!="build"))|length) as $steered
        | "\($steered)/\(length) decisions amended or demoted"' "$CORPUS"

# Calibration cross-tab
jq -s 'group_by(.pre_confidence)[] | {confidence:.[0].pre_confidence,
        n:length, predicted:(map(select(.prediction_outcome=="predicted"))|length)}' "$CORPUS"
```

Metrics are computed at read time from raw facts — the corpus never stores a derived accuracy, so
you can change how you measure without rewriting history.

**Facts, not verdicts.** The corpus records what happened, not why. Some cells are deliberately
ambiguous: `high` confidence + `surprised`, for instance, could mean too much was left to the
agent *or* that the design was weak upstream — the data alone cannot tell which, and the cause
matters too much to guess. Read the cross-tabs as evidence a human interprets, never as an
automated conclusion. No cause is inferred at write time, and none is encoded in the schema; the
data itself is the deliverable.

## The sensitivity call

Once per sitting, before appending: *is the project's identity something you'd rather not have in
a shareable corpus?*

- **Default** — log the real `project` name.
- **If yes** — log a stable alias (`proj-<short-hash>`). The measurements still aggregate; only the
  name is withheld.

Because the record **structurally holds no free text** — the item label and the reading pointer
live only in `RATIFICATION_LOG.md` — this alias-or-not is the *only* redaction decision. That is
what makes automatic capture safe: there is nowhere in a record for sensitive content to land, so
the corpus is presentation-fit by construction, not by per-item review.

## Two logs, two masters

| | `RATIFICATION_LOG.md` | `sends.jsonl` |
|---|---|---|
| **Lives** | in the project repo, beside the artifact | `~/.claude/ship-pipeline/` (user-global) |
| **Audience** | a dev/team auditing *this* build — a commit history of the human decisions | you, aggregating *across* builds for evidence |
| **Holds** | full record incl. item label + assigned reading (free text) | enums + scalars only — no free text |
| **Grain** | one row per judgment item + a per-sitting summary | one line per judgment item |

## Rules

- **Append-only.** One line per item; never rewrite a past line. Re-ratifying a doc appends fresh
  records (a new sitting) — it does not edit old ones. The corpus is a history, like the human log.
- **Version inside every record.** When the schema grows, bump `schema_version`; old records keep
  their number and still parse. Migration is additive by default.
- **No free text.** Anything a viewer shouldn't see has no field to live in.
- **`gap` omitted when aligned.** A `predicted` record has no `gap` field — there was no divergence
  to characterize.
- **`baseline` is per-item, sitting-inherited.** Set once at the sitting's open and stamped on each
  record; it changes mid-sitting only on an explicit, declared state change, never silent drift.

## Schema changelog

- **v1** (2026-07-11) — initial: `schema_version`, `source_skill`, `timestamp`, `project`,
  `development_stage`, `pre_confidence`, `prediction_outcome`, `decision_type`.
- **v2** (2026-07-15) — additive: `baseline` (documented/emergent/partial), `decision_origin`
  (human/ai/human+ai), `gap` (authored/missing-info/judgment, omitted when `predicted`). v1 records
  keep `schema_version:1` and still parse; the new fields are absent on them. Adds the axes that
  separate *foresight* (was I right) from *authorship* (who drove it) and *gap nature* (a fact I
  lacked vs a judgment I should have had) — so a `surprised` that was really an override stops
  reading as a miss. Ratified via `/ratify`; see the skill's `RATIFICATION_LOG.md`.
