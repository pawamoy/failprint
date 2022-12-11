"""Enumeration of possible output captures."""

from __future__ import annotations

import enum
import sys
from contextlib import contextmanager
from io import StringIO
from typing import Iterator, TextIO


class Capture(enum.Enum):
    """An enum to store the different possible output types."""

    STDOUT: str = "stdout"  # noqa: WPS115
    STDERR: str = "stderr"  # noqa: WPS115
    BOTH: str = "both"  # noqa: WPS115
    NONE: str = "none"  # noqa: WPS115

    def __str__(self):
        return self.value.lower()  # noqa: E1101 (false-positive)


def cast_capture(value: str | bool | Capture | None) -> Capture:
    """
    Cast a value to an actual Capture enumeration value.

    Arguments:
        value: The value to cast.

    Returns:
        A Capture enumeration value.
    """
    if value is None:
        return Capture.BOTH
    if value is True:
        return Capture.BOTH
    if value is False:
        return Capture.NONE
    if isinstance(value, Capture):
        return value
    # consider it's a string
    # let potential errors bubble up
    return Capture(value)


class _TextBuffer(StringIO):
    class _BytesBuffer:  # noqa: WPS431
        def __init__(self, text_buffer: _TextBuffer) -> None:
            self._text_buffer = text_buffer

        def flush(self) -> None:
            ...

        def write(self, value: bytes) -> int:
            return self._text_buffer.write(value.decode())

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.buffer = self._BytesBuffer(self)  # type: ignore[misc,assignment]


class StdBuffer:
    """A simple placeholder for three memory buffers."""

    def __init__(
        self,
        stdinput: str | None = None,
        stdout: _TextBuffer | None = None,
        stderr: _TextBuffer | None = None,
    ):
        """
        Initialize the object.

        Arguments:
            stdinput: String to use as standard input.
            stdout: A buffer for standard output.
            stderr: A buffer for standard error.
        """
        self.stdin: StringIO | TextIO = StringIO(stdinput) if stdinput is not None else sys.stdin
        self.stdout: _TextBuffer = stdout or _TextBuffer()
        self.stderr: _TextBuffer = stderr or _TextBuffer()


@contextmanager
def stdbuffer(stdinput: str | None = None) -> Iterator[StdBuffer]:
    """
    Capture output in a `with` statement.

    Arguments:
        stdinput: String to use as standard input.

    Yields:
        An instance of `StdBuffer`.
    """
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    buffer = StdBuffer(stdinput)

    sys.stdin = buffer.stdin
    sys.stdout = buffer.stdout
    sys.stderr = buffer.stderr

    yield buffer

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    buffer.stdin.close()
    buffer.stdout.close()
    buffer.stderr.close()
