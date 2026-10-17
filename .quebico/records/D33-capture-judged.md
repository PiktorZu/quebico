---
schema_version: 1
id: D33
kind: decision
title: Judge capture on all merged pull requests, and report those after the move apart
serves: [G3]
depends_on: [D31]
---

**Decided:** the pass line of the plan of 2026-08-29 — a capture rate of at least 70%
and a garbage rate of at most 30%, judged only once ten pull requests have merged — is
judged at the two Step 3 reviews (T3, T4) on every pull request merged since #2. The
pull requests merged after the move to `.quebico/records/` (D30) are also reported on
their own.

**Why:** the plan counted on the free-form records kept since Step 0 to lengthen the
observation from two weeks to about five. But the count since #2 stood at 10 of 10 at
the move, so it can hardly fail now, while what Step 3 adds is whether writing in the
schema's format keeps records from being written, the condition on which 0010 (D23) is
revisited. Only the later pull requests answer that.

**Rejected:**

- *Judging Step 3 on the later pull requests alone.* Too few to reach ten before Step 3
  ends.
- *Restarting the count at the move.* It throws away a month of evidence.
