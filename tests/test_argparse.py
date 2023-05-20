from gitappend import get_argparser
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any


def test_simple(tmp_path: Any) -> None:
    """Simulate call `git-append foo bar`.

    This test just checks that argparse is behaving correctly. Destination file
    is foo, source file is bar.
    """
    # set up the test files
    d = tmp_path / "test_simple"
    d.mkdir()

    foo = d / "foo"
    foo.write_text("foo")

    bar = d / "bar"
    bar.write_text("bar")

    # create the parser object
    parser = get_argparser()
    assert type(parser) is ArgumentParser

    # parse arguments into a namespace object
    args = parser.parse_args([foo.as_posix(), bar.as_posix()])
    assert type(args) is Namespace

    # unspecified arguments should get the correct defaults
    assert not args.debug
    assert not args.dryrun
    assert not args.verbose

    # check the source files (there should be only one)
    srcfiles = args.srcfiles
    assert len(srcfiles) == 1
    srcfile = Path(srcfiles[0].name).name  # kek
    assert srcfile == "bar"

    # check the destination file
    dstfile = Path(args.dstfile.name).name  # kekekek
    assert dstfile == "foo"
