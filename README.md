# Ship Pipeline

**A spec-driven process for building software with agents, operated as a set of Claude Code skills.**

It does not write code and it does not decide what to build. It decides one thing, repeatedly, and
makes the answer visible:

> **Is this spec specific enough that an agent can execute it without making decisions the owner
> would have wanted to make?**

The failure it exists to prevent: *building something massive, finding an issue, and now you have to
go back and make a ton of changes.*

**Who it's for.** A developer who builds with agents and remains responsible for the result — who
must be able to explain, defend, and evolve software they did not type. Not a manager approving
work, and not a user of a finished product: the person on the hook.

## The loop

Work is done in **increments**. One increment is one scoped thing to build, one design doc, one pass
through seven steps.

| Step | What happens | Who |
|---|---|---|
| **S1** | spec it, and approve it | **owner** |
| **S2** | an agent builds — tests first, seen failing, audited while the code is written | agent |
| **S3** | a fresh agent checks the result against the spec, both directions | agent |
| **S4** | review the findings | **owner** |
| **S5** | spec what must be protected against | **owner** rules, agent proposes |
| **S6** | drive it to green | agent |
| **S7** | sign off | **owner** |

**S2-S3 run without you, as do S6's fix cycles.** Your touchpoints are S1, S4, S5, S7 — and each is a
judgment, never a transcription task.

**Two promises, not one.** An increment that passes S3 is **conformant**: it does what was described.
Only one that passes S7 is **trusted**: it survived deliberate scrutiny. An initial build makes what
is described work; it does not promise robustness against cases nobody enumerated.

**Two loops with opposite polarity.** Rework at S2-S4 is a *defect* — its target is zero, and its
count measures whether the spec did its job. Iteration at S5-S7 is the phase *working as intended*
and says nothing about spec quality. A system that cannot tell them apart reads its own history
backwards.

## Your first increment

Three commands, in this order, in your own repo:

```bash
claude
```

```text
/design-doc      # S1 — derive the increment spec, read the declaration, approve it
/build-and-test  # S2-S4 — it dispatches the builder and both checks, then shows you the findings
/adversarial-review  # S5-S7 — spec the holes, drive to green, gate it
```

That's one increment. Then `/own-your-code` when you want the ownership doc, or `/auto-build`
instead of the middle two when you want the whole thing to run unattended.

**Do you need a project-tier `DESIGN.md` first?** No. `/design-doc` will offer to derive one, and an
increment doc can stamp `scope authority: none — authored here` when there is nothing above it. On a
project you expect to run more than a couple of increments through, derive the project doc first —
it's what the increments trace to.

## The declaration

Before you approve at S1, an agent that has **never seen the conversation that produced the spec**
reads it cold and enumerates every decision it would have to make to execute it. Each entry:

```
decision:  what it would have to choose
options:   what it would be choosing between
taking:    which it would take absent a ruling
reversal:  in plain language, what undoing this looks like if it is wrong
           — including anything already escaped (data written, calls made)
unknowns:  context it believes it lacks and would want before deciding
```

**No severity field, ever.** An agent can estimate what reversing something costs — how far it
spread, whether anything escaped, what else locks to it. It cannot estimate whether you'd *care*,
because that lives in what you value and exists nowhere in the code. So the system surfaces the bill
and never tells you whether to pay it.

Signing attests that the items on the list are ruled correctly. It does not attest that the list is
complete, and completeness is not gated on.

## Skills

**Tier 1 — this is what using Ship Pipeline means.** Five skills. You do not need to learn any others.

| Skill | Step | |
|---|---|---|
| `/design-doc` | S1 | v0.6.0 — derive the binding spec in a session, or sync a stale one. Dispatches `declare`, runs the scope check, presses on one test: *would a wrong build still pass this sentence?* |
| `/build-and-test` | S2-S4 | v0.2.0 — the harness. Dispatches the build agent, gates tests-red-before-implementation, runs the audit concurrently and conformance after, presents the findings and the rework count |
| `/adversarial-review` | S5-S7 | v0.3.0 — the hardening phase as one entry: spec the holes, drive to green, gate it |
| `/auto-build` | S1-S7 | v0.4.0 — run the whole increment unattended against a spec you approved; every decision it made comes back as a proposed design-doc amendment you rule on |
| `/own-your-code` | after | v2.4.0 — the onboarding that confers ownership, regenerated in place |

**Tier 2 — the machinery.** Individually callable, never required knowledge.

