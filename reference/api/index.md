# failprint

failprint package.

Run a command, print its output only if it fails.

Modules:

- **`capture`** – Deprecated. Import from failprint directly.
- **`cli`** – Deprecated. Import from failprint directly.
- **`debug`** – Deprecated. Import from failprint directly.
- **`formats`** – Deprecated. Import from failprint directly.
- **`lazy`** – Deprecated. Import from failprint directly.
- **`process`** – Deprecated. Import from failprint directly.
- **`runners`** – Deprecated. Import from failprint directly.

Classes:

- **`ArgParser`** – A custom argument parser with a helper method to add boolean flags.
- **`Capture`** – An enum to store the different possible output types.
- **`CaptureManager`** – Context manager to capture standard output and error at the file descriptor level.
- **`Format`** – Class to define a display format.
- **`LazyCallable`** – This class allows users to create and pass lazy callables to the runner.
- **`RunResult`** – Placeholder for a run result.

Functions:

- **`accept_custom_format`** – Store the value in formats if it starts with custom.
- **`add_flags`** – Add some boolean flags to the parser.
- **`as_python_statement`** – Transform a callable and its arguments into a Python statement string.
- **`as_shell_command`** – Rebuild a command line from system arguments.
- **`get_parser`** – Return the CLI argument parser.
- **`main`** – Run the main program.
- **`printable_command`** – Transform a command or function into a string.
- **`run`** – Run a command in a subprocess or a Python function, and print its output if it fails.
- **`run_command`** – Run a command.
- **`run_function`** – Run a function.
- **`run_function_get_code`** – Run a function and return a exit code.
- **`run_pty_subprocess`** – Run a command in a PTY subprocess.
- **`run_subprocess`** – Run a command in a subprocess.

Attributes:

- **`CmdFuncType`** – Type for a command or function.
- **`CmdType`** – Type for a command.
- **`WINDOWS`** – A boolean variable indicating whether the current system is Windows.

## CmdFuncType

```
CmdFuncType = Union[CmdType, Callable, LazyCallable]
```

Type for a command or function.

## CmdType

```
CmdType = Union[str, list[str]]
```

Type for a command.

## WINDOWS

```
WINDOWS = startswith('win') or name == 'nt'
```

A boolean variable indicating whether the current system is Windows.

## ArgParser

Bases: `ArgumentParser`

A custom argument parser with a helper method to add boolean flags.

Methods:

- **`add_bool_argument`** – Add a boolean flag/argument to the parser.

### add_bool_argument

```
add_bool_argument(
    truthy: Sequence[str],
    falsy: Sequence[str],
    truthy_help: str = "",
    falsy_help: str = "",
    **kwargs: Any,
) -> None
```

Add a boolean flag/argument to the parser.

Parameters:

- **`truthy`** (`Sequence[str]`) – Values that will store true in the destination.
- **`falsy`** (`Sequence[str]`) – Values that will store false in the destination.
- **`truthy_help`** (`str`, default: `''` ) – Help for the truthy arguments.
- **`falsy_help`** (`str`, default: `''` ) – Help for the falsy arguments.
- **`**kwargs`** (`Any`, default: `{}` ) – Remaining keyword arguments passed to argparse.ArgumentParser.add_argument.

Source code in `src/failprint/_internal/cli.py`

```
def add_bool_argument(
    self,
    truthy: Sequence[str],
    falsy: Sequence[str],
    truthy_help: str = "",
    falsy_help: str = "",
    **kwargs: Any,
) -> None:
    """Add a boolean flag/argument to the parser.

    Arguments:
        truthy: Values that will store true in the destination.
        falsy: Values that will store false in the destination.
        truthy_help: Help for the truthy arguments.
        falsy_help: Help for the falsy arguments.
        **kwargs: Remaining keyword arguments passed to `argparse.ArgumentParser.add_argument`.
    """
    truthy_kwargs = {**kwargs, "help": truthy_help, "action": "store_true"}
    falsy_kwargs = {**kwargs, "help": falsy_help, "action": "store_false"}

    mxg = self.add_mutually_exclusive_group()
    mxg.add_argument(*truthy, **truthy_kwargs)
    mxg.add_argument(*falsy, **falsy_kwargs)
```

