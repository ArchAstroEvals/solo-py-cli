# mdh

Minimal Markdown-to-HTML converter CLI. Supports headings, paragraphs, inline
styles, links, images, lists (flat and nested), fenced code, blockquotes,
tables, horizontal rules, and hard breaks.

## Install

```sh
pip install .
```

## Usage

```sh
python -m mdh notes.md
python -m mdh notes.md -o notes.html
cat notes.md | python -m mdh
python -m mdh notes.md --standalone --title "Notes" --css "body{font:sans-serif}" -o notes.html
python -m mdh --version
```

Missing input files exit with status 2.

## License

MIT
