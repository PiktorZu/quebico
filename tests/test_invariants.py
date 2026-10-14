"""Property: on any record set the schema allows, `quebico check` finds no data error,
and its answers are exactly those of the rules in docs/questions.md read the plainest
way — with depends_on closed under transitivity by repeated widening, not by a search."""

from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from quebico import check

KINDS = ("goal", "task", "decision", "premise")
# docs/schema.md: the links each kind holds, and the kinds each may point to
LINKS = {
    "task": {"serves": ("decision", "goal")},
    "decision": {
        "serves": ("goal",),
        "depends_on": ("premise", "decision"),
        "supersedes": ("decision",),
    },
}
Records = dict[str, dict[str, Any]]


@st.composite
def record_sets(draw: st.DrawFn) -> Records:
    kinds = draw(st.lists(st.sampled_from(KINDS), min_size=1, max_size=10))
    kind_of = {f"{kind[0].upper()}{n}": kind for n, kind in enumerate(kinds)}
    records: Records = {}
    for record_id, kind in kind_of.items():
        fields: dict[str, Any] = {
            "schema_version": 1,
            "id": record_id,
            "kind": kind,
            "title": f"Record {record_id}",
        }
        for link, targets in LINKS.get(kind, {}).items():
            choices = [other for other, k in kind_of.items() if k in targets]
            if choices and draw(st.booleans()):
                fields[link] = draw(st.lists(st.sampled_from(choices), max_size=3))
        if kind == "task":
            fields["closed"] = draw(st.booleans())
        if kind == "premise":
            fields["holds"] = draw(st.booleans())
        records[record_id] = fields
    return records


def expected_answers(records: Records) -> tuple[set[tuple[str, ...]], set[str]]:
    def kind(record_id: str) -> str:
        return records[record_id]["kind"]

    superseded = {old for f in records.values() for old in f.get("supersedes", [])}
    in_force = {i for i in records if kind(i) == "decision" and i not in superseded}
    reach = {i: set(f.get("depends_on", [])) for i, f in records.items()}
    widened = True
    while widened:
        widened = False
        for record_id, reached in reach.items():
            wider = reached.union(*(reach[other] for other in reached))
            if wider != reached:
                reach[record_id], widened = wider, True
    q1 = {
        (decision, premise)
        for decision in in_force
        for premise in reach[decision]
        if kind(premise) == "premise" and records[premise]["holds"] is False
    }

    def to_a_goal(target: str) -> bool:
        serves = records[target].get("serves", [])
        return kind(target) == "goal" or (
            target in in_force and any(kind(goal) == "goal" for goal in serves)
        )

    q2 = {
        task
        for task, fields in records.items()
        if kind(task) == "task"
        and fields["closed"] is False
        and not any(to_a_goal(target) for target in fields.get("serves", []))
    }
    return q1, q2


@given(records=record_sets())
def test_answers_follow_the_rules(
    tmp_path_factory: pytest.TempPathFactory, records: Records
) -> None:
    directory = tmp_path_factory.mktemp("records")
    paths: list[Path] = []
    for record_id, fields in records.items():
        path = directory / f"{record_id}.md"
        front_matter = yaml.safe_dump(fields, sort_keys=False)
        path.write_text(f"---\n{front_matter}---\n", encoding="utf-8")
        paths.append(path)
    findings = check(paths)
    assert {f.code for f in findings} <= {"stale-premise", "orphan-task"}
    stale = {f.ids for f in findings if f.code == "stale-premise"}
    orphans = {f.ids[0] for f in findings if f.code == "orphan-task"}
    assert (stale, orphans) == expected_answers(records)
