# 0009 — The watch questions are frozen: the two that v0.1 answers

**Decided:** `docs/questions.md` is frozen. It fixes two questions — stale-premise
downstream and orphan tasks, the two checks v0.1 ships (0002) — as rules that two readers
applying them to the same records answer identically. From them follow four node types
(goal, task, decision, premise), three edge types (`serves`, `depends on`, `supersedes`)
and two recorded states: a task is open or closed, a premise holds or no longer holds.
Contradiction, drift, and context for a task are listed as not frozen and require nothing
of schema v0.1.

The rules settle three readings that 0002 left open:

- Stale-premise downstream follows `depends on` from decision to decision, through
  decisions in any state. After the rename to Quebico, a decision built on "name it
  Omoikane" still reaches the failed premise behind it.
- "No recorded reconsideration" means "not superseded": a superseded decision is no
  longer reported.
- Orphan tasks looks only at open tasks, follows task → decision → goal, and does not
  count a superseded decision as a way to a goal. The PyPI placeholder task is reported
  once 0004 supersedes the plan it served.

This supersedes 0005. The context question is not frozen, so the two slots proposed there
stay reserved and unimplemented, and rejected alternatives stay in each record's text.

Two departures from the plan of 2026-08-29:

- The plan froze three questions and deferred only drift. Contradiction is not frozen:
  whether two decisions clash needs judgment, and what a mechanical stand-in would need —
  issue nodes, or rejected alternatives as structured data — neither frozen question
  requires. The plan's own test applies: a question that cannot be written as a rule is
  not yet usable for design.
- The plan put two open-issue nodes among the 15 records. There is no issue node. An open
  question is recorded as a decision to wait, depending on the premise that what it waits
  for has not happened; when that happens, stale-premise downstream brings the wait back.
  0005 was such a record, and this freeze ends the condition it waited on.

**Why:** `CLAUDE.md` allows only the node and edge types a frozen question requires, and
v0.1 exists to show that the schema was derived from the questions (0002). Freezing only
what v0.1 answers keeps the schema to what can be checked now.

The draft was traced before it was frozen. Twenty-five records from this project's own
history — 14 decisions, 5 premises, 4 tasks, 2 goals — were run through both rules by hand
in twelve scenarios. Eight independent sessions, given only the rules, matched the
hand-worked answers in every scenario they were given; the final text was checked against
all twelve. Four independent writers recorded the same material (0001, 0004, 0005, 0007,
0008 and two tasks) using only the vocabulary, and all four got the same answers to both
questions.

**Rejected:**

- *Freezing contradiction now*, over issue nodes or structured rejected alternatives. It
  adds structure that no v0.1 check reads, and it would still miss the contradictions
  worth catching: a writer who did not notice a conflict does not link to the old issue.
- *Freezing the context question*, and with it 0005's two slots. Nothing consumes the
  answer yet, so nothing about it could be verified.
- *Counting a superseded decision as a stale foundation on its own.* It would also report
  decisions built on a replaced decision when no premise failed. One real case exists: the
  convention to run `chmod 644` on files copied from the Windows drive rested on the route
  through the WSL clone that 0008 replaced. It goes beyond 0002's definition; kept as a
  proposal, to be weighed against the Step 3 data.
- *Recording rules in the questions file*: that decisions are never edited, and that each
  holds one choice. Neither can be checked on a single commit. How records are written is
  settled with schema v0.1.

**Revisit:** if writing schema v0.1 and its 15 records turns up something the four node
types and three edge types cannot express, the questions change by a recorded decision.
