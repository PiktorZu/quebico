"""The command line. `quebico check` fails only on data errors (0011)."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from quebico import check
from quebico.questions import CODES

RECORDS = Path(".quebico/records")


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}" + ("" if number == 1 else "s")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="quebico",
        description="Record the reasoning that connects your project, and put it to work.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    check_command = commands.add_parser(
        "check",
        help="report data errors in the records, or else answer the watch questions",
    )
    check_command.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=RECORDS,
        help=f"where the records are (default: {RECORDS})",
    )
    directory: Path = parser.parse_args(argv).directory
    if directory.exists() and not directory.is_dir():
        check_command.error(f"{directory} is not a directory")
    if not directory.exists():
        print(
            f"quebico: {directory} does not exist, so there are no records",
            file=sys.stderr,
        )
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:  # file names need not be text the console can show
        reconfigure(errors="backslashreplace")
    paths = sorted(path for path in directory.rglob("*.md") if path.is_file())
    findings = check(paths)
    for finding in findings:
        print(finding)
    answers = [finding for finding in findings if finding.code in CODES]
    errors = len(findings) - len(answers)
    if errors:
        summary = f"{_count(errors, 'data error')} (watch questions skipped)"
    else:
        counts = [f"{sum(a.code == code for a in answers)} {code}" for code in CODES]
        summary = ", ".join(["no data errors", *counts])
    print(f"checked {_count(len(paths), 'record')}: {summary}")
    return 1 if errors else 0
