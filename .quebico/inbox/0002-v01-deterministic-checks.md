# 0002 — v0.1 answers questions: two deterministic checks and a Mermaid view

**Decided:** the "visualization" in v0.1 is replaced by two structural checks that run
over the graph with no LLM involved, plus a Mermaid view:

- **Stale-premise downstream** — decisions that depend on a premise marked as no longer
  holding and have no recorded reconsideration.
- **Orphan tasks** — tasks with no path to any goal.
- **Mermaid export** — GitHub renders it as-is. Visualization in v0.1 stops there.

**Why:** v0.1 exists to show that the schema was derived from the questions. A picture
cannot show that; an answer can. A deterministic check can be judged yes or no against
hand-worked expected answers, and its precision depends only on the quality of the data,
so the first time Quebico argues back it does so with the least risk of a false alarm.
It is also less code than a bespoke visualization.

The risk-ordered plan (2026-08-29) paired stale-premise downstream with *decisions
without recorded rationale* and left orphan tasks conditional. A look at comparable
tools on 2026-09-20 changed the pair. KaelinGraf/redraft already reports decisions with
no recorded rationale, so shipping that check would show nothing new, and generic
orphan-node checks exist as well (decisiongraph/dg, redraft). What none of the tools
surveyed does is ask whether a task has a path to a goal, or follow a premise that no
longer holds to the decisions still standing on it.

**Rejected:**

- *Visualization as the v0.1 deliverable.* A graph can look right while answering
  nothing, and "looks right" cannot be judged yes or no.
- *Decisions without recorded rationale as a required check.* Already done elsewhere;
  it proves nothing about this schema.
- *An interactive viewer or a web UI.* Not until a Mermaid view stops being readable.

**Consequences:**

- Step 1: the 15 real records must include two or three real tasks, or the orphan-task
  check has nothing to answer. If tasks cannot be expressed, that is a schema defect to
  fix before any code is written.
- Step 2: the orphan-task check is built unconditionally.
- If the schedule slips, the cut order is now: move the English write-up back one week,
  then drop the Mermaid view. Neither check is cut, and Step 1 and Step 3 are never cut.
- The README roadmap is updated to match.
