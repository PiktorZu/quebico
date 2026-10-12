"""Acceptance: the fifteen records and nine moments in tests/acceptance/ (0010).

A moment is written out as files — the records it lists, with the states its `set`
gives — and `quebico check` runs on those files, so the test goes through the same
path as the command line.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml

from quebico import check

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


def test_the_fifteen_records_have_no_data_error() -> None:
    assert check(sorted(RECORDS.values())) == []


@pytest.mark.parametrize("moment", MOMENTS, ids=[m["name"] for m in MOMENTS])
def test_no_moment_has_a_data_error(moment: dict[str, Any], tmp_path: Path) -> None:
    assert check(materialize(moment, tmp_path)) == []
