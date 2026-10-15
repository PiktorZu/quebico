"""The Mermaid view: what `quebico graph` prints (0015, 0016), pinned with inline-snapshot
(0013).

The records here are written from dictionaries, so that titles full of what YAML,
Mermaid or HTML would misread need no quoting by hand.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml
from inline_snapshot import snapshot

from quebico import graph
from quebico.cli import main

REPOSITORY = Path(__file__).parent.parent


def write(directory: Path, records: list[dict[str, Any]]) -> list[Path]:
    paths: list[Path] = []
    for fields in records:
        path = directory / f"{fields['id']}.md"
        front_matter = yaml.safe_dump({"schema_version": 1, **fields}, sort_keys=False)
        path.write_text(f"---\n{front_matter}---\n", encoding="utf-8")
        paths.append(path)
    return paths


def test_the_acceptance_records_as_they_stand(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The naming saga is greyed out, being superseded or no longer holding, and T2,
    the one answer to the watch questions, is highlighted."""
    monkeypatch.chdir(REPOSITORY)
    assert main(["graph", "tests/acceptance/records"]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == snapshot("""\
```mermaid
flowchart LR
    n1["decision D1<br>Name the project<br>Omoikane"]:::inactive
    n2["decision D2<br>Tell the Omoikane myth<br>in the README"]:::inactive
    n3["decision D3<br>Rename the project to<br>Quebico"]
    n4["decision D4<br>Tell the Kuebiko story<br>in the README"]
    n5["decision D5<br>Hold the name on PyPI by<br>publishing an empty<br>0.0.1"]:::inactive
    n6["decision D6<br>Validate the schema on<br>paper against 15 real<br>records before writing<br>code"]
    n7["decision D7<br>Make the PyPI<br>placeholder optional and<br>never empty"]
    n8["decision D8<br>Defer the two proposed<br>reserved slots until the<br>questions are frozen"]:::inactive
    n9["decision D9<br>Freeze the two watch<br>questions that v0.1<br>answers"]
    n10(["goal G1<br>v0.1 answers the watch<br>questions on this<br>repository's own records"])
    n11(["goal G2<br>Keep a clear claim to<br>the name quebico"])
    n12[/"premise P1<br>No active project in<br>this space is called<br>Omoikane"/]:::inactive
    n13[/"premise P2<br>The watch questions have<br>not been frozen yet"/]:::inactive
    n14("task T1<br>Write the 15 acceptance<br>records")
    n15("task T2<br>Publish the empty 0.0.1<br>to PyPI"):::answer
    n1 -.->|depends_on| n12
    n2 -.->|depends_on| n1
    n3 ==>|supersedes| n1
    n4 -.->|depends_on| n3
    n4 ==>|supersedes| n2
    n5 -->|serves| n11
    n6 -->|serves| n10
    n7 -->|serves| n11
    n7 ==>|supersedes| n5
    n8 -.->|depends_on| n13
    n9 -->|serves| n10
    n9 ==>|supersedes| n8
    n14 -->|serves| n6
    n15 -->|serves| n5
    classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3
    classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000
```
""")


def test_every_kind_link_and_state(tmp_path: Path) -> None:
    records = [
        {"id": "G1", "kind": "goal", "title": "The goal"},
        {
            "id": "D1",
            "kind": "decision",
            "title": "In force, on a premise that holds",
            "serves": ["G1"],
            "depends_on": ["P1"],
        },
        {
            "id": "D2",
            "kind": "decision",
            "title": "In force, on a premise that no longer holds",
            "serves": ["G1"],
            "depends_on": ["P2"],
        },
        {
            "id": "D3",
            "kind": "decision",
            "title": "Supersedes D4",
            "supersedes": ["D4"],
        },
        {"id": "D4", "kind": "decision", "title": "Superseded by D3", "serves": ["G1"]},
        {"id": "P1", "kind": "premise", "title": "Holds"},
        {"id": "P2", "kind": "premise", "title": "No longer holds", "holds": False},
        {"id": "T1", "kind": "task", "title": "Open, serves D1", "serves": ["D1"]},
        {"id": "T2", "kind": "task", "title": "Open, serves only D4", "serves": ["D4"]},
        {
            "id": "T3",
            "kind": "task",
            "title": "Closed",
            "serves": ["G1"],
            "closed": True,
        },
    ]
    assert graph(write(tmp_path, records)) == snapshot("""\
```mermaid
flowchart LR
    n1["decision D1<br>In force, on a premise<br>that holds"]
    n2["decision D2<br>In force, on a premise<br>that no longer holds"]:::answer
    n3["decision D3<br>Supersedes D4"]
    n4["decision D4<br>Superseded by D3"]:::inactive
    n5(["goal G1<br>The goal"])
    n6[/"premise P1<br>Holds"/]
    n7[/"premise P2<br>No longer holds"/]:::inactive
    n8("task T1<br>Open, serves D1")
    n9("task T2<br>Open, serves only D4"):::answer
    n10("task T3<br>Closed"):::inactive
    n1 -->|serves| n5
    n1 -.->|depends_on| n6
    n2 -->|serves| n5
    n2 -.->|depends_on| n7
    n3 ==>|supersedes| n4
    n4 -->|serves| n5
    n8 -->|serves| n1
    n9 -->|serves| n4
    n10 -->|serves| n5
    classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3
    classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000
```
""")


def test_links_are_drawn_as_written_once_each(tmp_path: Path) -> None:
    """A cycle and a self-link are drawn like any other link, and a link given twice,
    once. Links keep the order they are written in; nodes follow the ids as text, so
    D10 comes before D2, and both before d3."""
    records = [
        {
            "id": "D1",
            "kind": "decision",
            "title": "Supersedes itself",
            "supersedes": ["D1"],
            "depends_on": ["D2", "D2"],
        },
        {"id": "D2", "kind": "decision", "title": "Rests on D1", "depends_on": ["D1"]},
        {
            "id": "D10",
            "kind": "decision",
            "title": "Rests on D2, then D1",
            "depends_on": ["D2", "D1"],
        },
        {
            "id": "d3",
            "kind": "decision",
            "title": "Supersedes D10",
            "supersedes": ["D10"],
        },
    ]
    assert graph(write(tmp_path, records)) == snapshot("""\
```mermaid
flowchart LR
    n1["decision D1<br>Supersedes itself"]:::inactive
    n2["decision D10<br>Rests on D2, then D1"]:::inactive
    n3["decision D2<br>Rests on D1"]
    n4["decision d3<br>Supersedes D10"]
    n1 -.->|depends_on| n3
    n1 ==>|supersedes| n1
    n2 -.->|depends_on| n3
    n2 -.->|depends_on| n1
    n3 -.->|depends_on| n1
    n4 ==>|supersedes| n2
    classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3
    classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000
```
""")


def test_titles_and_ids_cannot_break_the_diagram(tmp_path: Path) -> None:
    """Record ids never reach Mermaid's syntax, and a title shows as it is written,
    whatever it holds: only letters, digits, spaces and plain punctuation are written as
    themselves, the rest as entity codes such as #35;, and a word joiner (#8288;)
    splits what Mermaid reads even after decoding them. Titles wrap at spaces only."""
    records = [
        {
            "id": "end",
            "kind": "goal",
            "title": "`quebico check` fails only on data errors",
        },
        {
            "id": "o1",
            "kind": "decision",
            "title": 'Say "hi" & <b>bold</b>, #quot; and #35;<br>',
            "serves": ["end"],
            "depends_on": ["x-1"],
        },
        {
            "id": "x-1",
            "kind": "premise",
            "title": "%%{init: {'theme': 'dark'}}%% style:café; a/b [/ c /]",
        },
        {
            "id": "graph",
            "kind": "task",
            "title": "日本語の題, _not_ **bold**: see .quebico/inbox/0015-graph-prints.md",
            "serves": ["o1"],
        },
        {
            "id": "style",
            "kind": "decision",
            "title": "Strip \\r\\n from C:\\notes\\new.md | = ~ @ ^",
        },
        {
            "id": "classDef",
            "kind": "goal",
            "title": "fa:fa-car costs $$x^2$$, or $$}$$, and ﬂ°°1¶ß",
        },
    ]
    assert graph(write(tmp_path, records)) == snapshot("""\
```mermaid
flowchart LR
    n1(["goal classDef<br>fa#58;#8288;fa-car costs #36;#8288;#36;x#94;2#36;#8288;#36;,<br>or #36;#8288;#36;#125;#36;#8288;#36;, and #64258;#8288;#176;#176;1#182;#8288;#223;"])
    n2(["goal end<br>#96;quebico check#96; fails<br>only on data errors"])
    n3("task graph<br>#26085;#26412;#35486;#12398;#38988;, _not_ #42;#42;bold#42;#42;#58;<br>see<br>.quebico/inbox/0015-graph-prints.md")
    n4["decision o1<br>Say #34;hi#34; #38; #60;b#62;bold#60;/b#62;,<br>#35;quot#59; and #35;35#59;#60;br#62;"]
    n5["decision style<br>Strip #92;r#92;#8288;n from<br>C#58;#92;#8288;notes#92;#8288;new.md #124; #61; #126; #64;<br>#94;"]
    n6[/"premise x-1<br>#37;#37;#123;init#58; #123;'theme'#58;<br>'dark'#125;#125;#37;#37; style#58;caf#233;#59;<br>a/b #91;/ c /#93;"/]
    n3 -->|serves| n4
    n4 -->|serves| n2
    n4 -.->|depends_on| n6
    classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3
    classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000
```
""")


def test_a_data_error_gives_no_graph(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The errors go where `quebico graph > graph.md` cannot hide them in the file."""
    write(tmp_path, [{"id": "G1", "kind": "goal", "title": "A goal"}])
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    assert main(["graph", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (
        f"{tmp_path / 'a.md'}: front-matter: "
        "the file must open with a line of three dashes (---)\n"
        "quebico: 1 data error, so no graph\n"
    )


def test_no_records_give_an_empty_flowchart(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nowhere"
    assert main(["graph", str(missing)]) == 0
    captured = capsys.readouterr()
    assert captured.out == snapshot("""\
```mermaid
flowchart LR
    classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3
    classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000
```
""")
    assert (
        captured.err == f"quebico: {missing} does not exist, so there are no records\n"
    )


def test_the_default_directory_is_quebico_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    records = tmp_path / ".quebico" / "records"
    records.mkdir(parents=True)
    paths = write(records, [{"id": "G1", "kind": "goal", "title": "A goal"}])
    monkeypatch.chdir(tmp_path)
    assert main(["graph"]) == 0
    assert capsys.readouterr().out == graph(paths)


def test_a_file_in_place_of_the_directory_is_a_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("# Only prose\n", encoding="utf-8")
    with pytest.raises(SystemExit) as stopped:
        main(["graph", str(tmp_path / "a.md")])
    assert stopped.value.code == 2
    assert "is not a directory" in capsys.readouterr().err
