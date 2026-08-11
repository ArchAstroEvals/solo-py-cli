from mdh.converter import render_inline


def test_bold():
    assert render_inline("a **bold** word") == "a <strong>bold</strong> word"


def test_italic():
    assert render_inline("a *italic* word") == "a <em>italic</em> word"


def test_code():
    assert render_inline("a `code` word") == "a <code>code</code> word"


def test_escapes_html():
    assert render_inline("<b>x</b>") == "&lt;b&gt;x&lt;/b&gt;"
