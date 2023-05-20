"""Command-line application for combining source files in git."""

import argparse
from argparse import ArgumentParser
import logging
import os
import sys
import subprocess
from shlex import quote
import pathlib
from typing import Optional
from functools import cache


def get_argparser() -> ArgumentParser:
    """Parse command-line arguments."""
    parser = ArgumentParser(
        prog="git-append", description="Concatenate files in git"
    )
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        dest="dryrun",
        default=False,
        help="A 'dry-run' makes no file changes",
    )
    parser.add_argument(
        "dstfile",
        type=argparse.FileType("a"),
        help="Destination file, to be appended to from source files",
    )
    parser.add_argument(
        "srcfiles",
        nargs="+",
        type=argparse.FileType("r"),
        help="Source files to be added to dstfile and then removed",
    )
    return parser


def main() -> None:
    """Parse command-line arguments and manage file appending."""
    parser = get_argparser()
    args = parser.parse_args()
    logging.basicConfig(format=">>> %(message)s", level=get_log_level(args))
    logging.debug(args)

    # check for dstfile in *srcfiles
    if args.dstfile.name in [x.name for x in args.srcfiles]:
        logging.error(
            f"found destination file '{quote(args.dstfile.name)}'"
            "in list of source files, that's bad"
        )
        exit(1)

    # Loop over srcfiles, appending each to dstfile.
    bytes = 0
    for srcfile in args.srcfiles:
        tmp = srcfile.read()
        bytes += len(tmp)
        if args.dryrun:
            logging.info("""Dry run: no changes""")
        else:
            logging.info(
                f"""Appending {len(tmp)} bytes to {quote(args.dstfile.name)}"""
            )
            args.dstfile.write(tmp)
            remove_file(srcfile.name)

    sys.stderr.write(
        f"Wrote {bytes} bytes to file '{quote(args.dstfile.name)}'.\n"
    )


@cache
def git_root(filename: str) -> Optional[str]:
    """Find the parent folder containing a .git/ subfolder."""
    # I genuinely do not like this.
    p = pathlib.Path(filename)
    seen = {}

    # traverse 100 directories deep looking for the git root folder
    for _ in range(100):
        if p.is_file():
            p = p.parent
        elif p in seen:
            # we've been here before?!?!?!
            return None
        elif p.is_dir():
            seen[p] = True
            tmp = p / ".git"
            if tmp.exists():
                return p.as_posix()

    # give up if we haven't found it yet
    return None


def remove_file(filename: str) -> None:
    """Remove file filename.

    If the file is tracked in the github index, remove it with `git rm -f`,
    otherwise remove it with `rm -f`.
    """
    if in_index(filename):
        logging.info(f"file {quote(filename)} is in the repo")
        logging.debug(f"calling: git rm -f '{quote(filename)}'")
        proc = subprocess.run(
            ["git", "rm", "--force", filename], capture_output=True
        )
        logging.debug(proc)
    else:
        logging.info(f"file {quote(filename)} is NOT in the repo")
        logging.debug(f"calling: os.remove({quote(filename)})")
        os.remove(filename)


def in_index(filename: str) -> bool:
    """Return True if `filename` is tracked in git, False otherwise."""
    # FIXME: should filename be an absolute path? That seems important.
    proc = subprocess.run(
        ["git", "ls-files", "--error-unmatch", filename],
        capture_output=True,
        cwd=git_root(filename),
    )
    logging.debug(proc)
    return proc.returncode == 0


def get_log_level(args: argparse.Namespace) -> int:
    """Decide the logging level from the command-line arguments."""
    if args.debug:
        return logging.DEBUG
    if args.verbose:
        return logging.INFO
    return logging.WARNING
