"""Tests for the `runners` module."""

import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest
from hypothesis import given
from hypothesis.strategies import characters, integers, text

from failprint.capture import Capture
from failprint.lazy import lazy
from failprint.process import WINDOWS
from failprint.runners import run, run_function


def test_run_silent_command_silently(capsys: pytest.CaptureFixture) -> None:
    """Run a silent command, silently.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run(["true"], silent=True)
    outerr = capsys.readouterr()
    assert not outerr.out
    assert not outerr.err


def test_run_verbose_command_silently(capsys: pytest.CaptureFixture) -> None:
    """Run a verbose command, silently.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run("echo VERBS", silent=True)
    outerr = capsys.readouterr()
    assert not outerr.out
    assert not outerr.err


def test_run_silent_command_verbosely(capsys: pytest.CaptureFixture) -> None:
    """Run a silent command, verbosely.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run(["true"])
    outerr = capsys.readouterr()
    assert "true" in outerr.out
    assert not outerr.err


def test_run_failing_silent_command_verbosely(capsys: pytest.CaptureFixture) -> None:
    """Run a failing silent command, verbosely.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    run(["false"])
    outerr = capsys.readouterr()
    assert "false" in outerr.out
    assert not outerr.err


def test_run_verbose_command_verbosely(capsys: pytest.CaptureFixture) -> None:
    """Run a verbose command, verbosely.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert run("echo VERBS").code == 0
    outerr = capsys.readouterr()
    assert "VERBS" in outerr.out
    assert not outerr.err


def test_return_success_code() -> None:
    """Check the return code of a successful command."""
    assert run(["true"]).code == 0


def test_return_failure_code() -> None:
    """Check the return code of a failing command."""
    assert run(["false"]).code == 1


def test_return_shell_custom_code() -> None:
    """Check the return code of a shell exit."""
    assert run("exit 15").code == 15


@pytest.mark.skipif(WINDOWS, reason="runs on Linux only")
def test_run_linux_shell_command() -> None:
    """Run a Linux shell command.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    result = run("echo herbert | grep -o er", capture=True, silent=True)
    assert result.code == 0
    assert result.output.split("\n").count("er") == 2


@pytest.mark.skipif(WINDOWS, reason="runs on Linux only")
def test_run_linux_program() -> None:
    """Run a GNU/Linux program."""
    marker = "THIS VERY LINE"
    assert run(["grep", "-q", marker, __file__]).code == 0
    assert run(["grep", "-q", r"NOT\s*THIS\s*LINE", __file__]).code == 1


@given(integers())
def test_callable_exit_codes(code: int) -> None:
    """Check the return codes of Python callables.

    Arguments:
        code: Hypothesis fixture to provide various integers.
    """
    assert run(lambda: code).code == code


def test_handling_system_exit() -> None:
    """Check that we handle system exit."""
    assert run(lambda: sys.exit()).code == 0
    assert run(lambda: sys.exit(0)).code == 0
    assert run(lambda: sys.exit(1)).code == 1
    assert run(lambda: sys.exit("bye")).code == 1


def test_succeed_with_none_result() -> None:
    """Check the return code when a callable returns `None`."""
    assert run(lambda: None).code == 0


def test_succeed_with_truthy_object() -> None:
    """Check the return code when a callable returns a truthy object."""
    assert run(object).code == 0


def test_fails_with_falsy_object() -> None:
    """Check the return code when a callable returns a falsy object."""

    class Meh:
        def __bool__(self):
            return False

    assert run(Meh).code == 1


def test_run_callable_return_boolean() -> None:
    """Check the return code when a callable returns a boolean."""
    assert run(lambda: True).code == 0
    assert run(lambda: False).code == 1


