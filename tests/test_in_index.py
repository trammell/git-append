from gitappend import git_root, in_index
from typing import Any
import sys
import subprocess


def test_in_index(tmp_path: Any) -> None:
    """Test code that determines if a file is in git or not."""

    # set up the repo
    d = tmp_path / "repo"
    d.mkdir()
    proc = subprocess.run(
        ["git", "init", d.as_posix()],
        capture_output=True,
        cwd=d.as_posix(),
    )
    assert proc.returncode == 0

    # add a file to the dir, but not the repo
    foo = d / "foo"
    foo.write_text("foo")

    # in_index should return False
    assert not in_index(foo.as_posix())

    # now add it to the repo
    proc = subprocess.run(
        ["git", "add", foo.name],
        capture_output=True,
        cwd=d.as_posix(),
    )
    assert proc.returncode == 0

    # in_index should return True
    assert in_index(foo.as_posix())
