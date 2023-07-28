"""failprint package.

Run a command, print its output only if it fails.
"""

from __future__ import annotations

from failprint.capture import Capture, CaptureManager
from failprint.cli import main
from failprint.formats import Format, formats
from failprint.lazy import LazyCallable, lazy
from failprint.process import WINDOWS
from failprint.runners import run

__all__: list[str] = [
    "Capture",
    "CaptureManager",
    "Format",
    "formats",
    "lazy",
    "LazyCallable",
    "main",
    "run",
    "WINDOWS",
]
