"""Command-line interface for mdh."""
import argparse
import sys

from .converter import convert


def build_parser():
    parser = argparse.ArgumentParser(prog="mdh", description="Convert Markdown to HTML.")
    parser.add_argument("input", nargs="?", help="Input Markdown file (default: stdin).")
    return parser


def read_input(path):
    if path:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main(argv=None):
    args = build_parser().parse_args(argv)
    sys.stdout.write(convert(read_input(args.input)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
