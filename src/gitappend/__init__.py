"""Command-line application for combining source files in git."""

import argparse
from argparse import ArgumentParser
import logging
import os
import sys
import subprocess


def get_argparser() -> ArgumentParser:
    """Parse command-line arguments."""
    parser = ArgumentParser(
        prog="git-append", description="Append and remove files in git"
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
        "srcfile",
        nargs="+",
        type=argparse.FileType("r"),
        help="Source file to be appended to dstfile and removed",
    )
    parser.add_argument(
        "dstfile",
        type=argparse.FileType("a"),
        help="Destination file to be extended with source contents",
    )
    return parser


def main(parser: ArgumentParser) -> None:
    """Parse command-line arguments and manage file appending."""
    args = parser.parse_args()
    logging.basicConfig(format=">>> %(message)s", level=get_log_level(args))
    logging.debug(args)

    # check for srcfile==dstfile
    if args.dstfile.name in [x.name for x in args.srcfile]:
        logging.error("found dstfile in srcfile list, that's bad")
        exit(1)

    """Append args.srcfile to args.destfile."""
    bytes = 0
    for srcfile in args.srcfile:
        tmp = srcfile.read()
        bytes += len(tmp)
        if args.dryrun:
            logging.info("""Dry run: no changes""")
        else:
            logging.info(
                f"""Appending {len(tmp)} bytes to {args.dstfile.name}"""
            )
            args.dstfile.write(tmp)
            force_remove(srcfile.name)

    sys.stderr.write(f"Wrote {bytes} bytes to file '{args.dstfile.name}'.\n")


def force_remove(filename: str) -> None:
    """Remove file filename.

    If the file is in github, remove it with `git rm -f`, otherwise remove it
    with `rm -f`
    """
    if file_in_repo(filename):
        logging.info(f"file {filename} is in the repo")
        logging.debug(f"calling: git rm -f '{filename}'")
        proc = subprocess.run(
            ["git", "rm", "--force", filename], capture_output=True
        )
        logging.debug(proc)
    else:
        logging.info(f"file {filename} is NOT in the repo")
        logging.debug(f"calling: os.remove({filename})")
        os.remove(filename)


def file_in_repo(filename: str) -> bool:
    """Return True if filename is tracked in git, False otherwise."""
    proc = subprocess.run(
        ["git", "ls-files", "--error-unmatch", filename], capture_output=True
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
