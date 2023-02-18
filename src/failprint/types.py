"""
Special types.

Attributes:
    CmdType: Type for a command.
    CmdFuncType: Type for a command or function.
"""

from __future__ import annotations

from typing import Callable, List, Union

from failprint.lazy import LazyCallable

CmdType = Union[str, List[str]]  # noqa: E1136 (bug on Python 3.9)
CmdFuncType = Union[CmdType, Callable, LazyCallable]  # noqa: E1136 (bug on Python 3.9)
