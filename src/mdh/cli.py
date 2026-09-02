"""Command-line interface for mdh."""
import argparse
import sys

from . import __version__
from .converter import convert, render_document


def build_parser():
    parser = argparse.ArgumentParser(prog="mdh", description="Convert Markdown to HTML.")
    parser.add_argument("input", nargs="?", help="Input Markdown file (default: stdin).")
    parser.add_argument("-o", "--output", help="Output HTML file (default: stdout).")
    parser.add_argument("--standalone", action="store_true", help="Emit a full HTML document.")
    parser.add_argument("--title", default="Document", help="Title for standalone output.")
    parser.add_argument("--css", help="Inline CSS for standalone output.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def read_input(path):
    if path:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        body = convert(read_input(args.input))
    except FileNotFoundError:
        print(f"mdh: {args.input}: No such file or directory", file=sys.stderr)
        return 2
    if args.standalone:
        html = render_document(body, title=args.title, css=args.css)
    else:
        html = body
    html += "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(html)
    else:
        sys.stdout.write(html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
