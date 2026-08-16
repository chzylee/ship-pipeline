---
name: audit-tests
description: 'Audit a failing test suite against the design doc it claims to cover, and answer one question: WOULD THESE TESTS CATCH A WRONG BUILD? Runs after the tests are red and before the implementation exists — concurrently with the building agent, so it costs no wall-clock. Its method is adversarial and concrete: for each test, construct a wrong-but-plausible implementation that satisfies the spec''s words while violating its intent, and report whether the test actually fails on it. Names tautological, vacuous, and mock-bound tests individually, and names every binding requirement with no test behind it. Internal to Ship Pipeline — normally dispatched by /build-and-test; you do not need to invoke it by name to use the pipeline, though you can. It reads TESTS against the SPEC; checking CODE against the spec is `conformance`''s job and this skill never does it. It never edits a test, never writes an implementation, and never reports a suite adequate because it is red. Triggers on "audit these tests", "would these tests catch a wrong build", "are these tests any good", "check the tests against the spec", or reaching the concurrent audit step of S2. Done when every test is graded against the requirement it claims, every weak test is named with the wrong build that would survive it, and every untested binding requirement is listed.'
---

# Audit Tests

Read a red test suite and its design doc, and say whether those tests would **catch a wrong build**.

Nothing else in the pipeline asks this. Writing tests before the implementation proves a test *can*
fail. It does not prove the test fails for the **right reason** — and a test that fails for the
wrong reason will pass for the wrong reason too, five minutes later, and be believed.

## The failure it exists to kill

**The green suite that guarantees nothing.** The tests were written first and observed failing, so
the discipline looks satisfied. But one asserts the mock was called rather than that anything
happened. One restates the implementation instead of the requirement, so it will agree with the code
no matter what the code does. One fails today only because the module does not exist yet, and will
pass the moment anything is importable. Three binding requirements have no test at all.

Then the implementation lands, everything goes green, and the green is read as evidence.

**Red is cheap when nothing is built.** Almost any string of characters fails against an empty
module. That is the trap this skill exists for.

## The method: construct the wrong build

For each test, do this concretely rather than by inspection:

1. **Read the requirement the test claims to cover.**
2. **Invent an implementation that a competent, hurried agent would plausibly write** — one that
   satisfies the requirement's *words* while getting its *intent* wrong. Not an absurd one. The
   realistic near-miss.
3. **Ask whether this test fails against that implementation.**
4. **If it would pass, the test is inadequate**, and you say so with the specific wrong build that
   survives it.

Naming the surviving wrong build is not optional decoration. It is the finding. "This test is weak"
is unactionable; *"an implementation that returns the first match instead of the closest one passes
this test"* tells the builder exactly what to add.

## What you are looking for

- **Tautological** — the assertion restates the implementation, so it agrees with any behavior the
  code happens to have. Often reads as thorough.
- **Vacuous** — asserts something that cannot fail: a truthy check on a non-empty object, a call
  count with no outcome, an exception type with no message or state check.
- **Mock-bound** — verifies the test double was used, not that anything was accomplished. The
  system under test could be deleted and the test would stand.
- **Import-red only** — currently fails because nothing exists yet, and would pass against any
  implementation at all. The most common false positive in a red-first suite, and the hardest to
  see, because it *is* red and red is what everyone was looking for.
- **Mis-anchored** — cites a requirement it does not actually exercise.
- **Uncovered** — a binding requirement with no test behind it. This is a finding about the *tests*,
  which is why it belongs here.

## What "done" is here

Every test graded against the requirement it claims, with a named surviving wrong build wherever the
grade is inadequate; every uncovered binding requirement listed. No test edited, no implementation
written.

**Success test.** A builder reads your report and knows exactly which tests to strengthen and what
each one has to start catching — without re-deriving your reasoning.

## Where it sits — the handshake

**Upstream:** the increment design doc and the test files, after the tests are red and **before the
implementation exists.** Dispatched by `/build-and-test`.

**You run concurrently with the building agent.** That is why this check is affordable: it occupies
no time the build was not already spending. Do not wait for the implementation, and do not read it
if it appears — your judgment must come from the spec and the tests alone, or it will drift into
grading the code, which is not your job.

**You hold no context from the building agent, and none from `conformance`.** Two separate checks
run on this increment and they are deliberately different agents. An agent that approved these tests
has a stake in their adequacy, and is the least likely reader to later conclude that a build passed
tests which were never good enough.

**Downstream:** `/build-and-test`, which presents your report to the owner.

## Scope — hold this line

- **Owns:** grading tests against the spec · naming the wrong build that survives each weak test ·
  listing binding requirements with no test.
- **Does NOT:** edit or write tests (a weak test is a finding, never a patch) · write or read the
  implementation · check code against the spec — that is `conformance`, a different agent on
  different inputs · judge whether the design is good · report a suite adequate on the grounds that
  it is red · declare the tests sufficient in some overall sense.

## Procedure

**0 · Confirm your inputs.** State that you hold the design doc and the tests, that no
implementation is in scope, and that you carry no context from the building agent. If an
implementation is already present and complete, say so — the audit still runs, but the concurrency
guarantee it was designed around did not hold, and the owner should know.

**1 · Index the binding requirements.** Every `MUST` in the increment, by id.

**2 · Map tests to requirements.** Each test → the requirement it claims. Note any test claiming
nothing, and any requirement claimed by nothing.

**3 · Grade each test by constructing the wrong build.** Per the method above. Record the surviving
implementation in plain terms wherever the test does not catch it.

**4 · Report.** Per test: the requirement, the grade, and — where inadequate — the wrong build that
survives. Then the list of uncovered binding requirements.

**5 · Stop.** No fixes, no rewrites, no overall verdict on the suite's quality.

## The kill rule

**Red is not evidence.** A test that fails against nothing tells you nothing about whether it will
fail against something wrong. If you cannot name a wrong build that a test would catch, that test
has not been shown to work — say so plainly, and do not let the suite's redness stand in for it.
