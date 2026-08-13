from mdh.converter import convert, render_inline


def test_link():
    assert render_inline("[docs](https://example.com)") == '<a href="https://example.com">docs</a>'


def test_image():
    assert render_inline("![alt](pic.png)") == '<img alt="alt" src="pic.png">'


def test_link_inside_paragraph():
    assert convert("see [docs](https://example.com) now") == '<p>see <a href="https://example.com">docs</a> now</p>'
