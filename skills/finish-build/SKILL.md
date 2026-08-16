---
name: finish-build
description: 'Drive committed, ratified-but-deferred failing tests to green until the increment is genuinely done and the Acceptance Gate can rule on it. This is S6, and it is AUTONOMOUS: it does not stop for the owner and does not ask them to predict each fix. What matters is that they review the output, not that they approve every move on the way there — the prediction beat lives at S5, where /ratify is baked into /test-spec and the owner rules on what must be protected against. Per owed behavior it names the trap a naive fix walks into, makes the change, verifies red-then-green with nothing regressed, and logs the trap, the fix, and the evidence, so the result is a green light someone can actually read rather than one they have to trust. Real mechanism forks are picked, recorded in declaration form, logged to docs/decision_log.md with a design-doc impact line, and SURFACED in the output — never halted for, never buried. Iteration here is the phase working as intended and says nothing about the quality of the design doc, unlike the rework loop at build time whose target is zero. On completion it chains straight into /acceptance-gate, so the owner never has to remember to knock on that door; the gate still refuses to pass any human leg on their behalf. Internal to Ship Pipeline — normally reached by /adversarial-review. Accepts --retrace. Triggers on "finish the build", "work the xfails to green", "drive the code-fix step", "take this to definition of done", or starting the make-it-pass step after tests are written. Not done until the suite is fully green with deferred markers removed, no prior test regressed, every fork logged and surfaced, and docs/build_status.md advanced.'
---

# Finish Build

Drive an increment from **"tests written, some deliberately failing"** to **"the one green command
that IS done"** — the Acceptance Gate's bar.

This is **S6**. `/test-spec` ratified what must be protected against, the tests were built, and a set
of them is committed **failing on purpose** (`xfail(strict)`) to pin behavior the code does not have
yet. This skill makes the code catch up, one behavior at a time.

## This step is autonomous

**It does not stop for the owner, and it does not ask them to predict each fix.** What matters is
that they review the *output*, not that they approve every move on the way there.

The prediction beat lives at the touchpoints, principally **S5** — `/ratify` is baked into
`/test-spec`, where the owner rules on what must be protected against and what they are willing to
be wrong about. That is where their judgment is load-bearing and where nobody else can substitute
for them. Re-running the same ceremony per fix spends attention on execution, where the owner is not
the oracle, and buys nothing S5 did not already buy.

So: work the list, log everything, and hand back a result the owner can actually read.

## The failure it exists to kill

**The green nobody can explain.** A stack of fixes gets applied, the suite turns green, and the
increment is called done — and afterward no one can say what was wrong, why each fix is right, or
what would have made it wrong. A passing suite you cannot account for is worth no more than an OK
clicked without reading.

Autonomy does not change that. It changes *where the accounting happens*: not in a live dialogue
per fix, but in a record complete enough that reading it confers the same understanding. **If the
log does not let the owner reconstruct what happened, this skill has failed even with a green
suite.**

## What "done" is here

Not "the suite is green." Green is necessary and not sufficient — a suite can be green because
ratified behaviors sit parked under `xfail`.

Done is: **every deferred marker removed, the suite fully green with nothing regressed, every fork
logged and surfaced, every owed design amendment struck, and `docs/build_status.md` advanced.**

**Success test.** The owner reads the output and can point at any behavior that was owed and say
what it does, where the fix lives, and the trap a naive fix falls into — without having watched it
happen.

## Where it sits — the handshake

**Upstream:** the ratified `TEST_SPEC.md` must-cover index and the built test suite with its
committed-failing items. Normally reached by `/adversarial-review`, which sequences S5 → S6 → S7.

**Downstream, this skill chains directly into `/acceptance-gate`** once its definition of done
holds. The owner does not have to remember to invoke the gate — but chaining automates the
*invocation*, never the *verdict*. The gate still presents its human legs as blocking stops and
still refuses to pass one on anyone's behalf.

Assume a fresh session: **self-orient from the repo, not from prior conversation.** On entry, run
the suite to see the current pass / xfail / red state, read `TEST_SPEC.md`, read
`docs/checks/<increment>.md` for what the audit and conformance passes already found, and read
`docs/build_status.md` for position. Everything needed is on disk. If there is no test spec, say so
— reconstruct the contract from the tests themselves and stamp the work un-anchored to spec.

**Options.** `--retrace` · on completion, produce an account of how the work went via `/retrace`,
appended to `docs/retrace/<increment>.md`. The fixes are the most instructive material a learner can
read, because they are where the reasoning is visible.

## Scope — hold this line

- **Owns:** ordering the owed behaviors, the per-item fix loop, picking and recording forks,
  surfacing them in the output, striking owed amendments, advancing `docs/build_status.md`, and
  chaining into the gate.
