# Ship Pipeline — Project Design Doc

```
Layer:            combined (product + technical)
Slice:            project
Binding:          yes
Scope authority:  none — authored here
Sources:          owner rulings, derive session 2026-08-13/14 (authoritative: intent)
                  README.md 2026-08-10 (authoritative: shipped state)
                  Ship Pipeline wiki ≤2026-07-16 (authoritative: prior doctrine)
                  Kiro vs. Ship Pipeline comparison 2026-08-06 (context only)
Reconciled:       2026-08-15
Status:           ratified — derive session 2026-08-13/14, 13 stops logged
                  amended 2026-08-15 (v1 scoping session): R-19, C-1, A-18, A-19, Q-1
```
*design-doc v0.4.0 · 2026-08-14*

---

## 1 · What this is

Ship Pipeline is a spec-driven process for building software with agents, operated as a set of
Claude Code skills. It does not write code and it does not decide what to build. It decides one
thing, repeatedly, and makes the answer visible.

## 2 · Who it's for

A developer who builds with agents and remains responsible for the result — who must be able to
explain, defend, and evolve software they did not type. Not a manager approving work, and not a
user of a finished product: the person on the hook.

## 3 · The one job

> **Decide whether a spec is specific enough that an agent can execute it without making decisions
> the owner would have wanted to make.**

Everything else in this document is machinery for that sentence. A mechanism that does not serve
it is ceremony.

**The failure it exists to prevent**, in the owner's words: *building something massive, finding an
issue, and now you have to go back and make a ton of changes.*

---

## 4 · Requirements

### The loop

```
R-1 · MUST · src: owner ruling, this session
    Work is done in increments. Every increment passes through seven steps in order:
    S1 spec and approve · S2 agent builds · S3 fresh agent checks against the spec ·
    S4 owner review · S5 adversarial test spec and approve · S6 agent tests, fixes,
    greens · S7 owner sign-off. Completing S1-S7 completes the increment.

R-2 · MUST · src: owner ruling, this session; clarified 2026-08-15
    S2 and S3 run without human intervention, as do S6's test-fix cycles. The owner's
    touchpoints are S1, S4, S5, S7 — and each is a judgment, never a transcription task.
    S6 IS autonomous. What matters is that the owner reviews the output, not that they
    approve each fix on the way. Prediction-before-reveal belongs at the touchpoints —
    principally S5, where `/ratify` is baked into the test spec — and not per-fix at S6.

R-3 · MUST · src: owner ruling, this session
    Within S2 the agent writes the tests for the specced behavior and observes them
    failing before writing the implementation. Rigor here may be rough; S3 is what
    keeps it honest.

R-4 · MUST · src: owner ruling, this session
    S3 is performed by an agent that did not write the code and did not audit the tests
    (R-16), and checks both directions: built-but-unspecced (creep) and specced-but-unbuilt
    (gap).

R-5 · MUST · src: owner ruling, this session
    Every increment gets a hardening pass (S5-S7), however brief, including increments
    where it is expected to find nothing. The pass is warranted by how agents fail, not
    by its yield.

R-6 · MUST · src: owner ruling, this session
    S5's test spec is agent-proposed and owner-ruled — the agent seeds "what holes should
    we protect against" because the owner cannot enumerate the failure modes of code they
    did not write. S1's spec runs the opposite way: owner-authored, agent-pressed.

R-16 · MUST · src: owner ruling, this session
    S2 carries a second, concurrent verification thread. Once the tests are red and before
    the implementation exists, an independent agent audits the tests against the spec:
    would these tests catch a wrong build? It runs while the building agent writes code,
    so it costs no wall-clock. Red-first (R-3) proves a test CAN fail; this proves it
    fails for the right reason.
    This agent is DISTINCT from S3's. An agent that approved the tests has a stake in
    their adequacy and is the least likely reader to conclude that a build passed tests
    which were never good enough.

R-18 · MUST · src: owner ruling, this session; amended 2026-08-15
    Building itself is not a skill — it is an agent working from the increment design doc,
    which is therefore the build interface. What IS a skill is the harness around it: a
    skill whose job is to ENSURE building occurs inside the test/review framework.
    The harness IS subagent orchestration, and the build agent is one of the agents it
    dispatches. It confirms the tests are red before implementation, dispatches the audit
    (R-16) concurrently, and dispatches conformance (R-4) after. This converts R-3, R-4,
    and R-16 from protocol the process asks for into behavior the skill performs.
    "Not a skill" means no skill AUTHORS code — it does not mean nothing launches the
    build. A harness that cannot start what it harnesses is inert. This is also why
    `declare` exists: it is the build agent's interface for stating what it would choose
    before it chooses it.

R-19 · MUST · src: owner ruling, this session
    An autonomous mode exists that runs S1-S7 without stopping — for overnight runs and
    any increment the owner elects to be out of. It is governed by A-14: everything the
    owner would have ruled on is presented as a reviewable batch at the end.
    The design doc is MODE-FREE. Mode is carried by the invoking composite, never by the
    artifact, and no skill downstream of the doc branches on it.
    `/auto-build` MAY report that a spec looks thin to run unsupervised. That report is
    C-1's `unknowns` read at composite altitude — the same mechanism one level up, not a
    second one. It informs; it never refuses the run (A-17).
```

