---
schema_version: 1
id: D29
kind: decision
title: Draw records left to right, a shape per kind, a line per link
depends_on: [D28]
---

Was inbox 0016 (#11).

**Decided:** `quebico graph` (0015) draws a record set like this:

- **Left to right** (`flowchart LR`). Every arrow points from a record to what it serves,
  rests on or supersedes, so tasks sit on the left, and goals, premises and older
  decisions toward the right.
- **A shape per kind**: a goal is a stadium, a decision a rectangle, a premise a
  parallelogram, a task a rounded rectangle. Each label opens with the kind and the id
  (`decision D4`), then the title, wrapped at spaces to lines of about 24 characters.
- **A line per link, with its name**: `serves` solid, `depends_on` dotted, `supersedes`
  thick. A link given twice is drawn once; a cycle or a self-link is drawn as it is.
- **Two states drawn apart**: whatever is no longer live — a superseded decision, a
  closed task, a premise that no longer holds — is grey with a dashed border. The
  answers to the watch questions — a decision in stale-premise downstream, an orphan
  task — are filled orange.
- **Node ids `n1`, `n2`, …** in the order of the record ids. The record id appears only
  in the label.

**Why:** a Mermaid flowchart has no legend, and GitHub shows the picture alone. The kind
in each label and the name on each line let it be read without one; the shapes and line
styles then let the eye group what the words say.

Left to right keeps the view legible as the records grow. A record set grows mostly in
breadth — more decisions and tasks side by side — and left to right turns breadth into
height, which scrolls, where top to bottom turns it into width, which GitHub shrinks to
fit. On the fifteen acceptance records the two come out about as wide.

Grey for everything no longer live lets the live graph stand out. On this project's own
history it greys the Omoikane saga — the name, the myth, the premise that failed — which
is what happened. A failed premise is grey, not red: P1 and P2 no longer hold, but
nothing stands on them any more, and red would raise an alarm no answer backs.

Highlighting the answers puts the two questions on the map. From a highlighted decision,
the dotted lines lead to the failed premise behind it, which the written answer names
only at its two ends (0014).

Lines of about 24 characters keep nodes narrow on Mermaid 10, which does not wrap
labels, and within the width at which Mermaid 11 wraps them itself. Quebico wraps only
at spaces, so that paths, URLs and identifiers stay whole; Mermaid 11 may still break
one wider than its own line at a hyphen. A title in a script written without spaces,
such as Japanese, is not wrapped by Quebico: Mermaid 11 wraps it itself, and Mermaid 10
draws it on one long line. Numbered node ids, because a record id can be a
Mermaid keyword (`end`) or begin like an edge (`o1`, `x1`).

The views were rendered and checked with Mermaid 10.9 and 11.16, in light and dark
themes.

**Rejected:**

- *Top to bottom, or bottom to top.* See above.
- *A legend drawn as a subgraph.* Clutter in every view; the labels carry it.
- *A colour per question.* The shape already tells a decision (stale-premise) from a
  task (orphan), and `quebico check` words the answer.
- *A diamond for decisions*, the flowchart sign for a branch. A decision here is a choice
  already made, and a diamond around a long title grows very large.
- *Subgraphs by kind.* They constrain the layout, and the shapes already tell kinds apart.
- *Breaking long words* so that no node grows wide. A broken path or URL reads worse
  than a wide node.

**Revisit:** when the Step 3 reviews look at how the view is used, or when it stops
being readable as the records grow, which is the condition 0002 set for looking past
Mermaid.
