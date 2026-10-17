---
schema_version: 1
id: D22
kind: decision
title: Wait for the Step 3 data before counting a superseded foundation as stale
depends_on: [P6]
---

Split from inbox 0009 (#5) under rule 1, and recorded as a decision to wait (rule 7).

0009 did not adopt *counting a superseded decision as a stale foundation on its own*: it
would also report decisions built on a replaced decision when no premise failed. One
real case exists: the convention to run `chmod 644` on files copied from the Windows
drive rested on the route through the WSL clone that 0008 replaced. It goes beyond
0002's definition, so it was kept as a proposal, to be weighed against the Step 3 data.
