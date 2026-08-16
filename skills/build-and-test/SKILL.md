---
name: build-and-test
description: 'Ensure that building happens INSIDE the test-and-review framework rather than alongside it. This is not a skill that starts a build — the build is an agent working from the increment design doc, and that doc is the build interface. This is the harness around it: it holds the checkpoints that turn "we should write tests first" and "someone should check this" from protocol into behavior. It confirms the tests exist and were observed FAILING before any implementation, dispatches `audit-tests` concurrently with the implementation work so the check costs no wall-clock, dispatches `conformance` once the code exists, and presents both reports plus the rework count to the owner. The two checks run in separate fresh contexts, sharing nothing with the builder or with each other. An increment that passes here is CONFORMANT — it matches what was specified — and is NOT yet trusted; nothing has attacked it. Tier 1: this is one of the five skills that make up using Ship Pipeline. Skipping it is legal and puts every invariant it enforces back on willpower. Accepts --retrace to record how the work was done. Triggers on "build this increment", "build and test X", "run the build harness", "build against this design doc", or reaching S2. Done when the tests were observed red before implementation existed, an audit report and a conformance report exist from two distinct fresh contexts, and the rework count is stated.'
---

# Build and Test

Hold the frame that building happens inside.

**This skill does not write the code — it dispatches the agent that does.** It is subagent
orchestration: a build agent works from the increment design doc, and two verification agents work
in isolation from it and from each other. The doc is the build interface and nothing here replaces
it. What this skill owns is the *frame*: the checkpoints that have to hold whether or not anyone
remembers to hold them, and the dispatching that makes them hold.

"Building is not a skill" means **no skill authors code**. It does not mean nothing launches the
build.

It covers **S2 through S4** — build, independent check, owner review.

## The failure it exists to kill

**The discipline that only exists when someone is watching.** Everyone agrees tests come first. Then
the build is going well, the implementation is obvious, and the tests get written after — shaped, at
that point, by the code they are supposed to be judging. Everyone agrees a fresh pair of eyes should
check the result. Then the build looks fine, checking it feels like ceremony, and it gets skipped
exactly on the increments where it was cheapest to run.

Protocol degrades under confidence. Mechanism does not. This skill exists so that three things
happen because the skill performs them, not because anyone chose well that day:

1. tests exist and were seen failing **before** any implementation
2. an independent agent asks whether those tests would catch a wrong build, **while** the build runs
3. an independent agent checks the result against the spec **after**

## What "done" is here

Tests observed red before implementation existed · an audit report and a conformance report from two
distinct fresh contexts · the rework count stated · both reports presented to the owner.

**An increment that passes here is CONFORMANT, not TRUSTED.** It does what was described. Nobody has
tried to break it, and no edge case has been considered. Say this plainly when you close — the two
promises get conflated constantly, and this is where the conflation starts.

## The sequence

**1 · Read the doc. It is your only input.**
The increment design doc determines everything below. It carries no mode and tells you nothing about
who is supervising — that is not your concern and not in it.

**2 · Dispatch the build agent, tests first.**
Dispatch an agent that holds the increment design doc and writes **the tests for the specced
behavior, before any implementation.** Then **run them and show the failure output.** Not "the tests
are written." Not "they should fail." Run them; paste what came back.

If tests already exist for this increment, run them and show the output instead of commissioning new
ones.

What is not negotiable is the ordering. A test written after the code it judges has been shaped by
that code, and no amount of later review recovers what that costs.

**If implementation already exists, this gate cannot be satisfied.** Say so and let the owner rule
whether to continue. Do not quietly grade it as passed.

**3 · Dispatch `audit-tests` — concurrently.**
The moment the tests are red, dispatch `audit-tests` in a fresh context, holding the doc and the
tests and nothing else. **It runs while the implementation is being written.** That concurrency is
what makes the check affordable: it occupies no time the build was not already spending. Do not wait
for it before letting the build proceed, and do not let it see the implementation.