## Capture

Bases: `Enum`

An enum to store the different possible output types.

Methods:

- **`cast`** – Cast a value to an actual Capture enumeration value.
- **`here`** – Context manager to capture standard output/error.

Attributes:

- **`BOTH`** – Capture both standard output and error.
- **`NONE`** – Do not capture anything.
- **`STDERR`** – Capture standard error.
- **`STDOUT`** – Capture standard output.

### BOTH

```
BOTH = 'both'
```

Capture both standard output and error.

### NONE

```
NONE = 'none'
```

Do not capture anything.

### STDERR

```
STDERR = 'stderr'
```

Capture standard error.

### STDOUT

```
STDOUT = 'stdout'
```

Capture standard output.

### cast

```
cast(value: str | bool | Capture | None) -> Capture
```

Cast a value to an actual Capture enumeration value.

Parameters:

- **`value`** (`str | bool | Capture | None`) – The value to cast.

Returns:

- `Capture` – A Capture enumeration value.

Source code in `src/failprint/_internal/capture.py`

```
@classmethod
def cast(cls, value: str | bool | Capture | None) -> Capture:  # noqa: FBT001
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
```

### here

```
here(stdin: str | None = None) -> Iterator[CaptureManager]
```

Context manager to capture standard output/error.

Parameters:

- **`stdin`** (`str | None`, default: `None` ) – Optional input.

Yields:

- `CaptureManager` – A lazy string with the captured contents.

Examples:

```
>>> def print_things() -> None:
...     print("1")
...     sys.stderr.write("2\n")
...     os.system("echo 3")
...     subprocess.run(["sh", "-c", "echo 4 >&2"])
>>> with Capture.BOTH.here() as captured:
...     print_things()
... print(captured)
1
2
3
4
```

Source code in `src/failprint/_internal/capture.py`

```
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
```

## CaptureManager

```
CaptureManager(
    capture: Capture = BOTH, stdin: str | None = None
)
```

Context manager to capture standard output and error at the file descriptor level.

Usable directly through Capture.here.

Examples:

```
>>> def print_things() -> None:
...     print("1")
...     sys.stderr.write("2\n")
...     os.system("echo 3")
...     subprocess.run(["sh", "-c", "echo 4 >&2"])
>>> with CaptureManager(Capture.BOTH) as captured:
...     print_things()
... print(captured)
1
2
3
4
```

Parameters:

- **`capture`** (`Capture`, default: `BOTH` ) – What to capture.
- **`stdin`** (`str | None`, default: `None` ) – Optional input.

Methods:

- **`__enter__`** – Set up the necessary file descriptors and temporary files to capture output.
- **`__exit__`** – Restore the original file descriptors and reads the captured output.

Attributes:

- **`output`** (`str`) – Captured output.

Source code in `src/failprint/_internal/capture.py`

```
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
```

### output

```
output: str
```

Captured output.

Raises:

- `RuntimeError` – When accessing captured output before exiting the context manager.

### __enter__

```
__enter__() -> CaptureManager
```

Set up the necessary file descriptors and temporary files to capture output.

Source code in `src/failprint/_internal/capture.py`

```
def __enter__(self) -> CaptureManager:  # noqa: PYI034 (false-positive)
    """Set up the necessary file descriptors and temporary files to capture output."""
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
        self._devnull = open(os.devnull, "w")

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
```

### __exit__

```
__exit__(
    exc_type: type[BaseException] | None,
    exc_value: BaseException | None,
    exc_traceback: TracebackType | None,
) -> None
```

Restore the original file descriptors and reads the captured output.

Source code in `src/failprint/_internal/capture.py`

```
def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_value: BaseException | None,
    exc_traceback: TracebackType | None,
) -> None:
    """Restore the original file descriptors and reads the captured output."""
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
```

## Format

```
Format(
    template: str,
    *,
    progress_template: str | None = None,
    accept_ansi: bool = True,
)
```

Class to define a display format.

Parameters:

- **`template`** (`str`) – The main template.
- **`progress_template`** (`str | None`, default: `None` ) – The template to show progress.
- **`accept_ansi`** (`bool`, default: `True` ) – Whether to accept ANSI sequences.

Attributes:

- **`accept_ansi`** – Whether to accept ANSI sequences.
- **`progress_template`** – The template to show progress.
- **`template`** – The main template.

Source code in `src/failprint/_internal/formats.py`

```
def __init__(self, template: str, *, progress_template: str | None = None, accept_ansi: bool = True) -> None:
    """Initialize the object.

    Arguments:
        template: The main template.
        progress_template: The template to show progress.
        accept_ansi: Whether to accept ANSI sequences.
    """
    self.template = template
    """The main template."""
    self.progress_template = progress_template
    """The template to show progress."""
    self.accept_ansi = accept_ansi
    """Whether to accept ANSI sequences."""
```

### accept_ansi

```
accept_ansi = accept_ansi
```

Whether to accept ANSI sequences.

### progress_template

```
progress_template = progress_template
```

The template to show progress.

### template

```
template = template
```

The main template.

## LazyCallable

```
LazyCallable(
    call: Callable[_P, _R],
    args: tuple,
    kwargs: dict,
    name: str | None = None,
)
```

Bases: `Generic[_R]`

This class allows users to create and pass lazy callables to the runner.

Parameters:

- **`call`** (`Callable[_P, _R]`) – The origin callable.
- **`args`** (`tuple`) – The \*args to pass when calling.
- **`kwargs`** (`dict`) – The \*\*kwargs to pass when calling.
- **`name`** (`str | None`, default: `None` ) – The name of the callable.

Methods:

- **`__call__`** – Call the lazy callable.

Attributes:

- **`args`** – The \*args to pass when calling.
- **`call`** – The original callable.
- **`kwargs`** – The \*\*kwargs to pass when calling.
- **`name`** – The name of the callable, if any.

Source code in `src/failprint/_internal/lazy.py`

```
def __init__(self, call: Callable[_P, _R], args: tuple, kwargs: dict, name: str | None = None) -> None:
    """Initialize a lazy callable.

    Parameters:
        call: The origin callable.
        args: The `*args` to pass when calling.
        kwargs: The `**kwargs` to pass when calling.
        name: The name of the callable.
    """
    self.call = call
    """The original callable."""
    self.args = args
    """The `*args` to pass when calling."""
    self.kwargs = kwargs
    """The `**kwargs` to pass when calling."""
    self.name = name
    """The name of the callable, if any."""
```

### args

```
args = args
```

The `*args` to pass when calling.

### call

```
call = call
```

The original callable.

### kwargs

```
kwargs = kwargs
```

The `**kwargs` to pass when calling.

### name

```
name = name
```

The name of the callable, if any.

### __call__

```
__call__() -> _R
```

Call the lazy callable.

Source code in `src/failprint/_internal/lazy.py`

```
def __call__(self) -> _R:
    """Call the lazy callable."""
    return self.call(*self.args, **self.kwargs)
```

## RunResult

```
RunResult(code: int, output: str)
```

Placeholder for a run result.

Parameters:

- **`code`** (`int`) – The exit code of the command.
- **`output`** (`str`) – The output of the command.

Attributes:

- **`code`** – The exit code of the command.
- **`output`** – The output of the command.

Source code in `src/failprint/_internal/runners.py`

```
def __init__(self, code: int, output: str) -> None:
    """Initialize the object.

    Arguments:
        code: The exit code of the command.
        output: The output of the command.
    """
    self.code = code
    """The exit code of the command."""
    self.output = output
    """The output of the command."""
```

### code

```
code = code
```

The exit code of the command.

### output

```
output = output
```

The output of the command.

## accept_custom_format

```
accept_custom_format(string: str) -> str
```

Store the value in `formats` if it starts with custom.

Parameters:

- **`string`** (`str`) – A format name.

Returns:

- `str` – The format name, or custom if it started with custom=.

Source code in `src/failprint/_internal/formats.py`

