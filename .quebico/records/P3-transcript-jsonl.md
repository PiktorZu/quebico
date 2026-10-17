---
schema_version: 1
id: P3
kind: premise
title: Claude Code hooks hand the session transcript to a command as JSONL
---

From inbox 0003 (#3): the hook input includes `transcript_path`, so a plain command can
read the session transcript (JSONL) directly. This is observed behaviour, not a
documented stability guarantee. It stops holding if Claude Code's hooks documentation or
release notes change either one.

Checked again on 2026-10-15: `transcript_path` is still an input field of every hook
event, and the documentation's example path ends in `.jsonl`. It also says that the file
is written asynchronously and may lag the conversation, and points hooks that need the
turn's final text to `last_assistant_message` on `Stop`.
