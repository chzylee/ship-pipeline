---
name: auto-build
description: 'Run an entire increment from S1 to S7 without stopping — for overnight runs and any increment the owner elects to be out of. It takes ANY increment design doc; it does not require one written for it, because the doc carries no mode and no skill downstream of it branches on how the work is supervised. Nothing halts: a decision that would normally stop the run is picked, logged, and carried, because the election to run autonomously IS the ruling to continue. Everything the owner would have ruled on comes back at the end as ONE reviewable batch — the declaration, the conformance and audit findings, every mid-run pick, the skip list, and the gate''s human legs, which are deferred rather than skipped because a check''s value is that it ran. The batch has one job and it is not a rubber-stamp veto: each entry is a PROPOSED AMENDMENT TO THE DESIGN DOC, so the doc ends up explaining what was actually built and can guide the next build. Rejecting a decision the finished code already depends on is not a choice anyone can exercise — it IS the rework this pipeline exists to prevent — so where a pick is bad and embedded, the skill names the rework cost from its recorded reversal picture and calls it rework. It MAY report that a spec looks thin to run unsupervised; that report informs and NEVER refuses, because a system that can override the owner''s accepted risk has taken authority it does not have. Tier 1: one of the five skills that make up using Ship Pipeline. Accepts --retrace, and recording is worth more here than anywhere else, since nobody watched the work happen. Triggers on "build this autonomously", "run this overnight", "auto-build X", "do the whole increment without me", or an explicit election to be out of the loop. Done when the increment has passed through S1-S7 and every decision it made sits in one batch as a proposed design-doc amendment the owner rules on.'
---

# Auto Build

Run one increment end to end — S1 through S7 — with nobody in the room.

For overnight runs, and for any increment the owner has decided not to sit through. It composes the
whole pipeline:

```
S1  /design-doc → declare        spec it, enumerate the decisions
S2  /build-and-test              red-first, audit concurrently
S3    ↳ conformance              check it both directions
S4    (batched, not skipped)
S5  /adversarial-review          spec the holes
S6    ↳ /finish-build            drive to green
S7    ↳ /acceptance-gate         prove the checklist
```

## Your input is a spec — you never write one

**This skill takes an approved increment design doc and runs the build process against it.** It does
not derive the design, and it does not author scope.

That boundary is the reason the whole thing is legitimate. Delegating execution is a decision the
owner signs by invoking this skill against a spec they read. Delegating the *design* would mean an
agent deciding overnight what gets built — and there would be nothing the owner had approved for the
work to be checked against, which is the one thing this pipeline is for.

If no design doc exists, say so and stop. Getting to a design doc is upstream work, and the owner may
do it with `/design-doc` or with anything else; this skill starts once it exists.

## The doc carries no mode, and neither do you

**You accept any increment design doc.** There is no such thing as a doc written *for* autonomous
execution — the artifact records no mode, nothing reads a mode off an artifact, and no skill will ask
you for one.

What a skill beneath you *may* do is present differently when a ruling has to be deferred rather than
taken live — `/acceptance-gate`'s human legs become batch entries under you. That is presentation,
not a different artifact and not a different standard. Every check still runs and every input is the
same one any other caller would supply.

Mode is carried by *you*, the composite being invoked. That is the whole mechanism: **the owner
chose autonomy by running this skill**, and every skill beneath you behaves exactly as it always
does.

## Nothing halts

Normally, a decision surfacing after the owner has signed stops the increment and goes back to them.
Here it does not.

**The election to run autonomously is the ruling to continue.** When you hit a decision — declared
or not — you pick, you log it, and you carry on. The ruling still happens; it happens at the end,
in the batch.

Log every pick in declaration form: what you chose, what the options were, what you took, what
reversing it would look like including anything that already escaped, and what context you lacked.
That is what makes the batch reviewable rather than a summary.

## Standing in for the owner — one proxy, plus one cold check

Four places in a run would normally ask the owner something: **S1** (is this spec good enough to
build from), **S4** (conformance found unspecced work — keep it or cut it), **S5** (which failure
modes we protect against, and which we deliberately do not), and **S7 leg 5** (do these tests
actually check anything real). Leg 6 — a real person using the thing — cannot be simulated by
anything and stays outstanding.

**S1, S4, and S5 are judgment. One proxy agent carries all three.**

These take the owner's values as their input. There is no right answer sitting there to be found —
there is a standard to apply, and the thing that matters is applying it consistently rather than
contradicting at S5 what was accepted at S1. That is what a person does, and it needs continuity, so
it is one agent across the run and not three.

**S7 leg 5 is verification. A fresh agent does it.**

"Do these assertions check anything real" has a right answer, and being cold is what finds it. The
proxy cannot do this one: by S7 it approved the spec these tests came from and has a stake in that
approval holding up — and having read the whole run, nothing in it looks surprising to it anymore.
That is precisely the blindness a cold reader exists to cure. Dispatch a separate agent that holds
the test diff and the spec and none of the run.

Record every proxy ruling in declaration form. **The proxy's calls are a first pass, not a verdict** —
they land in the batch and the owner rules on them there.

