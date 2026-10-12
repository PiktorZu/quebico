# 0012 — Front matter is read with PyYAML, typing only what the schema uses

**Decided:** `quebico check` reads front matter with PyYAML's safe loader, narrowed to
what `docs/schema.md` uses:

- Implicit typing is cut down to null, `true` and `false` spelled exactly so, and whole
  numbers written in decimal without a leading zero. Every other plain scalar is a
  string.
- An explicit `!!bool` tag still makes a boolean only of `true` or `false`; anything
  else under it stays text.
- A key given twice in one mapping is invalid YAML, as the YAML specification says,
  not a value that silently replaces the first.

PyYAML is the project's first runtime dependency. Files are read as UTF-8; a byte-order
mark and Windows line endings are accepted, since drafts are written on Windows (0008).

**Why:** PyYAML follows YAML 1.1, where `yes`, `on`, `NO` and `OFF` are booleans,
`2026-10-10` is a date and `012` is the octal number 10. Read that way, `closed: yes`
would pass, though the schema allows only `true` and `false`; a valid id such as `NO`
would turn into `false`, and every link to it would break; a title such as `2026-10-10`
would stop being text. And PyYAML keeps the last of two equal keys without a word, so a
second `depends_on` line would erase the first along with its link to a premise. With
the loader narrowed, each of these is a data error or a string, as the schema reads
them, and the data-error tests pin every case.

Python adds a trap the loader cannot remove: `True == 1`, so `schema_version: true`
passes a plain comparison with 1. The field is checked by type as well as value.

What the narrowing leaves: an id spelled `null`, `true` or `false` still reads as null or
a boolean and is reported as invalid. Quote it, as the schema already says for a title
that YAML would misread.

**Rejected:**

- *PyYAML as it comes.* The cases above.
- *ruamel.yaml*, which reads YAML 1.2 and rejects repeated keys. Its booleans are closer
  to the schema's, but `True` is still one, so it would need narrowing too.
- *A parser for a subset of YAML, written here.* The schema asks for valid YAML, so it
  would reject records that are valid, such as a link list written as a block sequence.
