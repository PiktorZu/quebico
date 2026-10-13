"""The watch questions (docs/questions.md): one row per small record set and its answers.

A record is written on one line: its id and kind, then its links and state, such as
"D1 decision serves=G1 depends_on=P1,D2" or "P1 premise holds=false". Each row gives
the stale-premise pairs (decision, premise) and the orphan tasks it must report.
"""

from pathlib import Path

import pytest

from quebico import check


def write(directory: Path, lines: list[str]) -> list[Path]:
    paths: list[Path] = []
    for line in lines:
        record_id, kind, *rest = line.split()
        fields = ["schema_version: 1", f"id: {record_id}", f"kind: {kind}"]
        fields.append(f"title: Record {record_id}")
        for item in rest:
            name, value = item.split("=")
            state = name in ("closed", "holds")
            fields.append(f"{name}: {value}" if state else f"{name}: [{value}]")
        path = directory / f"{record_id}.md"
        path.write_text("---\n" + "\n".join(fields) + "\n---\n", encoding="utf-8")
        paths.append(path)
    return paths


Pairs = list[tuple[str, str]]
ROWS: list[tuple[str, list[str], Pairs, list[str]]] = [
    ("no records", [], [], []),
    # Q1: decisions in force that still stand on a premise that no longer holds
    (
        "a decision on a premise that no longer holds",
        ["D1 decision depends_on=P1", "P1 premise holds=false"],
        [("D1", "P1")],
        [],
    ),
    (
        "a premise that still holds",
        ["D1 decision depends_on=P1", "P1 premise"],
        [],
        [],
    ),
    (
        "a premise recorded as holding",
        ["D1 decision depends_on=P1", "P1 premise holds=true"],
        [],
        [],
    ),
    (
        "a superseded decision is not reported",
        [
            "D1 decision depends_on=P1",
            "P1 premise holds=false",
            "D2 decision supersedes=D1",
        ],
        [],
        [],
    ),
    (
        "the chain runs through decisions in force",
        [
            "D2 decision depends_on=D1",
            "D1 decision depends_on=P1",
            "P1 premise holds=false",
        ],
        [("D1", "P1"), ("D2", "P1")],
        [],
    ),
    (
        "a long chain",
        [
            "D4 decision depends_on=D3",
            "D3 decision depends_on=D2",
            "D2 decision depends_on=D1",
            "D1 decision depends_on=P1",
            "P1 premise holds=false",
        ],
        [("D1", "P1"), ("D2", "P1"), ("D3", "P1"), ("D4", "P1")],
        [],
    ),
    (
        "the chain runs through a superseded decision",
        [
            "D2 decision depends_on=D1",
            "D1 decision depends_on=P1",
            "P1 premise holds=false",
            "D3 decision supersedes=D1",
        ],
        [("D2", "P1")],
        [],
    ),
    (
        "two ways to one premise give one pair",
        [
            "D1 decision depends_on=D2,D3",
            "D2 decision depends_on=P1",
            "D3 decision depends_on=P1",
            "P1 premise holds=false",
        ],
        [("D1", "P1"), ("D2", "P1"), ("D3", "P1")],
        [],
    ),
    (
        "two failed premises give two pairs",
        [
            "D1 decision depends_on=P1,P2",
            "P1 premise holds=false",
            "P2 premise holds=false",
        ],
        [("D1", "P1"), ("D1", "P2")],
        [],
    ),
    (
        "a cycle of depends_on",
        [
            "D1 decision depends_on=D2",
            "D2 decision depends_on=D1,P1",
            "P1 premise holds=false",
        ],
        [("D1", "P1"), ("D2", "P1")],
        [],
    ),
    (
        "a decision that depends on itself",
        ["D1 decision depends_on=D1,P1", "P1 premise holds=false"],
        [("D1", "P1")],
        [],
    ),
    (
        "a decision that supersedes itself is not in force",
        ["D1 decision depends_on=P1 supersedes=D1", "P1 premise holds=false"],
        [],
        [],
    ),
    (
        "superseded, even by a decision that is itself superseded",
        [
            "D1 decision depends_on=P1",
            "P1 premise holds=false",
            "D2 decision supersedes=D1",
            "D3 decision supersedes=D2",
        ],
        [],
        [],
    ),
    (
        "only the decision is reported, not the task that serves it",
        [
            "T1 task serves=D1",
            "D1 decision serves=G1 depends_on=P1",
            "G1 goal",
            "P1 premise holds=false",
        ],
        [("D1", "P1")],
        [],
    ),
    # Q2: open tasks that serve no goal, directly or through a decision in force
    ("a task that serves a goal", ["T1 task serves=G1", "G1 goal"], [], []),
    ("a task that serves nothing", ["T1 task"], [], ["T1"]),
    ("a task with an empty serves", ["T1 task serves="], [], ["T1"]),
    ("a closed task is never reported", ["T1 task closed=true"], [], []),
    ("a task recorded as open", ["T1 task closed=false"], [], ["T1"]),
    (
        "a task through a decision in force",
        ["T1 task serves=D1", "D1 decision serves=G1", "G1 goal"],
        [],
        [],
    ),
    (
        "a task through a decision that serves no goal",
        ["T1 task serves=D1", "D1 decision"],
        [],
        ["T1"],
    ),
    (
        "a task through a superseded decision",
        [
            "T1 task serves=D1",
            "D1 decision serves=G1",
            "G1 goal",
            "D2 decision serves=G1 supersedes=D1",
        ],
        [],
        ["T1"],
    ),
    (
        "one way to a goal is enough",
        ["T1 task serves=D1,G1", "D1 decision", "G1 goal"],
        [],
        [],
    ),
    (
        "depends_on is not a way to a goal",
        [
            "T1 task serves=D2",
            "D2 decision depends_on=D1",
            "D1 decision serves=G1",
            "G1 goal",
        ],
        [],
        ["T1"],
    ),
    (
        "a task through a decision that supersedes itself",
        ["T1 task serves=D1", "D1 decision serves=G1 supersedes=D1", "G1 goal"],
        [],
        ["T1"],
    ),
]


@pytest.mark.parametrize(
    ("lines", "q1", "q2"),
    [pytest.param(lines, q1, q2, id=name) for name, lines, q1, q2 in ROWS],
)
def test_watch_questions(
    tmp_path: Path, lines: list[str], q1: Pairs, q2: list[str]
) -> None:
    findings = check(write(tmp_path, lines))
    assert {f.code for f in findings} <= {"stale-premise", "orphan-task"}
    assert sorted(f.ids for f in findings if f.code == "stale-premise") == sorted(q1)
    assert sorted(f.ids[0] for f in findings if f.code == "orphan-task") == sorted(q2)


def test_the_questions_wait_for_records_without_data_errors(tmp_path: Path) -> None:
    paths = write(tmp_path, ["T1 task"])
    broken = tmp_path / "broken.md"
    broken.write_text("# Only prose\n", encoding="utf-8")
    assert [f.code for f in check([*paths, broken])] == ["front-matter"]


def test_answers_come_in_the_order_of_their_ids(tmp_path: Path) -> None:
    decisions = [f"D{n} decision depends_on=P1" for n in range(1, 9)]
    tasks = [f"T{n} task" for n in range(1, 9)]
    lines = [*reversed(decisions), "P1 premise holds=false", *reversed(tasks)]
    pairs = [(f"D{n}", "P1") for n in range(1, 9)]
    orphans = [(f"T{n}",) for n in range(1, 9)]
    assert [f.ids for f in check(write(tmp_path, lines))] == [*pairs, *orphans]
