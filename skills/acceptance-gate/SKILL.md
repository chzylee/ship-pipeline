---
name: acceptance-gate
description: 'Administer the Acceptance Gate for ONE increment — the leg-checklist that decides it is DONE: the one command green on a clean checkout, every failure path triggered and clean, the documented path producing the artifacts, the owner''s evidence-read of the suite, and the human legs (owner spot-trace + real-user read). This is S7. It runs the checklist and records the verdict; it never fixes code (red findings route to /finish-build), never weakens a test, and never passes a human leg on anyone''s behalf — it presents those as blocking stops and records the owner''s ruling. Under an autonomous run the human legs do not vanish and are not skipped: they become entries in the end-of-run review batch, because a check''s value is that it ran. Internal to Ship Pipeline — the tier-1 skill that reaches it is /adversarial-review, which sequences S5-S7; within that, it is invoked automatically when /finish-build completes, so the owner never has to remember it. You do not need to invoke it by name to use the pipeline, though you can. The criterion to /finish-build''s driver: finish-build drives parked xfail legs to green; this proves the whole gate and either advances the increment or names exactly what blocks. Triggers on "run the acceptance gate", "gate this increment", "is this done", "verify it end to end", "final check before ownership", or /finish-build completing. Done when every leg is passed or explicitly deferred to a named discharger, the gate record is written to docs/build_status.md, and the verdict (ADVANCE / BLOCKED) is stated with evidence.'
---

# Acceptance Gate

Decide, with evidence, whether this increment is **done** — where done is a command that passes, not
a feeling — and either advance it or name exactly what blocks it. This skill **administers** the
gate: it runs the mechanical legs itself, presents the evidence legs to the owner, and records every
outcome. **It changes nothing.**

It is the **criterion** to `/finish-build`'s **driver**: finish-build exists to drive the parked
`xfail(strict)` legs to green; this skill proves the whole checklist — including everything
finish-build never touches — and issues the verdict.

## The failure it exists to kill

**"Done" as a feeling — the gate as formality.** The suite is green, so it ships: nobody ran the
documented path from a clean state, nobody triggered the failure paths, nobody read the assertions,
no real user touched it. Each unrun leg is a class of false positive left alive:
works-on-my-machine, happy-path-only, demo-ware, agent-asserted-success,
built-beautifully-wanted-by-no-one. The gate is the last place these die cheaply.

## What "done" is here (calibration — read this first)

Done is **every leg passed, or explicitly deferred to a named discharger** — never silently skipped.
The legs:

1. **The one command** — green on a **clean checkout** (fresh clone or `git stash`-clean state, the
   documented environment), not the working tree that grew the work.
2. **Every deferred marker gone** — `/finish-build` completed; no `xfail`/skip markers remain;
   nothing regressed. (If markers remain, this gate is premature — route to `/finish-build`.)
3. **Failure paths** — every failure the spec names, triggered live and on purpose; each lands as
   plain English a non-technical user could act on. A stack trace is a FAIL.
4. **The documented path** — the README/quickstart, followed verbatim, produces the promised
   artifacts.
5. **The owner's evidence-read** — the test-file diff and the assertions, presented for the owner to
   actually read. Green is a claim; the assertions are the evidence. **Blocking stop.**
6. **The human legs** — owner spot-trace of one end-to-end scenario, and the real-user read (a real
   user runs the documented path, observed, unaided). These cannot be performed by this skill or any
   agent; they are administered as blocking stops and their outcomes recorded.

**Success test.** When this closes, the owner can say: the documented command passes from nothing,
failures speak human, a person other than the builder has run it, and I read what the tests actually
assert — or the record names precisely which leg is deferred, to whom, and why.

## Under an autonomous run

Everything mechanical still executes. What changes is who reads the two legs that need a reader.

**Leg 5, the evidence-read — a FRESH agent does it, and it still happens.** Dispatch an agent holding
the test diff and the ratified spec and **nothing from the run**, and ask it what the assertions
actually check, mapped to spec items. It reports; its report goes in the batch. It must not be the
proxy that ruled earlier in the run: that agent approved the spec these tests came from, so it has a
stake in the answer, and after a whole run nothing in it looks surprising to it anymore.

