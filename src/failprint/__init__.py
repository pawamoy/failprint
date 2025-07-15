"""failprint package.

Run a command, print its output only if it fails.
"""

from __future__ import annotations

from failprint._internal.capture import Capture, CaptureManager
from failprint._internal.cli import main
from failprint._internal.formats import Format, formats
from failprint._internal.lazy import LazyCallable, lazy
from failprint._internal.process import WINDOWS
from failprint._internal.runners import run

__all__: list[str] = [
    "WINDOWS",
    "Capture",
    "CaptureManager",
    "Format",
    "LazyCallable",
    "formats",
    "lazy",
    "main",
    "run",
]
