# Schema v0.1

**Status: frozen by decision 0010**, together with the acceptance records in
`tests/acceptance/`. It changes only by a recorded decision, together with the expected
answers it changes.

`docs/questions.md` fixes what records must be able to say: four kinds of record, three
kinds of link, two recorded states. This file fixes how a record is written down, and
adds nothing to that list. Where the two files disagree, `docs/questions.md` wins.

## A record

Every `.md` file under `.quebico/records/`, at any depth, is a record of the repository
it sits in; other files there are ignored. A rule runs on all of them at one commit.

The file opens with YAML front matter, which holds everything Quebico reads. The body
holds what only people read, in free prose: for a decision, what was decided, why, which
alternatives were rejected and why, and anything else worth keeping.

~~~markdown
---
schema_version: 1
id: D4
kind: decision
title: Tell the Kuebiko story in the README
supersedes: [D2]
depends_on: [D3]
---

The README opens with Kuebiko, a scarecrow that stands still in the field and sees
everything ...
~~~

## Fields

| Field | On | Value |
|---|---|---|
| `schema_version` | every record | The number `1` |
| `id` | every record | Unique in the record set, case included. An ASCII letter, then ASCII letters, digits or `-` |
| `kind` | every record | `goal`, `task`, `decision` or `premise` |
| `title` | every record | One line. Reports and the Mermaid view show it |
| `serves` | task, decision | Ids. A task serves decisions or goals; a decision serves goals |
| `depends_on` | decision | Ids of premises or decisions |
| `supersedes` | decision | Ids of decisions |
| `closed` | task | `true` once the task is closed; absent or `false` while it is open |
| `holds` | premise | `false` once the premise is recorded as no longer holding; absent or `true` while it holds |

A link is always a list, even of one id or none: `serves: [G1]`. `closed` and `holds`
take `true` or `false`, spelled exactly so. No other field exists; in particular,
whether a decision is in force is not recorded — it follows from `supersedes`. Quote a
title that YAML would misread, such as one containing `: `.

By convention an id is the kind's initial and a number (`G1`, `T3`, `D12`, `P2`), and the
file is named after the id and the title (`D4-kuebiko-story.md`). Neither is checked.

## Data errors

`quebico check` reports each of these, and the rules in `docs/questions.md` run only on a
record set with none:

- a file under `.quebico/records/` whose front matter is missing or is not valid YAML;
- a missing `schema_version`, `id`, `kind` or `title`, or any value the table does not
  allow;
- a field the table does not list, or lists only for other kinds — so that a typo such
  as `depend_on` cannot silently drop a link;
- two records with the same id;
- a link to an id that no record has, or to a kind its term does not allow.

The last item is the pair that `docs/questions.md` names; nothing else is a data error.
A cycle, or a record that links to itself, is allowed: the rules answer it like any
other link.

## Writing records

No rule can see these on one commit, so nothing checks them; the questions answer well
only when records follow them.

1. **One record, one choice.** When a later decision might replace part of an earlier
   one, that part is a record of its own. 0001 decided how capture is measured and also
   to hold off branch protection; 0007 replaced only the second, so they are two
   records.
2. **A decision that changes is superseded, not rewritten.** Write the new decision and
   let it supersede the old one. Edit a record only to correct it or to change its
   state: `closed: true` when a task closes, `holds: false` when a premise stops holding.
3. **Depend only on what the decision would fall with.** Put a premise or decision under
   `depends_on` only if this decision would have to be reconsidered were that one to
   fail or be replaced. Something cited as background is not a link.
4. **A task serves the decision it carries out.** Link a task straight to a goal only
   when no decision lies between them; otherwise, once that decision is superseded,
   orphan tasks cannot notice.
5. **Goals are few and written on purpose.** A record never invents a goal so that it
   has something to serve.
6. **A decision from before the inbox is recorded when something supersedes it.**
   Decisions made before the recording convention (PR #2, 2026-09-15) were never
   written down. Record one — a title is enough — when a new decision supersedes it, so
   that the tasks and decisions still resting on it can be found. A record missed since
   then stays missing (0001); the new decision names it in its prose.
7. **An open question is a decision to wait**, depending on a premise that what it
   waits for has not happened (0009). When it happens, the premise stops holding, and
   stale-premise downstream brings the wait back. Any other condition for revisiting a
   decision stays in its prose.
8. **To keep a decision after its premise fails, decide again:** a new decision
   supersedes the old one and depends on whatever it rests on now.

## Acceptance records

`tests/acceptance/` holds fifteen records from this project's own history and nine
moments — seven from that history, two constructed — each with both questions answered
by hand. They were written
before any code, and `quebico check` must reproduce every answer (Step 2).
