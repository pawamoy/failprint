"""Functions to run commands and capture output."""

import enum
import os
import shutil
import subprocess  # noqa: S404 (we don't mind the security implication)
import sys
import textwrap
import traceback
from contextlib import contextmanager
from io import StringIO
from typing import Callable, List, Optional, Tuple, Union

from ansimarkup import ansiprint
from jinja2 import Environment

from failprint.formats import DEFAULT_FORMAT, Format, accept_custom_format, formats, printable_command
from failprint.types import CmdFuncType, CmdType

try:
    from ptyprocess import PtyProcessUnicode
except ModuleNotFoundError:
    # it does not work on Windows
    PtyProcessUnicode = None  # noqa: WPS440 (block variable overlap)


class Output(enum.Enum):
    """An enum to store the different possible output types."""

    STDOUT: str = "stdout"  # noqa: WPS115
    STDERR: str = "stderr"  # noqa: WPS115
    COMBINE: str = "combine"  # noqa: WPS115
    NOCAPTURE: str = "nocapture"  # noqa: WPS115

    def __str__(self):
        return self.value.lower()  # noqa: E1101 (false-positive)


class StdBuffer:
    """A simple placeholder for two memory buffers."""

    def __init__(self, out=None, err=None):
        """
        Initialize the object.

        Arguments:
            out: A buffer for standard output.
            err: A buffer for standard error.
        """
        self.out = out or StringIO()
        self.err = err or StringIO()


