"""Block-level Markdown to HTML conversion (v2: line parser)."""
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


def _consume_list(lines, i):
    first = LIST_RE.match(lines[i])
    ordered = first.group(2)[0].isdigit()
    items = []
    while i < len(lines):
        match = LIST_RE.match(lines[i])
        if not match:
            break
        items.append(render_inline(match.group(3).strip()))
        i += 1
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{t}</li>" for t in items) + f"</{tag}>", i


def convert(markdown):
    lines = markdown.split("\n")
    out = []
    para = []
    i = 0
    in_fence = False

    def flush_para():
        if para:
            out.append(f"<p>{render_inline(' '.join(para))}</p>")
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
        if LIST_RE.match(line):
            flush_para()
            html_list, i = _consume_list(lines, i)
            out.append(html_list)
            continue
        if line.lstrip().startswith(">"):
            flush_para()
            quotes = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quotes.append(lines[i].lstrip()[1:].lstrip())
                i += 1
            out.append("<blockquote>" + "\n".join(f"<p>{render_inline(q)}</p>" for q in quotes) + "</blockquote>")
            continue
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            flush_para()
            level = len(match.group(1))
            out.append(f"<h{level}>{render_inline(match.group(2).strip())}</h{level}>")
            i += 1
            continue
        para.append(line.strip())
        i += 1
    flush_para()
    return "\n".join(out)
