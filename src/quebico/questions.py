"""The two watch questions of docs/questions.md, asked of a record set with no data error."""

from quebico.records import Finding, Record

CODES = ("stale-premise", "orphan-task")


def _in_force(records: dict[str, Record]) -> set[str]:
    """Decisions that no decision supersedes, whatever that decision's own state."""
    superseded = {old for record in records.values() for old in record.supersedes}
    return {
        record_id
        for record_id, record in records.items()
        if record.kind == "decision" and record_id not in superseded
    }


def _named(record: Record) -> str:
    return f"{record.kind} {record.id} {record.title!r}"


def stale_premises(records: dict[str, Record]) -> list[Finding]:
    """Q1: each decision in force, with each failed premise it reaches along depends_on.

    The chain may pass through decisions in any state.
    """
    findings: list[Finding] = []
    for decision in (records[record_id] for record_id in _in_force(records)):
        seen: set[str] = set()
        todo = list(decision.depends_on)
        while todo:
            reached = records[todo.pop()]
            if reached.id in seen:
                continue
            seen.add(reached.id)
            todo.extend(reached.depends_on)
            if reached.kind == "premise" and not reached.holds:
                message = (
                    f"{_named(decision)} still stands on {_named(reached)},"
                    " which no longer holds"
                )
                ids = (decision.id, reached.id)
                findings.append(Finding("stale-premise", decision.path, message, ids))
    return sorted(findings, key=lambda finding: finding.ids)


def orphan_tasks(records: dict[str, Record]) -> list[Finding]:
    """Q2: each open task that serves no goal, directly or through a decision in force."""
    in_force = _in_force(records)

    def leads_to_a_goal(target: Record) -> bool:
        if target.kind == "goal":
            return True
        return target.id in in_force and any(
            records[goal].kind == "goal" for goal in target.serves
        )

    findings: list[Finding] = []
    for task in sorted(records.values(), key=lambda record: record.id):
        if task.kind != "task" or task.closed:
            continue
        if not any(leads_to_a_goal(records[target]) for target in task.serves):
            message = (
                f"open {_named(task)} serves no goal,"
                " directly or through a decision in force"
            )
            findings.append(Finding("orphan-task", task.path, message, (task.id,)))
    return findings
