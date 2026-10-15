# 0015 — `quebico graph` prints Mermaid in Markdown, only for records without data errors

**Decided:** `quebico graph [DIR]` reads the same records as `quebico check`, under the
same directory rules (0011), and prints them on standard output as a Mermaid flowchart
inside a Markdown code block (```` ```mermaid ````). Sent to a `.md` file, or pasted into
a pull request, an issue or a README, it renders on GitHub as it is (0002).

- When the records have a data error, no graph is printed. The data errors go to
  standard error, worded as `quebico check` words them, then one line saying there is no
  graph, and the command exits with 1.
- The output is plain ASCII. In a title, everything but letters, digits, spaces and
  plain punctuation (`-.,'()/!?+_`) is written as a Mermaid entity code, such as `#35;`
  for `#`. A word joiner (U+2060), which shows as nothing, is put inside each sequence
  that Mermaid reads even after decoding entity codes: `\n`, `fa:fa-…`, `$$`, and
  Mermaid's own placeholders `ﬂ°` and `¶ß`.

**Why:** GitHub draws Mermaid only inside a mermaid code block, so printing the block
makes "GitHub renders it as-is" true of the output itself: one redirect or one paste,
nothing to wrap by hand. Inside the block is plain Mermaid for any other tool.

No graph on a data error, because a link that does not resolve has nothing to point to,
and a graph drawn without it looks complete while leaving out exactly what is broken.
The watch questions wait for records without data errors for the same reason
(`docs/schema.md`). The errors go to standard error so that they are seen even when the
graph is redirected, and never end up in the file; the exit code lets a script tell.

Entity codes, because Mermaid and HTML read meaning into many characters: `"` ends a
label, `<b>` turns bold, `%%{init: …}%%` changes the configuration, `#quot;` is an
entity, and before parsing, Mermaid drops a semicolon from a line where `style:` is
followed by a `#`. Naming the few characters let through is safer than naming the many
that are not. Entity codes alone are not enough, though: Mermaid decodes them and then
still reads `\n` as a line break and `fa:fa-car` as an icon, and Mermaid 11 reads
`$$…$$` as maths, so that a title holding `$$}$$` stopped the whole diagram from
rendering. The independent review before this pull request found these. The word joiner splits them,
and every case in the tests was rendered on Mermaid 10.9 and 11.16 to check. ASCII also
survives any console encoding, Windows code pages included.

The cost is length: a character outside ASCII takes about seven, so records with
Japanese titles reach Mermaid's default limit of 50,000 characters at a couple of
hundred, about a third as many as with English titles.

**Rejected:**

- *Bare Mermaid source.* Every reader would have to wrap it before GitHub renders it.
- *A flag to choose the format, or an option to name an output file.* Nothing needs
  either yet, and a redirect names the file.
- *Drawing what can be drawn despite data errors.* For the reasons above.
- *Escaping only what breaks the syntax.* It would leave HTML, directives and entity
  codes to whichever Mermaid version reads them. The allowed list leaves only the few
  sequences Mermaid reads after decoding, named above.
- *Titles in UTF-8 as they are*, which would keep the output short. On Windows,
  Python writes a redirect in the local code page unless its UTF-8 mode is on, and
  GitHub then shows such titles garbled.
