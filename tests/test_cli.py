"""Tests for the `cli` module."""

import pytest

from failprint import cli


def test_main():
    """Fails without arguments."""
    with pytest.raises(SystemExit):
        cli.main([])


def test_show_help(capsys):
    """
    Shows help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "failprint" in captured.out


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
def test_printable_command(cmd, expected) -> None:
    """
    Correctly transform a list of arguments into a runnable shell command.

    Arguments:
        cmd: The command as a list of arguments.
        expected: The expected result after transformation.
    """
    assert cli.printable_command(cmd) == expected
