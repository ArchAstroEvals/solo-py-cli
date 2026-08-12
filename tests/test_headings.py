from mdh.converter import convert


def test_h1():
    assert convert("# Hello") == "<h1>Hello</h1>"


def test_h3():
    assert convert("### Deep") == "<h3>Deep</h3>"


def test_paragraph():
    assert convert("just text") == "<p>just text</p>"


def test_hash_without_space_is_paragraph():
    assert convert("#nospace") == "<p>#nospace</p>"
