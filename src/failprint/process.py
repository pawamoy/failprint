"""Functions related to subprocesses."""

from __future__ import annotations

import contextlib
import subprocess  # noqa: S404 (we don't mind the security implication)

from failprint import WINDOWS
from failprint.capture import Capture
from failprint.formats import printable_command
from failprint.types import CmdType

if not WINDOWS:
    from ptyprocess import PtyProcessUnicode


def run_subprocess(
    cmd: CmdType,
    capture: Capture = Capture.BOTH,
    shell: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]:
    """
    Run a command in a subprocess.

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

        if capture == Capture.BOTH:
            stderr_opt = subprocess.STDOUT
        else:
            stderr_opt = subprocess.PIPE

    if shell and not isinstance(cmd, str):
        cmd = printable_command(cmd)

    process = subprocess.run(  # noqa: S603,W1510 (we trust the input, and don't want to "check")
        cmd,
        input=stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
        shell=shell,  # noqa: S602 (shell=True)
        universal_newlines=True,
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
    capture: Capture = Capture.BOTH,
    stdin: str | None = None,
) -> tuple[int, str] | None:
    """
    Run a command in a PTY subprocess.

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
        process.setecho(False)
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
            print(output_data, end="", flush=True)  # noqa: WPS421 (print)
        else:
            pty_output.append(output_data)

    output = "".join(pty_output).replace("\r\n", "\n")
    return process.wait(), output
