# Watch questions

**Status: frozen on 2026-10-08 by decision 0009.** It changes only by a recorded
decision, together with the expected answers it changes.

This file fixes the two questions v0.1 answers (0002). Schema v0.1 is derived from them
and tested against them: a node type or edge type exists only if one of them requires it
(`CLAUDE.md`), and this file applies the same test to states. A question is frozen here
only when it has a rule that two careful readers — or two sessions — applying it to the
same records answer identically.

## Terms

- **Goal** — an outcome the project wants.
- **Task** — work to be done. *Open* until it is closed.
- **Decision** — a choice among alternatives. *In force* unless some decision supersedes
  it, whatever that decision's own state.
- **Premise** — something a decision takes to be true that is not itself a decision. It
  *holds* until it is recorded as no longer holding.
- **serves** — X exists for the sake of Y: task → decision or goal; decision → goal.
- **depends on** — a decision rests on a premise, or builds on another decision:
  decision → premise or decision.
- **supersedes** — a newer decision replaces an older one: decision → decision.

A relation exists only where a record states it. A rule runs on one set of records: the
repository at one commit. A reference that does not resolve, or an edge that joins kinds
its term does not allow, is a data error for `quebico check` to report; the rules run
only on a set of records with no data error.

## Q1 — Stale-premise downstream

**Asks:** Which decisions still stand on a premise that no longer holds?

**Rule:** Report every pair of an in-force decision and a premise recorded as no longer
holding, where the premise can be reached from the decision along `depends on`. The
chain may pass through decisions in any state.

**Does not catch:**

- a premise that has stopped holding but is not recorded as such — noticing that is
  v0.3;
- a decision built on a superseded decision, when no failed premise lies behind it.

## Q2 — Orphan tasks

**Asks:** Which tasks serve no goal?

**Rule:** Report every open task that neither serves a goal nor serves an in-force
decision that serves a goal.

**Does not catch:**

- whether a link means anything — a catch-all goal silences this question;
- a task that serves a goal the project has already reached or given up.

## What the two questions require

| Required | Q1 | Q2 |
|---|:-:|:-:|
| Decision | ● | ● |
| Premise — holds or no longer holds | ● | |
| Goal | | ● |
| Task — open or closed | | ● |
| `depends on` | ● | |
| `serves` | | ● |
| `supersedes` | ● | ● |

Four node types, three edge types, two recorded states. Whether a decision is in force
is not recorded: it follows from `supersedes`. No rule reads a record's text; where the
what, the why and the rejected alternatives are kept is for schema v0.1 to settle.

## Not frozen

None of these requires anything of schema v0.1.

- **Contradiction** — does a proposal or a new decision contradict a decision still in
  force? Telling whether two decisions clash needs judgment, so no rule over these
  records decides it. Left to v0.3.
- **Drift** — are we drifting from the direction we set? There is no yes-or-no
  definition yet. Left to v0.3.
- **Context for a task** — what context matters for this task? Nothing consumes the
  answer yet. The two slots reserved in 0005 stay reserved.
