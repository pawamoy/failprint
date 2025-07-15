"""failprint package.

Run a command, print its output only if it fails.
"""

from __future__ import annotations

from failprint._internal.capture import Capture, CaptureManager
from failprint._internal.cli import ArgParser, add_flags, get_parser, main
from failprint._internal.formats import (
    Format,
    accept_custom_format,
    as_python_statement,
    as_shell_command,
    formats,
    printable_command,
)
from failprint._internal.lazy import LazyCallable, lazy
from failprint._internal.process import WINDOWS
from failprint._internal.runners import (
    RunResult,
    run,
    run_command,
    run_function,
    run_function_get_code,
    run_pty_subprocess,
    run_subprocess,
)
from failprint._internal.types import CmdFuncType, CmdType

__all__: list[str] = [
    "WINDOWS",
    "ArgParser",
    "Capture",
    "CaptureManager",
    "CmdFuncType",
    "CmdType",
    "Format",
    "LazyCallable",
    "RunResult",
    "accept_custom_format",
    "add_flags",
    "as_python_statement",
    "as_shell_command",
    "formats",
    "get_parser",
    "lazy",
    "main",
    "printable_command",
    "run",
    "run_command",
    "run_function",
    "run_function_get_code",
    "run_pty_subprocess",
    "run_subprocess",
]
