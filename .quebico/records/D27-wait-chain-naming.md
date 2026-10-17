---
schema_version: 1
id: D27
kind: decision
title: Wait for the Step 3 reviews before naming the chain in a stale-premise answer
depends_on: [P6]
---

Was inbox 0014 (#10). Recorded as a decision to wait (rule 7).

**Proposed, not decided.** A stale-premise answer names only the two ends: the decision
in force and the failed premise it reaches. When the premise is reached through other
decisions, the answer could name them too — "decision D4 … still stands on premise P1 …,
through D3, D2 and D1" — because D4's own record never mentions P1.

**Why:** an answer the reader cannot trace back is the easiest kind to dismiss, and
whether answers get acted on is what the Step 3 reviews look at. The independent review
of the watch questions raised it. In this project's own history, the README myth (D2) is
reported against the premise behind the name (P1), which D2's record reaches only through
the name decision (D1).

**Not done now:** the rule in `docs/questions.md` reports pairs, and v0.1 ships that rule.
Naming a chain also means choosing one when there are several, and the code budget left
for the Mermaid view is about a hundred lines.

**Decide:** in Step 3, when the weekly reviews look at how the answers are received.