### Approval and the declaration

```
R-7 · MUST · src: owner ruling, this session
    Approval authority is the owner's at S1, S4, S5, and S7. An agent's readiness claim
    is a request for review, never a verdict.

R-8 · MUST · src: owner ruling, this session
    Delegation is itself an approval. Where an agent settles decisions without asking, it
    does so under a threshold the owner set and signed — never under its own assessment
    that a decision was small.

R-9 · MUST · src: owner ruling, this session
    Before S1's approval the agent produces a DECLARATION: every decision it would have to
    make to execute this spec.

R-10 · MUST · src: owner ruling, this session
    Each declaration entry states the decision and, in plain language, what reversing it
    would look like if it turns out wrong. Entries carry no significance label.

R-11 · MUST · src: owner ruling, this session
    A decision surfacing after the owner has signed — declared or not — halts the increment
    and is presented in declaration form. The owner rules carry / escalate / revert. The
    system never picks. In autonomous mode the halt is pre-ruled by the election to run
    (A-17): the agent picks, logs, and continues, and the batch at A-14 is where the
    ruling actually happens.
```

### Sizing

```
R-12 · MUST · src: owner ruling, this session
    An increment is sized by the complexity the owner can hold at once, never by surface
    area. Screen count, file count, and diff size are not sizing signals.

R-13 · MUST · src: owner ruling, this session
    Scope adequacy is assessed during S1, before approval, by the skill producing the spec.
    It proposes a split; it never splits unilaterally.

R-14 · MUST · src: owner ruling, this session
    Two oversize detectors, both firing before code exists: declaration length (mechanical)
    and the owner noticing the urge to skim at approval (self-reported). The urge to
    ok-click is an instrument, not merely a failure.

R-15 · MUST · src: owner ruling, this session
    Rework iterations at S2-S4 are counted and surfaced. The count is the spec-quality
    metric — it measures whether S1 did its job.
```

### The learning surface

```
R-17 · DEFAULT · src: owner ruling, this session; clarified 2026-08-15
    An increment may produce a RETRACE: a readable account of how the agent worked and why
    it made the moves it made. Optional to read, non-binding, and never a gate — its
    audience is a developer who wants to learn the reasoning rather than inherit the
    result. Distinct from `/own-your-code`, which describes the system as it stands;
    retraces are the per-increment raw material that consolidation draws on.
    A retrace is SUPPLEMENTARY — a learning resource, not a deliverable, and not a peer of
    the ownership doc. `/own-your-code` is the document that matters: it is what confers
    ownership, and nothing may stand in for it. Retraces default OFF under autonomous runs
    and are opted into at launch, never prompted for mid-run.
```

---

## 5 · Architecture and invariants