@contextmanager
def stdbuffer():
    """
    Capture output in a `with` statement.

    Yields:
        An instance of `StdBuffer`.
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    buffer = StdBuffer()

    sys.stdout = buffer.out
    sys.stderr = buffer.err

    yield buffer

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    buffer.out.close()
    buffer.err.close()


def run(  # noqa: WPS231 (high complexity)
    cmd: CmdFuncType,
    args=None,
    kwargs=None,
    number: int = 1,
    output_type: Optional[Union[str, Output]] = None,
    title: Optional[str] = None,
    fmt: Optional[str] = None,
    pty: bool = False,
    progress: bool = True,
    nofail: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> int:
    """
    Run a command in a subprocess or a Python function, and print its output if it fails.

    Arguments:
        cmd: The command to run.
        args: Arguments to pass to the callable.
        kwargs: Keyword arguments to pass to the callable.
        number: The command number.
        output_type: The type of output.
        title: The command title.
        fmt: The output format.
        pty: Whether to run in a PTY.
        progress: Whether to show progress.
        nofail: Whether to always succeed.
        quiet: Whether to not print the command output.
        silent: Don't print anything.

    Returns:
        The command exit code, or 0 if `nofail` is True.
    """
    format_name: str = fmt or os.environ.get("FAILPRINT_FORMAT", DEFAULT_FORMAT)  # type: ignore
    format_name = accept_custom_format(format_name)
    format_obj = formats.get(format_name, formats[DEFAULT_FORMAT])

    env = Environment(autoescape=False)  # noqa: S701 (no HTML: no need to escape)
    env.filters["indent"] = textwrap.indent

    command = printable_command(cmd, args, kwargs)

    if not silent and progress and format_obj.progress_template:
        progress_template = env.from_string(format_obj.progress_template)
        ansiprint(progress_template.render({"title": title, "command": command}), end="\r")

    # default output method is to combine
    if output_type is None:
        output_type = Output.COMBINE

    # make sure output_type is an enum value
    elif isinstance(output_type, str):
        output_type = Output(output_type)

    if callable(cmd):
        code, output = _run_function(cmd, args, kwargs, output_type)
    else:
        code, output = _run_command(cmd, output_type, format_obj, pty)

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

    return 0 if nofail else code


def _run_command(cmd: CmdType, output_type: Output, format_obj: Format, pty: bool) -> Tuple[int, str]:
    """
    Run a command.

    Arguments:
        cmd: The command to run.
        output_type: The type of output.
        format_obj: The format to use.
        pty: Whether to run in a PTY.

    Returns:
        The exit code and the command output.
    """
    shell = isinstance(cmd, str)

    # if chosen format doesn't accept ansi, or on Windows, don't use pty
    if pty and not (format_obj.accept_ansi and PtyProcessUnicode):
        pty = False

    # pty can only combine, so only use pty when combining
    if pty and output_type in {Output.COMBINE, Output.NOCAPTURE}:
        if shell:
            cmd = ["sh", "-c", cmd]  # type: ignore  # we know cmd is str
        return _run_pty_subprocess(cmd, output_type)  # type: ignore  # we made sure cmd is a list

    # we are on Windows
    if PtyProcessUnicode is None:
        # make sure the process can find the executable
        if not shell:
            cmd[0] = shutil.which(cmd[0]) or cmd[0]  # type: ignore  # we know cmd is a list
        return _run_subprocess(cmd, output_type, shell=shell)  # noqa: S604 (shell=True)

    return _run_subprocess(cmd, output_type, shell=shell)  # noqa: S604 (shell=True)


def _run_subprocess(
    cmd: CmdType,
    output_type: Output,
    shell: bool = False,
) -> Tuple[int, str]:
    """
    Run a command in a subprocess.

    Arguments:
        cmd: The command to run.
        output_type: The type of output.
        shell: Whether to run the command in a shell.

    Returns:
        The exit code and the command output.
    """
    if output_type == Output.NOCAPTURE:
        stdout_opt = None
        stderr_opt = None

    else:
        stdout_opt = subprocess.PIPE

        if output_type == Output.COMBINE:
            stderr_opt = subprocess.STDOUT
        else:
            stderr_opt = subprocess.PIPE

    if shell and not isinstance(cmd, str):
        cmd = printable_command(cmd)

    process = subprocess.Popen(  # noqa: S603 (we trust the input)
        cmd,
        stdin=sys.stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
        shell=shell,  # noqa: S602 (shell=True)
    )
    stdout, stderr = process.communicate()

    if output_type == Output.NOCAPTURE:
        output = ""
    elif output_type == Output.STDERR:
        output = stderr.decode("utf8")
    else:
        output = stdout.decode("utf8")

    code = process.returncode

    return code, output


def _run_pty_subprocess(cmd: List[str], output_type: Output) -> Tuple[int, str]:
    """
    Run a command in a PTY subprocess.

    Arguments:
        cmd: The command to run.
        output_type: The type of output.

    Returns:
        The exit code and the command output.
    """
    process = PtyProcessUnicode.spawn(cmd)

    pty_output: List[str] = []

    while True:
        try:
            output_data = process.read()
        except EOFError:
            break
        if output_type == Output.NOCAPTURE:
            print(output_data, end="", flush=True)  # noqa: WPS421 (print)
        else:
            pty_output.append(output_data)

    process.close()

    output = "".join(pty_output)
    code = process.exitstatus

    return code, output


def _run_function(func, args=None, kwargs=None, output_type: Output = None) -> Tuple[int, str]:
    """
    Run a function.

    Arguments:
        func: The function to run.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
        output_type: The type of output.

    Returns:
        The exit code and the function output.
    """
    args = args or []
    kwargs = kwargs or {}

    if output_type == Output.NOCAPTURE:
        return _run_function_get_code(func, sys.stderr, args, kwargs), ""

    with stdbuffer() as buffer:
        if output_type is None or output_type == Output.COMBINE:
            # combining stdout and stderr
            # -> redirect stderr to stdout
            buffer.err = buffer.out

        code = _run_function_get_code(func, buffer.err, args, kwargs)

        if output_type == Output.STDERR:
            output = buffer.err.getvalue()
        else:
            output = buffer.out.getvalue()

    return code, output


def _run_function_get_code(func: Callable, stderr, args=None, kwargs=None) -> int:
    """
    Run a function and return a exit code.

    Arguments:
        func: The function to run.
        stderr: A file descriptor to write potential tracebacks.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        An exit code.
    """
    try:
        result = func(*args, **kwargs)
    except Exception:  # noqa: W0703 (catching Exception on purpose)
        print(traceback.format_exc(), file=stderr)  # noqa: WPS421 (print)
        return 1
    try:
        return int(result)
    except (ValueError, TypeError):
        if result is None or bool(result):
            return 0
        return 1
