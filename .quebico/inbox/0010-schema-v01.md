# 0010 — Schema v0.1: the vocabulary of 0009, one Markdown file per record

**Decided:** schema v0.1 is `docs/schema.md`.

- It keeps the vocabulary 0009 derived from the frozen questions — goal, task, decision,
  premise; `serves`, `depends_on`, `supersedes`; a task's `closed` and a premise's
  `holds` — and borrows nothing from IBIS, MADR or Agent Trace, because nothing in the
  fifteen records needed it.
- A record is one Markdown file. Its YAML front matter holds everything Quebico reads:
  `schema_version`, `id`, `kind`, `title`, the links and the state. Its body holds the
  prose: what was decided, why, and what was rejected.
- Records live in `.quebico/records/`, from Step 3. Until then the provisional inbox
  stays in use; `CLAUDE.md` and the inbox README now say so.
- Eight writing rules say how records are written. They settle the five points left
  open when the trial records for 0009 were written, and the two that 0009 left to the
  schema: one choice per record, and a decision that changes is superseded rather than
  rewritten. Nothing checks them, because none can be seen on one commit.
- Fifteen records of this project's history and nine moments — seven from that history,
  two constructed — with both questions answered by hand, are the acceptance test for
  `quebico check`. They live in `tests/acceptance/`, apart from the live records.

**Why:** the questions read only kinds, links and states, so the front matter carries
exactly those, plus the title a person needs to recognise a record; the prose stays as
free as it has been in the inbox. An inbox file becomes a record by gaining front
matter — split, or joined by a premise record for what it rests on or waits for, where
the writing rules ask.

The schema was tested before it was frozen. Two independent sessions, given only
`docs/questions.md`, a draft of this schema and the records of each moment, found no
data error and answered both questions in all nine moments exactly as worked by hand;
a third, auditing the whole change, re-derived every answer. Two more, given the same
two files, the text of 0004, 0005 and 0009 and the other twelve records, wrote those
three decisions with exactly the links of the hand-written versions; D7–D9 in
`tests/acceptance/` are one of theirs, unedited. That shows new records being linked
into an existing set, not being created from nothing: the premise D8 waits on was among
the records they were given. No decision needs more than six lines of front matter,
against the plan's limit of thirty.

**Rejected:**

- *One YAML file per record*, with the prose in block scalars. Prose reads worse there,
  in review as well, and an inbox file could not become a record by gaining front
  matter.
- *The title as the body's first heading.* Quebico would then read the body.
- *Writing every state out.* `docs/questions.md` already makes "open" and "holds" the
  starting states.
- *Checking the writing rules.* None of them can be seen on one commit.
- *Recording every condition for revisiting a decision as a premise.* Only an open
  question needs one; making every "Revisit" a record adds work the capture problem can
  least afford, and two writers would draw the line differently.
- *Recording any decision that is missing when a later one supersedes it.* For a
  decision a pull request failed to record, that is the backfill 0001 forbids; only
  decisions from before the recording convention are recorded this way.
- *The fifteen records as the first live records too*, as the plan of 2026-08-29 had
  it. The test must stay fixed while the live records keep changing — T1 closes with
  this very change — and the moments need states that no longer hold. Step 3 copies the
  records into `.quebico/records/` as its starting point, so nothing is written twice by
  hand.
- *The plan's choice of material*, which included the publication channels, the license
  and the development environment. None of them changes either answer; the records
  chosen are the ones whose links do.

**Consequences:**

- 0003's premise — that the session-end hook hands over the transcript as JSONL — is
  recorded as a premise in Step 3, with the rest of the inbox.
- 0006's first condition for moving extraction to a repository of its own, that the
  record format has settled, is not met yet: the format settles when Step 3 shows records
  keep being written in it, and no extractor exists.

**Revisit:** if a record in Step 2 or Step 3 cannot be written in this schema, or if the
Step 3 capture data shows that the format itself is what keeps records from being
written.
