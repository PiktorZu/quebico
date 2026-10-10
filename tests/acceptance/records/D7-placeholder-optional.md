---
schema_version: 1
id: D7
kind: decision
title: Make the PyPI placeholder optional and never empty
serves: [G2]
supersedes: [D5]
---

Publishing an empty `quebico` 0.0.1 to hold the name goes from a planned step to
optional, and nothing is scheduled. If it is ever done, it is a minimal real package
marked pre-alpha that links to the repository, never an empty one. An empty package
comes close to what PyPI's name-retention policy (PEP 541) treats as squatting, and the
public repository already establishes the claim; the name was free on PyPI on
2026-08-29, and a coined spelling is unlikely to collide. `pyproject.toml` moves to
`0.1.0.dev0` with a real description, so nothing claims a release that has not happened.

Rejected: publishing the placeholder now as naming insurance. Fifteen minutes of work,
but it buys little that the repository has not already bought, and it can read as
squatting.
