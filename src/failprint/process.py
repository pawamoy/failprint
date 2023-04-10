"""Functions related to subprocesses."""

from __future__ import annotations

import contextlib
import subprocess
from typing import TYPE_CHECKING

from failprint import WINDOWS
from failprint.capture import Capture
from failprint.formats import printable_command

if TYPE_CHECKING:
    from failprint.types import CmdType

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

    process = subprocess.run(
        cmd,
        input=stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
        shell=shell,
        text=True,
        encoding="utf8",
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
