---
schema_version: 1
id: D32
kind: decision
title: Limit the v0.1 visualization to a Mermaid view that GitHub renders as-is
supersedes: [D12]
---

Split from inbox 0002 (#3) under rule 1: the view can be cut or replaced without
touching the checks. 0002 drops it before either check if the schedule slips, and looks
past it only when it stops being readable.

0002 kept one picture beside the two checks: a Mermaid export, which GitHub renders
as-is. Visualization in v0.1 stops there. An interactive viewer or a web UI was
rejected until a Mermaid view stops being readable.
