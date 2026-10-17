---
schema_version: 1
id: D26
kind: decision
title: Write snapshot tests with inline-snapshot
---

Was inbox 0013 (#10).

**Decided:** the snapshot tests that `CLAUDE.md` asks for — the wording of the answers
now, the Mermaid view next — use inline-snapshot, which keeps each expected output inside
the test that checks it. It is a development dependency only.

**Why:** the wording of an answer is part of what gets reviewed, and the review happens
on the pull request's diff. With the expected text in the test itself, a change of
wording shows up as one readable change next to the code that made it. Run without a
flag, it only compares: a mismatch fails, and nothing in the test is rewritten.

**Rejected:**

- *syrupy*, the other candidate in the plan of 2026-08-29. It keeps snapshots in separate
  files, so a diff shows the wording apart from the test it belongs to.
- *Plain string comparisons.* Fine for a line or two, but a long output has to be
  retyped by hand whenever it changes.
