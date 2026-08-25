from mdh.converter import convert


def test_hr_dashes():
    assert convert("---") == "<hr>"


def test_hr_stars():
    assert convert("***") == "<hr>"


def test_hard_break():
    assert convert("a  \nb") == "<p>a<br>b</p>"


def test_soft_break_keeps_space():
    assert convert("a\nb") == "<p>a\nb</p>"
