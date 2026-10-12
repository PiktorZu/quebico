"""Quebico records the reasoning that connects a project, and puts it to work."""

from collections.abc import Iterable
from pathlib import Path

from quebico.records import Finding, load

__all__ = ["Finding", "check"]


def check(paths: Iterable[Path]) -> list[Finding]:
    """Everything `quebico check` reports on these record files.

    For now that is the data errors of docs/schema.md; the watch questions of
    docs/questions.md come next, and run only on a record set with no data error.
    """
    _, errors = load(paths)
    return errors