def test_callable_capture_none(capsys: pytest.CaptureFixture) -> None:
    """Check that nothing is captured while running a callable.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    msg = "out"
    assert run(lambda: print(msg), capture=False, silent=True).code == 0
    outerr = capsys.readouterr()
    assert msg in outerr.out


def test_callable_capture_both() -> None:
    """Check that all is captured while running a callable."""
    msg_stdout = "out\n"
    msg_stderr = "err\n"
    result = run(
        lambda: sys.stdout.write(msg_stdout) and sys.stderr.write(msg_stderr),
        capture=True,
        fmt="custom={{output}}",
    )
    assert msg_stdout in result.output
    assert msg_stderr in result.output


def test_callable_capture_stdout() -> None:
    """Check that stdout is captured while running a callable."""
    msg_stdout = "out"
    msg_stderr = "err"
    result = run(
        lambda: sys.stdout.write(msg_stdout) and sys.stderr.write(msg_stderr),
        capture="stdout",
        fmt="custom={{output}}",
    )
    assert msg_stdout in result.output
    assert msg_stderr not in result.output


def test_callable_capture_stderr() -> None:
    """Check that stderr is captured while running a callable."""
    msg_stdout = "out"
    msg_stderr = "err"
    result = run(
        lambda: sys.stdout.write(msg_stdout) and sys.stderr.write(msg_stderr),
        capture="stderr",
        fmt="custom={{output}}",
    )
    assert msg_stdout not in result.output
    assert msg_stderr in result.output


def test_process_capture_none(capfd: pytest.CaptureFixture) -> None:
    """Check that nothing is captured while running a process.

    Arguments:
        capfd: Pytest fixture to capture output.
    """
    assert run([sys.executable, "-V"], capture=False, silent=True).code == 0
    outerr = capfd.readouterr()
    assert "Python" in outerr.out


def test_process_capture_both() -> None:
    """Check that all is captured while running a process."""
    msg_stdout = "out"
    msg_stderr = "err"
    result = run(
        ["bash", "-c", f"echo {msg_stdout}; echo {msg_stderr} >&2"],
        capture=True,
        fmt="custom={{output}}",
    )
    assert msg_stdout in result.output
    assert msg_stderr in result.output


def test_process_capture_stdout() -> None:
    """Check that stdout is captured while running a process."""
    msg_stdout = "out"
    msg_stderr = "err"
    result = run(
        ["bash", "-c", f"echo {msg_stdout}; echo {msg_stderr} >&2"],
        capture="stdout",
        fmt="custom={{output}}",
    )
    assert msg_stdout in result.output
    assert msg_stderr not in result.output


def test_process_capture_stderr() -> None:
    """Check that stderr is captured while running a process."""
    msg_stdout = "out"
    msg_stderr = "err"
    result = run(
        ["bash", "-c", f"echo {msg_stdout}; echo {msg_stderr} >&2"],
        capture="stderr",
        fmt="custom={{output}}",
    )
    assert msg_stdout not in result.output
    assert msg_stderr in result.output


def test_cancel_pty() -> None:
    """Test that using PTY is canceled if the format does not support it."""
    with patch("failprint.runners.run_subprocess", new=MagicMock(return_value=(0, ""))) as run_sub:  # noqa: SIM117
        with patch("failprint.runners.run_pty_subprocess", new=MagicMock(return_value=(0, ""))) as run_pty_sub:
            run("true", pty=True, fmt="tap")
            assert not run_pty_sub.called
            assert run_sub.called


@pytest.mark.skipif(WINDOWS, reason="no PTY support on Windows")
def test_run_pty_shell() -> None:
    """Test running a shell command in a PTY."""
    with patch("failprint.runners.run_pty_subprocess", new=MagicMock(return_value=(0, ""))) as run_pty_sub:
        run("true", pty=True)
        assert run_pty_sub.called


def test_run_callable_raising_exception(capfd: pytest.CaptureFixture) -> None:
    """Test running a callable raising an exception.

    Arguments:
        capfd: Pytest fixture to capture output.
    """
    assert run(lambda: 1 / 0).code == 1
    outerr = capfd.readouterr()
    assert "ZeroDivisionError:" in outerr.out


@given(text(alphabet=characters(blacklist_categories="C")))
def test_pass_stdin_to_function(stdin: str) -> None:
    """Pass input to a normal subprocess.

    Arguments:
        stdin: Text sample generated by Hypothesis.
    """

    def print_stdin() -> None:
        print(sys.stdin.read(), end="")

    code, output = run_function(print_stdin, stdin=stdin)
    assert code == 0
    assert output == stdin


def test_run_lazy_callable(capfd: pytest.CaptureFixture) -> None:
    """Assert we can run a lazy callable and stringify it.

    Arguments:
        capfd: Pytest fixture to capture output.
    """

    @lazy
    def greet(name: str) -> int:
        print(f"hello {name}")
        return 1

    result = run(greet("tim"))
    outerr = capfd.readouterr()
    assert result.code == 1
    assert result.output == "hello tim\n"
    assert "greet('tim')" in outerr.out


def test_run_lazy_callable_without_calling_it(capfd: pytest.CaptureFixture) -> None:
    """Assert we can run a lazy callable without actually calling it.

    Arguments:
        capfd: Pytest fixture to capture output.
    """

    @lazy
    def greet(name: str) -> int:
        print(f"hello {name}")
        return 1

    result = run(greet, args=["tim"])
    outerr = capfd.readouterr()
    assert result.code == 1
    assert result.output == "hello tim\n"
    assert "greet('tim')" in outerr.out


def test_capture_function_and_subprocess_output(capsys: pytest.CaptureFixture) -> None:
    """Assert we capture everything when running a function.

    Arguments:
        capsys: Pytest fixture to capture output.
    """

    def function() -> None:
        print("print")
        sys.stdout.write("sys stdout write\n")
        os.system("echo os system")  # noqa: S605,S607
        subprocess.run(["sh", "-c", "echo sh -c echo"])  # noqa: S603,S607

    with capsys.disabled(), Capture.BOTH.here() as captured:
        function()

    lines = str(captured).rstrip("\n").split("\n")
    assert lines == ["print", "sys stdout write", "os system", "sh -c echo"]