```
A-1 · Severity has two axes: impact on use x cost to reverse. Neither alone decides it.

A-2 · An agent can estimate reversal cost — spread (how many places depend on it),
      escape (whether anything left the system before anyone would notice), and lock-in
      (whether other choices follow from it). All three are readable from the code.

A-3 · An agent cannot estimate impact. Impact is a property of what the owner values and
      exists nowhere in the codebase. Therefore significance is never computed by the
      system, only informed. This is why R-10 forbids significance labels.

A-4 · Time-to-discovery scales reversal cost. Because increment size bounds time-to-
      discovery, increment size is the sole control on how expensive a mistake becomes —
      and smaller increments make fewer decisions significant in the first place.

A-5 · Reversal cost and rework cost are the same quantity. One measure governs both
      "which decisions are yours" and "how bad is a failure."

A-6 · Two phases, two promises. An increment that passes S3 is CONFORMANT. Only one that
      passes S7 is TRUSTED. An initial build makes what is described work; it does not
      promise robustness against edge cases.

A-7 · Two loop kinds, opposite polarity. Rework at S2-S4 is a defect; its target is zero
      and its count is a quality signal. Iteration at S5-S7 is the phase working as
      intended; its count means nothing about spec quality. A system that cannot tell
      them apart reads the same trace backwards.

A-8 · A check's value is that it ran, not what it found. A hardening pass that surfaces
      nothing is a successful pass.

A-9 · Conformance and completeness are orthogonal. S3 can only check against what the
      spec determines; a decision the spec never made has nothing to conform to. A clean
      conformance result says nothing about whether the declaration was complete.

A-10 · One work level, no nesting. Groupings (version, feature, milestone) are planning
       labels the system does not model. Composability is available in theory and gets
       messy fast; it is deliberately absent.

A-11 · Two doc tiers and no more: project and increment. Nothing binding sits between
       them. Increments trace to this document.

A-12 · One repeatable action, one skill. Skills are atomic; the pipeline is the
       orchestration of them. Composition into larger units is a separate, optional
       layer — never a reason to fuse two actions into one skill.

A-13 · Composition is how the owner chooses autonomy. Running a composite skill that
       spans an approval point IS the approval for it, under R-8: delegation is a signed
       decision. This is legitimate precisely because it is chosen per increment, not
       configured once.

A-14 · A composite must still surface what it passed through. Everything the owner would
       have ruled on — the declaration, conformance findings, adversarial findings — is
       presented at the end as one reviewable batch. A composite that hides its decisions
       is ok-clicking at a higher altitude, and violates the transparency that R-10 exists
       to provide.
       AMENDED 2026-08-15: the batch's purpose is to bring the DESIGN DOC into agreement
       with what was decided, and each entry is presented as a proposed amendment to it.
       An after-the-fact "veto" over decisions the code already depends on is not a choice
       the owner can exercise — exercising it IS the rework this process exists to prevent.
       What they can rule is what the spec says from here. Where a pick is bad and already
       embedded, name the rework cost from its reversal picture and call it rework.

A-15 · Independence means a separate context. The auditing and conformance agents must
       share no context with the builder or with each other; freshness is the property,
       and it cannot be simulated inside one session. Subagent dispatch is the available
       mechanism; the requirement is the isolation.
       REFINED 2026-08-15 — freshness is required for VERIFICATION, not for JUDGMENT.
       A verification question has a right answer and a stake in the artifact hides it,
       so the reader must be cold. A judgment question takes the owner's values as its
       input; there is no answer to discover, only a standard to apply consistently, and
       consistency needs continuity. Where an agent stands in for the owner's judgment
       (A-17, autonomous runs), one proxy carries the run. Where it verifies, it is fresh.

A-16 · Composites come in two kinds, and only one of them must be built. CONVENIENCE
       composites bundle steps the owner would otherwise invoke by hand. ENFORCEMENT
       composites exist so an invariant holds mechanically rather than by discipline —
       R-18 is one. Skipping an enforcement composite is legal and puts the invariant
       back on willpower.

A-17 · Halting is never strictly gated. The owner may elect to run autonomously and
       knowingly accept the risk, and the system does not override that election. A
       system that can refuse the owner's accepted risk has taken authority R-7 says it
       does not have — the sovereignty invariant is the same one, read from the other
       side. Every mechanism here informs a choice; none of them may make one.

A-18 · Composites are shaped by STAGE OF THE PROCESS FROM THE HUMAN'S POINT OF VIEW, not
       by technical affinity. Atomicity below (A-12) is what makes flexible composition
       possible; grouping above exists so the operator meets a small, legible surface.
       Simplicity of use is an asset, not a compromise.

A-19 · A skill is told what it needs to do its job and nothing more. Project-level
       rationale — why a tolerance exists, what the surrounding structure catches, what
       the process is trading off — stays in THIS document unless withholding it would
       inhibit the skill's execution. A skill that knows a false negative is tolerated is
       a skill that can talk itself into one.

A-20 · The roster is TIERED BY AUDIENCE. Tier 1 is what using Ship Pipeline means — the set a
       user invokes, and the whole of what they must learn. Tier 2 is the machinery: atomic
       (A-12) and individually callable, but reached through tier 1 and never required
       knowledge. A user must be able to build spec-driven without knowing a tier-2 name.
       Tiering is carried in the skill DESCRIPTION, not the directory — a tier-2 description
       states it is internal and names the tier-1 skill that reaches it.
```

