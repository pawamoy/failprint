"""Tests for the `cli` module."""

import pytest

from failprint import cli


def test_main():
    """Fails without arguments."""
    with pytest.raises(SystemExit):
        cli.main([])


def test_main_help(capsys):
    """Shows help."""
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "failprint" in captured.out
