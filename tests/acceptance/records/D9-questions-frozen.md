---
schema_version: 1
id: D9
kind: decision
title: Freeze the two watch questions that v0.1 answers
serves: [G1]
supersedes: [D8]
---

`docs/questions.md` is frozen with the two checks v0.1 ships, stale-premise downstream
and orphan tasks, each written as a rule that two readers applying it to the same
records answer identically; four node types, three edge types and two recorded states
follow from them. Unlike the plan of 2026-08-29, contradiction is not frozen and there
is no issue node: an open question is a decision to wait. Drift and context for a task
stay unfrozen too, so the slots proposed on 2026-09-20 stay reserved.

`CLAUDE.md` allows only the node and edge types a frozen question requires, and v0.1
exists to show that the schema was derived from the questions; freezing only what v0.1
answers keeps the schema to what can be checked now.

Rejected: freezing contradiction now, which adds structure no v0.1 check reads and would
still miss conflicts nobody noticed; freezing the context question, since nothing
consumes its answer yet; and counting a superseded decision as a stale foundation on its
own, which goes beyond the v0.1 definition and stays a proposal for Step 3.
