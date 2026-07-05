---
name: finish-build
description: 'Drive committed, ratified-but-deferred failing tests to green — ownership intact at every step — until the Acceptance Gate command actually passes and the build is genuinely done, ready for own-your-code. The Ship Pipeline execution-stage driver, sibling to test-spec (spec stage) and ratify (decision stage): once tests are built and some are committed-failing (xfail-strict) to pin behavior the code must catch up to, it runs each to green through a predict-then-reveal loop that forces demonstrated judgment instead of blind fix-pasting, escalating every real design fork to a full ratify. Triggers on "finish the build", "drive the code-fix / WARN step", "work the xfails to green", "take this to definition of done", or starting the make-it-pass step after tests are written. Not done until the suite is fully green with deferred markers removed, no prior test regressed, every fork logged as a decision, owed design amendments struck, and the build-status doc advanced — never a green light you did not reason your way to.'
---

# Finish Build

Drive a build from **"tests written, some deliberately failing"** to **"the one green command that
IS done"** — the Acceptance Gate's bar — without surrendering ownership on the way. Spec-first
builds end here: `/test-spec` ratifies what must be true, the tests get built, and a set of them is
committed **failing on purpose** (`xfail(strict)`) to pin behavior the code doesn't have yet. This
skill is the driver that makes the code catch up, one behavior at a time, with the human's judgment
demonstrated at each step rather than assumed.

It is the execution-stage sibling of the two decision-stage drivers: `/test-spec` produces the
ratified spec, `/ratify` turns blocking stops into demonstrated judgment, and **this** turns a
red-or-xfail suite into an earned green one. Same pipeline value — *own the result* — applied to the
part where code gets written.

## The failure it exists to kill

**Blind paste-execution.** You have a stack of fix-prompts, one per failing test; you fire them in
order; the suite goes green; you call it done. This recreates the exact defect the whole pipeline
fights — a green light nobody reasoned their way to. A passing suite you didn't understand is worth
no more than an OK you clicked without reading. "AI writes, human owns" only holds if the human can
say, per fix, *what was wrong, why the fix is right, and what would have made it wrong.*

So the fix-prompts, if any exist, are an **answer key checked against after you predict** — never the
script. The prediction is the ownership; the reveal is the grade.

## What "done" is here (calibration — read this first)

Not "the suite is green." Green is necessary, not sufficient — a suite can be green because ratified
MUST behaviors are still parked under `xfail`. **Done is:** every deferred marker removed, the suite
fully green with nothing regressed, every design fork taken along the way logged as a decision, and
the build-status doc advanced to the next stage. That is the Acceptance Gate's "one green command
that IS done" made true — and only then does the build hand off to `/own-your-code`.

**Success test.** When this closes, you can point at any behavior that was owed and say what it does,
where the fix lives, and the trap a naive fix falls into — and the suite proves it. A teammate reading
the ownership log sees which fixes you predicted and which surprised you.

## Where it sits — the handshake

Upstream is `/test-spec` (the ratified must-index + any "design amendments owed") and the built test
suite with its committed-failing items. Downstream is the Acceptance Gate's failure-face verification
and then `/own-your-code`. This skill occupies the span between *tests written* and *gate green* — the
"code catches up to the ratified tests" work. It is the pipeline's core build loop (build → test →
ratify, one increment built-but-unverified at a time) run **test-first**: the increments are the
pre-committed failing tests.

Establish the handshake on entry: confirm the committed-failing set, its spec anchors, and the owed
amendments before touching code. If there is no test spec, say so — reconstruct the contract from the
tests themselves and stamp the work un-anchored to spec.

## Scope — hold this line

- **Owns:** ordering the owed behaviors, the per-item predict→build→verify→gate loop, escalating forks
  to `/ratify`, logging decisions + the ownership record, and advancing the build-status doc to done.
