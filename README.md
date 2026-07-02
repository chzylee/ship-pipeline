# Ship Pipeline

**A guided build process that keeps senior-engineer ownership in LLM-speed development.**

LLMs hand you build velocity; what they quietly take is the act of coding itself — and with
it the things seniority is made of: knowing why every decision was made, what "done" actually
means, whether the build honors the design, and being able to defend and evolve the result.
Skip those and you ship faster right up until you can't support, explain, or grow what you
shipped.

Ship Pipeline is that seniority, put back in as **process**. It guides a build from design
through shipping with clarity on what's going on at every stage, and it generates the
documentation as it goes — so you (or anyone below staff-level expertise, or anyone who just
didn't type the code) can build at LLM speed **and own the result**: every deliverable is
paired with a verifier that binds it to its source, "done" is a command that passes rather
than a feeling, and the trail it leaves is the onboarding a teammate could pick up cold.

## The pipeline

| # | Stage | What it produces | What verifies it |
|---|-------|------------------|------------------|
| ▸ | Scout — find what to build | a Build Brief: what to build + first user | Reality Probe: a 30-min pre-code test + kill criterion |
| 0 | Scope Gate | the one job, definition of done, not-in-v0 list | segment / one-job / kill criteria |
| 1 | Design Doc | the canonical spec everything traces to | design review |
| 2 | Build Prompt | the paste-ready builder prompt | cross-model cold read (or a two-build bake-off) |
| — | *the build* | AI implements | — |
| 3 | Build Review | code ↔ design reconciliation | fresh judge: six checks → judgment + blockers |
| 4 | Test Spec | what must be tested, every item anchored | traces to the design doc, bounded by not-in-scope |
| 5 | Acceptance Gate | the one green command that IS "done" | failure paths triggered and read as the user |
| 6 | Own Your Code | onboarding that confers ownership | re-derive a decision cold |

You can enter at any stage — each skill establishes the handshake with the stage before it. The
`▸` front door (`/scout`) is optional: start there when you don't have an idea yet; otherwise begin
at the Scope Gate.

## Skills

Skills are forged from real ships and land here as they prove out — this repo is harvested,
not built ahead.

| Skill | Status |
|-------|--------|
| `/scout` | **Available** (v2.0) — the front door: inverted office-hours that discovers what to build from a person + their real work → a Build Brief |
| `/own-your-code` | **Available** (v2.0) — turn an AI-built repo into an onboarding that confers ownership |
| `/test-spec` | Forged on a real ship; migrating into this repo |
| `/build-prompt` | Next up — turn a design doc into a hardened builder prompt |
| `/build-review`, `/acceptance-gate`, `/bake-off`, `/current-state` | Being harvested |

## Install

Two ways to install. The **default gives skills their bare names** (`/own-your-code`) —
cleaner to use day to day. Plugin mode namespaces them (`/ship-pipeline:own-your-code`) —
choose it if you prefer skills indexed under the suite's name or want plugin-manager
updates.

### Default — bare skill names (30-second install)

Paste this into Claude Code:

```text
Install ship-pipeline: run
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
for s in ~/repos/ship-pipeline/skills/*/; do
  ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"
done
```

Symlinks mean a `git pull` updates every installed skill in place.

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
claude plugin install ship-pipeline@ship-pipeline
```

## Update

- **Bare-name install:** `git -C ~/repos/ship-pipeline pull` — symlinked skills update
  instantly. Or paste: *"Update ship-pipeline: git -C ~/repos/ship-pipeline pull, then tell
  me what changed."*
- **Plugin install:** `claude plugin update ship-pipeline` (every push to this repo is a
  release — versions track commits).

## Uninstall

- **Bare-name install:** remove the symlinks and the clone:
  `for s in ~/repos/ship-pipeline/skills/*/; do rm ~/.claude/skills/"$(basename "$s")"; done && rm -rf ~/repos/ship-pipeline`
- **Plugin install:** `claude plugin uninstall ship-pipeline`

## Requirements

Nothing to run: the skills work with a stock Claude Code install, no dependencies or keys.
Optional: `/own-your-code`'s cross-model onboarding read can use a genuinely
different-lineage model if a free `OPENROUTER_API_KEY` or `GEMINI_API_KEY` is present in
`~/.secrets/llm.env` — see [skills/own-your-code/README.md](skills/own-your-code/README.md).