- **Does NOT:** re-litigate the spec (ratified at S5) · invent behavior no ratified test pins ·
  "improve" code outside the failing tests' contracts · weaken, skip, or delete a failing test · halt
  for a fork · issue the gate verdict.

If a test looks wrong, that is a spec question — surface it. Never re-scope by editing the test to
pass.

## Orient — before the loop

1. **Inventory** the committed-failing tests (`xfail(strict)`, `skip`, or plain red) and map each to
   its spec anchor and the code seam it names.
2. **Order** them cheapest-first and dependency-aware. Group the purely mechanical; isolate any
   carrying a real mechanism fork.
3. State the plan, the count (*"9 owed: 8 mechanical, 1 fork"*), and the definition of done. Then run.

## The core loop — per owed behavior

1. **Name the trap.** Before writing the fix, state the non-obvious way a naive fix is wrong —
   double-escaping, breaking an adjacent contract, a fix that greens the test while the behavior
   stays wrong. Write it down. An agent that has articulated the trap tends not to walk into it, and
   the owner reading the log later needs it more than you do.
2. **Fix.** Make the change, named and guardrailed. Remove the deferred marker as the behavior lands.
3. **Verify.** Run the suite. The target flips green **and** nothing that passed before regresses.
   Red-then-green on the one test is the evidence — never prose that says it's fixed.
4. **Gate.** Advance only on green. One item at a time (WIP 1); do not stack fixes.
5. **Log.** Per item: the behavior, the trap, the fix, the evidence.

**Marker discipline.** `xfail(strict)` is your ally: fix a behavior but forget to drop its marker and
the now-passing test hard-fails (XPASS). That failure is not noise — it is the suite enforcing that a
landed behavior gets un-parked. Never silence it by re-adding the marker.

## Decision forks — pick, log, surface

An item with a real mechanism fork (dedupe vs refuse vs restructure; which of several valid designs)
is a decision, not an execution item. **You do not halt for it.** Pick, and record it in declaration
form — the decision, the options, what you took, what reversing it would cost including anything
already escaped, and what you did not know.

- Log it in `docs/decision_log.md` with its `design-doc impact:` line. A mechanism chosen without a
  logged decision is a silent fork, and silent forks are the thing this pipeline exists to kill.
- **Surface every fork in the output.** The owner rules on them when they read the result — at the
  gate's evidence stop, or in the batch if this ran unattended. A fork buried in a log nobody opens
  has been decided by you.
- Where a fork means the design itself has to change, say so plainly and route the amendment to the
  design doc. A decision is not done until the doc it invalidates is updated.

## Running under a composite

When `/auto-build` invokes this step, nothing above changes — it was already autonomous. Forks are
picked, logged, and carried into that run's batch instead of into the gate's evidence stop. Same
records, later reading.

## Definition of Done

Not done until **all** hold:

- The suite is **fully green with every deferred marker removed** — state the before/after counts
  (*"86 passed / 9 xfailed → 95 passed / 0 xfailed"*).
- **No previously-passing test regressed.**
- **Every fork** is logged with its `design-doc impact:` line **and surfaced in the output**.
- **Every owed design amendment** is struck.
- `docs/build_status.md` is advanced: this step ✅, position → acceptance gate.
- The **per-item record** exists — behavior, trap, fix, evidence — so the result is readable.

Then, and only then, **chain into `/acceptance-gate`**.

## Anti-patterns it prevents

- **The unexplained green** — a suite that passes with no account of what was wrong or why each fix
  is right.
- **Unearned done** — calling it finished with markers still parked, or an XPASS silenced.
- **Silent forks** — a mechanism chosen without a logged decision.
- **Scope drift** — editing a test to pass, or "fixing" code no failing test pins.
- **Owed-amendment rot** — a behavior lands but the design-doc amendment never does.
- **Halting on execution** — stopping to ask about a call the owner ratified the shape of at S5.

## Composes with

- **`/adversarial-review`** (the composite that reaches it) — sequences S5 → S6 → S7.
- **`/test-spec`** (upstream) — its ratified must-cover index and owed amendments; honors its scope.
- **`/acceptance-gate`** (downstream, chained) — the green command this produces is the gate's bar.
- **`/retrace`** (optional) — the account of how the fixes went.
- **`docs/build_status.md`** — the canonical in-repo position tracker it advances.

## The kill rule

**The record is the ownership.** This step runs without the owner, which means the log is the only
thing standing between them and a green light they have to take on faith. A run that greens the suite
and leaves behind a summary rather than an account has not saved them work — it has moved the
unexamined trust from the code into the report.