**Leg 6, the human legs — deferred, never waived.** The owner spot-trace and the real-user read
cannot be performed by any agent. They become entries in the batch, still outstanding and still
needing their person, each with what it still needs.

A check's value is that it ran, not what it found. Skipping a leg destroys that value; deferring its
*ruling* keeps it. **Never mark a human leg passed because nobody was there to fail it.**

## Where it sits — the handshake

**Upstream:** the ratified `TEST_SPEC.md`, the built suite, and `/finish-build`'s completion (markers
gone). This gate is **reached automatically when `/finish-build` closes** — the owner does not have
to remember it. Chaining automates the invocation, never the verdict.

**Downstream:** `/own-your-code` on a proven increment.

Establish the handshake on entry: read `docs/build_status.md` for position, `TEST_SPEC.md` for the
must-cover index and the named failure paths, and the increment design doc's definition of done for
the one command. **If the suite does not exist, this gate is premature** — verdict BLOCKED, routed
back to `/adversarial-review`. Do not build it here.

## Scope — hold this line

- **Owns:** the leg checklist, running the mechanical legs, presenting the evidence and human legs as
  blocking stops, recording outcomes, writing the gate record, the verdict.
- **Does NOT:** fix code (red → `/finish-build`) · weaken, skip, or delete a failing test (a failing
  test is a finding — stop and report) · re-litigate the spec (ratified; gaps route to `/test-spec`)
  · perform a human leg · check the code against the design doc (that was `conformance`, at S3) ·
  hunt for unspecified behavior (that was `/test-spec`, at S5 — this gate verifies what was agreed).

## Procedure

**0 · Preflight.** Read `docs/build_status.md`, `TEST_SPEC.md`, the increment design doc's DoD.
Confirm `/finish-build` is complete (no deferred markers). State the one command and the leg list
before running anything — the checklist is declared, then executed.

**1 · Suite check.** Confirm the suite exists and covers the ratified spec — every test citing the
spec item it covers, every MUST covered, nothing the spec marks out-of-scope. Run everything; paste
real output — evidence, never asserted success.

**If the suite does not exist, this gate is premature: verdict BLOCKED, routed to
`/adversarial-review`.** Do not write it here. A gate that authors the thing it grades has stopped
being a gate, and it contradicts leg 2 — a suite that was never built cannot have had
`/finish-build` complete against it.

**2 · Mechanical legs.** Clean checkout → the one command → paste output. Trigger each named failure
path → paste each message → grade plain-English or FAIL. Follow the documented path verbatim →
confirm the artifacts exist.

**3 · Evidence stop (blocking).** Present the test-file diff and a digest of what the assertions
actually check, mapped to spec items. The owner reads and rules — this is a `/ratify`-style stop:
elicit what they expect the suite to cover before showing the digest where practical.

**4 · Human legs (blocking).** Present each as a stop: owner spot-trace (one scenario, end to end, by
hand) · real-user read (scheduled or performed; if it cannot happen now, it is **deferred with a
named discharger and date**, recorded — never waived silently). Under an autonomous run these become
batch entries rather than live stops, still recorded as outstanding — see above.

**5 · Record + verdict.** Write the gate record into `docs/build_status.md` (each leg ✓ /
deferred→named discharger + date), append the sitting to `RATIFICATION_LOG.md` if rulings were
elicited, and state the verdict: **ADVANCE** (→ `/own-your-code`) or **BLOCKED** (the exact legs,
each routed: red suite → `/finish-build` · spec gap → `/test-spec` · human leg → its named
discharger).

## The kill rule

A failing gate does not advance — fix or cut, never argue. The gate's authority is that it is
mechanical where it can be and recorded where it can't; the moment a leg is skipped by vibe, the
gate stops meaning "done" and the pipeline's exit criterion is gone.
