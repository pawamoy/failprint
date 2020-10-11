"""Tests for the `formats` module."""

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
        (["a", "command", "with", "\"'"], 'a command with "\\"\'"'),  # noqa: WPS342 (raw string)
        # both quotes and spaces
        (["a", "command", "with", "\" '"], 'a command with "\\" \'"'),  # noqa: WPS342 (raw string)
    ],
)
def test_printable_command_with_list(cmd, expected) -> None:
    """
    Correctly transform a list of arguments into a runnable shell command.

    Arguments:
        cmd: The command as a list of arguments.
        expected: The expected result after transformation.
    """
    assert printable_command(cmd) == expected


@given(text())
def test_printable_command_with_string(cmd):
    """
    Correctly transform a string into a runnable shell command.

    Arguments:
        cmd: The command as a string.
    """
    assert printable_command(cmd) == cmd


class Repr:  # noqa: D101,C0115 (missing docstring)
    def __init__(self, value):  # noqa: D107 (missing docstring)
        self.value = value

    def __repr__(self):
        return f"Repr(value={self.value!r})"


@pytest.mark.parametrize(
    ("cmd", "args", "kwargs", "expected"),
    [
        (lambda: 0, None, None, "<lambda>()"),  # noqa: WPS522 (implicit primitive/lambda)
        (lambda _: _, None, None, "<lambda>()"),
        (lambda: 0, [6], None, "<lambda>(6)"),  # noqa: WPS522
        (lambda _: _, [6], None, "<lambda>(6)"),
        (lambda: 0, None, {"kwarg": "hello"}, "<lambda>(kwarg='hello')"),  # noqa: WPS522
        (lambda _: _, None, {"kwarg": 6}, "<lambda>(kwarg=6)"),
        (lambda: 0, [6, 7], {"kwarg": 3.2}, "<lambda>(6, 7, kwarg=3.2)"),  # noqa: WPS522
        (lambda _: _, [True, None, 5.5], {"kwarg": True}, "<lambda>(True, None, 5.5, kwarg=True)"),
        (
            printable_command,
            [Repr(0)],
            {"repr": Repr("marvin")},
            "printable_command(Repr(value=0), repr=Repr(value='marvin'))",
        ),
    ],
)
def test_printable_command_with_callable(cmd, args, kwargs, expected):
    """
    Correctly transform a callable into a runnable shell command.

    Arguments:
        cmd: The command as a string.
        args: Arguments passed to `printable_command`.
        kwargs: Keyword arguments passed to `printable_command`.
        expected: The expected result after transformation.
    """
    assert printable_command(cmd, args, kwargs) == expected


def test_tap_format(capsys):
    """
    Check the tap output format.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run(["true"], fmt="tap")
    outerr = capsys.readouterr()
    assert "ok" in outerr.out
    run(["false"], fmt="tap")
    outerr = capsys.readouterr()
    assert "not ok" in outerr.out
