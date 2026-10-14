"""The command line: what `quebico check` reads, prints and exits with (0011)."""

import os
import sys
from pathlib import Path

import pytest
from inline_snapshot import snapshot

from quebico.cli import main

GOAL = "---\nschema_version: 1\nid: G1\nkind: goal\ntitle: A goal\n---\n"
REPOSITORY = Path(__file__).parent.parent
NOTHING_FOUND = "no data errors, 0 stale-premise, 0 orphan-task"


def test_records_without_errors_exit_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "g.md").write_text(GOAL, encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 0
    assert capsys.readouterr().out == f"checked 1 record: {NOTHING_FOUND}\n"


def test_a_data_error_exits_one_and_names_the_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 1
    assert capsys.readouterr().out == (
        f"{tmp_path / 'a.md'}: front-matter: "
        "the file must open with a line of three dashes (---)\n"
        "checked 1 record: 1 data error (watch questions skipped)\n"
    )


def test_only_markdown_files_are_records(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "g.md").write_text(GOAL, encoding="utf-8")
    (tmp_path / "notes.txt").write_text("not a record", encoding="utf-8")
    (tmp_path / "README").write_text("not a record either", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 0
    assert capsys.readouterr().out == f"checked 1 record: {NOTHING_FOUND}\n"


def test_records_are_found_at_any_depth(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    nested = tmp_path / "goals" / "2026"
    nested.mkdir(parents=True)
    (nested / "g.md").write_text(GOAL, encoding="utf-8")
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    assert main(["check", str(tmp_path)]) == 1
    assert capsys.readouterr().out.endswith(
        "checked 2 records: 1 data error (watch questions skipped)\n"
    )


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
    assert captured.out == f"checked 0 records: {NOTHING_FOUND}\n"
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
    assert capsys.readouterr().out == f"checked 1 record: {NOTHING_FOUND}\n"


def test_the_answers_are_printed_but_do_not_fail_the_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    records = tmp_path / "records"
    records.mkdir()
    for name, front_matter in {
        "D1.md": "id: D1\nkind: decision\ntitle: Name it Omoikane\ndepends_on: [P1]",
        "D2.md": "id: D2\nkind: decision\ntitle: Tell its myth\ndepends_on: [D1]",
        "P1.md": "id: P1\nkind: premise\ntitle: No one else uses Omoikane\nholds: false",
        "T1.md": "id: T1\nkind: task\ntitle: Publish an empty 0.0.1",
    }.items():
        content = f"---\nschema_version: 1\n{front_matter}\n---\n"
        (records / name).write_text(content, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert main(["check", "records"]) == 0
    assert capsys.readouterr().out == snapshot("""\
records/D1.md: stale-premise: decision D1 'Name it Omoikane' still stands on premise P1 'No one else uses Omoikane', which no longer holds
records/D2.md: stale-premise: decision D2 'Tell its myth' still stands on premise P1 'No one else uses Omoikane', which no longer holds
records/T1.md: orphan-task: open task T1 'Publish an empty 0.0.1' serves no goal, directly or through a decision in force
checked 4 records: no data errors, 2 stale-premise, 1 orphan-task
""")


def test_the_acceptance_records_as_they_stand(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(REPOSITORY)
    assert main(["check", "tests/acceptance/records"]) == 0
    assert capsys.readouterr().out == snapshot("""\
tests/acceptance/records/T2-publish-placeholder.md: orphan-task: open task T2 'Publish the empty 0.0.1 to PyPI' serves no goal, directly or through a decision in force
checked 15 records: no data errors, 0 stale-premise, 1 orphan-task
""")
