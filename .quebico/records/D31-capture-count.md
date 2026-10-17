---
schema_version: 1
id: D31
kind: decision
title: Count a pull request as captured when it adds a record or declares no decisions
serves: [G3]
supersedes: [D10]
---

**Decided:** 0001's capture rule (D10) carries over with the inbox replaced by
`.quebico/records/`. Every pull request merged into `main` either adds at least one
record there or states the exact line `Decisions: none`. A pull request that only
changes a state — closes a task, marks a premise as no longer holding — states
`Decisions: none` unless it also records a decision. The denominator stays every merged
pull request since #2, misses are never backfilled, and `main` is reached only through
pull requests (D18). How the count is judged is D33.

**Why:** the rule moves with the records and otherwise stays as it was, so the count
stays comparable across the move.

**Rejected:** *counting a state change as a capture.* A pull request could close a task,
leave the decision behind it unrecorded, and still count.
