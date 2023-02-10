"""Tests for the `cli` module."""

import pytest

from failprint import cli


def test_fail_without_arguments():
    """Fails without arguments."""
    with pytest.raises(SystemExit):
        cli.main([])


def test_show_help(capsys):
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "failprint" in captured.out


def test_run_command():
    """Run a simple command."""
    assert cli.main(["echo", "hello"]) == 0


def test_accept_custom_format(capsys):
    """
    Run a command with a custom output format.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["--no-progress", "-f", "custom={{output}}", "echo", "custom"]) == 0
    outerr = capsys.readouterr()
    assert "custom" in outerr.out
