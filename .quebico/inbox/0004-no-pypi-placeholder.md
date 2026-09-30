# 0004 — No placeholder release on PyPI

**Decided:** publishing an empty 0.0.1 of `quebico` to PyPI to hold the name is
downgraded from a planned step to optional, and nothing is scheduled. If it is ever
done, it is a minimal real package marked pre-alpha that links here, never an empty one.

**Why:** the name was free on PyPI when checked on 2026-08-29. An empty package comes
close to what PyPI's name-retention policy (PEP 541) treats as squatting, and the public
repository already establishes the claim in practice. "quebico" is a coined spelling, so
the chance of a collision on PyPI is low.

**Rejected:** *publishing the placeholder now as naming insurance.* Fifteen minutes of
work, but it buys little that the repository has not already bought, and it can read as
squatting.

**Consequence:** `pyproject.toml` moves from uv's default `version = "0.1.0"` to
`0.1.0.dev0` and gets a real description, so nothing in the repository claims a release
that has not happened.
