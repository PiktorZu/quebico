"""The code budget in CLAUDE.md: at most 500 lines under src/ until v0.1, tests excluded.

Every physical line of every Python file counts, blank lines and comments included, so
the measure needs no judgment. Raising the budget takes a recorded decision.
"""

from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
BUDGET = 500


def test_src_stays_within_the_budget() -> None:
    lines = sum(
        len(p.read_text(encoding="utf-8").splitlines()) for p in SRC.rglob("*.py")
    )
    assert lines <= BUDGET, f"src/ has {lines} lines; the budget to v0.1 is {BUDGET}"
