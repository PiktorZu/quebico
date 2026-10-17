---
schema_version: 1
id: D24
kind: decision
title: Fail quebico check only on data errors
---

Was inbox 0011 (#9).

**Decided:** `quebico check [DIR]` exits with 1 when the records have a data error
(`docs/schema.md`) and with 0 otherwise — including when it answers the watch questions
with stale-premise downstream or orphan tasks. It prints what it finds either way. CI
runs it on every pull request, so a data error fails the run and a finding does not.
DIR defaults to `.quebico/records/`. A directory that does not exist is an empty record
set: a note on standard error, no records, exit 0. A path that exists but is not a
directory is a usage error (exit 2), so a mistyped argument cannot pass as an empty
record set.

**Why:** a data error is a defect. The rules cannot run on such records, and a mistyped
id or field silently drops a link. A finding is the opposite: the records are sound and
the project has something a person should judge — a wait that has come back, a task
that no longer serves a goal. If findings failed CI, the cheapest way back to green
would be the corrupt one: close the task, set the premise back to holding, or delete the
link, whether or not anything was decided. That is cheating on tests, applied to the
records, and in Step 3 it would also distort the capture and garbage rates the records
are kept to measure. It would bite at once: the fifteen acceptance records as they stand
already report T2, the PyPI placeholder task, as an orphan.

A missing directory is not an error so that the command runs in any repository before it
records anything — this one included, until Step 3 creates `.quebico/records/` — and so
that CI can run it from the start without the workflow changing later.

**Rejected:**

- *Failing on findings too.* For the reasons above.
- *A separate exit code for findings, or a flag to choose.* An interface nothing consumes
  yet; CI only needs to know whether the records are sound.
- *An error for a missing directory.* CI would have to skip the step until Step 3, and a
  new repository would see an error before it had recorded anything.

**Revisit:** if the Step 3 reviews show findings going unread because nothing fails,
surface them — on the pull request, say — before making them fail.
