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


def test_standalone(tmp_path, capsys):
    src = tmp_path / "doc.md"
    src.write_text("# T\n")
    assert main([str(src), "--standalone", "--title", "T"]) == 0
    out = capsys.readouterr().out
    assert "<title>T</title>" in out
    assert "<h1>T</h1>" in out


def test_standalone_css(tmp_path, capsys):
    src = tmp_path / "doc.md"
    src.write_text("hi\n")
    assert main([str(src), "--standalone", "--css", "body{color:red}"]) == 0
    out = capsys.readouterr().out
    assert "<style>body{color:red}</style>" in out


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")
    assert "mdh 0.1.1" in capsys.readouterr().out


def test_missing_file(capsys):
    assert main(["nope.md"]) == 2
    assert "No such file" in capsys.readouterr().err


def test_empty_stdin(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'stdin', io.StringIO(''))
    assert main([]) == 0
    assert capsys.readouterr().out == '
'
