# CLAUDE.md

Working agreements for Quebico. Read this before making any change in this repository.

## What this project is

Quebico records the reasoning that connects a project — goals, decisions, and the
premises behind them — as a small fixed-vocabulary graph stored as plain files inside
the repository it watches, and uses that graph to answer questions the project cannot
answer today: orphan tasks, contradictions, stale premises, drift.

Status: **pre-v0.1**. No installable code yet. See `README.md` for the roadmap.

Language: everything in this repository is written in English. Design write-ups are
published in English and Japanese.

## The current phase, and what NOT to build

This project is working through a risk-ordered plan. Two uncertainties must be settled
before any feature work:

1. **Can the schema answer the watch questions?** Settled on paper, with zero code,
   against 15 real records.
2. **Does recording actually keep happening?** This is the "capture problem" that
   killed thirty years of design-rationale research. Settled by dogfooding and
   measurement.

Until both pass, the following are out of scope. Do not write them, do not propose
them, do not scaffold for them:

- Anything that calls an LLM. Automatic extraction lands in v0.2, not before.
- A graph database, a server, a daemon, a web UI, a plugin system, a config system.
- Any node type or edge type that no frozen question requires.

**Code budget to v0.1: 500 lines total under `src/`**, tests excluded. If a change
would break that budget, stop and say so instead of writing it.

**The meta-rule for every task**: you must be able to state in one line *which
uncertainty it removes, at what cost, and how its outcome is judged yes or no.*
A task that cannot be stated that way gets dropped, not done.

## Recording convention (provisional — replaced by schema v0.1)

This is the most important section in this file. It exists so that the capture problem
can be measured starting now, before the schema exists.

**When a decision about direction, design, or operations is made in a session, write it
to `.quebico/inbox/` as one free-form Markdown file** named `NNNN-short-slug.md`.
Cover three things: what was decided, why, and which alternatives were rejected and why.
Free-form is deliberate — do not invent a schema here. These files migrate to the fixed
schema once it exists.

**Every pull request must do exactly one of two things, with no third option:**

- add at least one file under `.quebico/inbox/`, or
- state the exact line `Decisions: none` in its description.

This is what makes the capture rate objectively measurable later. The denominator is
every merged PR — observable from git history, independent of anyone's memory — and the
numerator is the PRs that did one of the two. A PR that silently does neither is a
capture miss and counts against the rate. **Do not backfill missed records.** The misses
are the measurement.

**Nothing reaches `main` except through a pull request** — no direct commits, no direct
pushes, not even for a one-line fix. This is not a style rule. Work that never became a
PR appears in neither the numerator nor the denominator, so a direct push does not merely
bend the convention, it silently deletes evidence.

What counts as a decision: anything a future contributor would ask "why is it like
this?" about. Renaming a variable is not a decision. Choosing the schema vocabulary,
adopting a timeout rule, accepting or rejecting a plan revision — all decisions.

## Development conventions

- Python 3.12+, managed with `uv`. `src/` layout.
- PR-based development even as a solo developer. The PR trail is not ceremony: it is
  the test data for the v0.2 automatic extractor.
- Every data file carries a `schema_version` field from its first line of existence.
- Graph data lives in a dedicated directory: `.quebico/` inside the repository being
  watched — including this one. Quebico dogfoods itself.
- CI arrives when the first code lands, not before: `ruff`, `pyright`, `pytest`, plus
  schema validation of the graph data. CI runs deterministic tests only; evals run
  outside CI.

## Testing (applies from the first line of code onward)

- Classical, Detroit-school TDD. **No mocks.** The test boundary is
  `check(files) -> findings`.
- Table-driven tests via `pytest.mark.parametrize`: one row per (mini-graph → expected
  finding). Every new real example found while dogfooding is added as one more row.
- The 15 hand-written records and their hand-worked expected answers are the acceptance
  fixture, written before the implementation exists.
- Property-based tests (Hypothesis) are capped at 2–3 properties: parser robustness and
  checker invariants. Nothing more.
- Snapshot tests for Mermaid output and alert wording.
- Not used: BDD/Gherkin, TCR, coverage-percentage targets. Mutation testing is optional,
  at most once before the v0.1 tag.
- The v0.2 LLM parts are **not** developed with TDD. They use error-analysis-first evals
  built from real traces, and their output must pass `quebico check` — the deterministic
  tests are the guardrail.

## Working agreements for agents

Three prohibitions, no exceptions:

1. **No over-engineering.** Build what the current step needs and nothing beyond it.
2. **No unrequested features.** If something seems like a good idea and nobody asked for
   it, write it to `.quebico/inbox/` as a proposal instead of implementing it.
3. **No cheating on tests.** Never disable, skip, weaken, or delete a test to make a run
   pass. A failing test is information — report it.

Optional practice: write tests and implementation in separate sessions (writer /
reviewer split) when a change is large enough that one session would be tempted to fit
the test to the code.

If a request conflicts with this file — the code budget, the out-of-scope list, the
prohibitions — say so before acting, and name the rule it conflicts with.