| Skill | Reached by | |
|---|---|---|
| `declare` | `/design-doc` | v0.2.0 — cold-reads the spec and enumerates what it would have to choose |
| `audit-tests` | `/build-and-test` | v0.1.0 — would these tests catch a wrong build? Names the wrong build that survives each weak one |
| `conformance` | `/build-and-test` | v0.1.0 — creep and gap, reported separately |
| `/test-spec` | `/adversarial-review` | v0.7.0 — the adversarial spec for one increment, agent-proposed and owner-ruled. This is where `/ratify` is baked in |
| `/finish-build` | `/adversarial-review` | v0.3.0 — drives parked `xfail` legs to green, autonomously, logging the trap and evidence per fix |
| `/acceptance-gate` | `/finish-build` | v0.4.0 — the leg-checklist that decides done |
| `/retrace` | `--retrace` on either harness | v0.2.0 — how the agent actually worked, wrong turns included. Supplementary; off by default |
| `/ratify` | every approval stop | **external** — see Dependency below |

**Add-ons, on their own clock.** `/scout` (v2.0) discovers what to build from a person and their real
work; `/sidequest` (v0.1) sources low-ownership builds. They feed S1's input; they are not steps of
the pipeline, which takes one scoped thing at a time and does not ask where it came from.

## Composition, and why it's safe

**One repeatable action, one skill.** The pipeline is the orchestration of them, and composites like
`/adversarial-review` and `/auto-build` exist because grouping by *stage of the process from your
point of view* is better UX than making you remember eight names.

**Running a composite that spans an approval point IS the approval for it** — delegation is itself a
signed decision, and it is legitimate precisely because you choose it per increment rather than
configuring it once. What makes that honest is the other half: **a composite must surface everything
it passed through.** One that hides its decisions is ok-clicking at a higher altitude.

**Permission scope is yours.** An unattended run needs your Claude Code permission settings
configured for the commands it will actually run — the test suite, a clean-checkout clone, whatever
the build touches. No skill here manages, requests, or widens permissions; that would be a tool
deciding its own reach. Set it before you launch an overnight run, or it will stop at the first
prompt and wait.

**Nothing here can refuse you.** You may elect to run autonomously and knowingly accept the risk.
`/auto-build` may report that a spec looks thin; it may not decline to run it. A system that can
override the owner's accepted risk has taken authority it does not have. Every mechanism informs a
choice; none of them may make one.

## What each run carries in-repo

State, decisions, and provenance live in the **project's own repo**, so a cold clone is
self-describing. Each fact has one home.

| Artifact | Lives at | Source of truth for |
|---|---|---|
| Project design | `DESIGN.md` | what the project is intended to become |
| Increment design | `docs/design/<increment>.md` | what this one pass builds |
| Position + gate legs | `docs/build_status.md` | where this project is |
| Ratified test contract | `TEST_SPEC.md` | what must be true to trust it |
| Decisions + forks | `docs/decision_log.md` | why it is the way it is |
| Ownership record | `RATIFICATION_LOG.md` | demonstrated judgment + blind spots |
| Audit + conformance findings | `docs/checks/<increment>.md` | what the S2-S3 checks found, and the rework count |
| **Ownership doc** | `docs/own_your_code.md` | **the deliverable that matters** — what lets someone step back in and own the project |
| Retraces | `docs/retrace/<increment>.md` | how the agent worked. **Supplementary**, non-binding, off by default |

**The repo is canonical.** A wiki restates; it does not decide. Where a wiki disagrees with these
files, these files are right and the wiki is stale.

**Two doc tiers and no more** — project and increment. Nothing binding sits between them. Version,
feature, and milestone are planning labels this system does not model; decomposing a project into
increments is your activity, not the system's.

### The `design-doc impact:` line — the drift fix

Every `decision_log.md` and `RATIFICATION_LOG.md` entry carries a `design-doc impact:` line: `none`,
or the design unit it changed. **A decision is not done until the doc it invalidates is updated.**

Drift is normal and predates AI — details get ironed out in code faster than in the spec, and the
spec is the one artifact with no immediate consumer, so nothing breaks *today* when it goes stale.
What breaks is the next agent, which has no memory and takes the stale doc as truth. On the one
project where this has been measured so far, drifts were faithfully *recorded* and none
*propagated* — capture worked, routing didn't exist. That's thin evidence, and the mechanism is
cheap enough to be worth running anyway. This line is the routing, and `/design-doc sync` is only
the backstop for when it's missed.

**The framework ships the catch.** A `PostToolUse` hook
([`hooks/impact-line-reminder.sh`](hooks/impact-line-reminder.sh)) fires on any edit to a
`decision_log.md` or `RATIFICATION_LOG.md` and nudges for the impact line when it's absent. Scoped by
artifact name (inert everywhere else), non-blocking, and dependency-free (POSIX `sh` + `grep`).
Plugin installs load it from `hooks/hooks.json`; bare-skill installs add it to `settings.json`
(snippet below).

