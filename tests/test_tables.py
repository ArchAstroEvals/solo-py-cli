from mdh.converter import convert


def test_table():
    md = "| a | b |\n|---|---|\n| 1 | 2 |"
    html = convert(md)
    assert "<table>" in html
    assert "<th>a</th>" in html
    assert "<td>1</td>" in html


def test_table_renders_inline():
    assert "<strong>x</strong>" in convert("| a |\n|---|\n| **x** |")


def test_table_alignment():
    md = "| a | b |\n|:--|--:|\n| 1 | 2 |"
    html = convert(md)
    assert 'align="left"' in html
    assert 'align="right"' in html
