from gitappend import remove_file
from typing import Any


def test_remove(tmp_path: Any) -> None:
    """Test appending one file to another, no git involved."""

    # set up the test files
    d = tmp_path / "test_remove"
    d.mkdir()
    foo = d / "foo"
    foo.write_text("foo")

    assert foo.exists()
    assert foo.read_text() == "foo"

    # now remove the file
    remove_file(foo.as_posix())
    assert not foo.exists()
