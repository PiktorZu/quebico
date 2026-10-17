---
schema_version: 1
id: D30
kind: decision
title: Move the inbox into .quebico/records/ and retire it
---

**Decided:** Step 3 starts by moving the provisional inbox into schema v0.1.

- Each inbox note became a record by gaining front matter (0010), and the file moved with
  it, so `git log --follow` still shows its history. Its first line keeps the inbox
  number and the pull request that added it (`Was inbox 0009 (#5).`), because documents
  cite decisions by those numbers.
- Notes holding more than one choice were split (rule 1): 0001, 0002, 0004 and 0009.
  Premises that decisions rest on or wait for became records of their own.
- Three decisions from before the inbox were recorded because inbox decisions superseded
  them (rule 6): the README's roadmap for v0.1 and v0.2 (D12, D14) and working in the
  WSL clone (D19). A decision from before the inbox is recorded when the project had
  announced it (D12, D14), worked under it (D19) or scheduled a task under it (D5, T2).
  Where 0009 and 0010 depart from the plan of 2026-08-29, they settle what that plan
  proposed for Steps 1 and 3 before any of it was carried out; those proposals stay
  among their rejected alternatives.
- The fifteen acceptance records are the starting point (0010), copied as they are
  except that T1 and T2 are closed, D7 gains the premise it rests on, D9 gains the checks
  it freezes, and D7, D8 and D9 carry the full text of 0004, 0005 and 0009. New records
  continue their ids, from D10 and P3.
- The inbox and its README are gone, and the recording convention lives in `CLAUDE.md`
  alone: every pull request either adds a record or says `Decisions: none` (D31). Schema
  v0.1 has no kind for a proposal, so an idea nobody asked for goes in the pull request
  description, or becomes a decision to wait when it should come back at a known point
  (rule 7), as 0014 became D27. `CLAUDE.md` also now says what 0011 (D24) implies: a
  finding is never silenced by editing records.

**Why:** one place for records, so that `quebico check` and CI read everything the
project has decided, and Step 3 measures recording on the same set the watch questions
run on.

**Rejected:**

- *Keeping the inbox as a frozen archive beside the records.* The same reasoning would
  live twice, and the copies would drift apart.
- *Records that point back to inbox notes left in place.* Everything would be written
  twice; 0010 meant a note to become a record by gaining front matter.
- *Inbox numbers as ids* (`D0009`). Two styles of id in one set, and the fifteen records
  already give 0004, 0005 and 0009 the ids D7, D8 and D9.
