"""Tests for the `process` module."""

import locale

import pytest

from failprint import WINDOWS
from failprint.capture import Capture
from failprint.process import decoder, get_windows_encoding, run_pty_subprocess, run_subprocess


@pytest.mark.skipif(not WINDOWS, reason="relevant on Windows only")
@pytest.mark.xfail()
def test_decoder_on_windows():
    """Test the decoder on Windows."""
    code_page = get_windows_encoding()
    assert code_page != locale.getpreferredencoding()
    text = "program not found"
    try:
        encoded = text.encode(code_page)
    except LookupError:
        pass  # noqa: WPS420
    else:
        assert decoder.decode(encoded) == text


@pytest.mark.skipif(WINDOWS, reason="relevant on Linux only")
def test_decoder_on_linux():
    """Test the decoder on Linux."""
    text = "program not found"
    assert decoder.decode(text.encode(decoder.encoding)) == text


def test_run_list_of_args_as_shell():
    """Test that a list of arguments is stringified."""
    code, output = run_subprocess(["python", "-V"], shell=True)  # noqa: S604 (shell=True)
    assert code == 0
    assert "Python" in output


def test_run_unknown_shell_command():
    """Run an unknown command in a shell."""
    code, output = run_subprocess("mlemlemlemlemle", shell=True)  # noqa: S604 (shell=True)
    assert code > 0
    assert output


def test_run_unknown_command():
    """Run an unknown command without a shell."""
    # maybe this exception should be caught in the code?
    with pytest.raises(FileNotFoundError):
        run_subprocess("mlemlemlemlemle")


@pytest.mark.skipif(WINDOWS, reason="no PTY support on Windows")
def test_run_pty_subprocess_capture_none(capsys):
    """
    Run a PTY subprocess without capturing output.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    code, output = run_pty_subprocess(["bash", "-c", "echo PTY"], capture=Capture.NONE)
    assert code == 0
    assert not output
    outerr = capsys.readouterr()
    assert "PTY" in outerr.out