## The batch, and what it is actually for

A run this long makes decisions the owner did not see made. Handing those back as a list to approve
or reject after the fact would be theatre — by then the code depends on them, and rejecting one *is*
"go back and make a ton of changes," which is the exact failure this whole pipeline exists to
prevent. Offering a choice the owner cannot actually exercise is worse than offering none.

**So the batch has one job: bring the design doc up to date with what was decided, so the doc
explains what is being built and can guide the next build.** Every entry is presented as a **proposed
amendment to the increment design doc** — the decision, and the sentence the doc should now carry.
The owner rules amendment by amendment. What they are ruling is *what the spec says from here*, which
is a decision they can genuinely make, rather than a rollback they cannot.

Assemble:

- the **declaration** from `declare`, and every decision that surfaced after it
- every **mid-run pick**, in declaration form, each with the doc amendment it implies
- the **conformance findings** — creep and gap, kept separate. Creep is the sharpest input here: it
  is either scope the doc should now state, or code that should come out.
- the **audit findings** — which tests would not have caught a wrong build
- the **rework count** from S2-S4
- the **skip list** from S5 — every case the run decided not to protect against
- the **gate's human legs**, outstanding, with what each still needs

**A composite that hides its decisions is ok-clicking at a higher altitude.** If this skill returns
"done, all green," it has defeated the transparency the pipeline is built to produce, from behind an
artifact that looks like rigor. Return the batch. Always. Including when everything went well.

**Where a pick is genuinely bad and the code already depends on it, say so plainly** — name what
undoing it costs, using the reversal picture already recorded. Do not present that as a veto. It is
a rework decision, and the owner deserves to see it labelled as one.

## The human legs are deferred, never waived

`/acceptance-gate`'s owner spot-trace and real-user read cannot be performed by any agent. They do
not disappear because nobody was watching.

**They run as far as they can and then wait.** Everything mechanical executes; everything needing a
person is recorded as outstanding and lands in the batch. Never mark a human leg passed because
there was no one there to fail it — a check's value is that it ran, and skipping one destroys that
value while deferring its ruling keeps it.

## You may warn. You may not refuse.

If the spec looks thin to run unsupervised — the declaration is long, entries carry heavy reversal
pictures, `unknowns` fields keep coming back full — **say so, plainly, before you start.**

That report is the declaration's `unknowns` field read one level up: the same mechanism at composite
altitude, not a second one.

**Then run anyway if the owner said to run.** The owner may elect autonomy and knowingly accept the
risk, and you do not override that election. A system that can refuse the owner's accepted risk has
taken authority it does not have. Every mechanism here informs a choice. None of them may make one.

## What "done" is here

The increment has passed through S1-S7, and **every decision the run made sits in one batch as a
proposed design-doc amendment the owner rules on.**

Not "the increment shipped." Not "everything passed." Done is that the work happened, nothing that
needed a person got quietly resolved without one, and the design doc can be brought back into
agreement with what actually exists.

## Options

`--retrace` · **off by default here, and never asked about.** Prompting for it mid-run would defeat
the point of an unattended run, so it is set at launch or not at all.

A retrace is a **learning resource** — supplementary material, not a deliverable of the run. It costs
space and produces something nobody needs in order to own the result. Default to not producing it.
Pass the flag when you specifically want the account of how the work went.

**`/own-your-code` is the document that matters.** It is what confers ownership; a retrace is raw
material it may draw on. Do not treat the two as peers, and never let a retrace stand in for the
ownership doc.

## Scope — hold this line

- **Owns:** sequencing S1-S7 without halting · logging every pick in declaration form · assembling
  and presenting the batch · deferring the human legs · reporting a thin spec before starting.
- **Does NOT:** refuse to run · skip a check because nobody is watching · mark a human leg passed ·
  return a summary in place of the batch · decide anything the batch does not surface · relax any
  step's own rules because the run is autonomous.

## Procedure

**0 · Read the doc and report.** If the spec looks thin for unsupervised execution, say so now, with
specifics. Then proceed.

**1 · S1.** Read the increment design doc. **You do not derive one** — see *Your input is a spec*
above. Dispatch `declare`. Record the declaration whole; it opens the batch.

**2 · S2-S4.** Run `/build-and-test`. Red-first gate, `audit-tests` concurrently, `conformance` after,
both in separate fresh contexts. Collect the findings rather than presenting them. Count rework.

**3 · S5-S7.** Run `/adversarial-review`. At each of its halts, rule and log rather than stop.
`/finish-build` forks get picked and recorded. `/acceptance-gate` runs its mechanical legs and defers
its human ones.

**4 · Assemble the batch.** Every item above, in one document, each in a form the owner can act on.
Order by reversal weight — what escaped, what locks other things in, what spread — never by your
guess at importance.

**5 · Return it and stop.** Do not recommend what the owner should accept.

## The kill rule

**Autonomy is about who is present, not about what gets checked.** Every check still runs, every
decision still gets recorded, every human leg still gets its person eventually. The moment this skill
starts trading rigor for the fact that nobody is looking, it becomes the exact failure the pipeline
exists to prevent — arriving faster and with a green light attached.
