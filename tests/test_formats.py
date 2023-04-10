"""Tests for the `formats` module."""

from typing import Callable, Sequence

import pytest
from hypothesis import given
from hypothesis.strategies import text

from failprint.formats import printable_command
from failprint.runners import run


@pytest.mark.parametrize(
    ("cmd", "expected"),
    [
        # empty arg
        (["an", "empty", ""], 'an empty ""'),
        # normal command
        (["a", "normal", "command"], "a normal command"),
        # spaces
        (["a", "command", "with", " "], 'a command with " "'),
        # single quotes
        (["a", "command", "with", "'"], 'a command with "\'"'),
        # double quotes
        (["a", "command", "with", '"'], "a command with '\"'"),
        # both quotes
        (["a", "command", "with", "\"'"], 'a command with "\\"\'"'),
        # both quotes and spaces
        (["a", "command", "with", "\" '"], 'a command with "\\" \'"'),
    ],
)
def test_printable_command_with_list(cmd: list[str], expected: str) -> None:
    """Correctly transform a list of arguments into a runnable shell command.

    Arguments:
        cmd: The command as a list of arguments.
        expected: The expected result after transformation.
    """
    assert printable_command(cmd) == expected


@given(text())
def test_printable_command_with_string(cmd: str) -> None:
    """Correctly transform a string into a runnable shell command.

    Arguments:
        cmd: The command as a string.
    """
    assert printable_command(cmd) == cmd


class Repr:  # noqa: D101 (missing docstring)
    def __init__(self, value: str | int):  # noqa: D107 (missing docstring)
        self.value = value

    def __repr__(self):
        return f"Repr(value={self.value!r})"


@pytest.mark.parametrize(
    ("cmd", "args", "kwargs", "expected"),
    [
        (lambda: 0, None, None, "<lambda>()"),
        (lambda _: _, None, None, "<lambda>()"),
        (lambda: 0, [6], None, "<lambda>(6)"),
        (lambda _: _, [6], None, "<lambda>(6)"),
        (lambda: 0, None, {"kwarg": "hello"}, "<lambda>(kwarg='hello')"),
        (lambda _: _, None, {"kwarg": 6}, "<lambda>(kwarg=6)"),
        (lambda: 0, [6, 7], {"kwarg": 3.2}, "<lambda>(6, 7, kwarg=3.2)"),
        (lambda _: _, [True, None, 5.5], {"kwarg": True}, "<lambda>(True, None, 5.5, kwarg=True)"),
        (
            printable_command,
            [Repr(0)],
            {"repr": Repr("marvin")},
            "printable_command(Repr(value=0), repr=Repr(value='marvin'))",
        ),
    ],
)
def test_printable_command_with_callable(
    cmd: Callable,
    args: Sequence | None,
    kwargs: dict | None,
    expected: str,
) -> None:
    """Correctly transform a callable into a runnable shell command.

    Arguments:
        cmd: The command as a string.
        args: Arguments passed to `printable_command`.
        kwargs: Keyword arguments passed to `printable_command`.
        expected: The expected result after transformation.
    """
    assert printable_command(cmd, args, kwargs) == expected


def test_tap_format(capsys: pytest.CaptureFixture) -> None:
    """Check the tap output format.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run(["true"], fmt="tap")
    outerr = capsys.readouterr()
    assert "ok" in outerr.out
    run(["false"], fmt="tap")
    outerr = capsys.readouterr()
    assert "not ok" in outerr.out
