"""Quebico records the reasoning that connects a project, and puts it to work."""

from collections.abc import Iterable
from pathlib import Path

from quebico.questions import orphan_tasks, stale_premises
from quebico.records import Finding, load

__all__ = ["Finding", "check"]


def check(paths: Iterable[Path]) -> list[Finding]:
    """Everything `quebico check` reports on these record files.

    That is the data errors of docs/schema.md or, on a record set with none, the
    answers to the two watch questions of docs/questions.md.
    """
    records, errors = load(paths)
    if errors:
        return errors
    return stale_premises(records) + orphan_tasks(records)
