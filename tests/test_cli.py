import io
import sys

from mdh.cli import main


def test_stdin_to_stdout(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO("# Hi\n"))
    assert main([]) == 0
    assert capsys.readouterr().out == "<h1>Hi</h1>\n"


def test_file_input(tmp_path, capsys):
    src = tmp_path / "doc.md"
    src.write_text("**bold**\n")
    assert main([str(src)]) == 0
    assert capsys.readouterr().out == "<p><strong>bold</strong></p>\n"


def test_output_file(tmp_path, capsys):
    src = tmp_path / "doc.md"
    src.write_text("hi\n")
    dest = tmp_path / "out.html"
    assert main([str(src), "-o", str(dest)]) == 0
    assert dest.read_text() == "<p>hi</p>\n"
    assert capsys.readouterr().out == ""
