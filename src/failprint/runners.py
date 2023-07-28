"""Functions to run commands and capture output."""

from __future__ import annotations

import os
import shutil
import sys
import textwrap
import traceback
from typing import TYPE_CHECKING, Callable, Sequence

import colorama
from ansimarkup import ansiprint
from jinja2 import Environment

from failprint.capture import Capture
from failprint.formats import DEFAULT_FORMAT, accept_custom_format, formats, printable_command
from failprint.lazy import LazyCallable
from failprint.process import WINDOWS, run_pty_subprocess, run_subprocess

if TYPE_CHECKING:
    from failprint.types import CmdFuncType, CmdType

if WINDOWS:
    colorama.init()


class RunResult:
    """Placeholder for a run result."""

    def __init__(self, code: int, output: str) -> None:
        """Initialize the object.

        Arguments:
            code: The exit code of the command.
            output: The output of the command.
        """
        self.code = code
        self.output = output


def run(
    cmd: CmdFuncType,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    number: int = 1,
    capture: str | bool | Capture | None = None,
    title: str | None = None,
    fmt: str | None = None,
    pty: bool = False,
    progress: bool = True,
    nofail: bool = False,
    quiet: bool = False,
    silent: bool = False,
    stdin: str | None = None,
    command: str | None = None,
) -> RunResult:
    """Run a command in a subprocess or a Python function, and print its output if it fails.

    Arguments:
        cmd: The command to run.
        args: Arguments to pass to the callable.
        kwargs: Keyword arguments to pass to the callable.
        number: The command number.
        capture: The output to capture.
        title: The command title.
        fmt: The output format.
        pty: Whether to run in a PTY.
        progress: Whether to show progress.
        nofail: Whether to always succeed.
        quiet: Whether to not print the command output.
        silent: Don't print anything.
        stdin: String to use as standard input.
        command: The command to display.

    Returns:
        The command exit code, or 0 if `nofail` is True.
    """
    format_name: str = fmt or os.environ.get("FAILPRINT_FORMAT", DEFAULT_FORMAT)  # type: ignore[assignment]
    format_name = accept_custom_format(format_name)
    format_obj = formats.get(format_name, formats[DEFAULT_FORMAT])

    env = Environment(autoescape=False)  # noqa: S701 (no HTML: no need to escape)
    env.filters["indent"] = textwrap.indent

    command = command if command is not None else printable_command(cmd, args, kwargs)

    if not silent and progress and format_obj.progress_template:
        progress_template = env.from_string(format_obj.progress_template)
        ansiprint(progress_template.render({"title": title, "command": command}), end="\r")

    capture = Capture.cast(capture)

    if callable(cmd):
        code, output = run_function(cmd, args=args, kwargs=kwargs, capture=capture, stdin=stdin)
    else:
        code, output = run_command(cmd, capture=capture, ansi=format_obj.accept_ansi, pty=pty, stdin=stdin)

    if not silent:
        template = env.from_string(format_obj.template)
        ansiprint(
            template.render(
                {
                    "title": title,
                    "command": command,
                    "code": code,
                    "success": code == 0,
                    "failure": code != 0,
                    "number": number,
                    "output": output,
                    "nofail": nofail,
                    "quiet": quiet,
                    "silent": silent,
                },
            ),
        )

    return RunResult(0 if nofail else code, output)


def run_command(
    cmd: CmdType,
    *,
    capture: Capture = Capture.BOTH,
    ansi: bool = False,
    pty: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        ansi: Whether to accept ANSI sequences.
        pty: Whether to run in a PTY.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command output.
    """
    shell = isinstance(cmd, str)

    # if chosen format doesn't accept ansi, or on Windows, don't use pty
    if pty and (not ansi or WINDOWS):
        pty = False

    # pty can only combine, so only use pty when combining
    if pty and capture in {Capture.BOTH, Capture.NONE}:
        if shell:
            cmd = ["sh", "-c", cmd]  # type: ignore[list-item]  # we know cmd is str
        return run_pty_subprocess(cmd, capture=capture, stdin=stdin)  # type: ignore[arg-type]  # we made sure cmd is a list

    # we are on Windows
    if WINDOWS:
        # make sure the process can find the executable
        if not shell:
            cmd[0] = shutil.which(cmd[0]) or cmd[0]  # type: ignore[index]  # we know cmd is a list
        return run_subprocess(cmd, capture=capture, shell=shell, stdin=stdin)

    return run_subprocess(cmd, capture=capture, shell=shell, stdin=stdin)


def run_function(
    func: Callable,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    capture: Capture = Capture.BOTH,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a function.

    Arguments:
        func: The function to run.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
        capture: The output to capture.
        stdin: String to use as standard input.

    Returns:
        The exit code and the function output.
    """
    args = args or []
    kwargs = kwargs or {}

    if capture == Capture.NONE:
        return run_function_get_code(func, args=args, kwargs=kwargs), ""

    with capture.here(stdin=stdin) as captured:
        code = run_function_get_code(func, args=args, kwargs=kwargs)

    return code, str(captured)


def run_function_get_code(
    func: Callable,
    *,
    args: Sequence,
    kwargs: dict,
) -> int:
    """Run a function and return a exit code.

    Arguments:
        func: The function to run.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        An exit code.
    """
    try:
        result = func(*args, **kwargs)
    except SystemExit as exit:
        if exit.code is None:
            return 0
        if isinstance(exit.code, int):
            return exit.code
        sys.stderr.write(str(exit.code))
        return 1
    except Exception:  # noqa: BLE001
        sys.stderr.write(traceback.format_exc() + "\n")
        return 1

    # if func was a lazy callable, recurse
    if isinstance(result, LazyCallable):
        return run_function_get_code(result, args=(), kwargs={})

    # first check True and False
    # because int(True) == 1 and int(False) == 0
    if result is True:
        return 0
    if result is False:
        return 1
    try:
        return int(result)
    except (ValueError, TypeError):
        if result is None or bool(result):
            return 0
        return 1


__all__ = [
    "run",
    "run_command",
    "run_function",
    "run_function_get_code",
    "RunResult",
]
