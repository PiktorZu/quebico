---
schema_version: 1
id: D16
kind: decision
title: Version the package 0.1.0.dev0 until a release is made
---

Split from inbox 0004 (#3) under rule 1: how versions are numbered and whether a
placeholder is published can each be replaced without the other.

`pyproject.toml` moved from uv's default `version = "0.1.0"` to `0.1.0.dev0` and got a
real description, so that nothing in the repository claims a release that has not
happened.
