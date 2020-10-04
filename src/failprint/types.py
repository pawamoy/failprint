"""
Special types.

Attributes:
    CmdType: Type for a command.
    CmdFuncType: Type for a command or function.
"""

from typing import Callable, List, Union

CmdType = Union[str, List[str]]
CmdFuncType = Union[CmdType, Callable]
