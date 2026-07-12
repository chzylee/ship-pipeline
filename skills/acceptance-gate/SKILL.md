---
name: acceptance-gate
description: 'Administer the Acceptance Gate — the leg-checklist that decides a build is DONE: the one command green on a clean checkout, every failure path triggered and clean, the documented path producing the artifacts, the owner''s evidence-read of the suite, and the human legs (owner spot-trace + real-user read on main-lane builds). This skill runs the checklist and records the verdict; it never fixes code (red findings route to /finish-build), never weakens a test, and never passes a human leg on the human''s behalf — it presents those as blocking stops and records the owner''s ruling. The criterion to /finish-build''s driver: finish-build drives parked xfail legs to green; this skill proves the whole gate and advances the build to /own-your-code or names exactly what blocks. Triggers on "run the acceptance gate", "gate this build", "is this build done", "verify the build end to end", "final check before ownership", or reaching the gate stage after /finish-build completes. Done when every leg is passed or explicitly deferred to a named discharger, the gate record is written to docs/build_status.md, and the verdict (ADVANCE / BLOCKED) is stated with evidence.'
---

# Acceptance Gate

Decide, with evidence, whether this build is **done** — where done is a command that passes, not a
feeling — and either advance it to `/own-your-code` or name exactly what blocks it. This skill
**administers** the gate: it runs the mechanical legs itself, presents the evidence legs to the
owner, and records every outcome. It changes nothing.

It is the **criterion** to `/finish-build`'s **driver**: finish-build exists to drive the parked
`xfail(strict)` legs to green; this skill proves the whole checklist — including everything
finish-build never touches — and issues the verdict.

## The failure it exists to kill

**"Done" as a feeling — the gate as formality.** The suite is green, so the build ships: nobody ran
the documented path from a clean state, nobody triggered the failure paths, nobody read the
assertions, no real user touched it. Each unrun leg is a class of false positive left alive:
works-on-my-machine, happy-path-only, demo-ware, agent-asserted-success, built-beautifully-wanted-
by-no-one. The gate is the last place these die cheaply.

## What "done" is here (calibration — read this first)

Done is **every leg of the checklist passed, or explicitly deferred to a named discharger** — never
silently skipped. The legs:

1. **The one command** — green on a **clean checkout** (fresh clone or `git stash`-clean state, the
   documented environment), not the working tree that grew the build.
2. **Every deferred marker gone** — `/finish-build` completed; no `xfail`/skip markers remain;
   nothing regressed. (If markers remain, this gate is premature — route to `/finish-build`.)
3. **Failure paths** — every failure the spec names, triggered live and on purpose; each lands as
   plain English a non-technical user could act on. A stack trace is a FAIL.
4. **The documented path** — the README/quickstart, followed verbatim, produces the promised
   artifacts.
5. **The owner's evidence-read** — the test-file diff and the assertions, presented for the owner
   to actually read. Green is a claim; the assertions are the evidence. **Blocking stop.**
6. **The human legs (main lane only)** — owner spot-trace of one end-to-end scenario, and the
   real-user read (a real user runs the documented path, observed, unaided). These cannot be
   performed by this skill or any agent; they are administered as blocking stops and their
   outcomes recorded. Sidequest-lane builds waive these for the ≤10-minute acceptance touchpoint.

**Success test.** When this closes, the owner can say: the documented command passes from nothing,
failures speak human, a person other than the builder has run it, and I read what the tests
actually assert — or the record names precisely which leg is deferred, to whom, and why.

## Where it sits — the handshake

Upstream: the ratified `TEST_SPEC.md`, the built suite, and `/finish-build`'s completion (markers
gone). Downstream: `/own-your-code` on a proven build. Establish the handshake on entry: read
`docs/build_status.md` for position, `TEST_SPEC.md` for the MUST index and the named failure
paths, and the Design Doc's definition of done for the one command. If the suite does not exist
yet, build it first from the spec (rules below), then gate.

## Scope — hold this line

- **Owns:** the leg checklist, running the mechanical legs, presenting the evidence and human legs
  as blocking stops, recording outcomes, writing the gate record, the verdict.
- **Does NOT:** fix code (red → `/finish-build`) · weaken, skip, or delete a failing test (a
  failing test is a finding — stop and report) · re-litigate the spec (ratified; gaps route to
  `/test-spec`) · perform a human leg · hunt for unspecified behavior (the adversarial pass lives
  at the spec sweep and pre-release, never here — this gate verifies what was specified).

## Procedure

**0 · Preflight.** Read `docs/build_status.md`, `TEST_SPEC.md`, the Design Doc's DoD. Confirm
`/finish-build` is complete (no deferred markers). State the one command and the leg list before
running anything — the checklist is declared, then executed.

**1 · Suite check (build it only if absent).** If tests don't yet exist, build them from the
ratified spec: every test cites its spec item in a comment; every MUST covered, SHOULDs where
cheap; nothing the spec marks out-of-scope or deliberately-skipped. Show the test-file diff. Run
everything; paste real output — evidence, never asserted success.

**2 · Mechanical legs.** Clean checkout → the one command → paste output. Trigger each named
failure path → paste each message → grade plain-English or FAIL. Follow the documented path
verbatim → confirm the artifacts exist.

**3 · Evidence stop (blocking).** Present the test-file diff and a digest of what the assertions
actually check, mapped to spec items. The owner reads and rules — this is a `/ratify`-style stop:
elicit what they expect the suite to cover before showing the digest where practical.

**4 · Human legs (blocking, main lane).** Present each as a stop: owner spot-trace (one scenario,
end to end, by hand) · real-user read (scheduled or performed; if it cannot happen now, it is
**deferred with a named discharger and date**, recorded — never waived silently).

**5 · Record + verdict.** Write the gate record into `docs/build_status.md` (the gate-legs
checklist: each leg ✓ / deferred→named step + date), append the sitting to `RATIFICATION_LOG.md`
if rulings were elicited, and state the verdict: **ADVANCE** (→ `/own-your-code`) or **BLOCKED**
(the exact legs, each routed: red suite → `/finish-build` · drift → build review · spec gap →
`/test-spec` · human leg → its named discharger).

## The kill rule

A failing gate does not advance — fix or cut, never argue. The gate's authority is that it is
mechanical where it can be and recorded where it can't; the moment a leg is skipped by vibe, the
gate stops meaning "done" and the pipeline's exit criterion is gone.