---

## 6 · Contracts

```
C-1 · The declaration entry — CLOSED. Any field not listed is a fork to the decision log.

      decision:  what the agent would have to choose
      options:   what it would be choosing between
      taking:    which it would take absent a ruling
      reversal:  in plain language, what undoing this looks like if it is wrong
                 — including anything already escaped (data written, calls made)
      unknowns:  context the agent believes it lacks and would want before deciding;
                 empty when it has none

      No severity, priority, or significance field. See A-3.

      `unknowns` is honest reporting, not self-assessment — the agent names what it
      cannot see, which is the one thing it can report reliably (A-3, §8). False
      negatives are accepted: the surrounding structure is what catches misses, and
      trusting the owner makes for better usage than a field that nags. Per A-19 this
      rationale stays here; the declaring skill is not told the tolerance exists.

C-2 · Artifact homes — the repo is canonical.

      DESIGN.md                        this document
      docs/design/<increment>.md       increment design docs
      docs/build_status.md             position, gate legs
      docs/decision_log.md             forks and their `design-doc impact:` line
      RATIFICATION_LOG.md              predicted / surprised / no-opinion
      TEST_SPEC.md                     the ratified test contract
      docs/checks/<increment>.md       audit (R-16) + conformance (R-4) findings, and the
                                       rework count. Written by the S2-S3 harness; read by
                                       the hardening phase and by the ownership doc.
      docs/retrace/<increment>.md      retraces (R-17). Non-binding by construction.
      docs/own_your_code.md            the ownership doc. Regenerated in place, disposable.

C-3 · The wiki is a derived surface, never a second canonical. It restates; it does not
      decide. Where it disagrees with this document, this document is right and the wiki
      is stale. See Q-2.
```

---

## 7 · Design — screens and states

`design-deferred` — Ship Pipeline has no UI. Its surface is skills invoked in Claude Code.

---

## 8 · Assumptions and dependencies

- **`/ratify` is an external dependency**, living in `chzylee/skill-library`. The pipeline
  invokes it by name at approval stops. If it is absent, approval stops still occur but lose
  prediction-before-reveal and the ownership record.
- **Agents can enumerate more reliably than they can self-assess.** R-9 rests on this: a
  well-specified agent and a guessing agent report identical confidence, but both can list what
  they would have to choose.
- **The owner reads the declaration.** Every guarantee here degrades to nothing if S1's approval
  is given without reading — which is why R-14 makes the urge to skim a reportable signal.

---

## 9 · Definition of Done — project tier

Ship Pipeline is working when all of the following hold on a real project:

- **DOD-1** · An increment goes S1 to S7 with the owner never reading the implementation, and the
  owner can state what it does and what was decided.
- **DOD-2** · Rework at S2-S4 trends toward zero across increments. A rising count means specs are
  degrading, not that the agent is worsening.
- **DOD-3** · No decision meeting the owner's own significance bar was made without appearing in a
  declaration first — measured by the surprise column of `RATIFICATION_LOG.md`.
- **DOD-4** · A failure is bounded by one increment. No incident requires unwinding work across
  increments.

---

## 10 · Not in scope

