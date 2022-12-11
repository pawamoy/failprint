"""
failprint package.

Run a command, print its output only if it fails.
"""

from __future__ import annotations

import os
import sys

WINDOWS = sys.platform.startswith("win") or os.name == "nt"

__all__: list[str] = []  # noqa: WPS410 (the only __variable__ we use)
