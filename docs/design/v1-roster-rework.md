# Ship Pipeline v1 — Roster Rework

```
Layer:            technical
Slice:            increment
Binding:          yes
Scope authority:  DESIGN.md (project tier)
Sources:          DESIGN.md 2026-08-15 (authoritative: design)
                  v1 scoping session 2026-08-15 (authoritative: scope, tiering)
                  skills/ on disk 2026-08-15 (authoritative: current state)
Status:           written directly, NOT derived — Q-1 rules that v1 is built outside S1-S7
```
*2026-08-15*

---

## 1 · What this increment is

Rework the full Ship Pipeline skill roster so it matches `DESIGN.md`. The design differs enough
from prior versions that partial conformance is not a state worth occupying (Q-1).

**Not built under S1-S7.** The loop is what v1 provides, not what produces it. Ship Pipeline is
tested experimentally by use on real projects — the owner judged that a better instrument than
self-hosting.

**Sized as one increment** under R-12 because the rework is low-complexity: the skill bodies
largely formalize how the owner already prompts builds, stripped to what is project-independent.

---

## 2 · The two tiers

**Tier 1 is what "using Ship Pipeline" means.** A user learns these five and can run a
spec-driven build. Simplicity of use is an asset (A-18).

**Tier 2 is the machinery.** Individually callable — atomicity is preserved (A-12) — but nobody
has to learn them by name. Tier 2 is reached through tier 1.

Tiering is expressed **in the skill description**: a tier-2 description states that it is internal
to Ship Pipeline and names the tier-1 skill that normally reaches it. Same directory; direct
invocation still works. The description is what keeps it out of a user's working set.

---

## 3 · Shared contract — every skill in this increment

```
K-1 · VOCABULARY. project / increment / grouping used precisely. "build" is a VERB, never a
      noun. built = the specced behavior works · validated = an independent agent confirms it
      matches the spec · tested = it survived deliberate attack.

K-2 · THE DECLARATION ENTRY (C-1, CLOSED at five fields):
        decision · options · taking · reversal · unknowns
      No severity, priority, or significance field (A-3, R-10).

K-3 · INFORMATION HIDING (A-19). A skill is told what it needs to do its job and nothing more.
      Project-level rationale — why a tolerance exists, what the surrounding structure catches,
      what the process trades off — stays in DESIGN.md. Specifically: no skill body states that
      false negatives on `unknowns` are tolerated.

K-4 · ARTIFACTS ARE MODE-FREE (R-19). The DOC records no mode, and nothing reads a mode off an
      artifact. Mode is carried by the invoking composite.
      A mode MAY guide a session — where to press, where to pay special attention, whether a
      ruling is taken live or deferred to a batch. What it may never do is change what an
      artifact CONTAINS, or make one artifact readable only by a caller in a given mode.
      Test: could this skill be handed the same inputs by a different caller and still be
      correct? If yes, it is compliant, even when it presents differently.

K-5 · INDEPENDENCE IS A SEPARATE CONTEXT (A-15). Where a skill requires a fresh agent, it means
      no shared context — not a fresh section of the same session. Subagent dispatch is the
      mechanism; isolation is the requirement.

K-6 · SKILLS ARE FUNCTIONS. Each declares its inputs, its outputs, and its done-criteria. A
      skill reads its stated inputs and nothing ambient.

K-7 · HOUSE FORMAT. `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description` —
      description carries purpose, scope boundary, triggers, and done-condition), plus `VERSION`.
      Body sections, in order: title · one-paragraph purpose · "The failure it exists to kill" ·
      "What done is here" · "Where it sits — the handshake" · "Scope — hold this line"
      (Owns / Does NOT) · "Procedure" (numbered) · a closing kill rule.

K-8 · NOTHING MAY REFUSE THE OWNER (A-17). Every mechanism informs a choice; none makes one.
      A skill may report that something looks thin. No skill blocks on its own judgment.
```

---

## 4 · Tier 1

### `/design-doc` — S1, spec it · **REWORK** (422 ln)

| | |
|---|---|
| **In** | whatever inputs exist (notes, repo, parent doc); the owner, in dialogue |
| **Out** | `DESIGN.md` (project tier) or `docs/design/<increment>.md` (increment tier) |
| **Traces** | R-6, R-9, R-13, R-14, A-11, A-19 |

**Gains:** the C-1 declaration contract · dispatch of `declare` before the approval stop (R-9) ·
WHEN/SHALL done-criteria · the scope check (R-13) — assessed during S1 before approval, proposes a
split, never takes one.

The scope check is **three reads, none of which computes a size.** Its substantive one surfaces the
heaviest `reversal` pictures so the owner sees what they are signing off on — ordered by escape,
then lock-in, then spread, all readable from code (A-2), and never presented as a ranking of
importance (A-3). The entry count is a prompt to ask, not a threshold. The owner's self-reported
urge to skim is R-14's other detector. Sizing is complexity the owner can hold (R-12); the skill
informs that judgment and never makes it.

**Loses:** all "produces design NEVER ordering — sequencing belongs to the Build Plan" language
(`/build-plan` dissolved at stop 6) · any tier beyond project and increment (A-11) · any language
implying the doc records who will supervise the build (K-4).

