#!/usr/bin/env sh
# Ship Pipeline — write-time drift catch.
#
# Fires on every Edit/Write, but only acts on the two ship-pipeline decision
# artifacts. When a decision is recorded WITHOUT a `design-doc impact:` line, it
# reminds the model to add one — the write-time routing that keeps a recorded
# decision from silently rotting the design doc it contradicts.
#
# Harvested from the Runway v1 sync (2026-07-23): 14 drifts were all faithfully
# recorded in the decision log and NONE propagated to the design doc, because
# nothing routed them. This line is the routing. It is a NUDGE, never a wall —
# it never blocks a write.
#
# Portable POSIX sh; parses the raw hook payload with grep (no jq / no python),
# so it runs in Git Bash on Windows and any POSIX shell on macOS/Linux.

input=$(cat)

# Only the two ship-pipeline decision artifacts. Anything else: stay silent.
echo "$input" | grep -qE '"file_path"[^,}]*(decision_log\.md|RATIFICATION_LOG\.md)' || exit 0

# If the change already carries the impact line, the convention is being kept.
echo "$input" | grep -qi 'design-doc impact' && exit 0

# Otherwise nudge — non-blocking, model-visible, actionable. exit 0 never blocks.
cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Ship Pipeline drift catch: this decision_log / RATIFICATION_LOG entry has no `design-doc impact:` line. A decision is not done until the doc it invalidates is updated — add `design-doc impact: none`, or name the design unit/section it changes. If it changed the design, propagate it now (or run /design-doc sync). This is the write-time catch; sync is only the backstop."}}
JSON
exit 0
