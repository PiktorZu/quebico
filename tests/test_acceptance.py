"""Acceptance: the fifteen records and nine moments in tests/acceptance/ (0010).

A moment is written out as files — the records it lists, with the states its `set`
gives — and `quebico check` runs on those files, so the test goes through the same
path as the command line.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml

from quebico import Finding, check

ACCEPTANCE = Path(__file__).parent / "acceptance"


def _split(path: Path) -> tuple[dict[str, Any], str]:
    _, front_matter, body = path.read_text(encoding="utf-8").split("---\n", 2)
    return yaml.safe_load(front_matter), body


RECORDS = {
    _split(path)[0]["id"]: path
    for path in sorted((ACCEPTANCE / "records").glob("*.md"))
}
MOMENTS: list[dict[str, Any]] = yaml.safe_load(
    (ACCEPTANCE / "moments.yaml").read_text(encoding="utf-8")
)["moments"]


def materialize(moment: dict[str, Any], directory: Path) -> list[Path]:
    """Write the records of one moment into directory, with that moment's states."""
    states: dict[str, dict[str, Any]] = moment.get("set") or {}
    paths: list[Path] = []
    for record_id in moment["records"]:
        fields, body = _split(RECORDS[record_id])
        front_matter = yaml.safe_dump(
            fields | states.get(record_id, {}), sort_keys=False
        )
        path = directory / RECORDS[record_id].name
        path.write_text(f"---\n{front_matter}---\n{body}", encoding="utf-8")
        paths.append(path)
    return paths


def test_fixture_is_complete() -> None:
    assert len(RECORDS) == 15
    assert len(MOMENTS) == 9


def answers(findings: list[Finding]) -> tuple[set[tuple[str, ...]], set[str]]:
    """The stale-premise pairs and the orphan tasks, insisting on nothing else."""
    assert {f.code for f in findings} <= {"stale-premise", "orphan-task"}
    q1 = {f.ids for f in findings if f.code == "stale-premise"}
    q2 = {f.ids[0] for f in findings if f.code == "orphan-task"}
    return q1, q2


def test_the_fifteen_records_as_they_stand() -> None:
    """As of 2026-10-09 — the freeze-recorded moment — T2 is the one orphan."""
    assert answers(check(sorted(RECORDS.values()))) == (set(), {"T2"})


@pytest.mark.parametrize("moment", MOMENTS, ids=[m["name"] for m in MOMENTS])
def test_each_moment_is_answered_as_worked_by_hand(
    moment: dict[str, Any], tmp_path: Path
) -> None:
    expected = (
        {tuple(pair) for pair in moment["expect"]["q1"]},
        set(moment["expect"]["q2"]),
    )
    assert answers(check(materialize(moment, tmp_path))) == expected
