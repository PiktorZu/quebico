"""Property: on any record set the schema allows, `quebico check` finds no data error,
and its answers are exactly those of the rules in docs/questions.md read the plainest
way — with depends_on closed under transitivity by repeated widening, not by a search.
`quebico graph` draws that same set faithfully: each record once, in its kind's shape
and its state, with its whole title, and each link once (0016)."""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from quebico import check, graph

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
# Any title the schema allows: one line, not blank.
TITLES = st.text(min_size=1).filter(lambda t: t.strip() != "" and t.splitlines() == [t])
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
            "title": draw(TITLES),
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


SHAPES = {
    "goal": ("([", "])"),
    "decision": ("[", "]"),
    "premise": ("[/", "/]"),
    "task": ("(", ")"),
}
ARROWS = {"serves": "-->", "depends_on": "-.->", "supersedes": "==>"}
NODE = re.compile(r'    (n\d+)(\(\[|\[/|\[|\()"([^"]*)"(\]\)|/\]|\]|\))(?::::(\w+))?')
EDGE = re.compile(r"    (n\d+) (-->|-\.->|==>)\|(\w+)\| (n\d+)")
ENTITY = re.compile(r"#(\d+);")
# What Mermaid reads in a label even after decoding its entity codes (0015)
READ_AGAIN = re.compile(r"\\n|:fa-|\$\$|\ufb02\xb0|\xb6\xdf")


def bare(text: str) -> str:
    """Text without whitespace or word joiners, which is what wrapping leaves alone."""
    return "".join(text.replace("\u2060", "").split())


def assert_faithful(records: Records, view: str, answered: set[str]) -> None:
    """The view draws each record and each link once, as `records` has them."""
    lines = view.splitlines()
    assert lines[:2] == ["```mermaid", "flowchart LR"]
    assert lines[-1] == "```"
    nodes = [match for match in map(NODE.fullmatch, lines) if match]
    edges = [match for match in map(EDGE.fullmatch, lines) if match]
    styles = [line for line in lines if line.startswith("    classDef ")]
    assert len(nodes) + len(edges) + len(styles) + 3 == len(lines)
    superseded = {old for f in records.values() for old in f.get("supersedes", [])}
    drawn: dict[str, str] = {}
    for node, start, label, end, state in (match.groups() for match in nodes):
        head, *title = label.split("<br>")
        kind, record_id = head.split(" ")
        fields = records[record_id]
        assert kind == fields["kind"] and (start, end) == SHAPES[kind]
        ended = (
            record_id in superseded
            or fields.get("closed")
            or not fields.get("holds", 1)
        )
        assert state == (
            "answer" if record_id in answered else "inactive" if ended else None
        )
        escaped = "".join(title)  # only plain text, the rest as entity codes
        assert escaped.isascii() and not set(ENTITY.sub("", escaped)) & set('"#%&:;<>`')
        shown = [ENTITY.sub(lambda code: chr(int(code[1])), line) for line in title]
        assert not any(READ_AGAIN.search(line) for line in shown)
        assert bare("".join(shown)) == bare(fields["title"])  # all of the title
        drawn[node] = record_id
    assert sorted(drawn.values()) == sorted(records)
    links = sorted((drawn[m[1]], m[3], drawn[m[4]]) for m in edges)
    assert all(ARROWS[m[3]] == m[2] for m in edges)
    assert links == sorted(
        {
            (i, link, to)
            for i, f in records.items()
            for link in ARROWS
            for to in f.get(link, [])
        }
    )


@given(records=record_sets())
def test_answers_and_graph_follow_the_rules(
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
    q1, q2 = expected_answers(records)
    assert (stale, orphans) == (q1, q2)
    view = graph(paths)
    assert isinstance(view, str)
    assert_faithful(records, view, {decision for decision, _ in q1} | q2)
