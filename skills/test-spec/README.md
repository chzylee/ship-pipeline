# test-spec

A Claude skill that produces the **Test Spec** — the agreed-upon document of *what must be tested
to trust that a build executes its design properly.* It is the **verification-side dual of the
design doc**: where the design doc says what we're building and why, the Test Spec says how we'll
know it's built correctly.

Step 1 of the Testing & Validation phase of the LLM-assisted development pipeline. A green light is
a claim, not evidence — this skill is the human's control surface over *what gets greenlit*, so a
passing suite verifies expected behavior instead of patting itself on the back.

## What it does
Works by **dialogue**, gstack-style: a senior test/QA-lead persona reads the design doc (and code,
if present), proposes the must-be-true behaviors, invariants, and failure modes, and walks you
through them one at a time with blocking stops — so you **ratify exactly what gets tested** rather
than accepting a generated list. It triages every candidate by risk (`MUST` / `SHOULD` / `SKIP`),
names the verification method per item, and ends at an executable acceptance gate. A final
adversarial pass hunts the cases that were missed.

It produces the **spec, never the tests** — a separate build step writes tests from it. Like
`/office-hours` produces a design doc and never code.

## Output
`TEST_SPEC.md` at repo root — a **living** artifact (amend it as design evolves; keep it in version
control), optionally archived to the Testing & Validation Notion space. Done when the spec is
ratified.

## Install
This is a personal Claude skill. Symlink it into your Claude skills directory so `/test-spec`
resolves:

```bash
ln -s ~/repos/test-spec ~/.claude/skills/test-spec
```

On Windows (PowerShell, dev mode or admin):

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\test-spec" -Target "$env:USERPROFILE\repos\test-spec"
```

## Status
`v0.1.0` — first draft. Not yet validated against a real build; Runway is the intended first
prototype pass.
