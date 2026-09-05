"""Block-level helpers: lists and tables."""
import re

from .inline import render_inline

LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def _is_delim(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{1,}:?", c) for c in cells)


def _cell_align(marker):
    left = marker.startswith(":")
    right = marker.endswith(":")
    if left and right:
        return "center"
    if right:
        return "right"
    if left:
        return "left"
    return None


def _consume_table(lines, i):
    header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
    aligns = [_cell_align(c.strip()) for c in lines[i + 1].strip().strip("|").split("|")]
    rows = []
    j = i + 2
    while j < len(lines) and "|" in lines[j] and lines[j].strip():
        rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
        j += 1

    def cell(tag, text, align):
        attr = f' align="{align}"' if align else ""
        return f"<{tag}{attr}>{render_inline(text)}</{tag}>"

    thead = "<thead><tr>" + "".join(cell("th", h, a) for h, a in zip(header, aligns)) + "</tr></thead>"
    body = "<tbody>" + "".join("<tr>" + "".join(cell("td", v, a) for v, a in zip(row, aligns)) + "</tr>" for row in rows) + "</tbody>"
    return f"<table>{thead}{body}</table>", j


def _render_list(lines, i, indent):
    entries = []
    kind = None
    start = 1
    while i < len(lines):
        match = LIST_RE.match(lines[i])
        if not match:
            break
        level = len(match.group(1).expandtabs(4))
        if level < indent:
            break
        if level > indent:
            if not entries:
                break
            sub, i = _render_list(lines, i, level)
            entries[-1][1] += sub
            continue
        marker = match.group(2)
        if kind is None:
            kind = "ol" if marker[0].isdigit() else "ul"
            if kind == "ol":
                try:
                    start = int(marker[:-1])
                except ValueError:
                    start = 1
        entries.append([render_inline(match.group(3).strip()), ""])
        i += 1
    if not entries:
        return "", i
    if kind == "ol":
        open_tag = "<ol>" if start == 1 else f'<ol start="{start}">'
        close_tag = "</ol>"
    else:
        open_tag, close_tag = "<ul>", "</ul>"
    body = "".join(f"<li>{text}{sub}</li>" for text, sub in entries)
    return open_tag + body + close_tag, i
