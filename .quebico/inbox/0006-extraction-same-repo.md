# 0006 — Extraction stays in this repository

**Decided:** automatic extraction (v0.2) is built in this repository as its own package
next to the core — a uv workspace makes one repository with two packages cheap — and its
AI-related dependencies stay optional, so the core never needs them. Moving extraction
to a repository of its own is reconsidered when any one of these holds:

1. the record format under `.quebico/` has settled;
2. the extractor needs frequent releases that the core does not;
3. someone wants one side without the other;
4. the extractor's dependencies become a burden on the core.

**Why:** the seam between the two is where extraction writes candidate records into
`.quebico/` (today's inbox is its prototype), and that format has not been designed
yet: Step 1 designs it. Two repositories would turn every schema change in the meantime
into a coordinated change across both. One repository keeps the interface cheap to
change while it is still being found, and a separate package keeps the eventual split
cheap. Capture is also this project's central risk, so extraction is part of the core
bet rather than an accessory to it.

**Rejected:** *a separate repository from the start.* The seam is real, but its
interface does not exist yet, and neither half has a second user.
