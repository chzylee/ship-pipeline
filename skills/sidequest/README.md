# /sidequest

**Experimental v0.1.0** — drafted ahead of its first proven run (graduates per the suite's
harvest rule after the first sourced-and-shipped sidequest).

The autonomous half of the Ship Pipeline's ▸ Sourcing stage. /scout discovers main-lane builds
by interviewing a person; /sidequest mines the owner's own exhaust (work log, transcripts, git)
for **low-ownership-requirement** candidates — builds Claude Code can run autonomously
end-to-end because the owner never needs to defend the internals — screens them with the
**black-box test**, shapes them for low maintenance, and emits launch-ready autonomous build
briefs into a Notion stockpile ("Sidequest Projects").

## Invoke

- **"find me a sidequest" / "sidequest scan" / "stock the sidequest pile"** — mine + screen +
  stockpile (max 2 candidates per scan; zero is a valid result).
- **"sidequest this idea ..."** — screen one supplied idea against the black-box test.
- **A greenlight on a candidate** — seeded repo + committed BUILD_BRIEF.md + paste-ready
  launch prompt for the autonomous run.

## Requirements

None hard. Notion MCP recommended (stockpile + work-log mining); degrades to local markdown
briefs without it. Install like the rest of the suite (see the repo README); on Windows,
bare-name installs are copies — re-copy after updates.
