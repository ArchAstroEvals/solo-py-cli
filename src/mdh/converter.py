"""Markdown to HTML conversion."""
import html
import re

from .blocks import LIST_RE, _consume_table, _is_delim, _render_list
from .inline import render_inline


def render_document(body, title="Document", css=None):
    style = f"<style>{css}</style>" if css else ""
    head = f'<meta charset="utf-8"><title>{html.escape(title)}</title>{style}'
    return f"<!DOCTYPE html>\n<html>\n<head>{head}</head>\n<body>\n{body}\n</body>\n</html>"


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
