---
schema_version: 1
id: D8
kind: decision
title: Defer the two proposed reserved slots until the questions are frozen
depends_on: [P2]
---

The two schema slots proposed on 2026-09-20 are not adopted yet: rejected alternatives
and their reasons as a first-class item rather than free text, and the scope a decision
binds. They are decided in Step 1, when the questions are frozen, together with whether
to freeze a fifth question, what context matters for this task: if it is frozen, the
slots become types it requires; if not, they stay reserved and unimplemented. The slots
would let one query hand an agent a brief for a task, but `CLAUDE.md` rules out any node
or edge type that no frozen question requires, so fixing them first would put the schema
ahead of the questions.

Rejected: adopting both now as definitions only, as three earlier slots were reserved
during planning, which fixes part of the schema's shape before the question that would
justify it exists; and dropping them, since the context use case is real.
