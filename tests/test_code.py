from mdh.converter import convert


def test_fence():
    assert convert("```\nx = 1\n```") == "<pre><code>\nx = 1\n</code></pre>"


def test_fence_language():
    assert 'class="language-python"' in convert("```python\nx\n```")


def test_fence_escapes_html():
    assert "&lt;a&gt;" in convert("```\n<a>\n```")
