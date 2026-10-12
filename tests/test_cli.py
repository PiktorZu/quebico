"""The command line: what `quebico check` reads, prints and exits with (0011)."""

import os
import sys
from pathlib import Path

import pytest

from quebico.cli import main

GOAL = "---\nschema_version: 1\nid: G1\nkind: goal\ntitle: A goal\n---\n"
ACCEPTANCE_RECORDS = Path(__file__).parent / "acceptance" / "records"


def test_records_without_errors_exit_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "g.md").write_text(GOAL, encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 0
    assert capsys.readouterr().out == "checked 1 record: no data errors\n"


def test_a_data_error_exits_one_and_names_the_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 1
    assert capsys.readouterr().out == (
        f"{tmp_path / 'a.md'}: front-matter: "
        "the file must open with a line of three dashes (---)\n"
        "checked 1 record: 1 data error\n"
    )


def test_only_markdown_files_are_records(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "g.md").write_text(GOAL, encoding="utf-8")
    (tmp_path / "notes.txt").write_text("not a record", encoding="utf-8")
    (tmp_path / "README").write_text("not a record either", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 0
    assert capsys.readouterr().out == "checked 1 record: no data errors\n"


def test_records_are_found_at_any_depth(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    nested = tmp_path / "goals" / "2026"
    nested.mkdir(parents=True)
    (nested / "g.md").write_text(GOAL, encoding="utf-8")
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 1
    assert capsys.readouterr().out.endswith("checked 2 records: 1 data error\n")


def test_a_file_in_place_of_the_directory_is_a_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    with pytest.raises(SystemExit) as stopped:
        main(["check", str(tmp_path / "a.md")])
    assert stopped.value.code == 2
    assert "is not a directory" in capsys.readouterr().err


@pytest.mark.skipif(
    sys.platform != "linux", reason="needs a file name that is not UTF-8"
)
def test_output_survives_file_names_that_are_not_utf8(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / os.fsdecode(b"bad-\xff.md")).write_text(
        "# Only prose\n", encoding="utf-8"
    )
    assert main(["check", str(tmp_path)]) == 1
    assert "bad-\\udcff.md: front-matter: " in capsys.readouterr().out


def test_a_missing_directory_is_an_empty_record_set(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nowhere"
    assert main(["check", str(missing)]) == 0
    captured = capsys.readouterr()
    assert captured.out == "checked 0 records: no data errors\n"
    assert (
        captured.err == f"quebico: {missing} does not exist, so there are no records\n"
    )


def test_the_default_directory_is_quebico_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    records = tmp_path / ".quebico" / "records"
    records.mkdir(parents=True)
    (records / "g.md").write_text(GOAL, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert main(["check"]) == 0
    assert capsys.readouterr().out == "checked 1 record: no data errors\n"


def test_the_acceptance_records_pass(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check", str(ACCEPTANCE_RECORDS)]) == 0
    assert capsys.readouterr().out.endswith("checked 15 records: no data errors\n")