**Done:** WHEN a doc is produced at either tier, it SHALL carry its tier, binding status,
addressable requirement IDs, and a done-criteria section; AND at increment tier `declare` SHALL
have run and its declaration SHALL have been presented before the approval stop.

---

### `/build-and-test` — S2-S4, build it verified · **NEW** · enforcement composite

Its job is **not** to start a build. It is to ensure building occurs inside the test/review
framework (R-18) — converting R-3, R-4, and R-16 from protocol the process asks for into behavior
the skill performs.

| | |
|---|---|
| **In** | an increment design doc |
| **Out** | the built increment · audit report · conformance report · rework count · optional retrace |
| **Flags** | `--retrace` |
| **Traces** | R-2, R-3, R-4, R-15, R-16, R-18, A-6, A-15, A-16 |

**Sequence:** dispatch the build agent, tests first (R-18 as amended — the harness IS subagent
orchestration and the builder is one of its agents) → confirm the tests are red before any
implementation exists (R-3) → dispatch `audit-tests` concurrently, while the building agent writes
code, so it costs no wall-clock (R-16) → dispatch `conformance` after (R-4) → persist both reports
and the rework count to `docs/checks/<increment>.md` → present the S4 batch (R-15).

Persistence is not optional: `/adversarial-review` opens by reading the S3 findings and
`/own-your-code` consolidates them, so a report living only in one session's scrollback is a report
neither will find. The rework count only means anything as a trend (DOD-2), and a number stated once
in a session that then closes cannot trend.

`audit-tests` and `conformance` run in two **distinct** fresh contexts, sharing nothing with the
builder or with each other (A-15, stop 11).

**Done:** WHEN it returns, the tests SHALL have been observed failing before implementation
existed; an audit report and a conformance report SHALL exist from two distinct fresh contexts;
and the rework count SHALL be stated. An increment that passes here is CONFORMANT, not TRUSTED
(A-6).

---

### `/adversarial-review` — S5-S7, review it adversarially · **NEW** · convenience composite

One entry point for the hardening phase. Sequences `/test-spec` → `/finish-build` →
`/acceptance-gate`.

**Its scope is what the design never decided** — failure modes, edge cases, and the silly errors
that slip past a spec-conformant build. It does NOT re-check built-against-specced; `conformance`
did that at S3, and conformance and completeness are orthogonal (A-9). The review is adversarial
in posture, not destructive in aim: the goal is that nothing dumb survives, not that something
breaks.

| | |
|---|---|
| **In** | a conformant increment |
| **Out** | ratified `TEST_SPEC.md` · green suite · gate record + verdict · optional retrace |
| **Flags** | `--retrace` |
| **Traces** | R-2, R-5, A-7, A-8, A-14, A-16 |

**Halts** at S5 (owner ratifies the test spec) and at S7's human legs. Every link can halt. Under
A-14 it surfaces everything it passed through — a composite that hides its decisions is
ok-clicking at a higher altitude.

Runs on **every** increment, however brief, including ones where it is expected to find nothing
(R-5). Iteration here is the phase working as intended, not a defect — its count says nothing
about spec quality (A-7).

**Done:** WHEN it returns, a ratified test spec SHALL exist; the suite SHALL be green with
deferred markers removed; and the gate SHALL have issued ADVANCE or BLOCKED with evidence.

---

### `/auto-build` — S1-S7 unattended · **NEW**

| | |
|---|---|
| **In** | an increment design doc — **any** doc. It does not require one authored for it (K-4) |
| **Out** | the completed increment · the A-14 review batch |
| **Traces** | R-11, R-19, A-13, A-14, A-17, C-1 |

**Behavior:** does not halt. A decision surfacing mid-run is picked, logged, and continued — the
election to run autonomously IS the ruling to continue (R-11). `/acceptance-gate`'s human legs
become entries in the end-of-run batch rather than blocking stops; they are **not** skipped,
because a check's value is that it ran (A-8).

It MAY report that a spec looks thin to run unsupervised. That report is C-1's `unknowns` read at
composite altitude — the same mechanism one level up, not a second one. **It never refuses the
run** (A-17, K-8).

**Done:** WHEN it returns, every decision the owner would have ruled on SHALL be present in one
reviewable batch AS A PROPOSED DESIGN-DOC AMENDMENT, and no stop SHALL have been silently
discharged.

---

### `/own-your-code` — after · **INTACT**, light touch (256 ln)

Single change: consume `docs/retrace/<increment>.md` as raw material rather than re-deriving the
same history. Per-increment retraces are what consolidation draws on (R-17).

---

## 5 · Tier 2

### `declare` · **NEW**

The builder's interface for stating what it would decide.

| | |
|---|---|
| **In** | an increment design doc, and nothing else |
| **Out** | a declaration — C-1 entries, five fields each |
| **Reached by** | `/design-doc` at S1 |
| **Traces** | R-9, R-10, R-14, A-3, A-15, C-1 |

