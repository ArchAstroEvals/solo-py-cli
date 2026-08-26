"""Block-level Markdown to HTML conversion (v3: nested lists)."""
import html
import re

LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+(.*)$")


def render_inline(text):
    out = html.escape(text)
    out = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*`\n]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*`\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"!\[([^\]\n]*)\]\(([^)\s]+)\)", r'<img alt="\1" src="\2">', out)
    out = re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    return out


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


def convert(markdown):
    lines = markdown.split("\n")
    out = []
    para = []
    i = 0
    in_fence = False

    def flush_para():
        if para:
            out.append(f"<p>{render_inline(chr(10).join(para)).replace('  ' + chr(10), '<br>')}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_para()
            if not in_fence:
                in_fence = True
                lang = line[3:].strip()
                cls = f' class="language-{lang}"' if lang else ""
                out.append(f"<pre><code{cls}>")
            else:
                in_fence = False
                out.append("</code></pre>")
            i += 1
            continue
        if in_fence:
            out.append(html.escape(line))
            i += 1
            continue
        if not line.strip():
            flush_para()
            i += 1
            continue
        if "|" in line and i + 1 < len(lines) and _is_delim(lines[i + 1]):
            flush_para()
            html_table, i = _consume_table(lines, i)
            out.append(html_table)
            continue
        if LIST_RE.match(line):
            flush_para()
            html_list, i = _render_list(lines, i, 0)
            out.append(html_list)
            continue
        if line.lstrip().startswith(">"):
            flush_para()
            quotes = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quotes.append(lines[i].lstrip()[1:].lstrip())
                i += 1
            out.append("<blockquote>" + chr(10).join(f"<p>{render_inline(q)}</p>" for q in quotes) + "</blockquote>")
            continue
        if re.fullmatch(r"\s*([-*_])(\s*\1){2,}\s*", line):
            flush_para()
            out.append("<hr>")
            i += 1
            continue
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            flush_para()
            level = len(match.group(1))
            out.append(f"<h{level}>{render_inline(match.group(2).strip())}</h{level}>")
            i += 1
            continue
        stripped = line.strip()
        if stripped and line.endswith("  "):
            stripped += "  "
        para.append(stripped)
        i += 1
    flush_para()
    return chr(10).join(out)
