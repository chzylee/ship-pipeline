---
name: declare
description: 'Read a design doc COLD — holding that document and nothing else — and enumerate every decision you would have to make in order to execute it. Produces the DECLARATION: one closed five-field entry per decision (decision, options, taking, reversal, unknowns), plus the entry count. This is the mechanical form of the question the whole pipeline turns on: a spec that produces a short declaration from a reader who was not in the room is specific; one that produces a long declaration is not. Internal to Ship Pipeline — normally reached by /design-doc at S1, before the owner''s approval; you do not need to invoke it by name to use the pipeline, though you can. It enumerates and NEVER decides: it does not edit the doc, does not answer its own questions, does not build, and never labels a decision minor, major, or significant. Triggers on "declare against this spec", "what would you have to decide to build this", "run the declaration", "cold-read this design doc", or reaching the pre-approval step of S1. Done when every decision carries all five fields and no sixth, and the entry count has been reported.'
---

# Declare

Read a design doc as the person who has to execute it, and say **what you would have to choose**.

You are not reviewing the doc. You are not improving it. You are answering one question, honestly
and in full: *to build this, what would I have to decide that this document does not decide for me?*

## The failure it exists to kill

**The decision that surfaces in code review.** An agent builds from a spec, hits a hundred places
the spec is silent, picks its way through all of them, and ships. The owner sees the result and
learns — too late, with the code already depending on it — that three of those picks were theirs to
make. Nobody hid anything. The decisions were simply never said out loud while saying them was
still cheap.

A well-specified agent and a guessing agent report identical confidence. Neither can tell you which
one it is. But both can list what they would have to choose, and that list is the difference.

## The one constraint that makes this work: you must be cold

**You hold the design doc and nothing else.** No session history. No transcript of how it was
written. No memory of what anyone meant. If you have any of that, you are the wrong agent for this
and you should say so rather than proceed.

This is not ceremony. Obviousness is a property of having been in the room, not of the text. An
author reading their own spec cannot find the gaps, because every gap is filled in their head
before they reach it. A cold read is the only instrument that tests whether the **document** carries
the meaning.

## What "done" is here

Every decision you would have to make is written as one entry, five fields, no sixth. The entry
count is stated. Nothing else is required of you and nothing else is permitted.

**Success test.** An owner reads your declaration and can say: *that one is mine, I want it ruled;
those are yours, take them.* If they finish reading and cannot tell which is which, the entries were
too vague — not too few.

## The entry — CLOSED

Any field beyond these five is a fork to `docs/decision_log.md`, not something you add.

```
decision:  what you would have to choose
options:   what you would be choosing between
taking:    which you would take absent a ruling — always name one
reversal:  in plain language, what undoing this looks like if it turns out wrong,
           including anything that would already have escaped by then
           (data written, calls made, files handed to someone)
unknowns:  context you believe you lack and would want before deciding;
           empty when you have none
```

### On `taking`
Always name one. "It depends" is not an answer — you would in fact pick something, and saying which
is the entire value of the entry. A declaration that declines to state its lean has told the owner
nothing they can rule on.

### On `reversal`
You usually run **before the code exists** — so estimate this from what executing the spec *would*
produce, plus the existing codebase where there is one. Be concrete. Three things are estimable and
you should estimate them:
- **spread** — how many places would depend on this choice
- **escape** — whether anything would have left the system before anyone noticed (data written to a
  store, a message sent, a file produced someone else now holds)
- **lock-in** — whether other choices follow from this one

Write it as what a person would have to *do*, not as an adjective. "Rename a field in two files"
beats "low cost." "Rewrite the sync layer and migrate every row already written" beats "expensive."

### On `unknowns`
Say what you would want to know and cannot find in the document. Leave it empty when the document
answers you. This field is for what you lack — not for what you suspect, dislike, or would design
differently.

### There is no sixth field
**Never label a decision minor, major, significant, high-priority, or low-risk.** You cannot know.
Significance depends on impact on how the thing gets used, and that is a property of what the owner
values — it exists nowhere in the code and nowhere in the doc. You can report what reversing costs.
You cannot report what it matters. An entry that carries a significance label has taken a judgment
that is not yours, and it is worse than no entry, because the owner may believe it.

## What counts as a decision

Include it if choosing differently would **leave an observable trace**: different behavior,
different output, a name someone reads, a dependency added, a file or record written, a shape
another part of the system has to match.

Exclude what leaves no trace — a loop variable, the order of two independent statements, formatting
a linter settles.

When you genuinely cannot tell which side of that line something falls on, **include it.** A short
entry costs a sentence to read.

## Where it sits — the handshake

**Upstream:** an increment design doc, dispatched by `/design-doc` at S1 before the owner's
approval stop. It may also be run directly against any design doc.

**Downstream:** the owner, who reads the declaration and rules. Then `/design-doc`'s scope check,
which reads your **entry count** as its mechanical detector — which is why the count is stated
plainly and not left to be counted by hand.

## Scope — hold this line

- **Owns:** reading the doc cold · enumerating decisions · the five fields · the entry count.
- **Does NOT:** edit the design doc (a gap is an entry, never a patch) · answer its own questions ·
  recommend what the owner should rule · write code or tests · **rank or score entries by
  importance** · assess whether the doc is good · report confidence in its own completeness.

Emit entries in the order the doc raises them. Downstream may re-order them by reversal cost, which
is readable from the code — that is a different operation from ranking by importance, and it is not
yours to perform.

## Procedure

**1 · Confirm you are cold.** State that you hold the doc and nothing else. If you have session
context about how this doc was written, stop and say so — the result would be worthless and
falsely reassuring.

**2 · Read the whole doc once, as the executor.** Not as an editor. At every sentence, ask what you
would actually type next if you had to act on it.

**3 · Walk it again and mark every place you would have to pick.** Requirements, contracts, error
paths, boundaries the doc names but does not cross, and anything the doc calls closed that your
build would need to extend.

**4 · Write each as an entry.** Five fields. Concrete `taking`. Concrete `reversal`. `unknowns` only
where you actually lack something.

**5 · State the count.** One line, plainly: `N entries.`

**6 · Stop.** Do not summarize what you think it means. Do not tell the owner which ones matter.

## The kill rule

**Enumerate; never decide, never rank.** The moment you tell the owner which decisions are
important, you have taken the one judgment this entire mechanism exists to keep with them — and you
have taken it from behind a document that looks like transparency.
