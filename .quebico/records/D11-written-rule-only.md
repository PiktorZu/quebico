---
schema_version: 1
id: D11
kind: decision
title: Rely on a written rule, not branch protection, to keep main PR-only
---

Split from inbox 0001 (#2) under rule 1, because 0007 (D18) replaced this part of 0001
and not the rest.

0001 deferred branch protection on GitHub in favour of a written rule. Deferred rather
than rejected: the rule belongs in `CLAUDE.md` either way, because the agent doing the
work needs to read it, and a solo repository did not yet seem to need the enforcement
machinery.
