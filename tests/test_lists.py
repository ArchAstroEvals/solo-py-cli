from mdh.converter import convert


def test_unordered():
    assert convert("- a\n- b") == "<ul><li>a</li><li>b</li></ul>"


def test_ordered():
    assert convert("1. a\n2. b") == "<ol><li>a</li><li>b</li></ol>"


def test_list_stops_at_blank_line():
    html = convert("- a\n\ntext")
    assert "<ul><li>a</li></ul>" in html
    assert "<p>text</p>" in html
