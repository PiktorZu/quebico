# 0005 — Two proposed reserved slots wait for Step 1

**Decided:** not to adopt yet the two reserved schema slots proposed on 2026-09-20:

- *rejected alternatives and the reasons for rejecting them*, as a first-class item
  rather than free text;
- *the scope a decision binds* — which area, or which files, it governs.

They are decided in Step 1, together with whether to freeze a fifth question: *what
context matters for this task?* If that question is frozen, the two slots become types a
frozen question requires. If it is not, they stay reserved and unimplemented.

**Why:** the slots exist so that one query can hand an agent a brief for a task, on the
view that goals, decisions and premises, linked, make unusually good context for an
agent doing similar work. That use sits on top of the audit rather than replacing it.
But `CLAUDE.md` rules out any node or edge type that no frozen question requires, and
fixing the slots before the questions are frozen would put the schema ahead of the
questions — the reverse of how this project derives its schema.

**Rejected:**

- *Adopting both now as definitions only*, the way three earlier slots were reserved
  during planning (open/decided state on issues, a decision→outcome edge, a
  recommended-action field on alerts). Cheap on paper, but it fixes part of the schema's
  shape before the question that would justify it exists.
- *Dropping them.* The context use case is real; what is open is where it enters.

**Revisit:** in Step 1, when the questions are frozen.
