# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m failprint` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `failprint.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `failprint.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
from typing import List, Optional

from failprint.capture import Capture
from failprint.formats import accept_custom_format, formats
from failprint.runners import run


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="failprint")
    parser.add_argument(
        "-c",
        "--capture",
        choices=list(Capture),
        type=Capture,
        help="Which output to capture. Colors are supported with 'both' only, unless the command has a 'force color' option.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=formats.keys(),
        type=accept_custom_format,
        default=None,
        help="Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. "
        "Available variables: command, title (command or title passed with -t), code (exit status), "
        "success (boolean), failure (boolean), number (command number passed with -n), "
        "output (command output), nofail (boolean), quiet (boolean), silent (boolean). "
        "Available filters: indent (textwrap.indent).",
    )
    parser.add_argument("-n", "--number", type=int, default=1, help="Command number. Useful for the 'tap' format.")
    parser.add_argument(
        "--no-pty",
        action="store_false",
        dest="pty",
        default=True,
        help="Disable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_false",
        dest="progress",
        default=True,
        help="Don't print any progress while running a command.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        default=False,
        help="Don't print the command output, even if it failed.",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        dest="silent",
        default=False,
        help="Don't print anything.",
    )
    parser.add_argument("-t", "--title", help="Command title. Default is the command itself.")
    parser.add_argument(
        "-z",
        "--zero",
        "--nofail",
        action="store_true",
        dest="nofail",
        default=False,
        help="Don't fail. Always return a success (0) exit code.",
    )
    parser.add_argument("COMMAND", nargs="+")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `failprint` or `python -m failprint`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    options = parser.parse_args(args)
    return run(
        options.COMMAND,
        number=options.number,
        capture=options.capture,
        title=options.title,
        fmt=options.format,
        pty=options.pty,
        nofail=options.nofail,
        quiet=options.quiet,
        silent=options.silent,
        progress=options.progress,
    )
