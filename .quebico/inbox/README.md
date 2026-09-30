# `.quebico/inbox/` — provisional decision records

Quebico's schema does not exist yet. This directory is the stand-in that lets the
project start measuring its own capture rate before the schema is designed.

## The rule

When a decision about direction, design, or operations is made in a session, drop one
free-form Markdown file here, named `NNNN-short-slug.md` (`0001-`, `0002-`, … in the
order they were written). Cover three things:

- **What** was decided
- **Why**
- **Which alternatives were rejected**, and why

Free-form is deliberate. Do not add front matter, do not impose a structure, do not add
fields "for later". Anything invented here would contaminate the schema work it is
supposed to inform. These files migrate to the fixed schema once schema v0.1 exists.

Every pull request either adds a file here or states the exact line `Decisions: none`
in its description. A PR that silently does neither is a capture miss, and misses are
never backfilled — they are the measurement.

## Example shape

```markdown
# 0003 — Develop inside the WSL Linux filesystem, not on the mounted Windows drive

**Decided:** the working clone lives at `~/projects/quebico` inside WSL. The Windows
drive is used only for out-of-repo assets (plans, article drafts). Cloud sessions sync
through GitHub, never through the mounted drive.

**Why:** `/mnt/e` is slow enough for Python tooling that it changes how often tests get
run, and test-running frequency is load-bearing for the TDD loop here.

**Rejected:** working directly under `/mnt/e/...` so that every machine sees the same
folder — rejected because GitHub already provides that, at no cost to tool speed.
```

That is a shape, not a template. A record that is three sentences of prose is fine.
