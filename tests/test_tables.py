from mdh.converter import convert


def test_table():
    md = "| a | b |
|---|---|
| 1 | 2 |"
    html = convert(md)
    assert "<table>" in html
    assert "<th>a</th>" in html
    assert "<td>1</td>" in html


def test_table_renders_inline():
    assert "<strong>x</strong>" in convert("| a |
|---|
| **x** |")
