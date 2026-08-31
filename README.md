# mdh

Minimal Markdown-to-HTML converter CLI.

## Usage

```sh
python -m mdh notes.md
python -m mdh notes.md -o notes.html
cat notes.md | python -m mdh
python -m mdh notes.md --standalone --title "Notes" -o notes.html
```