**4 · The build agent implements.**
It works from the doc, against the red tests. **You launched it; you do not author or direct the
implementation** — the doc does that, which is what makes the doc the interface rather than you.
Your obligations while it runs: the audit stays isolated, the doc stays the only source of
requirements, and nothing outside the doc gets to add one.

Before it writes implementation, it states what it would have to choose — dispatch `declare` if that
has not already happened at S1. An agent that has articulated its picks can be held to them; one
that has not will make them silently.

**5 · Dispatch `conformance` — after.**
Once the implementation exists, dispatch `conformance` in a **second, separate** fresh context. It
holds the doc and the code, and nothing from the builder and nothing from `audit-tests`.

**Two agents, not one, and this is deliberate.** An agent that approved the tests has a stake in
their adequacy, and is the least likely reader to conclude that a build passed tests which were
never good enough. Reusing one agent for both saves nothing that matters and removes the property
both checks were bought for.

**6 · Persist both reports, then present at S4.**
Write the audit and conformance findings **and the rework count** to `docs/checks/<increment>.md`
before presenting them, and advance `docs/build_status.md` to `S4`.

The rework count has to persist: it is only meaningful as a trend across increments, and a number
stated once in a session that then closes cannot trend.
Downstream reads them from disk — `/adversarial-review` opens with them and `/own-your-code`
consolidates them — and a report that existed only in one session's scrollback is a report those
skills will not find.

Bring the owner:
- the **conformance** findings, both directions, kept separate: creep (built but never specced) and
  gap (specced but never built)
- the **audit** findings: which tests would not catch a wrong build, and the wrong build that
  survives each
- the **rework count** (below)
- the plain statement that this increment is conformant and not yet trusted

Creep is an owner ruling — keep or cut. Gap routes back to the build.

**7 · Rework, if any.**
When findings send work back, that is a **rework loop**, and it repeats from step 4. Count it.

## The rework count

**Count every return trip through S2-S4 and state the number when you close.**

This count is a **defect measure, and its target is zero.** It does not mean the agent is doing
badly. It measures whether the spec was good enough — every loop is a place the design doc left
something the build had to get wrong first in order to discover.

Do not conflate it with the iteration that happens later during adversarial review. That loop is the
phase working as intended and its count means nothing about spec quality. This one is the opposite
polarity, and a system that cannot tell them apart reads its own history backwards.

## Independence

`audit-tests` and `conformance` each require a **separate context** — no shared history with the
builder, and none with each other. Freshness is the property being bought, and it cannot be
simulated inside one session: an agent that has read the reasoning will read the artifact as the
argument for itself.

Subagent dispatch is the available mechanism. The requirement is the isolation, not the mechanism —
if isolation cannot be achieved, say so rather than approximating it.

## Options

`--retrace` · after the span closes, produce a readable account of how the work was done and why the
moves were made, via `/retrace`, appended to `docs/retrace/<increment>.md`. Non-binding, never a
gate, and it changes nothing about the sequence above.

## Scope — hold this line

- **Owns:** dispatching the build agent · the red-first gate · dispatching both checks into isolated
  contexts · enforcing that they are distinct agents · assembling and presenting the S4 batch · the
  rework count · persisting both reports.
- **Does NOT:** write the implementation · write or edit the tests · grade the tests itself (that is
  `audit-tests`) · check code against the spec itself (that is `conformance`) · rule on creep · fix
  gaps · attack the build for edge cases (that is `/adversarial-review`, and it comes later) ·
  declare the increment trusted or done.

## Where it sits — the handshake

**Upstream:** a ratified increment design doc from `/design-doc`, with its declaration presented and
the owner's approval given.

**Downstream:** `/adversarial-review`, which takes a conformant increment and hardens it. An
increment that stops here has been built and validated. It has not been tested in the sense that
matters.

## The kill rule

**The gate is the product.** If the red-first check is waved through, or one agent is reused for
both verifications, or the checks run but their findings are summarized into reassurance, this skill
has produced nothing — it has only made the absence of rigor harder to notice. Report what
happened, including when a checkpoint could not be satisfied.