**The constraint that makes it work: fresh context.** The agent that pressed the owner through the
derive knows what the owner meant, so the gaps are invisible to it. A cold read tests whether the
*document* carries the meaning — which is the one job made mechanical. The natural agent to do
this is the one about to build, reading the spec for the first time.

Per K-3, this skill is not told that false negatives are tolerated.

**Done:** WHEN it returns, every entry SHALL carry all five fields and no sixth; AND the entry
count SHALL be reported for R-14's mechanical oversize detector.

---

### `audit-tests` · **NEW**

| | |
|---|---|
| **In** | the increment design doc + the red test files. No implementation, no builder context |
| **Out** | an audit report grading each test against the spec item it claims to cover |
| **Reached by** | `/build-and-test`, concurrently with implementation |
| **Traces** | R-16, A-15 |

Red-first proves a test CAN fail. This proves it fails for the **right reason** — a tautological
test survives red-first, and nothing else in the pipeline catches that.

**Done:** WHEN it returns, each test SHALL be graded against its claimed spec item, and vacuous or
tautological tests SHALL be named individually.

---

### `conformance` · **NEW**

| | |
|---|---|
| **In** | the increment design doc + the built code. No builder context, no audit context |
| **Out** | creep list (built-but-unspecced) + gap list (specced-but-unbuilt), reported separately |
| **Reached by** | `/build-and-test`, after implementation |
| **Traces** | R-4, A-6, A-9, A-15 |

**Done:** WHEN it returns, both directions SHALL have been reported separately, AND the report
SHALL state its own limit: a clean conformance result says nothing about whether the declaration
was complete (A-9).

---

### `/test-spec` — S5 · **REWORK** (274 ln)

Narrowed to S5's adversarial spec for **one increment**. Agent-proposed and owner-ruled — the
agent seeds "what holes should we protect against," because the owner cannot enumerate the failure
modes of code they did not write (R-6).

**Loses:** the slice/sweep dual scope. Sweep was version-tier, and A-10/A-11 no longer model a
version tier.

**Reached by** `/adversarial-review`. **Traces** R-5, R-6, A-7, A-8.

---

### `/finish-build` — S6 · **REWRITE** (was 202 ln)

Rescoped from a vocab pass to a rewrite by the review loop. **S6 is autonomous** (R-2): the per-fix
predict-then-reveal loop is gone, because the prediction beat belongs at S5 where `/ratify` is baked
into `/test-spec`. Per behavior it names the trap, fixes, verifies red-then-green, and logs — the
record replaces the dialogue. Forks are picked, recorded in declaration form, logged with a
`design-doc impact:` line, and **surfaced**, never halted for. **Gains** `--retrace` and chains into
`/acceptance-gate`. **Reached by** `/adversarial-review`. **Traces** R-2, R-5, R-11, A-7.

---

### `/acceptance-gate` — S7 · **VOCAB** (99 ln)

Build-as-noun churn; reframed per **increment** rather than per project. Human legs remain
blocking stops — except under `/auto-build`, where they become batch entries (A-14). **Reached by**
`/finish-build` on completion. **Traces** R-2, A-8, A-14.

---

### `/retrace` · **NEW**

A readable account of how the agent worked and why it made the moves it made. Its value is
capturing agentic work that runs on its own — transparency and teaching.

| | |
|---|---|
| **In** | the loop's own record of decisions and moves |
| **Out** | `docs/retrace/<increment>.md`, appended by each loop that ran with the flag |
| **Reached by** | `--retrace` on `/build-and-test` and on `/adversarial-review` |
| **Traces** | R-17, C-2 |

Optional to read, non-binding, **never a gate**. Both loops append to one file per increment, so
the account covers how the thing was built *and* how it was fixed.

---

### `/ratify` · **EXTERNAL** — `chzylee/skill-library`

Not built here. Invoked by name at approval stops. Tier 2 in effect: the tier-1 skills reach it;
the user does not have to.

---

## 6 · Build order

```
1 · this manifest
2 · /design-doc rework  +  declare          — contract-defining, must land first
3 · audit-tests · conformance · /build-and-test · /retrace   — parallel once 2 is fixed
4 · /test-spec rework · /finish-build vocab · /acceptance-gate vocab
5 · /adversarial-review · /auto-build        — composites; need their parts to exist
6 · README.md rewrite                       — must match what actually landed
```

`docs/` did not exist before this file. C-2 names five paths under it; the skills that write them
create them on demand.

---

## 7 · Not in this increment

- `/scout`, `/sidequest` — add-ons on their own clock (§10)
- Building Ship Pipeline under Ship Pipeline (Q-1)
- The wiki sweep — derived surface, C-3

---

## 8 · Done — this increment

- **D-1** · All twelve roster entries match `DESIGN.md`. No skill contradicts a requirement or an
  invariant.
- **D-2** · Tier 1 is five skills. A user can run a spec-driven build without learning a tier-2
  name.
- **D-3** · No skill body carries project-level rationale that A-19 assigns to `DESIGN.md`.
- **D-4** · `README.md` describes the shipped roster. Staleness check 9 goes green.
- **D-5** · Usable: the roster can be pointed at a real project and run.
