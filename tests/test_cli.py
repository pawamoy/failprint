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
        (["a", "normal", "command"], "a normal command"),
        (["a", "command", "with", " "], "a command with \" \""),  # spaces
        (["a", "command", "with", "'"], "a command with \"'\""),  # single quotes
        (["a", "command", "with", '"'], "a command with '\"'"),  # double quotes
        (["a", "command", "with", "\"'"], "a command with \"\\\"'\""),  # both quotes
        (["a", "command", "with", "\" '"], "a command with \"\\\" '\""), # both quotes and spaces
    ]
)
def test_printable_command(cmd, expected):
    assert cli.printable_command(cmd) == expected
