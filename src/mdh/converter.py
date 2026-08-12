"""Block-level Markdown to HTML conversion (v1: paragraphs, headings, inline)."""
import html
import re


def render_inline(text):
    out = html.escape(text)
    out = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*`\n]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*`\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"!\[([^\]\n]*)\]\(([^)\s]+)\)", r'<img alt="\1" src="\2">', out)
    out = re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    return out


def render_block(line):
    match = re.match(r"^(#{1,6})\s+(.*)$", line)
    if match:
        level = len(match.group(1))
        return f"<h{level}>{render_inline(match.group(2).strip())}</h{level}>"
    return f"<p>{render_inline(line.strip())}</p>"


def convert(markdown):
    blocks = [b for b in markdown.split("\n\n") if b.strip()]
    return "\n".join(render_block(b.strip()) for b in blocks)