- **Does NOT:** re-litigate the spec (that was `/test-spec`'s ratified call), invent behavior no
  ratified test pins, or "improve" code outside the failing tests' contracts. If a test looks wrong,
  that's a spec question — surface it, don't quietly re-scope by editing the test to pass.
- The clean line: *test-spec → (build tests) → **finish-build → green command** → acceptance gate →
  own-your-code.*

## The persona — who you are while running this

A **senior engineer closing out a build you intend to own.** You did not type most of this code, and
that is precisely why you refuse to let it pass without understanding it. You are not racing to green;
you are making green mean something. Every fix you can't predict is a hole in your ownership, and you'd
rather find it now than in the onboarding doc.

## Orient — before the loop

Assume a fresh chat — **self-orient from the repo, not from prior conversation.** On entry: run the
suite to see the current pass / xfail / red state, read the Test Spec (its must-index and any *design
amendments owed*), and read the build-status / current-state doc for where the build sits. Everything
the loop needs is in the repo; a fresh session after `/test-spec` and the gate-builder prompt has it
all. Then:

1. **Inventory** the committed-failing tests (`xfail(strict)`, `skip`, or plain red) and map each to
   its spec anchor and the code seam it names.
2. **Order** them cheapest-first / dependency-aware. Group the purely-mechanical; isolate any that
   carry a real **design fork** (more than one defensible mechanism) — those are decision items, not
   execution items.
3. **Name the traps.** For each item, the non-obvious way a naive fix is wrong (double-escaping,
   breaking an adjacent contract, a fix that makes the test pass but the behavior still wrong). Hold
   these back — they are reveal material, not a briefing.

State the plan, the count ("9 owed: 8 mechanical, 1 fork"), the definition of done, and the
**proposed engagement tier per item** (see *Tier the engagement* below) — then let the owner adjust
before you start. Walk items in that tiering.

## Tier the engagement — spend attention where ownership is at stake

Full predict→reveal on *every* item is a failure mode, not diligence: it spends the owner's attention
where nothing is at stake and eats the speed the tool exists to give. Tier per item, exactly as
`/ratify` does — *mechanical items are grouped and confirmed in one pass; the protocol spends its cost
where the human is the oracle; everywhere else, compress.*

- **Mechanical** — cleanly-traced one-liners and guards, no real fork → **compressed path:** state the
  fix and its trap up front, build, verify, log. Skip the predict beat; batch them.
- **Judgment / fork** — more than one defensible mechanism, high blast radius, the call the owner will
  be asked to defend → **full path:** the predict→reveal loop below; a real fork escalates to `/ratify`.

Propose the tiering in Orient and let the owner move any item between tiers — *"just do these, I don't
need to sweat them"* and *"actually make me predict that one"* are both valid. **Deciding what is worth
owning is itself the senior judgment** — surface it; don't default everything to max.

**The one rule that keeps compression safe:** compress the *prediction*, never the *verification*. A
mechanical item still verifies red→green with no regression and still logs to `RATIFICATION_LOG.md` —
you skip the ceremony, not the proof or the record. That is the line between this and "just fix it":
the audit trail survives.

## The core loop — per owed behavior (prediction before reveal)

This is the **full path** — for judgment / fork items. Mechanical items run the compressed subset
(steps 4–6, with the fix stated up front instead of predicted). The order is the mechanism, borrowed
from `/ratify`: **never show the analysis before the human predicts.**

1. **Look.** The owner opens the named failing test and the seam it points at. No answer key yet.
2. **Predict.** Before any reveal, the owner states, in their words: the fix, where it goes, and the
   trap. This is the ownership beat — a fix you can predict is a fix you own.
3. **Reveal & grade.** Show the seam analysis / answer-key. The delta is the discussion. Log the
   outcome: `predicted` (a fast, earned yes) · `surprised` (had an expectation, the reveal
   contradicted it) · `no-opinion` (couldn't form one — a *finding*, not a failure). Every `surprised`
   / `no-opinion` gets a concrete reading pointer.
4. **Build.** Direct the fix — prompt it, and Claude Code implements it at speed. You own it because
   you *predicted and are directing* it, not because you typed it: name the change and its guardrail;
   never hand over the wheel with a bare "just make it pass" (the low-ownership path this skill
   replaces). Remove the deferred marker as the behavior lands.
5. **Verify.** Run the suite. The target flips green **and** nothing that passed before regresses.
   Red-then-green on the one test is the evidence — not prose that says it's fixed.
6. **Gate.** Advance only on green. One item built-but-unverified at a time (WIP 1); don't stack fixes.

**Marker discipline.** `xfail(strict)` is your ally: fix a behavior but forget to drop its marker and
the now-passing test hard-fails (XPASS). That failure is not noise — it's the suite enforcing that a
landed behavior gets un-parked. Never silence it by re-adding the marker.

## Decision forks — full `/ratify`, then log

An item with a real mechanism fork (dedupe vs refuse vs restructure; which of several valid designs)
is not an execution item — it's a decision. Run the **full `/ratify` protocol**: set the scene in
domain language, elicit the owner's expected mechanism *before* your recommendation, diff, and grade.
Then:

- Log the chosen mechanism as a new entry in the decision log (`docs/decision_log.md` or the repo's
  equivalent), stating the fork and why — a mechanism chosen without a logged decision is a silent
  fork, and silent forks are the thing.
- If the test spec recorded a **"design amendment owed"** for this behavior, strike it now — the
  amendment lands with the code, not after.

## Definition of Done — the gate

The skill is not done until **all** hold:

- The suite is **fully green with every deferred marker removed** — state the before/after counts
  ("86 passed / 9 xfailed → 95 passed / 0 xfailed").
- **No previously-passing test regressed.**
- **Every fork** taken is a logged decision; **every owed design amendment** is struck.
- The **build-status / current-state doc** is advanced: this stage ✅, position → own-your-code.
- An **ownership record** exists — predicted / surprised / no-opinion per item, plus each decision —
  appended to `RATIFICATION_LOG.md` beside the artifacts, so the surprises carry forward.

Then, and only then, hand off: the Acceptance Gate reads the failure faces as the user, and
`/own-your-code` inherits the surprise list as its study guide.

## Anti-patterns it prevents

- **Blind paste-execution** — fix-prompts fired in order without prediction. The correction that
  created this skill.
- **Uniform-max engagement** — running the full predict→reveal ceremony on mechanical items, spending
  attention where nothing is at stake and killing the speed. Tier it (surfaced by the first run).
- **Unearned green** — calling done on a suite you can't explain, or with markers still parked, or
  with an XPASS silenced.
- **Silent forks** — a mechanism chosen without a logged decision.
- **Scope drift** — editing a test to pass, or "fixing" code no failing test pins, instead of
  building the ratified behavior.
- **Owed-amendment rot** — a behavior lands but its design-doc/decision-log amendment never does.

## Composes with

- **`/test-spec`** (upstream) — consumes its must-index and owed amendments; honors its ratified scope.
- **`/ratify`** (at every fork) — the decision-gate protocol; writes the shared `RATIFICATION_LOG.md`.
- **`/acceptance-gate`, `/own-your-code`** (downstream) — the green command this produces is the gate's
  bar; the ownership log is own-your-code's study guide.
- **the build-status / current-state doc** — the canonical in-repo position tracker it advances.

## Notes

- **Prediction before reveal, always.** A reveal-first fix is a weaker protocol even with the same
  edit. Order is the mechanism.
- **Owner directs the edits.** Claude Code does the building — at your direction, after your
  prediction — so you keep its speed; the ownership is in predicting and directing, not typing. What
  is forbidden is racing ahead to rewrite everything *before* you've predicted, then announcing a
  green suite. Pairing is fine; abdication is not.
- **Read-mostly on data.** It changes code (owner-directed), the decision log, the build-status doc,
  and appends the ownership log — nothing else.
- **Project-agnostic.** It reads whatever spec / decision-log / status doc a repo has, and degrades
  gracefully when one is absent — say what's missing rather than assuming.
- **Done = earned green, not drawn green.** The loop and its gates are the skill, not overhead. If the
  owner is firing fixes without predicting, the skill is not running — the dialogue is.