The `docs/build_status.md` skeleton:

```markdown
# Build Status — <project>

Increment: **<name>**
Steps: S1 spec · S2 build · S3 conformance · S4 review · S5 adversarial spec · S6 green · S7 gate
Position: **S7 · Acceptance Gate** (in progress)
Rework count (S2-S4): 0

## Gate legs — S7
- [x] One command green on clean checkout — <date>
- [x] Failure paths triggered — <date>
- [ ] Real-user read — deferred → <name>, <date>

## Log
- <date> — advanced to <step>: <one line>
```

## Install

Paste this into Claude Code:

```text
Install the ship-pipeline skills for me. Clone
  git clone https://github.com/chzylee/ship-pipeline.git ~/repos/ship-pipeline
(or `git -C ~/repos/ship-pipeline pull` if it already exists), then symlink every
directory under ~/repos/ship-pipeline/skills/ into ~/.claude/skills/ (macOS/Linux:
`ln -sfn <skill-dir> ~/.claude/skills/<name>`; Windows: copy the folders instead and
note that updating means re-copying). If a name already exists in ~/.claude/skills/,
replace it only if it is a symlink or an older copy of the same skill — otherwise
list the conflict and skip it. Finish by listing what was installed and remind me to
restart Claude Code so the skills load.
```

Or do it by hand:

```bash
git clone https://github.com/chzylee/ship-pipeline.git ~/repos/ship-pipeline
```

```bash
for s in ~/repos/ship-pipeline/skills/*/; do ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"; done
```

Symlinks mean a `git pull` updates every installed skill in place.

> **Dependency:** `/ratify` and `/ratify-configure` are not in this repo — they live in
> [chzylee/skill-library](https://github.com/chzylee/skill-library) and the pipeline invokes them by
> name at its approval stops. Install them from there (one-skill prompt or the `skill-library`
> plugin — see that repo's README). Without them, approval stops still occur but lose
> prediction-before-reveal and the ownership record.

**The drift-catch hook (bare-skill installs only — plugin mode loads it automatically).** Add this to
`~/.claude/settings.json` (replace the path if you cloned elsewhere):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "sh \"$HOME/repos/ship-pipeline/hooks/impact-line-reminder.sh\"" }
        ]
      }
    ]
  }
}
```

It fires only on `decision_log.md` / `RATIFICATION_LOG.md` edits and is silent everywhere else.

### Plugin mode — namespaced `/ship-pipeline:*`

Paste this into Claude Code:

```text
Install the ship-pipeline plugin: run
  claude plugin marketplace add chzylee/ship-pipeline
then
  claude plugin install ship-pipeline@ship-pipeline
and confirm the skills are available (namespaced, e.g. /ship-pipeline:own-your-code).
```

Or by hand:

```bash
claude plugin marketplace add chzylee/ship-pipeline
```

```bash
claude plugin install ship-pipeline@ship-pipeline
```

## Update

- **Bare-name install:** `git -C ~/repos/ship-pipeline pull` — symlinked skills update instantly.
- **Plugin install:** `claude plugin update ship-pipeline` (every push is a release — versions track
  commits).

## Uninstall

- **Bare-name install:**
  `for s in ~/repos/ship-pipeline/skills/*/; do rm ~/.claude/skills/"$(basename "$s")"; done && rm -rf ~/repos/ship-pipeline`
- **Plugin install:** `claude plugin uninstall ship-pipeline`

## Requirements

Nothing to run: the skills work with a stock Claude Code install, no dependencies or keys. Optional:
`/own-your-code`'s cross-model onboarding read can use a genuinely different-lineage model if a free
`OPENROUTER_API_KEY` or `GEMINI_API_KEY` is present in `~/.secrets/llm.env` — see
[skills/own-your-code/README.md](skills/own-your-code/README.md).

## Known limits

- **Responsibility is not reduced.** This process makes the choices visible enough that
  responsibility is exercisable rather than nominal. It does not transfer any of it.
- **Declaration completeness is not guaranteed.** An agent that does not recognize a decision will
  not declare it. S3 and S5-S7 are the nets; increment sizing is what keeps a miss affordable.
- **Impact is unmodelable.** The system will surface decisions you don't care about and stay quiet
  about ones you do, whenever the reversal picture and the real stakes diverge.
- **Every threshold here is a starting cut, not a calibrated one.**
