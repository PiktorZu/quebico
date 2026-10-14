"""Records and their data errors, as docs/schema.md defines them."""

import re
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, TypeGuard, cast

import yaml
from yaml.constructor import ConstructorError

REQUIRED = ("schema_version", "id", "kind", "title")
FIELDS = {
    "goal": REQUIRED,
    "task": (*REQUIRED, "serves", "closed"),
    "decision": (*REQUIRED, "serves", "depends_on", "supersedes"),
    "premise": (*REQUIRED, "holds"),
}
LINKS = ("serves", "depends_on", "supersedes")
# The kinds each link may point to, by the kind of the record that holds it.
TARGETS = {
    ("task", "serves"): ("decision", "goal"),
    ("decision", "serves"): ("goal",),
    ("decision", "depends_on"): ("premise", "decision"),
    ("decision", "supersedes"): ("decision",),
}
_ID = re.compile(r"[A-Za-z][A-Za-z0-9-]*")


def _is_id(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and _ID.fullmatch(value) is not None


def _is_id_list(value: object) -> bool:
    items = cast(list[object], value) if isinstance(value, list) else None
    return items is not None and all(_is_id(item) for item in items)


def _shown(value: object, nested: bool = False) -> str:
    """A short, printable account of any value, for a message."""
    named = f"<{type(value).__name__}>"
    if value is None:
        return "nothing"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and abs(value) < 10**6:
        return str(value)
    if isinstance(value, str):
        return repr(value[:40]) + ("..." if len(value) > 40 else "")
    if isinstance(value, list) and not nested:
        items = cast(list[object], value)
        shown = [_shown(item, nested=True) for item in items[:5]]
        return "[" + ", ".join(shown + ["..."] * (len(items) > 5)) + "]"
    return named


# What each field may hold, as a test and as words for the error message.
_VALUES: dict[str, tuple[Callable[[object], bool], str]] = {
    "schema_version": (lambda v: type(v) is int and v == 1, "the number 1"),
    "id": (_is_id, "an ASCII letter, then ASCII letters, digits or -"),
    "kind": (
        lambda v: isinstance(v, str) and v in FIELDS,
        "goal, task, decision or premise",
    ),
    "title": (
        lambda v: isinstance(v, str) and v.strip() != "" and v.splitlines() == [v],
        "one line of text",
    ),
    "closed": (lambda v: type(v) is bool, "true or false"),
    "holds": (lambda v: type(v) is bool, "true or false"),
    **{link: (_is_id_list, "a list of ids, such as [G1]") for link in LINKS},
}


@dataclass(frozen=True)
class Finding:
    """One thing `quebico check` reports."""

    code: str
    path: Path
    message: str
    # The records an answer names: (decision, premise) or (task,).
    ids: tuple[str, ...] = ()

    def __str__(self) -> str:
        return f"{self.path}: {self.code}: {self.message}"


@dataclass(frozen=True)
class Record:
    """What Quebico reads from one record: its front matter."""

    path: Path
    id: str
    kind: str  # empty when the file names no valid kind
    title: str
    serves: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    closed: bool = False
    holds: bool = True


def _resolvers() -> dict[str | None, list[tuple[str, re.Pattern[str]]]]:
    """YAML's implicit typing, cut down to null, `true` and `false`, and whole numbers.

    Every other plain scalar stays a string, so an id such as NO or a title such as
    2026-10-10 reads as written, and yes or True is not a boolean (0012).
    """
    kept: dict[str | None, list[tuple[str, re.Pattern[str]]]] = {
        first: [(tag, regexp) for tag, regexp in resolvers if tag.endswith(":null")]
        for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    for tag, pattern, firsts in (
        ("tag:yaml.org,2002:bool", r"^(?:true|false)$", "tf"),
        ("tag:yaml.org,2002:int", r"^[-+]?(?:0|[1-9][0-9]*)$", "-+0123456789"),
    ):
        for first in firsts:
            kept.setdefault(first, []).append((tag, re.compile(pattern)))
    return kept


def _bool(loader: yaml.SafeLoader, node: yaml.ScalarNode) -> bool | str:
    """`true` and `false` only, even under an explicit !!bool tag; the rest stays text."""
    value = loader.construct_scalar(node)
    return {"true": True, "false": False}.get(value, value)


class _Loader(yaml.SafeLoader):
    yaml_implicit_resolvers = _resolvers()
    yaml_constructors: ClassVar[dict[str | None, Any]] = {
        **yaml.SafeLoader.yaml_constructors,
        "tag:yaml.org,2002:bool": _bool,
    }

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Hashable, Any]:
        """A mapping; a key given twice is invalid YAML, not a silent overwrite."""
        seen: set[tuple[str, str]] = set()
        for key, _ in node.value:
            if isinstance(key, yaml.ScalarNode):
                if (key.tag, key.value) in seen:
                    problem = f"the key {_shown(key.value)} appears twice"
                    raise ConstructorError(None, None, problem, key.start_mark)
                seen.add((key.tag, key.value))
        return super().construct_mapping(node, deep)


def _front_matter(path: Path) -> dict[Any, Any] | str:
    """The front matter of a record file, or why it cannot be read."""
    try:
        lines = path.read_text(encoding="utf-8-sig").split("\n")
    except UnicodeDecodeError:
        return "the file is not UTF-8 text"
    if lines[0].rstrip() != "---":
        return "the file must open with a line of three dashes (---)"
    end = next((n for n, line in enumerate(lines) if n and line.rstrip() == "---"), 0)
    if not end:
        return "the front matter is not closed by a line of three dashes (---)"
    try:
        fields = yaml.load("\n".join(lines[1:end]), Loader=_Loader)
    except yaml.MarkedYAMLError as error:
        mark = error.problem_mark
        where = f"line {mark.line + 2}: " if mark else ""
        return f"the front matter is not valid YAML ({where}{error.problem})"
    except Exception as error:  # noqa: BLE001 - PyYAML raises more, e.g. on !!int "09"
        return f"the front matter is not valid YAML ({_shown(str(error))})"
    if fields is None:
        return {}
    if not isinstance(fields, dict):
        return "the front matter must be a mapping of fields"
    return cast(dict[Any, Any], fields)


def _record(path: Path, fields: dict[Any, Any], errors: list[Finding]) -> Record:
    """The record these fields describe; its id or kind is empty when not valid.

    Appends the data errors found in the fields themselves; links are checked later,
    against the whole record set.
    """
    kind = fields.get("kind")
    kind = kind if isinstance(kind, str) and kind in FIELDS else ""
    for name in REQUIRED:
        if name not in fields:
            errors.append(Finding("field-value", path, f"{name} is missing"))
    for name, value in fields.items():
        if kind and name not in FIELDS[kind]:
            allowed = ", ".join(FIELDS[kind])
            message = f"a {kind} has no field {_shown(name)} (its fields: {allowed})"
            errors.append(Finding("unexpected-field", path, message))
        elif name not in _VALUES:
            message = f"no kind of record has a field {_shown(name)}"
            errors.append(Finding("unexpected-field", path, message))
        elif not _VALUES[name][0](value):
            message = f"{name} must be {_VALUES[name][1]} (found {_shown(value)})"
            errors.append(Finding("field-value", path, message))
    record_id, title = fields.get("id"), fields.get("title")

    def links(name: str) -> tuple[str, ...]:
        value = fields.get(name, [])
        allowed = kind and name in FIELDS[kind] and _is_id_list(value)
        return tuple(value) if allowed else ()

    return Record(
        path=path,
        id=record_id if _is_id(record_id) else "",
        kind=kind,
        title=title if isinstance(title, str) else "",
        serves=links("serves"),
        depends_on=links("depends_on"),
        supersedes=links("supersedes"),
        closed=fields.get("closed") is True,
        holds=fields.get("holds") is not False,
    )


def load(paths: Iterable[Path]) -> tuple[dict[str, Record], list[Finding]]:
    """Read record files: the records found, by id, and every data error."""
    records: dict[str, Record] = {}
    errors: list[Finding] = []
    read: list[Record] = []
    for path in paths:
        fields = _front_matter(path)
        if isinstance(fields, str):
            errors.append(Finding("front-matter", path, fields))
            continue
        record = _record(path, fields, errors)
        read.append(record)
        if record.id in records:
            message = f"id {record.id} is also used by {records[record.id].path}"
            errors.append(Finding("duplicate-id", path, message))
        elif record.id:
            records[record.id] = record
    for record in read:
        for name in LINKS:
            for target in getattr(record, name):
                if target not in records:
                    message = f"{name} links to {target}, but no record has that id"
                    errors.append(Finding("bad-link", record.path, message))
                elif records[target].kind not in ("", *TARGETS[record.kind, name]):
                    kinds = " or ".join(f"{k}s" for k in TARGETS[record.kind, name])
                    message = (
                        f"{name} links to {target}, which is a {records[target].kind};"
                        f" a {record.kind}'s {name} links only to {kinds}"
                    )
                    errors.append(Finding("bad-link", record.path, message))
    errors.sort(key=lambda finding: finding.path)
    return records, errors
