"""Output-printing formats."""

from __future__ import annotations

import inspect
from typing import Callable, Sequence

from failprint.lazy import LazyCallable
from failprint.types import CmdFuncType

DEFAULT_FORMAT = "pretty"


class Format:
    """Class to define a display format."""

    def __init__(self, template: str, progress_template: str | None = None, accept_ansi: bool = True) -> None:
        """
        Initialize the object.

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
    """
    Store the value in `formats` if it starts with custom.

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
    """
    Transform a command or function into a string.

    Arguments:
        cmd: The command or function to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A shell command or python statement string.
    """
    if isinstance(cmd, str):
        return cmd
    if isinstance(cmd, LazyCallable):
        return as_python_statement(cmd.call, cmd.args, cmd.kwargs)
    if callable(cmd):
        return as_python_statement(cmd, args, kwargs)
    return as_shell_command(cmd)


def as_shell_command(cmd: list[str]) -> str:  # noqa: WPS231 (not that complex)
    """
    Rebuild a command line from system arguments.

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
            part = f"'{part}'"
        elif has_single_quotes and has_double_quotes:
            # double and single quotes
            # -> escape double quotes, wrap in double quotes
            part = part.replace('"', r"\"")
            part = f'"{part}"'
        elif has_single_quotes or has_spaces:
            # spaces or single quotes
            # -> wrap in double quotes
            part = f'"{part}"'
        parts.append(part)
    return " ".join(parts)


def as_python_statement(func: Callable, args: Sequence | None = None, kwargs: dict | None = None) -> str:
    """
    Transform a callable and its arguments into a Python statement string.

    Arguments:
        func: The callable to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A Python statement.
    """
    func_name = getattr(func, "__name__", None)
    try:  # noqa: WPS229
        # climb back up to the frame above the call to run(),
        # to get the name passed from the external caller (user)
        ctx_run_call = inspect.currentframe().f_back.f_back.f_back.f_back  # type: ignore[union-attr]
        call_vars = ctx_run_call.f_locals.items()  # type: ignore[union-attr]
        func_name = next(var_name for var_name, var_val in call_vars if var_val is func)
    except (AttributeError, StopIteration):
        func_name = getattr(func, "__name__", "callable")

    args_str = [repr(arg) for arg in args] if args else []
    kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()] if kwargs else []  # noqa: WPS111,WPS221
    arguments = ", ".join(args_str + kwargs_str)
    return f"{func_name}({arguments})"
