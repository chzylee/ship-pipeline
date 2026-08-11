---
name: sidequest
description: 'Source and screen low-ownership-requirement build candidates for the sidequest lane — projects Claude Code can build autonomously end-to-end because the owner never needs to defend the internals. The second method of the Ship Pipeline sourcing stage (sibling of /scout, which discovers main-lane builds from a person). Screens every candidate with the black-box test ("would I be fine treating this as a black box I did not build, forever?"), shapes survivors for low maintenance, and emits stockpile entries with Origin plus, on greenlight, a launch-ready autonomous BUILD_BRIEF.md in a seeded repo. Use on "find me a sidequest", "sidequest scan", "run sidequest", "stock the sidequest pile", or "sidequest this idea" followed by the idea. Returning zero candidates is a valid outcome. If the idea would ever need its internals defended or evolved, it is a main-lane project - route to /scout or the pipeline instead.'
---

# Sidequest — source builds you never need to own

You run the **autonomous half of sourcing** — the second method of the Ship Pipeline's
▸ Sourcing stage. /scout discovers main-lane builds by interviewing a person; you **mine,
screen, and shape sidequests**: builds Claude Code runs autonomously end-to-end because the
owner never needs to defend the internals. Output = stockpile entries (+ on greenlight, a
launch-ready **BUILD_BRIEF.md** in a seeded repo), never code.

**Contract** (the step-function header):
- **Input:** nothing (scan mode) — or one candidate idea to screen ("sidequest this idea ...").
- **Deliverable:** stockpile entries under the **Sidequest Projects** Notion page (Status +
  Origin + black-box verdict + launch prompt + acceptance checklist); for greenlit candidates,
  a seeded repo with BUILD_BRIEF.md committed.
- **Verification:** the black-box test per candidate (dimensions logged as evidence) + the
  owner's one-word greenlight — the lane's only pre-build handshake. **Zero candidates emitted
  is a valid, good outcome — say so plainly.**

## Why this lane exists (calibrates every judgment below)

Main-lane throughput is capped by the owner's ratification bandwidth, not build capacity; a
build that consumes none of that bandwidth is nearly free. But that is only safe when ownership
is **never** required. Screen on **low ownership requirement, NOT low maintenance** — they come
apart: a project can be trivial to run but expensive to have built (a subtle algorithm, a
gnarly integration), and building it autonomously still leaves a defense the owner can't give.
When in doubt, it's a main-lane project wearing a low-maintenance mask — reject it and say why.

## Phase 0 — Backpressure (always run first)

Find the **Sidequest Projects** page (Notion search by name; if missing, offer to create it).
Read the entries' Status lines. **Skip scanning entirely** when ≥3 entries are
Briefed-but-unlaunched or ≥2 builds are in flight — report the stockpile state instead.
Sourcing what can't be greenlit or launched is inventory, not progress. (Screening a
user-supplied idea bypasses this check but still reports stockpile depth.)

## Phase 1 — Mine (scan mode only)

Sweep for **friction repeated ≥2×**, in order of signal quality:

1. The ts-pmo **Work Log** + capture inbox — repeated manual chores, logged annoyances.
2. **Recent session transcripts** — things the owner did by hand twice, workarounds, "again?" moments.
3. **git across local repos** — hand-run scripts, TODO clusters, copy-pasted utilities.

Prefer candidates with a **natural end date** (a job hunt, an event, a season): self-expiring
domains are maximally safe to under-own. Time-box the sweep — this runs while the owner is
away; do not boil the ocean.

## Phase 2 — Gate: the black-box test

Per candidate, answer: **"Would the owner be fine treating this as a black box they didn't
build — forever?"** The dimensions below are *evidence*, not the criterion — log each:

| Dimension | Passes | Fails |
| --- | --- | --- |
| Change pressure | local files, frozen data, pure computation | external APIs, scraped DOMs, format drift |
| Blast radius | read-only, local outputs | credentials custody, money, writes to systems of record (unless shaped dry-run-first) |
| Audience | the owner only, at v0 | anyone else depends on it |
| Output verifiability | correctness judgeable from outputs, by use | subtle data transforms you can't eyeball — **hard reject** |
| Recovery cost | regenerate-from-brief acceptable | accumulated state you'd mourn |

**Dedupe before emitting** — against the existing stockpile AND previously Discarded/rejected
entries (rejections recur; don't re-litigate them). Emit **at most 2 new candidates per scan**.

## Phase 3 — Shape

Low ownership requirement is partly **designed**, not just selected. Constrain every candidate:
local-first · file-in/file-out · frozen data + a 3-line refresh doc · no servers, accounts, or
runtime network · boring stack, minimal deps · fail loud rather than wrong. A candidate that
can't be shaped into this profile isn't a sidequest — route it to /scout or the main pipeline.

## Phase 4 — Stockpile; Brief on greenlight

**Every emitted candidate** becomes a subpage under Sidequest Projects carrying:

- **Status** — Candidate → Briefed → Built → Accepted / Discarded.
- **Origin** — the friction that sourced it and where it was spotted (Work Log · transcript ·
  git · conversation), with date. Origin is the evidence for the greenlight judgment and the
  calibration data for which sources produce sidequests that actually ship.
- **Black-box verdict** with the dimension log.
- Once Briefed: the **launch prompt** + acceptance checklist.

**On the owner's greenlight** (the one pre-build touchpoint):

1. Seed a repo in the owner's repos directory (kebab-case name; `git init`, commit BUILD_BRIEF.md).
2. **BUILD_BRIEF.md** carries: the lane declaration + **pre-delegated authority** (all
   handshakes resolved by the builder · ship ONE aesthetic · stop line = fully tested build, no
   deployment · accept-or-discard, never a debugging loop) · what it is, user, lifespan · a data
   plan that **never blocks** (frozen pull + fallback seed) · the shaping constraints · v0
   features + explicit non-goals · pipeline instructions at sidequest rigor (single fresh-judge
   verifiers; **Own-Your-Code not required** — ownership is deferred by design) · a
   **≤10-minute black-box acceptance checklist**.
3. Embed a self-contained **launch prompt** in the stockpile entry (pasting it into a fresh
   session starts the build). Precedents: the interview-reps brief for shape; the Rotato
   "Experiment: Autonomous Run" page for run mechanics (state in docs/PIPELINE_LOG.md +
   commits, resumable by construction).

## Lane rules (enforce; don't re-litigate per candidate)

- **One human touchpoint** after greenlight: the ≤10-min acceptance pass, as the user, black-box only.
- **Accept-or-discard:** one autonomous fix cycle after a failed acceptance, then discard.
  Debugging a sidequest is an ownership leak and a money leak.
- **WIP ≤ 2** concurrent autonomous builds; backpressure at the stockpile (Phase 0).
- **Graduation:** a sidequest that starts to matter (other users, feature demands, weekly
  reliance) gets ownership retrofitted — own-your-code + test-spec — and moves to the main
  lane. Low ownership is a deferral, not a write-off.

## Portability notes

- Resolve everything by name, never by hardcoded ID: the Sidequest Projects page, the Work
  Log, the repos directory (infer from the machine's layout; ask once if ambiguous).
- Notion is an **optional upgrade**: without it, write stockpile entries as local markdown
  next to the briefs and say where they would route.
- Console output ASCII-safe; files UTF-8 (JP-locale Windows consoles crash on stray non-ASCII).

**Status: Experimental v0.1.0** — drafted ahead of its first proven run (owner's direction,
2026-07-03); graduates per the harvest rule after the first sourced-and-shipped sidequest.
