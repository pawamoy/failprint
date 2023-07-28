"""Output-printing formats."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Callable, Sequence

from failprint.lazy import LazyCallable

if TYPE_CHECKING:
    from types import FrameType

    from failprint.types import CmdFuncType

DEFAULT_FORMAT = "pretty"
DEFAULT_CALLABLE_NAME = "callable"


class Format:
    """Class to define a display format."""

    def __init__(self, template: str, *, progress_template: str | None = None, accept_ansi: bool = True) -> None:
        """Initialize the object.

        Arguments:
            template: The main template.
            progress_template: The template to show progress.
            accept_ansi: Whether to accept ANSI sequences.
        """
        self.template = template
        self.progress_template = progress_template
        self.accept_ansi = accept_ansi


formats: dict[str, Format] = {
    "pretty": Format(
        "{% if success %}<green>✓</green>"
        "{% elif nofail %}<yellow>✗</yellow>"
        "{% else %}<red>✗</red>{% endif %} "
        "<bold>{{ title or command }}</bold>"
        "{% if failure %} ({{ code }}){% endif %}"
        "{% if failure and output and not quiet %}\n"
        "{{ ('  > ' + command + '\n') if title and command else '' }}"
        "{{ output|indent(2 * ' ') }}{% endif %}",
        progress_template="> {{ title or command }}",
    ),
    "tap": Format(
        "{% if failure %}not {% endif %}ok {{ number }} - {{ title or command }}"
        "{% if failure and output %}\n  ---\n  "
        "{{ ('command: ' + command + '\n  ') if title and command else '' }}"
        "output: |\n{{ output|indent(4 * ' ') }}\n  ...{% endif %}",
        accept_ansi=False,
    ),
}


def accept_custom_format(string: str) -> str:
    """Store the value in `formats` if it starts with custom.

    Arguments:
        string: A format name.

    Returns:
        The format name, or `custom` if it started with `custom=`.
    """
    if string.startswith("custom="):
        formats["custom"] = Format(string[7:])
        return "custom"
    return string


def printable_command(cmd: CmdFuncType, args: Sequence | None = None, kwargs: dict | None = None) -> str:
    """Transform a command or function into a string.

    Arguments:
        cmd: The command or function to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A shell command or python statement string.
    """
    if isinstance(cmd, str):
        return cmd
    if callable(cmd):
        return as_python_statement(cmd, args, kwargs)
    return as_shell_command(cmd)


def as_shell_command(cmd: list[str]) -> str:
    """Rebuild a command line from system arguments.

    Arguments:
        cmd: The command as a list of strings.

    Returns:
        A printable and shell-runnable command.
    """
    parts = []
    for part in cmd:
        if not part:
            parts.append('""')
            continue
        has_spaces = " " in part
        has_double_quotes = '"' in part
        has_single_quotes = "'" in part
        if has_double_quotes and not has_single_quotes:
            # double quotes, no single quotes
            # -> wrap in single quotes
            part = f"'{part}'"  # noqa: PLW2901
        elif has_single_quotes and has_double_quotes:
            # double and single quotes
            # -> escape double quotes, wrap in double quotes
            part = part.replace('"', r"\"")  # noqa: PLW2901
            part = f'"{part}"'  # noqa: PLW2901
        elif has_single_quotes or has_spaces:
            # spaces or single quotes
            # -> wrap in double quotes
            part = f'"{part}"'  # noqa: PLW2901
        parts.append(part)
    return " ".join(parts)


def as_python_statement(func: Callable | LazyCallable, args: Sequence | None = None, kwargs: dict | None = None) -> str:
    """Transform a callable and its arguments into a Python statement string.

    Arguments:
        func: The callable to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A Python statement.
    """
    if isinstance(func, LazyCallable):
        callable_name = func.name or _get_callable_name(func.call)
        args = args or func.args
        kwargs = kwargs or func.kwargs
    else:
        callable_name = _get_callable_name(func)
    args_str = [repr(arg) for arg in args] if args else []
    kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()] if kwargs else []
    arguments = ", ".join(args_str + kwargs_str)
    return f"{callable_name}({arguments})"


def _get_callable_name(callee: Callable) -> str:
    callable_name = getattr(callee, "__name__", None)
    if callable_name:
        return callable_name

    # Climb back up the frames to search the callable in the locals
    callable_name = None
    caller_frame: FrameType = inspect.currentframe()  # type: ignore[assignment]
    while callable_name is None and caller_frame.f_back:
        caller_frame = caller_frame.f_back
        callable_name = _find_callable_name_in_frame_locals(caller_frame, callee)

    return callable_name or DEFAULT_CALLABLE_NAME


def _find_callable_name_in_frame_locals(caller_frame: FrameType, callee: Callable) -> str | None:
    call_vars = caller_frame.f_locals.items()
    try:
        # ignore @py_assert variables from pytest
        return next(var_name for var_name, var_val in call_vars if var_val is callee and not var_name.startswith("@"))
    except StopIteration:
        return None


__all__ = [
    "accept_custom_format",
    "as_python_statement",
    "as_shell_command",
    "Format",
    "formats",
    "printable_command",
]
