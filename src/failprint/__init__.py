# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
    escape,
    formats,
    printable_command,
    unescape,
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
    "escape",
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
    "unescape",
]
