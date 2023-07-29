"""Enumeration of possible output captures."""

from __future__ import annotations

import enum
import os
import sys
import tempfile
from contextlib import contextmanager
from io import StringIO
from typing import IO, TYPE_CHECKING, Iterator, TextIO

if TYPE_CHECKING:
    from types import TracebackType


class Capture(enum.Enum):
    """An enum to store the different possible output types."""

    STDOUT: str = "stdout"
    STDERR: str = "stderr"
    BOTH: str = "both"
    NONE: str = "none"

    def __str__(self):
        return self.value.lower()

    @classmethod
    def cast(cls, value: str | bool | Capture | None) -> Capture:
        """Cast a value to an actual Capture enumeration value.

        Arguments:
            value: The value to cast.

        Returns:
            A Capture enumeration value.
        """
        if value is None:
            return cls.BOTH
        if value is True:
            return cls.BOTH
        if value is False:
            return cls.NONE
        if isinstance(value, cls):
            return value
        # consider it's a string
        # let potential errors bubble up
        return cls(value)

    @contextmanager
    def here(self, stdin: str | None = None) -> Iterator[CaptureManager]:
        """Context manager to capture standard output/error.

        Parameters:
            stdin: Optional input.

        Yields:
            A lazy string with the captured contents.

        Examples:
            >>> def print_things() -> None:
            ...     print("1")
            ...     sys.stderr.write("2\\n")
            ...     os.system("echo 3")
            ...     subprocess.run(["sh", "-c", "echo 4 >&2"])
            >>> with Capture.BOTH.here() as captured:
            ...     print_things()
            ... print(captured)
            1
            2
            3
            4
        """  # noqa: D301
        with CaptureManager(self, stdin=stdin) as captured:
            yield captured


class CaptureManager:
    """Context manager to capture standard output and error at the file descriptor level.

    Usable directly through [`Capture.here`][failprint.capture.Capture.here].

    Examples:
        >>> def print_things() -> None:
        ...     print("1")
        ...     sys.stderr.write("2\\n")
        ...     os.system("echo 3")
        ...     subprocess.run(["sh", "-c", "echo 4 >&2"])
        >>> with CaptureManager(Capture.BOTH) as captured:
        ...     print_things()
        ... print(captured)
        1
        2
        3
        4
    """  # noqa: D301

    def __init__(self, capture: Capture = Capture.BOTH, stdin: str | None = None) -> None:
        """Initialize the context manager.

        Parameters:
            capture: What to capture.
            stdin: Optional input.
        """
        self._temp_file: IO[str] | None = None
        self._capture = capture
        self._devnull: TextIO | None = None
        self._stdin = stdin
        self._saved_stdin: TextIO | None = None
        self._stdout_fd: int = -1
        self._stderr_fd: int = -1
        self._saved_stdout_fd: int = -1
        self._saved_stderr_fd: int = -1
        self._output: str | None = None

    def __enter__(self) -> CaptureManager:
        if self._capture is Capture.NONE:
            return self

        # Flush library buffers that dup2 knows nothing about.
        sys.stdout.flush()
        sys.stderr.flush()

        # Patch sys.stdin if needed.
        if self._stdin is not None:
            self._saved_stdin = sys.stdin
            sys.stdin = StringIO(self._stdin)

        # Open devnull if needed.
        if self._capture in {Capture.STDOUT, Capture.STDERR}:
            self._devnull = open(os.devnull, "w")  # noqa: SIM115

        # Create temporary file.
        # Initially we used a pipe but it would hang on writes given enough output.
        self._temp_file = tempfile.TemporaryFile("w+", encoding="utf8", prefix="failprint-")
        fdw = self._temp_file.fileno()

        # Redirect stdout to temporary file or devnull.
        self._stdout_fd = sys.stdout.fileno()
        self._saved_stdout_fd = os.dup(self._stdout_fd)
        if self._capture in {Capture.BOTH, Capture.STDOUT}:
            os.dup2(fdw, self._stdout_fd)
        elif self._capture is Capture.STDERR:
            os.dup2(self._devnull.fileno(), self._stdout_fd)  # type: ignore[union-attr]

        # Redirect stderr to temporary file or devnull.
        self._stderr_fd = sys.stderr.fileno()
        self._saved_stderr_fd = os.dup(self._stderr_fd)
        if self._capture in {Capture.BOTH, Capture.STDERR}:
            os.dup2(fdw, self._stderr_fd)
        elif self._capture is Capture.STDOUT:
            os.dup2(self._devnull.fileno(), self._stderr_fd)  # type: ignore[union-attr]

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        if self._capture is Capture.NONE:
            return

        # Flush everything before reading from pipe.
        sys.stdout.flush()
        sys.stderr.flush()

        # Restore stdin to its previous value.
        if self._saved_stdin is not None:
            sys.stdin = self._saved_stdin

        # Close devnull if needed.
        if self._devnull is not None:
            self._devnull.close()

        # Restore stdout and stderr to their previous values.
        os.dup2(self._saved_stdout_fd, self._stdout_fd)
        os.dup2(self._saved_stderr_fd, self._stderr_fd)

        # Read contents from temporary file, close it.
        if self._temp_file is not None:
            self._temp_file.seek(0)
            self._output = self._temp_file.read()
            self._temp_file.close()

    def __str__(self) -> str:
        return self.output

    @property
    def output(self) -> str:
        """Captured output.

        Raises:
            RuntimeError: When accessing captured output before exiting the context manager.
        """
        if self._output is None:
            raise RuntimeError("Not finished capturing")
        return self._output


__all__ = ["Capture", "CaptureManager"]
