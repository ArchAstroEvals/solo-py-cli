"""Command-line interface for mdh."""
import argparse
import sys

from .converter import convert


def build_parser():
    parser = argparse.ArgumentParser(prog="mdh", description="Convert Markdown to HTML.")
    parser.add_argument("input", nargs="?", help="Input Markdown file (default: stdin).")
    parser.add_argument("-o", "--output", help="Output HTML file (default: stdout).")
    return parser


def read_input(path):
    if path:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main(argv=None):
    args = build_parser().parse_args(argv)
    html = convert(read_input(args.input)) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(html)
    else:
        sys.stdout.write(html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
