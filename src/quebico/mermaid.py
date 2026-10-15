"""The Mermaid view of a record set, which `quebico graph` prints (0015, 0016)."""

import re
import textwrap

from quebico.questions import orphan_tasks, stale_premises
from quebico.records import LINKS, Record

SHAPES = {
    "goal": ("([", "])"),
    "decision": ("[", "]"),
    "premise": ("[/", "/]"),
    "task": ("(", ")"),
}
ARROWS = {"serves": "-->", "depends_on": "-.->", "supersedes": "==>"}
STYLES = (
    "classDef inactive color:#777,stroke:#777,stroke-dasharray:4 3",
    "classDef answer fill:#fde2c8,stroke:#d9480f,stroke-width:2px,color:#000",
)
PLAIN = set(" -.,'()/!?+_")
WRAP = textwrap.TextWrapper(24, break_long_words=False, break_on_hyphens=False)
# What Mermaid reads even after decoding entity codes: \n as a line break, fa:fa-… as
# an icon, $$ as maths, and its own placeholders ﬂ° and ¶ß.
READ_AGAIN = re.compile(
    r"(?<=\\)(?=n)|(?<=:)(?=fa-)|(?<=\$)(?=\$)|(?<=\ufb02)(?=\xb0)|(?<=\xb6)(?=\xdf)"
)


def _text(text: str) -> str:
    """Text for a label, shown as written: letters, digits, spaces and plain punctuation
    stay, the rest become entity codes, and a word joiner, which shows as nothing,
    splits whatever Mermaid would read even so."""
    return "".join(
        c if c.isascii() and (c.isalnum() or c in PLAIN) else f"#{ord(c)};"
        for c in READ_AGAIN.sub("\u2060", text)
    )


def flowchart(records: dict[str, Record]) -> str:
    """Records with no data error as a Mermaid flowchart, in a Markdown code block.

    The answers to the watch questions are highlighted, and whatever is superseded,
    closed or no longer holds is greyed out.
    """
    ids = sorted(records)
    node = {record_id: f"n{number}" for number, record_id in enumerate(ids, 1)}
    superseded = {old for record in records.values() for old in record.supersedes}
    answers = {f.ids[0] for f in stale_premises(records) + orphan_tasks(records)}
    lines = ["```mermaid", "flowchart LR"]
    for record_id in ids:
        record = records[record_id]
        start, end = SHAPES[record.kind]
        label = [f"{record.kind} {record_id}", *WRAP.wrap(record.title)]
        live = record_id not in superseded and not record.closed and record.holds
        state = ":::answer" if record_id in answers else "" if live else ":::inactive"
        text = "<br>".join(map(_text, label))
        lines.append(f'    {node[record_id]}{start}"{text}"{end}{state}')
    for record_id in ids:
        for name in LINKS:
            for target in dict.fromkeys(getattr(records[record_id], name)):
                arrow = f"{ARROWS[name]}|{name}|"
                lines.append(f"    {node[record_id]} {arrow} {node[target]}")
    return "\n".join([*lines, *(f"    {style}" for style in STYLES), "```"]) + "\n"
