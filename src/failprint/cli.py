# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m failprint` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `failprint.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `failprint.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import enum
import os
import subprocess  # noqa: S404 (we don't mind the security implication)
import sys
import textwrap
from typing import Dict, List, Optional, Tuple

from ansimarkup import ansiprint
from jinja2 import Environment
from ptyprocess import PtyProcessUnicode

DEFAULT_FORMAT = "pretty"


class Format:
    """Class to define a display format."""

    def __init__(self, template: str, progress_template: Optional[str] = None, accept_ansi: bool = True) -> None:
        """
        Initialize the object.

        Arguments:
            template: The main template.
            progress_template: The template to show progress.
            accept_ansi: Whether to accept ANSI sequences.
        """
        self.template = template
        self.progress_template = progress_template
        self.accept_ansi = accept_ansi


formats: Dict[str, Format] = {
    "custom": None,  # type: ignore
    "pretty": Format(
        "<bold>{% if success %}<green>✓</green>{% elif nofail %}<yellow>✗</yellow>{% else %}<red>✗</red>{% endif %} "
        "{{ title or command }}</bold>"
        "{% if failure %} ({{ code }}){% endif %}"
        "{% if failure and output and not quiet %}\n"
        "{{ ('  > ' + command + '\n') if title else '' }}"
        "{{ output|indent(2 * ' ') }}{% endif %}",
        progress_template="> {{ title or command }}",
    ),
    "tap": Format(
        "{% if failure %}not {% endif %}ok {{ number }} - {{ title or command }}"
        "{% if failure and output %}\n  ---\n  "
        "{{ ('command: ' + command + '\n  ') if title else '' }}"
        "output: |\n{{ output|indent(4 * ' ') }}\n  ...{% endif %}",
        accept_ansi=False,
    ),
}


class Output(enum.Enum):
    """An enum to store the different possible output types."""

    STDOUT: str = "stdout"  # noqa: WPS115
    STDERR: str = "stderr"  # noqa: WPS115
    COMBINE: str = "combine"  # noqa: WPS115

    def __str__(self):
        return self.value.lower()  # noqa: E1101 (false-positive)


def printable_command(cmd: List[str]) -> str:  # noqa: WPS231 (not that complex)
    """
    Rebuild a command line from system arguments.

    Arguments:
        cmd: The command as a list of strings.

    Returns:
        A printable and shell-runnable command.
    """
    parts = []
    for part in cmd:
        if " " in part:
            has_double_quotes = '"' in part
            has_single_quotes = "'" in part
            if has_double_quotes and not has_single_quotes:
                part = f"'{part}'"
            elif has_single_quotes and has_double_quotes:
                part = part.replace('"', r"\"")
                part = f'"{part}"'
            else:
                part = f'"{part}"'
        parts.append(part)
    return " ".join(parts)


def run(
    cmd: List[str],
    number: int = 1,
    output_type: Optional[Output] = None,
    title: Optional[str] = None,
    fmt: Optional[str] = None,
    use_pty: bool = True,
    progress: bool = True,
    nofail: bool = False,
    quiet: bool = False,
) -> int:
    """
    Run a command in a subprocess, and print its output if it fails.

    Arguments:
        cmd: The command to run.
        number: The command number.
        output_type: The type of output.
        title: The command title.
        fmt: The output format.
        use_pty: Whether to run in a PTY.
        progress: Whether to show progress.
        nofail: Whether to always succeed.
        quiet: Whether to not print the command output.

    Returns:
        The command exit code, or 0 if `nofail` is True.
    """
    format_name: str = fmt or os.environ.get("FAILPRINT_FORMAT", DEFAULT_FORMAT)  # type: ignore
    format_name = accept_custom_format(format_name)
    format_obj = formats.get(format_name, formats[DEFAULT_FORMAT])
    command = printable_command(cmd)

    env = Environment(autoescape=False)  # noqa: S701 (no HTML: no need to escape)
    env.filters["indent"] = textwrap.indent

    if progress and format_obj.progress_template:
        progress_template = env.from_string(format_obj.progress_template)
        ansiprint(progress_template.render({"title": title, "command": command}), end="\r")

    if not format_obj.accept_ansi and use_pty:
        use_pty = False

    if output_type is None:
        output_type = Output.COMBINE

    if output_type == Output.COMBINE and use_pty:
        code, output = run_pty_subprocess(cmd)
    else:
        code, output = run_subprocess(cmd, output_type)

    template = env.from_string(format_obj.template)
    ansiprint(
        template.render(
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
            },
        ),
    )

    return 0 if nofail else code


def run_subprocess(cmd: List[str], output_type: Output) -> Tuple[int, str]:
    """
    Run a command in a subprocess.

    Arguments:
        cmd: The command to run.
        output_type: The type of output.

    Returns:
        The exit code and the command output.
    """
    stdout_opt = subprocess.PIPE

    if output_type == Output.COMBINE:
        stderr_opt = subprocess.STDOUT
    else:
        stderr_opt = subprocess.PIPE

    process = subprocess.Popen(  # noqa: S603 (we trust the input)
        cmd,
        stdin=sys.stdin,
        stdout=stdout_opt,
        stderr=stderr_opt,
    )
    stdout, stderr = process.communicate()

    if output_type == Output.STDERR:
        output = stderr.decode("utf8")
    else:
        output = stdout.decode("utf8")

    code = process.returncode

    return code, output


def run_pty_subprocess(cmd: List[str]) -> Tuple[int, str]:
    """
    Run a command in a PTY subprocess.

    Arguments:
        cmd: The command to run.

    Returns:
        The exit code and the command output.
    """
    process = PtyProcessUnicode.spawn(cmd)

    pty_output = []

    while True:
        try:
            pty_output.append(process.read())
        except EOFError:
            break

    process.close()

    output = "".join(pty_output)
    code = process.exitstatus

    return code, output


def accept_custom_format(string: str) -> str:
    """
    Store the value in `formats` if it starts with custom.

    Arguments:
        string: A format name.

    Returns:
        The format name, or `custom` if it started with `custom=`.
    """
    if string.startswith("custom=") and formats["custom"] is None:
        formats["custom"] = Format(string[7:])
        return "custom"
    return string


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="failprint")
    parser.add_argument(
        "-f",
        "--format",
        choices=formats.keys(),
        type=accept_custom_format,
        default=None,
        help="Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. "
        "Available variables: title (command or title passed with -t), code (exit status), "
        "success (boolean), failure (boolean), n (command number passed with -n), "
        "output (command output). Available filters: indent (textwrap.indent).",
    )
    parser.add_argument(
        "--no-pty",
        action="store_false",
        dest="use_pty",
        default=True,
        help="Disable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.",
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=list(Output),
        type=Output,
        help="Which output to use. Colors are supported with 'combine' only, unless the command has a 'force color' option.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        default=False,
        help="Don't print the command output, even if it failed.",
    )
    parser.add_argument(
        "-z",
        "--zero",
        "--nofail",
        action="store_true",
        dest="nofail",
        default=False,
        help="Don't fail. Always return a success (0) exit code.",
    )
    parser.add_argument("-n", "--number", type=int, default=1, help="Command number. Useful for the 'tap' format.")
    parser.add_argument("-t", "--title", help="Command title. Default is the command itself.")
    parser.add_argument("COMMAND", nargs="+")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `failprint` or `python -m failprint`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    options = parser.parse_args(args)
    return run(
        options.COMMAND,
        number=options.number,
        output_type=options.output,
        title=options.title,
        fmt=options.format,
        use_pty=options.use_pty,
        nofail=options.nofail,
        quiet=options.quiet,
    )
