"""Special types.

Attributes:
    CmdType: Type for a command.
    CmdFuncType: Type for a command or function.
"""

from __future__ import annotations

from typing import Callable, Union

from failprint.lazy import LazyCallable

CmdType = Union[str, list[str]]
CmdFuncType = Union[CmdType, Callable, LazyCallable]

__all__ = ["CmdFuncType", "CmdType"]
