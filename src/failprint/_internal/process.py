# Functions related to subprocesses.

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
from typing import TYPE_CHECKING

from failprint._internal.capture import Capture
from failprint._internal.formats import printable_command

if TYPE_CHECKING:
    from failprint._internal.types import CmdType


WINDOWS = sys.platform.startswith("win") or os.name == "nt"
"""A boolean variable indicating whether the current system is Windows."""

if not WINDOWS:
    from ptyprocess import PtyProcessUnicode


def run_subprocess(
    cmd: CmdType,
    *,
    capture: Capture = Capture.BOTH,
    shell: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command in a subprocess.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        shell: Whether to run the command in a shell.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command raw output.
    """
    if capture == Capture.NONE:
        stdout_opt = None
        stderr_opt = None
    else:
        stdout_opt = subprocess.PIPE
        stderr_opt = subprocess.STDOUT if capture == Capture.BOTH else subprocess.PIPE

    if shell and not isinstance(cmd, str):
        cmd = printable_command(cmd)

    process = subprocess.run(  # noqa: S603
        cmd,
        input=stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
        shell=shell,
        text=True,
        encoding="utf8",
        check=False,
    )

    if capture == Capture.NONE:
        output = ""
    elif capture == Capture.STDERR:
        output = process.stderr
    else:
        output = process.stdout

    return process.returncode, output


def run_pty_subprocess(
    cmd: list[str],
    *,
    capture: Capture = Capture.BOTH,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command in a PTY subprocess.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command output.
    """
    process = PtyProcessUnicode.spawn(cmd)
    process.delayafterclose = 0.01  # default to 0.1
    process.delayafterterminate = 0.01  # default to 0.1
    pty_output: list[str] = []

    if stdin is not None:
        process.setecho(state=False)
        process.waitnoecho()
        process.write(stdin)
        process.sendeof()
        # not sure why but sending only one eof is not always enough,
        # so we send a second one and ignore any IO error
        with contextlib.suppress(OSError):
            process.sendeof()

    while True:
        try:
            output_data = process.read()
        except EOFError:
            break
        if capture == Capture.NONE:
            print(output_data, end="", flush=True)  # noqa: T201
        else:
            pty_output.append(output_data)

    output = "".join(pty_output).replace("\r\n", "\n")
    return process.wait(), output


__all__ = ["run_pty_subprocess", "run_subprocess"]
