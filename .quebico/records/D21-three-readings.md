---
schema_version: 1
id: D21
kind: decision
title: Settle three readings the v0.1 checks left open
depends_on: [D13]
---

Split from inbox 0009 (#5) under rule 1: a reading can change without unfreezing the
two questions.

The rules in `docs/questions.md` settle three readings that 0002 (D13) left open:

- Stale-premise downstream follows `depends on` from decision to decision, through
  decisions in any state. After the rename to Quebico, a decision built on "name it
  Omoikane" still reaches the failed premise behind it.
- "No recorded reconsideration" means "not superseded": a superseded decision is no
  longer reported.
- Orphan tasks looks only at open tasks, follows task → decision → goal, and does not
  count a superseded decision as a way to a goal. The PyPI placeholder task is reported
  once 0004 supersedes the plan it served.
