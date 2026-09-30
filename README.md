# Quebico

**Record the reasoning that connects your project — goals, decisions, and the premises behind them — as a graph you can put to work.**

> Named for **Kuebiko (久延毘古)**, the scarecrow god of the Kojiki: he cannot walk,
> yet he knows everything under heaven. When no other god could answer, Kuebiko could.
> Quebico stands in your repository the same way — seeing every goal, decision, and
> premise, and noticing when they stop lining up.

## Why

Project decisions live in chat logs, PR descriptions, meeting notes, and someone's head.
The *reasoning* behind them — which goal a decision serves, what premises it stands on,
which alternatives were rejected and why — evaporates within weeks.

Tools that ask you to record this by hand have failed for thirty years: that is the
"capture problem" that killed design rationale research. And the memory tools that do
survive are built for *recall* — they remind you of context while you generate.

Quebico makes a different bet: keep a **small, fixed-vocabulary graph** of your
project's reasoning — captured with **zero manual bookkeeping** — and use it to answer
questions your project cannot answer today:

- *Which goal does this task actually serve?* (orphan-task detection)
- *Does this new decision contradict an earlier one?*
- *Is the premise behind that decision still true?*
- *Are we drifting from the direction we set?*

Not just a memory that reminds you — one that can argue back.

## Status

**pre-v0.1 — building in public.** Nothing to install yet.
This repository's own development decisions are recorded with Quebico itself
(dogfooding from day one).

## Roadmap

- **v0.1** — fix the questions the graph must answer, derive a minimal decision &
  rationale schema from them, and store it as plain files inside your repo
  (YAML/Markdown with ID links, no graph DB). The first two checks ship here,
  deterministic and LLM-free: decisions still standing on a premise that no longer
  holds, and tasks that serve no goal — plus a Mermaid view that GitHub renders as-is
- **v0.2** — automatic extraction from Claude Code sessions (via a session-end hook,
  no server to keep running) and from PRs, with provenance edges required on every
  node
- **v0.3** — checks that need judgment: contradiction detection, and noticing on its
  own when a premise has gone stale — each with a recommended action

Each stage ships with a design write-up in English and Japanese.

## License

Apache-2.0