- **Composable or nested work units.** One work level; groupings are labels (A-10).
- **Decomposing a project into increments.** The owner's planning activity; the system takes one
  scoped thing at a time and does not ask where it came from.
- **Modeling versions, features, or milestones** as entities.
- **Parallel generation.** Parallelism is spent on verification (independent checks, adversarial
  passes, the concurrent test audit at R-16), never on producing more code at once.
- **Sourcing what to build.** `/scout` and `/sidequest` are add-ons that feed S1's input, not
  parts of the pipeline proper. They are owed their own rework on their own clock.
- **Deciding what the product should be.** Ship Pipeline is indifferent to whether the design is
  good; it decides whether it is specific.

---

## 11 · Known limits

- **Responsibility is not reduced.** In the owner's words: *at the end of the day it comes down to
  user responsibility, just as in less handheld cases.* This process makes the choices visible
  enough that responsibility is exercisable rather than nominal. It does not transfer any of it.
- **Declaration completeness is not guaranteed** and is not gated on. An agent that does not
  recognize a decision will not declare it. S3 and S5-S7 are the nets, and R-12's sizing is what
  keeps a miss affordable.
- **Impact is unmodelable.** The system will surface decisions you do not care about and stay quiet
  about ones you do, whenever the reversal picture and the real stakes diverge.
- **Evidence base is one project.** Every threshold here is a starting cut, not a calibrated one.
- **Rough TDD is accepted at S2.** Test quality inside the autonomous span is backstopped, not
  assured.

---

## 12 · Open items

```
Q-1 · CLOSED 2026-08-15 · What constitutes Ship Pipeline v1.
       RULED: v1 is the rework of the FULL skill roster to match this document — the
       design differs enough from prior versions that partial conformance is not a
       state worth occupying. ONE increment, ONE increment design doc structured by
       skill, each entry carrying its own inputs, outputs, and done-criteria.
       Built DIRECTLY, not under S1-S7: the loop is what v1 provides, not what produces
       it. Ship Pipeline is tested experimentally by use on real projects, which the
       owner judged the better instrument than self-hosting.
       Sizing note: permitted under R-12 because the rework is low-complexity — the
       skill bodies largely formalize how the owner already prompts builds, stripped to
       what is project-independent.

Q-2 · DEFAULT · Wiki vs. repo canonicality for Ship Pipeline's own process material.
       DEFAULT TAKEN: repo canonical (C-3), wiki demoted to a derived surface swept by
       staleness check 9. Rationale: the wiki currently contradicts both the README and
       itself on where run-state lives, and two homes for one fact is the drift this
       process exists to kill.
       ALTERNATIVE NOT TAKEN: wiki canonical for process, repo canonical for run-state —
       preserves the existing split at the cost of keeping the contradiction live.
```

---

## 13 · Glossary

| Term | Means |
|---|---|
| **project** | the whole thing. Has this document. Not a work unit. |
| **increment** | one scoped thing to build; one pass through S1-S7; one increment design doc. The only work unit. |
| **grouping** | version, feature, milestone — planning labels the system does not model. |
| **build** | a verb. Never a noun **naming a unit of work** — that word is `increment`. "A wrong build" (the software an agent produced) is fine; "this build" meaning a chunk of scoped work is not. |
| **built** | the specced behavior works. |
| **validated** | an independent agent confirms it matches the spec (S3-S4). |
| **tested** | it survived deliberate attack (S5-S7). |
| **declaration** | the agent's enumeration of decisions it would make, each with a reversal picture. |
| **significant** | high impact on use, or expensive to reverse. Ruled by the owner, never computed. |
| **rework loop** | S2-S4 repeating because the work was insufficient. A defect. |
| **hardening loop** | S5-S7 repeating because attacks found things. Working as intended. |
| **test audit** | the concurrent check that the tests would catch a wrong build (R-16). |
| **retrace** | a non-binding account of how an increment got made and why (R-17). |

---

## 14 · Pointers

- `README.md` — install, the shipped skill roster. **A derived surface: check 9 sweeps it.**
- `skills/` — the skills implementing these requirements.
- Ship Pipeline wiki — prior doctrine, now derived (C-3, Q-2).
- Kiro vs. Ship Pipeline comparison — benchmark context, non-binding.
