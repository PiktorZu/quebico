"""Property: whatever a file under the records directory holds, `quebico check` answers
with data errors, never with an exception."""

from pathlib import Path

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from quebico import check

DATA_ERRORS = {
    "front-matter",
    "field-value",
    "unexpected-field",
    "duplicate-id",
    "bad-link",
}
FIELDS = [
    "schema_version",
    "id",
    "kind",
    "title",
    "serves",
    "depends_on",
    "supersedes",
    "closed",
    "holds",
    "other",
]
VALUES = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats() | st.text(),
    lambda inner: (
        st.lists(inner, max_size=3) | st.dictionaries(st.text(), inner, max_size=3)
    ),
    max_leaves=6,
)
FRONT_MATTER = st.dictionaries(st.sampled_from(FIELDS), VALUES).map(
    lambda fields: f"---\n{yaml.safe_dump(fields)}---\n"
)
# YAML that a dictionary dumped by PyYAML never contains: tags, anchors and aliases,
# repeated keys, complex keys, block scalars.
TRICKY_YAML = st.lists(
    st.sampled_from(
        [
            "id: &a G1",
            "id: G1",
            "kind: task",
            "kind: decision",
            "title: *a",
            "title: |\n  two\n  lines",
            "title: !!timestamp 2026-10-10",
            "title: !!binary aGk=",
            "serves: [*a, G1]",
            "depends_on: !!set {a, b}",
            "closed: !!bool yes",
            "holds: !!bool false",
            "schema_version: !!int 0x1",
            "schema_version: !!float 1",
            '"x\\ud800": 1',
            "? [a, b]\n: c",
            "loop: &b [*b]",
        ]
    ),
    max_size=8,
).map(lambda lines: "---\n" + "\n".join(lines) + "\n---\n")
CONTENT = st.one_of(
    st.binary(),
    st.text(),
    st.text().map(lambda text: f"---\n{text}\n---\n"),
    FRONT_MATTER,
    TRICKY_YAML,
)


@given(contents=st.lists(CONTENT, min_size=1, max_size=3))
def test_any_files_give_data_errors_not_exceptions(
    tmp_path_factory: pytest.TempPathFactory, contents: list[str | bytes]
) -> None:
    directory = tmp_path_factory.mktemp("records")
    paths: list[Path] = []
    for number, content in enumerate(contents):
        path = directory / f"{number}.md"
        path.write_bytes(
            content if isinstance(content, bytes) else content.encode("utf-8")
        )
        paths.append(path)
    findings = check(paths)
    assert {f.code for f in findings} <= DATA_ERRORS
    assert {f.path for f in findings} <= set(paths)
    for finding in findings:  # every message prints, on one short line
        line = str(finding)
        line.encode("utf-8")
        assert "\n" not in line and len(line) < 500
