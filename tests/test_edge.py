from mdh.converter import convert


def test_empty():
    assert convert("") == ""


def test_whitespace_only():
    assert convert("  \n\n   ") == ""
