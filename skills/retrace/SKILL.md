---
name: retrace
description: 'Produce a RETRACE: a readable account of how an agent actually worked through an increment and why it made the moves it made. Its audience is a developer who wants to learn the reasoning rather than inherit the result — most valuably a newer engineer, and most valuably on work that ran autonomously, where nobody watched it happen. Internal to Ship Pipeline — normally reached by the --retrace flag on /build-and-test or /adversarial-review, which append to one file per increment so the account covers how the thing was built AND how it was fixed; you do not need to invoke it by name to use the pipeline, though you can. It is NON-BINDING BY CONSTRUCTION: optional to read, never a gate, never a source of requirements, and nothing downstream may cite it as authority. It records what happened, including the wrong turns — a retrace that reads like the work went smoothly is a retrace that was rewritten into a summary and has lost the thing it was for. Distinct from /own-your-code, which describes the system as it stands; retraces are the per-increment raw material that consolidation draws on. Triggers on "retrace this increment", "how did the agent build this", "write up how that went", "I want to see the reasoning not the result", or the --retrace flag on either harness. Done when the account is written to docs/retrace/<increment>.md, marked non-binding, and includes the moves that did not work.'
---

# Retrace

Write down **how the work actually went** — the moves, the reasoning behind them, and the turns that
did not pan out.

Not what got built. Not what the system does now. *How an agent got from a spec to a working thing,
and why it chose what it chose along the way.*

## This is supplementary — `/own-your-code` is the document that matters

A retrace is a **learning resource**, not a deliverable. Nobody needs one in order to own a project;
`/own-your-code` is what confers ownership, and a retrace is at most raw material it draws on. The
two are not peers, and a retrace never stands in for the ownership doc.

It is off by default under autonomous runs and opted into at launch. Produce one when it was asked
for, and do not campaign for it otherwise.

## Who this is for

A developer who wants to **learn the reasoning rather than inherit the result.** Most often someone
earlier in their career, reading work they did not do, trying to understand how a problem gets taken
apart — the part that is normally invisible because it happens inside someone else's head or inside
an agent's context window.

Its value is highest on **work that ran on its own.** When an agent builds unattended, the entire
reasoning trace is otherwise thrown away the moment the context closes. The artifact survives; the
thinking does not. This is the only place that thinking gets kept.

## The failure it exists to kill

**The clean narrative.** Work gets written up after the fact as though it proceeded in a straight
line: read the spec, wrote the tests, implemented, done. Every account of building anything reads
this way, and every one of them is useless to learn from, because the straight line is the one thing
that never happens.

What a learner needs is the part that gets edited out: the approach that seemed right and wasn't,
the requirement that turned out to mean something different on second read, the test that passed for
the wrong reason, the point where two options looked equally good and one got picked.

**A retrace with no wrong turns in it has been rewritten into a summary.** If the work genuinely had
none, say that explicitly — it is a surprising claim and it should read as one.

## It binds nothing

This is a property of the document, not a caveat on it.

- **Optional to read.** Nothing is blocked by it going unread.
- **Never a gate.** It does not pass, fail, approve, or hold anything.
- **Never a source of requirements.** A design decision described here is *reported*, not
  *established*. If it belongs in the design, it goes in the design doc — through the normal route,
  not by being written down here.
- **Never cited as authority.** Nothing downstream may point at a retrace to justify a behavior.

Mark it at the top of every file so a reader who arrives cold cannot mistake it for a spec.

## What goes in it

- **The route.** What was done, in the order it was done, at the grain a reader could follow.
- **The why behind each real choice.** Not every keystroke — the moves where something else was
  plausible.
- **The wrong turns**, and what made them look right at the time. This is the highest-value content
  in the document.
- **What the spec did not settle**, and what got picked instead. Where a declaration entry covered
  it, say so; where nothing did, that is worth a reader's attention.
- **Where the checks bit.** A test that caught something, a conformance finding that sent work back,
  an audit finding that exposed a test which would have passed a wrong build.

## What stays out

- Restating what the increment does — that is the design doc's job, and `/own-your-code` for the
  system as a whole.
- Grading the work, the agent, or the design.
- Recommendations. This is an account, not a review.
- Anything that reads as a requirement.

## Voice

Plain and specific. Past tense. Concrete about what was tried.

Write it so someone can follow the reasoning without having the code open, and without needing to
know the codebase already. Name things the way the code names them, and explain a term the first
time it appears.

**Do not dramatize and do not flatten.** A retrace that reads like a war story is as unhelpful as one
that reads like a changelog.

## Where it sits — the handshake

**Upstream:** the record of an increment's work — normally passed by `/build-and-test` or
`/adversarial-review` when invoked with `--retrace`.

**Output:** `docs/retrace/<increment>.md`. **Both harnesses append to the same file** for a given
increment, so one document covers how the thing was built and how it was hardened. Append; never
clobber a prior section.

**Downstream:** a human reader, and `/own-your-code`, which draws on retraces as raw material rather
than re-deriving the same history. Nothing else consumes it and nothing waits on it.

## Scope — hold this line

- **Owns:** the account of how the work went · the reasoning behind the moves · the wrong turns ·
  appending to the increment's retrace file · the non-binding marking.
- **Does NOT:** specify behavior · establish a decision · gate anything · review or grade the work ·
  edit the design doc, the tests, or the code · describe the system as it currently stands.

## Procedure

**1 · Gather the record** of what happened during the span — the moves, the checks, the findings,
the reversals.

**2 · Write the account in order**, at a grain a reader can follow.

**3 · Include the wrong turns** and what made each look right at the time. If there were none, say so
outright.

**4 · Append to `docs/retrace/<increment>.md`** under a heading naming the span (build, or
adversarial review). Do not overwrite what is already there.

**5 · Mark it non-binding** at the top of the file if the marking is not already present.

## The kill rule

**Report the work, do not improve it.** The moment a retrace is tidied into the version of events
that reflects well, it stops being the one artifact that shows a learner what the work actually
looks like — and becomes another clean narrative, which the world already has enough of.
