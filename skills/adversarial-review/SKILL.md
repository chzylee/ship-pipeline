---
name: adversarial-review
description: 'Run the hardening phase for one increment as a single entry point: spec what must be protected against, drive the code to green, and gate it. Sequences /test-spec (S5) → /finish-build (S6) → /acceptance-gate (S7), so the owner meets one skill instead of three. Its subject is what the design NEVER DECIDED — failure modes, edge cases, boundaries the spec named but did not cross, and the silly errors that survive a spec-conformant build. It does not re-check the code against the design doc; `conformance` did that at S3, and conformance and completeness are orthogonal. Adversarial in posture, not destructive in aim: the goal is that nothing dumb survives, not that something breaks. A convenience composite, not an enforcement one — every link can halt, and it stops at the owner''s two touchpoints (ratifying the test spec, and the gate''s human legs) rather than batching them away. Runs on EVERY increment, however brief, including ones where it is expected to find nothing — the pass is warranted by how agents fail, not by its yield. Iteration here is the phase working as intended and its count says nothing about spec quality. Tier 1: one of the five skills that make up using Ship Pipeline. Accepts --retrace. Triggers on "harden this", "adversarial review", "run the hardening pass", "what could go wrong with what I built", "review this for edge cases", or reaching S5. Done when a ratified test spec exists, the suite is green with deferred markers removed, and the gate has issued ADVANCE or BLOCKED with evidence.'
---

# Adversarial Review

Take an increment that **works** and find out whether it can be **trusted**.

One entry point for **S5 through S7**. It sequences three skills the owner would otherwise invoke by
hand:

```
/test-spec        S5  ·  what must be protected against   → owner ratifies
/finish-build     S6  ·  drive the code to green
/acceptance-gate  S7  ·  prove the whole checklist        → owner rules
```

## What this phase is for — and what it is not

By the time you run, the increment is **conformant**. An independent agent already checked the code
against the design doc in both directions: nothing built that was not specced, nothing specced that
was not built. **Do not do that again.** It is done, it was done by someone with fresher eyes than
yours, and repeating it spends the owner's attention on the one question already answered.

**Your subject is everything the design never decided.** A decision the spec never made has nothing
to conform to — which is precisely why a clean conformance result says nothing about it. Failure
modes. Edge cases. Boundaries the doc names and stops at. Invariants nobody wrote down. The
unglamorous errors that pass every test written for the happy path.

**Adversarial in posture, not destructive in aim.** You are not trying to break the thing. You are
making sure nothing dumb survives — the difference between an attack and a review, and the reason
this is the second one.

## Conformant is not trusted

Two promises, and this phase is where the second one gets made:

- **Conformant** (after S3) — it does what was described.
- **Trusted** (after S7) — it survived deliberate scrutiny.

An initial build makes what is described work. It does not promise robustness against cases nobody
enumerated. Everything below exists to close that gap, and nothing before it did.

## Every increment gets this pass

However brief. **Including the ones where you expect to find nothing.**

The pass is warranted by *how agents fail*, not by its yield. A pass that surfaces nothing is a
successful pass — the value is that it ran, not what it caught. Do not skip it on small increments,
and do not apologize for a clean result.

## Iteration here is not a defect

If this phase loops — the spec finds a hole, the fix reveals another, the gate sends something back
— that is **the phase working as intended.** Its count means nothing about the quality of the design
doc.

This is the opposite polarity from the rework loop at build time, whose target is zero because it
measures whether the spec did its job. Report them differently. A system that cannot tell them apart
reads its own history backwards.

## What "done" is here

A ratified `TEST_SPEC.md` section for this increment · the suite fully green with every deferred
marker removed and nothing regressed · a gate verdict of **ADVANCE** or **BLOCKED**, with evidence.

## It halts, and it surfaces

This is a **convenience** composite. It bundles steps the owner could invoke by hand; it does not
exist to make an invariant hold mechanically. That means two things:

**Every link can halt.** It stops at both of the owner's touchpoints in this phase:
- **S5** — the owner ratifies the test spec. Every `SKIP` is a decision about what they are willing
  to be wrong about. It is theirs.
- **S7** — the gate's evidence-read and human legs. The gate never passes one on anyone's behalf.

**It surfaces everything it passed through.** Running a composite that spans an approval point *is*
the approval for it — which is legitimate only because everything ruled inside it comes back out.
Present the skip list, the forks taken at S6, and the gate record. A composite that hides its
decisions is ok-clicking at a higher altitude.

If the owner stops mid-phase, that is a normal outcome, not a failure. Say where it stopped and what
remains.

## Options

`--retrace` · produce an account of how the hardening went via `/retrace`, appended to
`docs/retrace/<increment>.md` — the same file `/build-and-test` appends to, so one document covers
how the thing was built **and** how it got fixed. The fixes are the most instructive part for a
reader trying to learn rather than inherit.

## Scope — hold this line

- **Owns:** sequencing S5 → S6 → S7 · holding the halts at S5 and S7 · surfacing everything the
  phase decided · the phase-level verdict.
- **Does NOT:** re-check code against the design doc (that was `conformance`, at S3) · re-specify
  behavior the build already tested · fix code itself (that is `/finish-build`) · pass a human leg ·
  rule on a `SKIP` · declare the increment shippable on its own authority.

**On writing the tests — this skill dispatches the author.** Building tests from the ratified spec
is not a *skill*, for the same reason building code from the design doc is not one: it is an agent
working from a ratified artifact, and that artifact is the interface. But something has to launch
that agent, and it is this one. Same shape as `/build-and-test` at S2.

This skill holds the frame around it: the spec must be ratified first, the author works from the
spec and does **not** read the implementation, every test cites the spec item it covers, and tests
pinning behavior the code does not yet have are committed failing. It does not author them itself,
and it does not delegate the authorship to `/test-spec`, which produces the spec and never the tests.

## Where it sits — the handshake

**Upstream:** a conformant increment out of `/build-and-test`, with its conformance and audit
findings already reviewed by the owner at S4.

**Downstream:** `/own-your-code` on a trusted increment, or a named blocker.

## Procedure

**1 · Confirm conformance happened.** Read `docs/checks/<increment>.md` for the S3 findings. If
Advance `docs/build_status.md` to `S5` on entry — nothing between the two harnesses moves it
otherwise, and the tracker would skip two steps every increment. If
`/build-and-test` never ran, say so —
this phase assumes a build already checked against its spec, and running it against an unchecked one
means the owner is getting the adversarial pass without the conformance pass, which are different
things.

**2 · Run `/test-spec`.** Agent-proposed, owner-ruled. **Blocking stop** at ratification.

**3 · Build the tests from the ratified spec**, committed failing where they pin behavior the code
does not have yet.

**4 · Run `/finish-build`.** It is autonomous and does not stop per fix. Per owed behavior it names
the trap, fixes, verifies red-then-green, and logs. Mechanism forks are picked, recorded in
declaration form, and surfaced — never halted for.

**5 · `/acceptance-gate` runs on completion** — chained from `/finish-build`, not invoked separately.
**Blocking stops** at the evidence-read and the human legs.

**6 · Surface and close.** Present the skip list, the S6 forks, and the gate record together. State
the verdict and what, if anything, is deferred and to whom.

## The kill rule

**The skip list is the product.** Everything else here is machinery around one question the owner has
to answer: what are you willing to be wrong about? A phase that runs clean and never made them answer
it has produced a green light, not trust.
