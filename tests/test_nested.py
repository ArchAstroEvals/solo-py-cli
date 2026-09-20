from mdh.converter import convert


def test_nested_unordered():
    assert convert("- a\n  - b\n- c") == "<ul><li>a<ul><li>b</li></ul></li><li>c</li></ul>"


def test_nested_ordered():
    assert convert("1. a\n   1. b") == "<ol><li>a<ol><li>b</li></ol></li></ol>"


def test_star_bullets():
    assert convert("* a\n* b") == "<ul><li>a</li><li>b</li></ul>"


def test_paren_marker():
    assert convert("1) a\n2) b") == "<ol><li>a</li><li>b</li></ol>"


def test_mixed_nesting():
    assert convert('- a\n  1. b') == '<ul><li>a<ol><li>b</li></ol></li></ul>'
