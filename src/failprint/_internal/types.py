# Special types.

from __future__ import annotations

from typing import Callable, Union

from failprint._internal.lazy import LazyCallable

CmdType = Union[str, list[str]]
"""Type for a command."""
CmdFuncType = Union[CmdType, Callable, LazyCallable]
"""Type for a command or function."""

__all__ = ["CmdFuncType", "CmdType"]
