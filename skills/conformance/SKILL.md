---
name: conformance
description: 'Check a built increment against its design doc in BOTH directions and report them separately: CREEP (built but never specced — behavior, options, files, and surfaces nobody asked for) and GAP (specced but never built — binding requirements the code does not satisfy). Runs on a fresh context after the implementation exists, holding no history from the agent that wrote the code and none from `audit-tests`. Internal to Ship Pipeline — normally dispatched by /build-and-test; you do not need to invoke it by name to use the pipeline, though you can. It reads CODE against the SPEC; grading tests against the spec is `audit-tests`'' job and this skill never does it. It reports and never repairs: a finding is a finding, not a patch. It also always states its own limit — a clean result says nothing about whether the spec made the right decisions or whether the declaration was complete, because a decision the spec never made has nothing to conform to. Triggers on "check conformance", "does the build match the spec", "did the agent build what was specced", "find scope creep in this build", or reaching S3. Done when both directions are reported separately with evidence, every finding cites a requirement id or a code location, and the completeness limit is stated.'
---

# Conformance

Check the built increment against its design doc, **in both directions**, and report what you find.

This is **S3**. An increment that passes here is **conformant** — it matches what was specified. It
is not yet **trusted**; nothing has attacked it. Those are different promises and you only issue the
first one.

## The failure it exists to kill

**Two failures, opposite in shape, both invisible from inside the build.**

**Creep.** The agent built more than was asked. An extra config option, a retry nobody specified, a
second code path for a case that never came up, a file that exists for reasons the spec never gives.
Each addition looked helpful in the moment. Together they are surface area the owner never agreed
to, never reviewed, and now has to maintain — and the tests pass, because the tests were written for
what *was* specified.

**Gap.** The agent built less. A binding requirement is quietly unsatisfied — the happy path works,
the named error case does nothing, the boundary the spec drew is not enforced. This one is more
dangerous, because everything looks finished.

Neither is visible to whoever wrote the code. They know what they meant to do, so they read the diff
as the intent rather than as the artifact.

## The one constraint: you did not write this

**You hold the design doc and the code, and no history from the agent that produced either.** No
transcript, no reasoning, no explanation of why something is the way it is. If you have that
context, you are the wrong agent — you will read the code as the argument for itself.

**You also hold no context from `audit-tests`.** Two checks run on this increment and they are
deliberately separate agents on separate inputs.

## What "done" is here

Both directions reported **separately** — never merged into one list, because they mean opposite
things and route to opposite fixes. Every finding cites a requirement id, a code location, or both.
The completeness limit stated.

**Success test.** The owner reads your report and can act on every line without opening the diff:
each creep item is something they can rule keep-or-cut, and each gap item is something a builder can
go implement.

## The two directions

### CREEP — built but never specced
Walk the code. For each behavior, option, surface, file, and dependency, ask: **which requirement
asks for this?** Anything that cannot name one is a creep finding.

Report what it is, where it lives, and what it would take to remove. Do **not** report it as a
defect — it may be something the owner wants, and that is theirs to rule. You are reporting that it
was never agreed to.

Include: behavior no requirement describes · configuration nobody asked for · error handling beyond
the named failure paths · added dependencies · files whose existence the spec does not imply ·
abstractions built for cases the increment does not contain.

### GAP — specced but never built
Walk the binding requirements. For each `MUST` in this increment, ask: **where is it satisfied?**
Anything you cannot point at is a gap finding.

Report the requirement id, what the code does instead, and — where it is cheap to say — the test
that would have caught it. A requirement satisfied only by a test, with no implementation behind it,
is a gap.

## The limit you must state

**Conformance and completeness are orthogonal, and your report says so explicitly.**

You can only check against what the spec decided. A decision the spec never made has nothing to
conform to — so a clean result from you is *not* evidence that the declaration was complete, that
the design was right, or that the increment is safe. It is evidence of exactly one thing: what was
written down got built, and nothing else did.

State this in the report every time, including — especially — when you find nothing. A clean
conformance result is the single most likely finding in this pipeline to be over-read.

## Where it sits — the handshake

**Upstream:** the increment design doc and the built code, after implementation. Dispatched by
`/build-and-test`.

**Downstream:** `/build-and-test`, which presents your findings to the owner at S4. Creep routes to
an owner ruling (keep or cut). Gap routes back for another pass.

## Scope — hold this line

- **Owns:** both directions, reported separately · citing requirement ids and code locations ·
  stating the completeness limit.
- **Does NOT:** fix anything (a finding is never a patch) · grade tests against the spec — that is
  `audit-tests`, a different agent on different inputs · re-litigate the design · judge whether a
  requirement is a good idea · label a finding minor, major, or significant · declare the increment
  trusted, done, or ready to ship.

## Procedure

**0 · Confirm your inputs.** State that you hold the doc and the code, and that you carry no context
from the building agent or from `audit-tests`.

**1 · Index the binding requirements.** Every `MUST` in this increment, by id.

**2 · Walk the code for creep.** Every behavior, option, surface, file, dependency → which
requirement asks for it? Collect what cannot answer.

**3 · Walk the requirements for gaps.** Every `MUST` → where is it satisfied? Collect what you
cannot point at.

**4 · Report the two lists separately**, each finding with its evidence.

**5 · State the limit.** In the report, not as a footnote.

**6 · Stop.** No fixes, no rulings, no verdict beyond conformant / not conformant on what the spec
actually determined.

## The kill rule

**A clean result is not a green light.** You checked the build against the spec — nothing more.
Whether the spec was worth conforming to is a question you are structurally unable to answer, and
reporting anything that implies otherwise is the one way this check can do harm.
