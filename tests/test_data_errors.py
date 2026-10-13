"""Data errors (docs/schema.md): one row per small record set and the errors it raises.

Each row names the files to write and the (error, file) pairs `quebico check` must
report, one pair per error. The five errors follow the list in docs/schema.md:
front-matter, field-value, unexpected-field, duplicate-id, bad-link. A row with data
errors must report nothing else, since the watch questions wait for a record set with
none; the answers on a valid row are left to tests/test_questions.py.
"""

from pathlib import Path

import pytest

from quebico import check

GOAL = "schema_version: 1\nid: G1\nkind: goal\ntitle: A goal"
TASK = "schema_version: 1\nid: T1\nkind: task\ntitle: A task"
DECISION = "schema_version: 1\nid: D1\nkind: decision\ntitle: A decision"
PREMISE = "schema_version: 1\nid: P1\nkind: premise\ntitle: A premise"


def md(front_matter: str) -> str:
    return f"---\n{front_matter}\n---\n\nProse that only people read.\n"


def alias_bomb(levels: int = 9) -> str:
    """A title nine lists deep through aliases: short to write, 9**9 items to print."""
    lists = ["&l0 [" + ", ".join(["x"] * 9) + "]"]
    lists += [
        f"&l{n} [" + ", ".join([f"*l{n - 1}"] * 9) + "]" for n in range(1, levels)
    ]
    return "title: [" + ", ".join(lists) + "]"


