# scout

The **idea-discovery front door** of the ship pipeline: an *inverted* office-hours. office-hours
pressure-tests an idea you already have; **scout finds one you don't** — by starting from a person
and the work they actually do, interviewing one question at a time, and converging on a **Build
Brief** (a structured spec of what to build and why, not code).

For when you need an idea, not when you have one. It feeds the Build Brief into the rest of the
pipeline (Scope Gate → Design Doc → build → ...).

## What it does
- **Refuses a pre-formed solution** at the door and anchors on a *named* person + a slice of their work.
- **Sets a stakes mode** (Sprint / Venture / Learn) that tunes which gates are load-bearing.
- **Excavates the work** one question at a time; **front-loads a feasibility filter** (kills
  ToS-locked / doesn't-exist data sources before generating ideas).
- **Generates 2–3 candidate builds**, gates them, and you pick one.
- Produces a **Build Brief** ending in a **Reality Probe**: a 30-minute pre-code test with a kill
  criterion, so an idea that dies on first contact dies cheap.
- Keeps a **Scout Log** so killed ideas leave a one-line "death certificate" and their fragments can
  recombine into the winner.

## Invoke
`/scout`, or "what should I build" / "find me something to build for [named person]". Mid-run,
"stash / reset / park this" logs the current idea and restarts on a fresh subject.

If you already HAVE an idea to validate → use **/office-hours** instead (the forward direction).

## Requirements
None beyond Claude Code. Uses only built-in tools (AskUserQuestion, Read/Write/Grep/Glob, WebSearch).
Read-only on your files except the Build Brief it writes.
