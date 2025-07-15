"""Tests for the CLI."""

from __future__ import annotations

import sys

import pytest

from failprint._internal import debug
from failprint._internal.cli import main


def test_fail_without_arguments() -> None:
    """Fails without arguments."""
    with pytest.raises(SystemExit):
        main([])


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["-h"])
    captured = capsys.readouterr()
    assert "failprint" in captured.out


def test_run_command() -> None:
    """Run a simple command."""
    assert main(["--", sys.executable, "-c", "print('hello')"]) == 0


def test_accept_custom_format(capsys: pytest.CaptureFixture) -> None:
    """Run a command with a custom output format.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert main(["--no-progress", "-f", "custom={{output}}", "--", sys.executable, "-c", "print('custom')"]) == 0
    outerr = capsys.readouterr()
    assert "custom" in outerr.out


def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["-V"])
    captured = capsys.readouterr()
    assert debug._get_version() in captured.out


def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured
