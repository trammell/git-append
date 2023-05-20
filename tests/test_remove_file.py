from gitappend import remove_file
from typing import Any
import sys


def test_rm_1(tmp_path: Any) -> None:
    """Test appending one file to another, no git involved."""

    # set up the test files
    d = tmp_path / "test_rm_1"
    d.mkdir()
    foo = d / "foo"
    foo.write_text("foo")

    assert foo.exists()

    # remove_file(foo.as_posix())
    # end result:
    #   * this should remove file `bar`
    #   * this should not remove file `foo`
    #   * file `foo` should have had "bar" appended to it
    #assert not bar.exists()
    #assert foo.read_text() == "foobar"


# def test_append_2(tmp_path: Any) -> None:
#     """Test appending one file to another, no git involved."""
# 
#     # set up the test files
#     d = tmp_path / "test_append_1"
#     d.mkdir()
#     foo = d / "foo"
#     foo.write_text("foo")
#     bar = d / "bar"
#     bar.write_text("bar")
# 
#     # set sys.argv and invoke main
#     sys.argv[1:] = [foo.as_posix(), bar.as_posix()]
#     main()
# 
#     # end result:
#     #   * this should remove file `bar`
#     #   * this should not remove file `foo`
#     #   * file `foo` should have had "bar" appended to it
#     assert not bar.exists()
#     assert foo.exists()
#     assert foo.read_text() == "foobar"
