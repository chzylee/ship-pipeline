# Ratification Log — Ship Pipeline

Prediction-before-reveal at every blocking stop. `predicted` / `surprised` / `no-opinion` grade the
**owner's** anticipation of the recommendation, not whether the ruling was right. `surprised`
matters most: it means the owner would have built something else.

---

## Derive session — project design doc · 2026-08-13/14

### 1 · The one job — `predicted`
**Fork:** two core problems named (scoping judgment chunks · verifying specificity) — co-equal, or
one in service of the other?
**Owner:** *"the core mechanic is determining if the agent has enough specificity to confidently
claim it has the instructions to execute with minimal need for decisions that affect the build
significantly."*
**Recommendation:** the same — specificity is the job; chunking falls out of it.
**Consequence:** chunking demoted from core job to derived concern. v1 has one centerpiece.
`design-doc impact:` JOB, section 3

### 2 · What makes a decision significant — `predicted`
**Fork:** defensibility (the wiki's existing criterion) vs. cost to reverse.
**Owner:** cost to reverse. Naming is trivial (find-and-replace); database or framework is huge;
factory-vs-builder is ambiguous.
**Gap worked:** *reverse what?* — reversal cost measures changing the code, missing the case where
the code change is one line and the consequences are already loose.
**Consequence:** significance counts consequences, not just code. The owner's hedge on
factory-vs-builder exposed that reversal cost is a function of spread, not of the decision itself.
`design-doc impact:` A-2, A-4, A-5

### 3 · Who issues the readiness verdict — `surprised` (miscut fork)
**Fork as posed:** three mechanisms for producing a readiness signal.
**Owner:** *"Human must approve... It's like signing an agent's contract for work. Even if the
verdict is 'you, the agent, decides' that is up to the human to decide."*
**Why surprised:** the fork conflated two layers — who holds authority vs. what evidence earns the
signature. The owner separated them. Authority is settled and non-delegable; evidence became a
cleaner, still-open question answered at stop 7.
**Consequence:** delegation is itself a signed decision, which is what makes the auto-rule policy
legitimate rather than a loophole.
`design-doc impact:` R-7, R-8

### 4 · Is the declaration ever complete — `no-opinion` → resolved by default
Asked twice; answered twice with structure rather than a ruling, consistently implying the same
answer. Written as `Q-4 DEFAULT` rather than banked as a ruling: signing attests that the
significant items on the list are ruled correctly, not that the list is complete.
`design-doc impact:` Known limits; A-9

### 5 · Does the build loop repeat per increment — reframed by owner
**Asked:** is S2-S4 an increment loop?
**Owner:** it is a *rework* loop, fired by insufficient agent work, and its ideal count is zero.
**Consequence:** two loop kinds with opposite polarity were separated, and rework count became the
spec-quality metric — a countable read on the one job.
`design-doc impact:` A-7, R-15

### 6 · Two doc tiers or three — `predicted`
**Fork:** does a multi-increment feature get a binding doc above its increments?
**Owner:** two tiers. *"These are theoretically composable; however, building composability into
the system gets too messy very quickly."* Grouping stays a human planning activity the system
does not model.
**Consequence:** `/build-plan` has no remaining job and dissolves — a reversal of the prior
session's roster, surfaced rather than dropped quietly.
`design-doc impact:` A-10, A-11, Not in scope

### 7 · What happens to an undeclared decision — `surprised` (recommendation was internally inconsistent)
**Owner:** *"significant issues are like high severity outages: full stop... however severity is
again decided by both impact to usage and complexity to reverse... an agent cannot make an
assertion about how much the user can handle... the way to reduce failure opportunity is
transparency: here's the decision, in simple terms here's what reversing it would look like."*
**Why surprised:** the ratified A-5 had the agent tagging declared decisions significant-or-not,
which contradicted the authority invariant from stop 3. The owner caught it. Severity split into
two axes, one of which is unreadable from code.
**Consequence:** declarations carry a reversal picture and no significance label. The
carry/escalate/revert trichotomy dissolved — the same transparency mechanism fires late.
`design-doc impact:` A-1, A-3, R-10, R-11, C-1

### 8 · How far to trust tests the building agent writes — owner ruled beyond the recommendation
**Recommendation leaned:** the cheaper option — have the fresh agent audit the tests.
**Owner:** red-first. *"if the building agent writes tests first to ensure they fail and then
builds, that's good verification kinda like tdd. even if its rough, the agent evaluating the build
against design doc after helps keep things in check. that loop is totally autonomous."*
**Consequence:** S2 is red-first; rough rigor is explicitly tolerated because S3 backstops it. The
autonomous span (S2-S3) became explicit, which is what the speed claim rests on.
`design-doc impact:` R-3, R-4, R-2, A-6, Known limits

### 9 · Concurrent test audit — owner-initiated, no prediction stop
**Owner:** *"the fresh review agent can audit the tests while building agent builds... making sure
fresh eyes the build will be evaluated well after its built, and then review agent reviews again."*
**Closes:** red-first proves a test can fail, not that it fails for the right reason. A tautological
test survives red-first. Nothing previously caught that.
**Open sub-question:** whether the auditing and conformance passes use the same agent. Recommended
two, because an agent that approved the tests has a stake in them being adequate — the exact
contamination fresh-eyes exists to prevent.
`design-doc impact:` R-16, Not in scope (parallelism)

### 10 · `/build-plan` reworked into `/retrace` — owner-initiated, no prediction stop
**Owner:** *"a skill reviewing the plan the build agent followed... so a human developer can
optionally read back if they want to learn why the agent worked... valuable for a newer engineer."*
**Consequence:** the skill dissolved at stop 6 returns with a retrospective job. Renamed because
there is no plan in it. Non-binding by construction; per-increment retraces are the raw material
`/own-your-code` consolidates, rather than both re-deriving the same history.
`design-doc impact:` R-17, C-2, glossary

### 11 · Two fresh agents, not one — `predicted`
Owner confirmed the recommendation: the auditing and conformance passes use distinct agents,
because an agent that approved the tests has a stake in their adequacy.
`design-doc impact:` R-4, R-16

### 12 · Skill granularity and the composition layer — owner-initiated
**Owner:** *"1 repeatable action = 1 skill. This pipeline itself is the orchestration of skills
whether manual/auto. You can always automate composition of skills optionally."* And on driving the
loop: *"by virtue of their existence a user can choose to automate however they want... it comes
down to user choice."*
**Derived, not stated (flagged to owner):** a composite that spans an approval point must still
surface what it passed through, or delegation-as-approval hollows out R-7.
`design-doc impact:` A-12, A-13, A-14, A-16

### 13 · The harness, subagents, and autonomous sovereignty — owner-initiated
**Owner, on S2:** *"this shouldn't be a skill to 'start the build' but to 'ensure building occurs
within this test/review automation framework'"* — converting R-3/R-4/R-16 from protocol into
mechanism. Orchestration dispatches subagents to do the work.
**Owner, on halting:** *"halt and wait should never be strictly gated because we need user
sovereignty... that's a choice I should be allowed to make if I want and knowingly accept
responsibility for risk."*
**Consequence:** the R-11 conflict with autonomous mode resolves — the election to run autonomously
IS the ruling to continue. Sovereignty turns out to be R-7 read from the other side: a system that
can refuse the owner's accepted risk has taken authority it does not have.
**Derived, not stated (flagged to owner):** `/auto-build` requires its increment design doc to have
been derived in unattended mode, since a spec written for a reviewer who will not be there is a
category error. **Later overturned — see stop 16.**
`design-doc impact:` R-11, R-18, R-19, A-15, A-16, A-17

---

## v1 scoping session · 2026-08-15

Closes Q-1 and produces `docs/design/v1-roster-rework.md`. Grades marked `— (ungraded)` are awaiting
the owner's read; they are the stops where a recommendation was on the table.

### 14 · What makes v1 done — `— (ungraded)`, owner ruled against the recommendation
**Fork:** v1 is done when (A) the spine runs once on a real project · (B) the roster ships ·
(C) Ship Pipeline is self-hosting.
**Recommendation:** A, with C as method rather than criterion.
**Owner:** B. *"i dont think ship pipeline needs to be built with ship pipeline because i think that
level of testing is overkill for something that might even be better experimentally tested."* The
driver is increasing the automated work the owner can do for themselves.
**Consequence:** v1 is the full roster, validated experimentally by use rather than by self-hosting.
`design-doc impact:` Q-1

### 15 · Delivery ordering — dissolved by owner (fork was miscut)
**Asked:** single delivery vs. usable-early ordering.
**Owner:** neither — *"skills should minimally assume things about the caller… dont make me spend
more time than i need because you assume something of me."* Autonomous mode is not required and not
privileged; the outcome is invariant either way.
**Consequence:** the question presumed v1 should assume a usage pattern. It should not.
`design-doc impact:` none (dissolved)

### 16 · Where mode lives — dissolved by owner
**Asked:** per-invocation argument · a field in the doc · ambient run-state.
**Owner:** none of them. *"i dont think modes need to live anywhere… every individual piece of the
process has input and output agnostic to world outside it."* Clean architecture: the artifact is the
interface, and `/auto-build` is the outer layer that carries the mode.
**Later clarified by owner:** modes still guide the *session* — they suggest where to pay special
attention while producing a deliverable. What they may never do is change what the artifact contains.
**Consequence:** R-19's hard PRECONDITION (stop 13) is overturned. `/design-doc` keeps both press
modes; the doc records none. Derivable from A-13 — invoking the composite IS the mode.
`design-doc impact:` R-19

### 17 · Contract-first vs contract-by-use — `— (ungraded)`, recommendation taken
**Fork:** fix the artifact contract in its own increment · let it emerge from use · ship it with its
producer.
**Owner:** C — with the producer. Rationale added: skills are functions, a spec is a clear input.
**Consequence:** `/design-doc`'s rework is the first thing built; everything downstream reads a
contract that demonstrably exists.
`design-doc impact:` Q-1

### 18 · What shapes a composite — owner-initiated
**Owner:** *"those should be grouped by stage of the process from human point of view in the interest
of a smooth ux."* Plus the bar: usage describable simply, simplicity as an asset, the strength being
orchestrated verification baked in.
**Consequence:** A-12/A-13/A-16 established that composites exist and split two ways. Nothing said
what a composite may be *shaped by*. Now it does.
`design-doc impact:` A-18

### 19 · The roster is tiered by audience — owner-initiated
**Owner:** tier 1 is what a user invokes and the whole of what they must learn; tier 2 is the
machinery, callable but never required knowledge.
**Consequence:** tier 1 lands at five skills. Tiering is carried in the skill description, not the
directory, so direct invocation still works.
`design-doc impact:` A-20

### 20 · Is chaining the gate a risk — owner raised the hedge, resolved against it
**Owner:** `/acceptance-gate` belongs in tier 2 and should run automatically after `/finish-build`
*"unless this potentially adds problems instead of helping accountability."*
**Resolution:** no problem — the gate is self-blocking by construction; it never passes a human leg
on anyone's behalf. Chaining automates the invocation, not the verdict. Under `/auto-build` the human
legs become batch entries rather than being disabled, because a check's value is that it ran (A-8).
**Consequence:** `/adversarial-review` sequences S5-S7 as one tier-1 entry; two of the owner's four
touchpoints live inside it and both still halt.
`design-doc impact:` A-14, A-18

### 21 · Naming — owner ruled twice
**Owner:** `/build-and-test` for the S2-S4 harness. Then rejected `/harden` and `/attack-and-gate`
for the S5-S7 composite: *"the goal isnt to break things its to check against design and not let
silly errors slip past."* Settled on `/adversarial-review`.
**Flagged in return:** "check against design" is S3's job; S5-S7's subject is what the design never
decided. Written into the skill so it does not duplicate `conformance`.
`design-doc impact:` none (naming)

### 22 · What `declare` is for — owner reframed; recommendation overreached
**Recommendation:** `declare` must be a *different agent from the builder*, by the contamination
argument that produced R-16.
**Owner:** *"is declare its own skill to give builder agent a clear interface for elucidating the
plan it will take to build?"*
**Correction:** the owner's reading is closer to R-9 — declaring is enumeration, not verification,
and §8 already holds that agents enumerate more reliably than they self-assess. The real constraint
is **fresh context**, not a different agent: an agent carrying the derive session tests the session,
not the document.
`design-doc impact:` none (R-9 unchanged; clarified in the skill)

### 23 · Doc granularity for the v1 rework — `— (ungraded)`, recommendation taken
**Fork:** one doc · one per skill · one doc structured by skill.
**Owner:** C. *"the rework is low complexity overall. we are defining the shape here and the actual
skills themselves are somewhat of what i've been doing to prompt builds in this way already but
stripped to the process that's project independent."*
`design-doc impact:` Q-1

### 24 · Skills cite nothing project-specific — owner-initiated
**Owner:** *"the skills themselves are the wrong place to be citing specific things… specific risks
over specificity."*
**Consequence:** three Runway v1 citations in `/design-doc` genericized to the pattern they
demonstrate. Sits alongside A-19: a skill gets what it needs to do its job, and no more.
`design-doc impact:` A-19 (applied)

### 25 · The scope check is about reversal, not count — owner-initiated
**Owner:** a number is *"good as a warning to ask user"* but sizing is complexity and reversibility,
and *"the best way to do so is to elucidate what may need to be reversed if things go wrong."*
**Consequence:** the scope check's substantive read is now surfacing the heaviest `reversal` pictures
— ordered by escape, then lock-in, then spread, all readable from code (A-2) — and never presented as
a ranking of importance (A-3). The entry count demoted to a prompt to ask.
`design-doc impact:` R-13, R-14 (applied in skill)

### 26 · The re-entry lens replaces maintainability/UX/cost — owner-initiated
**Owner:** *"own-your-code is ideally for enabling someone to comfortably step back in and own a
project. it should theoretically be able to produce the same from an existing project. that's the
bar. ranking should correspond to that."*
**Closes:** an A-3 violation that had survived three prior versions — the old lens asked the agent to
rank decisions by impact on use, which is precisely the judgment A-3 says exists nowhere in the code.
**Consequence:** ranking is now **reconstruct / reach / surprise** — can the why be re-derived from
the source, how much else assumes it, would a competent reader guess wrong. All readable; none
estimate what the owner values. The decisions index lost its significance column. Working on any
project, with pipeline artifacts as optional inputs, became a stated constraint.
`design-doc impact:` A-3 (applied in skill)

---

## Review-and-fix loop · 2026-08-15

Three independent agents reviewed the built roster. The third — a fresh cold read by a different
model, asked to execute the skills literally rather than audit them — found eight blocking defects.
The rulings below closed them.

### 27 · The harness dispatches the build agent — owner-initiated, closes a BLOCKING defect
**Found:** R-18's "not to start a build," taken literally, left the pipeline's central skill waiting
forever for a builder that nothing in the roster launches. The same hole existed at S5 for the
adversarial tests. Every other execution defect was downstream of it.
**Owner:** *"the harness does dispatch the builder that's part of it's whole process. it's subagent
orchestration and build agent is part of this that's WHY `/declare` exists."*
**Consequence:** R-18 amended. "Not a skill" means no skill AUTHORS code; it never meant nothing
launches the build. `/build-and-test` dispatches the build agent, `/adversarial-review` dispatches the
test author, and `declare` is recognized as the build agent's own interface for stating its picks
before it makes them — which is what it was for all along.
`design-doc impact:` R-18

### 28 · S6 is autonomous; `/ratify` lives at S5 — owner-initiated, closes a BLOCKING defect
**Found:** R-2 and the README both promised S6 runs without the owner. `/finish-build` was built
entirely around per-fix predict-then-reveal, making it the most owner-intensive step in the pipeline.
One of the two was lying.
**Owner:** *"i think s6 gets to be autonomous because what matters is the human reviews the output at
the end. i think the step for ratify to be baked into is test-spec which makes this work better."*
**Consequence:** R-2 was right and the skill was wrong. `/finish-build` rewritten: autonomous, no
per-fix prediction, forks picked and logged and surfaced rather than halted for. The ownership beat
consolidates at S5, where the owner rules what must be protected against. The record replaces the
dialogue — and the skill's kill rule now says so: a run that leaves a summary instead of an account
has moved the unexamined trust from the code into the report.
`design-doc impact:` R-2

### 29 · "Veto intact" was AI-words — owner-initiated
**Found:** `/auto-build` offered the owner "veto intact" over decisions the finished code already
depended on. No skill described what executing a veto meant. Exercising one *is* "go back and make a
ton of changes" — the failure named on the project's own front page.
**Owner:** *"no clue where 'veto intact' came from that's a good observation of ai-words at work
taking away meaning. this is a bad idea in general and it only becomes good if it links very clearly
toward the goal of producing a design doc that explains what's being built and helps guide a build."*
**Consequence:** the batch's job is now explicit and singular — bring the design doc up to date with
what was decided. Every entry is a **proposed design-doc amendment**, which is a ruling the owner can
actually make, rather than a rollback they cannot. Where a pick is genuinely bad and embedded, the
skill names the rework cost plainly instead of calling it a veto.
`design-doc impact:` A-14 (amended — the phrase originated there, which is why it had spread to
five files)

### 30 · `/auto-build` takes a spec and never writes one — owner-initiated
**Found:** the input contract said "any increment design doc" while the procedure said "**Derive** or
read" — an agent authoring binding scope overnight, against R-6.
**Owner:** *"`/auto-build`'s input is a spec. it runs the build process given approved design. design
is the core of everything… auto-build should take a design doc as input."*
**Consequence:** "Derive or" struck. The skill now states why the boundary is load-bearing:
delegating execution is a decision the owner signs by invoking it against a spec they read;
delegating design would leave nothing approved for the work to be checked against.
**Context banked:** the next project after v1 is refining how one *gets* to a design doc, since the
owner sometimes designs with gstack or other tools first. That is upstream of this skill by
construction.
`design-doc impact:` none (R-6, R-19 unchanged; skill corrected to match)

### 31 · Human approval under autonomy — one proxy for judgment, a fresh agent for verification
**Fork:** when an agent stands in for the owner at an unattended run's approval points, does one
persistent agent carry them all, or does each get a fresh one?
**Owner:** *"human approval can be simulated by agent review… the whole point of auto is im saying an
agent can make calls for me this time."* Then raised the persistent-vs-fresh question directly and
took the recommendation.
**Recommendation, taken:** split by the KIND of decision. S1, S4, and S5 are judgment — they take the
owner's values as input, there is no answer to discover, and what matters is applying one standard
without contradicting yourself. That needs continuity: **one proxy carries all three.** S7 leg 5
(do the assertions check anything real) is verification — it has a right answer, and the proxy is the
worst possible reader of it, having approved the spec those tests came from and having found nothing
surprising in a run it read end to end. **A fresh agent does that one.**
**Consequence:** A-15 refined — freshness is required for verification, not for judgment. The proxy's
rulings are a first pass recorded in declaration form, not a verdict; they land in the batch.
**Noted, not built:** if overnight runs start waving things through, the escalation is a cold read of
the finished batch by an agent that never saw the run. Deferred until evidence says it is needed.
`design-doc impact:` A-15

### 32 · `/retrace` under autonomy — deferred by default, never asked
**Owner:** *"`/retrace` can be also specified ahead of time or deferred by default (not an ask when
invoked to preserve auto capability, but user can invoke while asking for retrace)."*
**Consequence:** the flag is set at launch or not at all. Prompting mid-run would defeat an
unattended run.
`design-doc impact:` none (R-17 unchanged)
