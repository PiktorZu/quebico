# 0003 — v0.2 extracts through a session-end hook, not an MCP server

**Decided:** v0.2 captures records through a Claude Code `Stop` / `SessionEnd` hook that
runs an extraction script over the session transcript and proposes records under
`.quebico/` as a diff, which reaches `main` only through a pull request. No server, no
daemon. An MCP server is added only when agents need to *read* the graph during a
session (recall), not before. Only the direction is decided here; the design waits for
the capture data from Step 3.

**Why:** the hook's input includes `transcript_path`, so a plain command can read the
session transcript (JSONL) directly — confirmed in the Claude Code hooks documentation
on 2026-08-29. That delivers what the MCP plan promised, automatic extraction with
provenance (session id, transcript reference), with nothing left running. It also fits
how evaluation data is meant to accumulate: each session transcript can be paired with
the records a human confirmed in the resulting PR, which is why this repository uses
PRs even with a single maintainer.

**Rejected:**

- *An MCP server as the v0.2 headline.* A resident process for a job that runs once per
  session. MCP earns its place when in-session recall is actually needed.
- *Writing extracted records straight into the graph.* A transcript can carry material
  from unrelated or confidential work into a public repository. A human reviews every
  extracted record in a PR first; that review is the confidentiality gate.

**Premise:** `transcript_path` and the JSONL transcript format are observed behaviour,
not a documented stability guarantee. Once the schema exists, this is the first premise
Quebico records and watches about itself. It stops holding if Claude Code's hooks
documentation or release notes change either one.
