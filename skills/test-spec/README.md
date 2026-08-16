# test-spec

A Claude skill that produces the **Test Spec** for one increment: the ratified list of *what must be
protected against for a conformant build to be trusted.*

This is **S5** of [Ship Pipeline](../../README.md) — the adversarial layer. It is normally reached
by `/adversarial-review` rather than invoked by name.

## What it does

By the time it runs, the increment already works: tests for the specced behavior exist, were
observed failing before the implementation, and were audited for whether they would catch a wrong
build. An independent agent checked the code against the design doc in both directions.

So this skill does **not** re-specify that. Its subject is **everything the design never decided** —
failure modes, edge cases, boundaries the spec named but did not cross, and the invariants nobody
wrote down.

It runs the opposite way from the design doc: **agent-proposed, owner-ruled.** The owner cannot
enumerate the failure modes of code they did not write; the agent can. So a senior test/QA-lead
persona proposes candidates and walks the owner through them one at a time with blocking stops. It
triages every candidate by risk (`MUST` / `SHOULD` / `SKIP`), names the verification method per item,
and ends at an executable acceptance scenario. A final adversarial pass hunts what was missed.

It produces the **spec, never the tests** — a separate step writes tests from it.

## Output

`TEST_SPEC.md` at repo root — a **living** artifact in version control. Each increment amends its
own section and its rows in the must-cover index; never clobbered, never forked. The repo is
canonical; a wiki may carry a dated, non-editable snapshot that names the repo file as its source.

Done when the owner has ratified it, not when a draft exists.

## Install

Installed with the rest of Ship Pipeline — see the [repo README](../../README.md#install). Do not
symlink this directory on its own; the skill references its siblings.

## Status

See [`VERSION`](VERSION). Narrowed to S5's adversarial spec in the v1 roster rework — it previously
carried a version-level "sweep" scope, which no longer exists now that the pipeline models only two
doc tiers.