```
def accept_custom_format(string: str) -> str:
    """Store the value in `formats` if it starts with custom.

    Arguments:
        string: A format name.

    Returns:
        The format name, or `custom` if it started with `custom=`.
    """
    if string.startswith("custom="):
        formats["custom"] = Format(string[7:])
        return "custom"
    return string
```

## add_flags

```
add_flags(
    parser: ArgParser, *, set_defaults: bool = True
) -> ArgParser
```

Add some boolean flags to the parser.

We made this method separate and public for its use in [duty](https://github.com/pawamoy/duty).

Parameters:

- **`parser`** (`ArgParser`) – The parser to add flags to.
- **`set_defaults`** (`bool`, default: `True` ) – Whether to set default values on arguments.

Returns:

- `ArgParser` – The augmented parser.

Source code in `src/failprint/_internal/cli.py`

```
def add_flags(parser: ArgParser, *, set_defaults: bool = True) -> ArgParser:
    """Add some boolean flags to the parser.

    We made this method separate and public
    for its use in [duty](https://github.com/pawamoy/duty).

    Arguments:
        parser: The parser to add flags to.
        set_defaults: Whether to set default values on arguments.

    Returns:
        The augmented parser.
    """
    # IMPORTANT: the arguments destinations should match
    # the parameters names of the failprint.runners.run function.
    # As long as names are consistent between the two,
    # it's very easy to pass CLI args to the function,
    # and it also allows to avoid duplicating the parser arguments
    # in dependent projects like duty (https://github.com/pawamoy/duty) :)
    parser.add_argument(
        "-c",
        "--capture",
        choices=list(Capture),
        type=Capture,
        help="Which output to capture. Colors are supported with 'both' only, unless the command has a 'force color' option.",
    )
    parser.add_argument(
        "-f",
        "--fmt",
        "--format",
        dest="fmt",
        choices=formats.keys(),
        type=accept_custom_format,
        default=None,
        help="Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. "
        "Available variables: command, title (command or title passed with -t), code (exit status), "
        "success (boolean), failure (boolean), number (command number passed with -n), "
        "output (command output), nofail (boolean), quiet (boolean), silent (boolean). "
        "Available filters: indent (textwrap.indent).",
    )
    parser.add_bool_argument(
        ["-y", "--pty"],
        ["-Y", "--no-pty"],
        dest="pty",
        default=True if set_defaults else None,
        truthy_help="Enable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.",
        falsy_help="Disable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.",
    )
    parser.add_bool_argument(
        ["-p", "--progress"],
        ["-P", "--no-progress"],
        dest="progress",
        default=True if set_defaults else None,
        truthy_help="Print progress while running a command.",
        falsy_help="Don't print progress while running a command.",
    )
    # TODO: specific to the format
    parser.add_bool_argument(
        ["-q", "--quiet"],
        ["-Q", "--no-quiet"],
        dest="quiet",
        default=False if set_defaults else None,
        truthy_help="Don't print the command output, even if it failed.",
        falsy_help="Print the command output when it fails.",
    )
    # TODO: specific to the format
    parser.add_bool_argument(
        ["-s", "--silent"],
        ["-S", "--no-silent"],
        dest="silent",
        default=False if set_defaults else None,
        truthy_help="Don't print anything.",
        falsy_help="Print output as usual.",
    )
    parser.add_bool_argument(
        ["-z", "--zero", "--nofail"],
        ["-Z", "--no-zero", "--strict"],
        dest="nofail",
        default=False if set_defaults else None,
        truthy_help="Don't fail. Always return a success (0) exit code.",
        falsy_help="Return the original exit code.",
    )
    return parser
```

## as_python_statement

```
as_python_statement(
    func: Callable | LazyCallable,
    args: Sequence | None = None,
    kwargs: dict | None = None,
) -> str
```

Transform a callable and its arguments into a Python statement string.

Parameters:

- **`func`** (`Callable | LazyCallable`) – The callable to transform.
- **`args`** (`Sequence | None`, default: `None` ) – Positional arguments passed to the function.
- **`kwargs`** (`dict | None`, default: `None` ) – Keyword arguments passed to the function.

Returns:

- `str` – A Python statement.

Source code in `src/failprint/_internal/formats.py`

```
def as_python_statement(func: Callable | LazyCallable, args: Sequence | None = None, kwargs: dict | None = None) -> str:
    """Transform a callable and its arguments into a Python statement string.

    Arguments:
        func: The callable to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A Python statement.
    """
    if isinstance(func, LazyCallable):
        callable_name = func.name or _get_callable_name(func.call)
        args = args or func.args
        kwargs = kwargs or func.kwargs
    else:
        callable_name = _get_callable_name(func)
    args_str = [repr(arg) for arg in args] if args else []
    kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()] if kwargs else []
    arguments = ", ".join(args_str + kwargs_str)
    return f"{callable_name}({arguments})"
```

## as_shell_command

```
as_shell_command(cmd: list[str]) -> str
```

Rebuild a command line from system arguments.

Parameters:

- **`cmd`** (`list[str]`) – The command as a list of strings.

Returns:

- `str` – A printable and shell-runnable command.

Source code in `src/failprint/_internal/formats.py`

```
def as_shell_command(cmd: list[str]) -> str:
    """Rebuild a command line from system arguments.

    Arguments:
        cmd: The command as a list of strings.

    Returns:
        A printable and shell-runnable command.
    """
    parts = []
    for part in cmd:
        if not part:
            parts.append('""')
            continue
        has_spaces = " " in part
        has_double_quotes = '"' in part
        has_single_quotes = "'" in part
        if has_double_quotes and not has_single_quotes:
            # double quotes, no single quotes
            # -> wrap in single quotes
            part = f"'{part}'"  # noqa: PLW2901
        elif has_single_quotes and has_double_quotes:
            # double and single quotes
            # -> escape double quotes, wrap in double quotes
            part = part.replace('"', r"\"")  # noqa: PLW2901
            part = f'"{part}"'  # noqa: PLW2901
        elif has_single_quotes or has_spaces:
            # spaces or single quotes
            # -> wrap in double quotes
            part = f'"{part}"'  # noqa: PLW2901
        parts.append(part)
    return " ".join(parts)
```

## get_parser

```
get_parser() -> ArgParser
```

Return the CLI argument parser.

Returns:

- `ArgParser` – An argparse parser.

Source code in `src/failprint/_internal/cli.py`

```
def get_parser() -> ArgParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = add_flags(ArgParser(prog="failprint"))
    # TODO: specific to the format
    parser.add_argument("-n", "--number", type=int, default=1, help="Command number. Useful for the 'tap' format.")
    # TODO: specific to the format
    parser.add_argument("-t", "--title", help="Command title. Default is the command itself.")
    parser.add_argument("cmd", metavar="COMMAND", nargs="+")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {debug._get_version()}")
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")
    return parser
```

## main

```
main(args: list[str] | None = None) -> int
```

Run the main program.

This function is executed when you type `failprint` or `python -m failprint`.

Parameters:

- **`args`** (`list[str] | None`, default: `None` ) – Arguments passed from the command line.

Returns:

- `int` – An exit code.

Source code in `src/failprint/_internal/cli.py`

```
def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `failprint` or `python -m failprint`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args).__dict__.items()
    return run(**{_: value for _, value in opts if value is not None}).code
```

## printable_command

```
printable_command(
    cmd: CmdFuncType,
    args: Sequence | None = None,
    kwargs: dict | None = None,
) -> str
```

Transform a command or function into a string.

Parameters:

- **`cmd`** (`CmdFuncType`) – The command or function to transform.
- **`args`** (`Sequence | None`, default: `None` ) – Positional arguments passed to the function.
- **`kwargs`** (`dict | None`, default: `None` ) – Keyword arguments passed to the function.

Returns:

- `str` – A shell command or python statement string.

Source code in `src/failprint/_internal/formats.py`

```
def printable_command(cmd: CmdFuncType, args: Sequence | None = None, kwargs: dict | None = None) -> str:
    """Transform a command or function into a string.

    Arguments:
        cmd: The command or function to transform.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        A shell command or python statement string.
    """
    if isinstance(cmd, str):
        return cmd
    if callable(cmd):
        return as_python_statement(cmd, args, kwargs)
    return as_shell_command(cmd)
```

## run

```
run(
    cmd: CmdFuncType,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    number: int = 1,
    capture: str | bool | Capture | None = None,
    title: str | None = None,
    fmt: str | None = None,
    pty: bool = False,
    progress: bool = True,
    nofail: bool = False,
    quiet: bool = False,
    silent: bool = False,
    stdin: str | None = None,
    command: str | None = None,
) -> RunResult
```

Run a command in a subprocess or a Python function, and print its output if it fails.

Parameters:

- **`cmd`** (`CmdFuncType`) – The command to run.
- **`args`** (`Sequence | None`, default: `None` ) – Arguments to pass to the callable.
- **`kwargs`** (`dict | None`, default: `None` ) – Keyword arguments to pass to the callable.
- **`number`** (`int`, default: `1` ) – The command number.
- **`capture`** (`str | bool | Capture | None`, default: `None` ) – The output to capture.
- **`title`** (`str | None`, default: `None` ) – The command title.
- **`fmt`** (`str | None`, default: `None` ) – The output format.
- **`pty`** (`bool`, default: `False` ) – Whether to run in a PTY.
- **`progress`** (`bool`, default: `True` ) – Whether to show progress.
- **`nofail`** (`bool`, default: `False` ) – Whether to always succeed.
- **`quiet`** (`bool`, default: `False` ) – Whether to not print the command output.
- **`silent`** (`bool`, default: `False` ) – Don't print anything.
- **`stdin`** (`str | None`, default: `None` ) – String to use as standard input.
- **`command`** (`str | None`, default: `None` ) – The command to display.

Returns:

- `RunResult` – The command exit code, or 0 if nofail is True.

Source code in `src/failprint/_internal/runners.py`

```
def run(
    cmd: CmdFuncType,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    number: int = 1,
    capture: str | bool | Capture | None = None,
    title: str | None = None,
    fmt: str | None = None,
    pty: bool = False,
    progress: bool = True,
    nofail: bool = False,
    quiet: bool = False,
    silent: bool = False,
    stdin: str | None = None,
    command: str | None = None,
) -> RunResult:
    """Run a command in a subprocess or a Python function, and print its output if it fails.

    Arguments:
        cmd: The command to run.
        args: Arguments to pass to the callable.
        kwargs: Keyword arguments to pass to the callable.
        number: The command number.
        capture: The output to capture.
        title: The command title.
        fmt: The output format.
        pty: Whether to run in a PTY.
        progress: Whether to show progress.
        nofail: Whether to always succeed.
        quiet: Whether to not print the command output.
        silent: Don't print anything.
        stdin: String to use as standard input.
        command: The command to display.

    Returns:
        The command exit code, or 0 if `nofail` is True.
    """
    format_name: str = fmt or os.environ.get("FAILPRINT_FORMAT", DEFAULT_FORMAT)  # type: ignore[assignment]
    format_name = accept_custom_format(format_name)
    format_obj = formats.get(format_name, formats[DEFAULT_FORMAT])

    env = Environment(autoescape=False)  # noqa: S701 (no HTML: no need to escape)
    env.filters["indent"] = textwrap.indent
    env.filters["escape"] = env.filters["e"] = escape
    env.filters["unescape"] = env.filters["u"] = unescape

    command = command if command is not None else printable_command(cmd, args, kwargs)

    if not silent and progress and format_obj.progress_template:
        progress_template = env.from_string(format_obj.progress_template)
        print(unescape(parse(progress_template.render({"title": title, "command": command}))), end="\r")  # noqa: T201

    capture = Capture.cast(capture)

    if callable(cmd):
        code, output = run_function(cmd, args=args, kwargs=kwargs, capture=capture, stdin=stdin)
    else:
        code, output = run_command(cmd, capture=capture, ansi=format_obj.accept_ansi, pty=pty, stdin=stdin)

    if not silent:
        template = env.from_string(format_obj.template)
        rendered = template.render(
            {
                "title": title,
                "command": command,
                "code": code,
                "success": code == 0,
                "failure": code != 0,
                "number": number,
                "output": output,
                "nofail": nofail,
                "quiet": quiet,
                "silent": silent,
            },
        )
        print(unescape(parse(rendered)))  # noqa: T201

    return RunResult(0 if nofail else code, output)
```

## run_command

```
run_command(
    cmd: CmdType,
    *,
    capture: Capture = BOTH,
    ansi: bool = False,
    pty: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]
```

Run a command.

Parameters:

- **`cmd`** (`CmdType`) – The command to run.
- **`capture`** (`Capture`, default: `BOTH` ) – The output to capture.
- **`ansi`** (`bool`, default: `False` ) – Whether to accept ANSI sequences.
- **`pty`** (`bool`, default: `False` ) – Whether to run in a PTY.
- **`stdin`** (`str | None`, default: `None` ) – String to use as standard input.

Returns:

- `tuple[int, str]` – The exit code and the command output.

Source code in `src/failprint/_internal/runners.py`

```
def run_command(
    cmd: CmdType,
    *,
    capture: Capture = Capture.BOTH,
    ansi: bool = False,
    pty: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        ansi: Whether to accept ANSI sequences.
        pty: Whether to run in a PTY.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command output.
    """
    shell = isinstance(cmd, str)

    # if chosen format doesn't accept ansi, or on Windows, don't use pty
    if pty and (not ansi or WINDOWS):
        pty = False

    # pty can only combine, so only use pty when combining
    if pty and capture in {Capture.BOTH, Capture.NONE}:
        if shell:
            cmd = ["sh", "-c", cmd]  # type: ignore[list-item]  # we know cmd is str
        return run_pty_subprocess(cmd, capture=capture, stdin=stdin)  # type: ignore[arg-type]  # we made sure cmd is a list

    # we are on Windows
    if WINDOWS:
        # make sure the process can find the executable
        if not shell:
            cmd[0] = shutil.which(cmd[0]) or cmd[0]  # type: ignore[index]  # we know cmd is a list
        return run_subprocess(cmd, capture=capture, shell=shell, stdin=stdin)

    return run_subprocess(cmd, capture=capture, shell=shell, stdin=stdin)
```

## run_function

```
run_function(
    func: Callable,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    capture: Capture = BOTH,
    stdin: str | None = None,
) -> tuple[int, str]
```

Run a function.

Parameters:

- **`func`** (`Callable`) – The function to run.
- **`args`** (`Sequence | None`, default: `None` ) – Positional arguments passed to the function.
- **`kwargs`** (`dict | None`, default: `None` ) – Keyword arguments passed to the function.
- **`capture`** (`Capture`, default: `BOTH` ) – The output to capture.
- **`stdin`** (`str | None`, default: `None` ) – String to use as standard input.

Returns:

- `tuple[int, str]` – The exit code and the function output.

Source code in `src/failprint/_internal/runners.py`

```
def run_function(
    func: Callable,
    *,
    args: Sequence | None = None,
    kwargs: dict | None = None,
    capture: Capture = Capture.BOTH,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a function.

    Arguments:
        func: The function to run.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
        capture: The output to capture.
        stdin: String to use as standard input.

    Returns:
        The exit code and the function output.
    """
    args = args or []
    kwargs = kwargs or {}

    if capture == Capture.NONE:
        return run_function_get_code(func, args=args, kwargs=kwargs), ""

    with capture.here(stdin=stdin) as captured:
        code = run_function_get_code(func, args=args, kwargs=kwargs)

    return code, str(captured)
```

## run_function_get_code

```
run_function_get_code(
    func: Callable, *, args: Sequence, kwargs: dict
) -> int
```

Run a function and return a exit code.

Parameters:

- **`func`** (`Callable`) – The function to run.
- **`args`** (`Sequence`) – Positional arguments passed to the function.
- **`kwargs`** (`dict`) – Keyword arguments passed to the function.

Returns:

- `int` – An exit code.

Source code in `src/failprint/_internal/runners.py`

```
def run_function_get_code(
    func: Callable,
    *,
    args: Sequence,
    kwargs: dict,
) -> int:
    """Run a function and return a exit code.

    Arguments:
        func: The function to run.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.

    Returns:
        An exit code.
    """
    try:
        result = func(*args, **kwargs)
    except SystemExit as exit:
        if exit.code is None:
            return 0
        if isinstance(exit.code, int):
            return exit.code
        sys.stderr.write(str(exit.code))
        return 1
    except Exception:  # noqa: BLE001
        sys.stderr.write(traceback.format_exc() + "\n")
        return 1

    # if func was a lazy callable, recurse
    if isinstance(result, LazyCallable):
        return run_function_get_code(result, args=(), kwargs={})

    # first check True and False
    # because int(True) == 1 and int(False) == 0
    if result is True:
        return 0
    if result is False:
        return 1
    try:
        return int(result)
    except (ValueError, TypeError):
        if result is None or bool(result):
            return 0
        return 1
```

## run_pty_subprocess

```
run_pty_subprocess(
    cmd: list[str],
    *,
    capture: Capture = BOTH,
    stdin: str | None = None,
) -> tuple[int, str]
```

Run a command in a PTY subprocess.

Parameters:

- **`cmd`** (`list[str]`) – The command to run.
- **`capture`** (`Capture`, default: `BOTH` ) – The output to capture.
- **`stdin`** (`str | None`, default: `None` ) – String to use as standard input.

Returns:

- `tuple[int, str]` – The exit code and the command output.

Source code in `src/failprint/_internal/process.py`

```
def run_pty_subprocess(
    cmd: list[str],
    *,
    capture: Capture = Capture.BOTH,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command in a PTY subprocess.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command output.
    """
    process = PtyProcessUnicode.spawn(cmd)
    process.delayafterclose = 0.01  # default to 0.1
    process.delayafterterminate = 0.01  # default to 0.1
    pty_output: list[str] = []

    if stdin is not None:
        process.setecho(state=False)
        process.waitnoecho()
        process.write(stdin)
        process.sendeof()
        # not sure why but sending only one eof is not always enough,
        # so we send a second one and ignore any IO error
        with contextlib.suppress(OSError):
            process.sendeof()

    while True:
        try:
            output_data = process.read()
        except EOFError:
            break
        if capture == Capture.NONE:
            print(output_data, end="", flush=True)  # noqa: T201
        else:
            pty_output.append(output_data)

    output = "".join(pty_output).replace("\r\n", "\n")
    return process.wait(), output
```

## run_subprocess

```
run_subprocess(
    cmd: CmdType,
    *,
    capture: Capture = BOTH,
    shell: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]
```

Run a command in a subprocess.

Parameters:

- **`cmd`** (`CmdType`) – The command to run.
- **`capture`** (`Capture`, default: `BOTH` ) – The output to capture.
- **`shell`** (`bool`, default: `False` ) – Whether to run the command in a shell.
- **`stdin`** (`str | None`, default: `None` ) – String to use as standard input.

Returns:

- `tuple[int, str]` – The exit code and the command raw output.

Source code in `src/failprint/_internal/process.py`

```
def run_subprocess(
    cmd: CmdType,
    *,
    capture: Capture = Capture.BOTH,
    shell: bool = False,
    stdin: str | None = None,
) -> tuple[int, str]:
    """Run a command in a subprocess.

    Arguments:
        cmd: The command to run.
        capture: The output to capture.
        shell: Whether to run the command in a shell.
        stdin: String to use as standard input.

    Returns:
        The exit code and the command raw output.
    """
    if capture == Capture.NONE:
        stdout_opt = None
        stderr_opt = None
    else:
        stdout_opt = subprocess.PIPE
        stderr_opt = subprocess.STDOUT if capture == Capture.BOTH else subprocess.PIPE

    if shell and not isinstance(cmd, str):
        cmd = printable_command(cmd)

    process = subprocess.run(  # noqa: S603
        cmd,
        input=stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
        shell=shell,
        text=True,
        encoding="utf8",
        check=False,
    )

    if capture == Capture.NONE:
        output = ""
    elif capture == Capture.STDERR:
        output = process.stderr
    else:
        output = process.stdout

    return process.returncode, output
```
