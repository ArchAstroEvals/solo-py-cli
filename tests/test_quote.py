from mdh.converter import convert


def test_quote():
    assert convert("> hello") == "<blockquote><p>hello</p></blockquote>"


def test_multiline_quote():
    html = convert("> one\n> two")
    assert "<p>one</p>" in html and "<p>two</p>" in html


def test_quote_with_inline():
    assert "<strong>hi</strong>" in convert("> **hi**")