ROWS: list[tuple[str, dict[str, str | bytes], list[tuple[str, str]]]] = [
    (
        "every kind and link the schema allows",
        {
            "g.md": md(GOAL),
            "d.md": md(DECISION + "\nserves: [G1]\ndepends_on: [P1]\nsupersedes: []"),
            "p.md": md(PREMISE + "\nholds: false"),
            "t.md": md(TASK + "\nserves: [D1, G1]\nclosed: true"),
        },
        [],
    ),
    # 1. front matter missing, or not valid YAML
    ("no front matter", {"a.md": "# Only prose\n"}, [("front-matter", "a.md")]),
    ("empty file", {"a.md": ""}, [("front-matter", "a.md")]),
    (
        "front matter never closed",
        {"a.md": f"---\n{GOAL}\n"},
        [("front-matter", "a.md")],
    ),
    (
        "not valid YAML",
        {"a.md": md(GOAL + "\nserves: [G1")},
        [("front-matter", "a.md")],
    ),
    ("front matter is a list", {"a.md": md("- G1\n- G2")}, [("front-matter", "a.md")]),
    ("not UTF-8", {"a.md": b"---\nid: \xff\n---\n"}, [("front-matter", "a.md")]),
    (
        "a key given twice",
        {"a.md": md(DECISION + "\ndepends_on: [D1]\ndepends_on: [D1]")},
        [("front-matter", "a.md")],
    ),
    # 2. a required field missing, or a value the table does not allow
    ("empty front matter", {"a.md": "---\n---\n"}, [("field-value", "a.md")] * 4),
    (
        "missing id",
        {"a.md": md(GOAL.replace("id: G1\n", ""))},
        [("field-value", "a.md")],
    ),
    (
        "schema_version 2",
        {"a.md": md(GOAL.replace("schema_version: 1", "schema_version: 2"))},
        [("field-value", "a.md")],
    ),
    (
        "schema_version true",
        {"a.md": md(GOAL.replace("schema_version: 1", "schema_version: true"))},
        [("field-value", "a.md")],
    ),
    (
        "schema_version 1.0",
        {"a.md": md(GOAL.replace("schema_version: 1", "schema_version: 1.0"))},
        [("field-value", "a.md")],
    ),
    (
        "schema_version quoted",
        {"a.md": md(GOAL.replace("schema_version: 1", 'schema_version: "1"'))},
        [("field-value", "a.md")],
    ),
    (
        "id starts with a digit",
        {"a.md": md(GOAL.replace("id: G1", "id: 1G"))},
        [("field-value", "a.md")],
    ),
    (
        "id with an underscore",
        {"a.md": md(GOAL.replace("id: G1", "id: G_1"))},
        [("field-value", "a.md")],
    ),
    (
        "id not ASCII",
        {"a.md": md(GOAL.replace("id: G1", "id: Ｇ1"))},
        [("field-value", "a.md")],
    ),
    (
        "unknown kind",
        {"a.md": md(GOAL.replace("kind: goal", "kind: issue"))},
        [("field-value", "a.md")],
    ),
    (
        "title left empty",
        {"a.md": md(GOAL.replace("title: A goal", "title:"))},
        [("field-value", "a.md")],
    ),
    (
        "title blank",
        {"a.md": md(GOAL.replace("title: A goal", 'title: "  "'))},
        [("field-value", "a.md")],
    ),
    (
        "title on two lines",
        {"a.md": md(GOAL.replace("title: A goal", "title: |\n  One\n  Two"))},
        [("field-value", "a.md")],
    ),
    (
        "title ending in a line break",
        {"a.md": md(GOAL.replace("title: A goal", 'title: "One\\n"'))},
        [("field-value", "a.md")],
    ),
    (
        "closed spelled yes",
        {"a.md": md(TASK + "\nclosed: yes")},
        [("field-value", "a.md")],
    ),
    (
        "closed spelled True",
        {"a.md": md(TASK + "\nclosed: True")},
        [("field-value", "a.md")],
    ),
    (
        "holds spelled off",
        {"a.md": md(PREMISE + "\nholds: off")},
        [("field-value", "a.md")],
    ),
    (
        "holds quoted",
        {"a.md": md(PREMISE + '\nholds: "false"')},
        [("field-value", "a.md")],
    ),
    (
        "link not a list",
        {"g.md": md(GOAL), "t.md": md(TASK + "\nserves: G1")},
        [("field-value", "t.md")],
    ),
    (
        "link to a number",
        {"t.md": md(TASK + "\nserves: [1]")},
        [("field-value", "t.md")],
    ),
    (
        "link to text that is not an id",
        {"t.md": md(TASK + '\nserves: ["\\ud800"]')},
        [("field-value", "t.md")],
    ),
    (
        "closed tagged !!bool yes",
        {"a.md": md(TASK + "\nclosed: !!bool yes")},
        [("field-value", "a.md")],
    ),
    (
        "number too long to print",
        {
            "a.md": md(
                GOAL.replace(
                    "schema_version: 1", "schema_version: !!int 0x" + "f" * 4000
                )
            )
        },
        [("field-value", "a.md")],
    ),
    (
        "title too large to print",
        {"a.md": md(GOAL.replace("title: A goal", alias_bomb()))},
        [("field-value", "a.md")],
    ),
    (
        "no kind, and a field no kind has",
        {"a.md": md(DECISION.replace("kind: decision\n", "") + "\ndepend_on: [D1]")},
        [("field-value", "a.md"), ("unexpected-field", "a.md")],
    ),
    (
        "unknown kind, and a field no kind has",
        {"a.md": md(GOAL.replace("kind: goal", "kind: Goal") + "\nfoo: bar")},
        [("field-value", "a.md"), ("unexpected-field", "a.md")],
    ),
    # YAML would read these as booleans, dates or numbers; the schema reads strings
    (
        "id NO stays a string",
        {
            "g.md": md(GOAL.replace("id: G1", "id: NO")),
            "t.md": md(TASK + "\nserves: [NO]"),
        },
        [],
    ),
    (
        "title that looks like a date",
        {"a.md": md(GOAL.replace("title: A goal", "title: 2026-10-10"))},
        [],
    ),
    (
        "title that looks like a number",
        {"a.md": md(GOAL.replace("title: A goal", "title: 09"))},
        [],
    ),
    # 3. a field the table does not list, or lists only for other kinds
    (
        "misspelled link",
        {"p.md": md(PREMISE), "d.md": md(DECISION + "\ndepend_on: [P1]")},
        [("unexpected-field", "d.md")],
    ),
    (
        "state of another kind",
        {"a.md": md(TASK + "\nholds: true")},
        [("unexpected-field", "a.md")],
    ),
    (
        "link on a goal",
        {"a.md": md(GOAL + "\nserves: [G1]")},
        [("unexpected-field", "a.md")],
    ),
    (
        "depends_on on a task",
        {"a.md": md(TASK + "\ndepends_on: []")},
        [("unexpected-field", "a.md")],
    ),
    # 4. two records with the same id
    ("same id twice", {"a.md": md(GOAL), "b.md": md(GOAL)}, [("duplicate-id", "b.md")]),
    (
        "ids that differ only in case",
        {"a.md": md(GOAL), "b.md": md(GOAL.replace("id: G1", "id: g1"))},
        [],
    ),
    (
        "the links of a record with a taken id are still checked",
        {
            "a.md": md(GOAL),
            "b.md": md(TASK.replace("id: T1", "id: G1") + "\nserves: [G9]"),
        },
        [("duplicate-id", "b.md"), ("bad-link", "b.md")],
    ),
    # 5. a link to an id no record has, or to a kind its term does not allow
    (
        "link to a missing id",
        {"t.md": md(TASK + "\nserves: [G9]")},
        [("bad-link", "t.md")],
    ),
    (
        "link in the wrong case",
        {"g.md": md(GOAL), "t.md": md(TASK + "\nserves: [g1]")},
        [("bad-link", "t.md")],
    ),
    (
        "task serves a premise",
        {"p.md": md(PREMISE), "t.md": md(TASK + "\nserves: [P1]")},
        [("bad-link", "t.md")],
    ),
    (
        "decision serves a decision",
        {
            "d.md": md(DECISION + "\nserves: [D2]"),
            "e.md": md(DECISION.replace("id: D1", "id: D2")),
        },
        [("bad-link", "d.md")],
    ),
    (
        "decision depends on a goal",
        {"g.md": md(GOAL), "d.md": md(DECISION + "\ndepends_on: [G1]")},
        [("bad-link", "d.md")],
    ),
    (
        "decision supersedes a task",
        {"t.md": md(TASK), "d.md": md(DECISION + "\nsupersedes: [T1]")},
        [("bad-link", "d.md")],
    ),
    (
        "the links of a record with an invalid id are still checked",
        {"t.md": md(TASK.replace("id: T1", "id: 1T") + "\nserves: [G9]")},
        [("field-value", "t.md"), ("bad-link", "t.md")],
    ),
    # allowed, though unusual
    (
        "id with a hyphen",
        {
            "g.md": md(GOAL.replace("id: G1", "id: G-1")),
            "t.md": md(TASK + "\nserves: [G-1]"),
        },
        [],
    ),
    (
        "decision that links to itself",
        {"d.md": md(DECISION + "\ndepends_on: [D1]\nsupersedes: [D1]")},
        [],
    ),
    (
        "Windows line endings and a byte-order mark",
        {"g.md": "\ufeff" + md(GOAL).replace("\n", "\r\n")},
        [],
    ),
]


@pytest.mark.parametrize(
    ("files", "expected"),
    [pytest.param(files, expected, id=name) for name, files, expected in ROWS],
)
def test_data_errors(
    tmp_path: Path, files: dict[str, str | bytes], expected: list[tuple[str, str]]
) -> None:
    for name, content in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_bytes(content.encode("utf-8"))
    findings = check(sorted(tmp_path.rglob("*.md")))
    if not expected:  # a valid record set: its answers are tested elsewhere
        findings = [
            f for f in findings if f.code not in ("stale-premise", "orphan-task")
        ]
    got = sorted((f.code, f.path.relative_to(tmp_path).as_posix()) for f in findings)
    assert got == sorted(expected)
