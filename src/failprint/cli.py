import argparse
import enum
import os
import subprocess
import sys
import textwrap

from ansimarkup import ansiprint
from jinja2 import DictLoader, Environment
from ptyprocess import PtyProcessUnicode

DEFAULT_FORMAT = "pretty"

FORMATS = {
    "custom": None,
    "pretty": (
        "<bold>{% if success %}<green>✓</green>{% else %}<red>✗</red>{% endif %} {{ title }}</bold>"
        "{% if failure %} ({{ code }}){% endif %}"
        "{% if failure and output %}\n{{ output|indent(2 * ' ') }}{% endif %}"
    ),
    "tap": (
        "{% if failure %}not {% endif %}ok {{ n }} - {{ title }}"
        "{% if failure and output %}\n  ---\n  output: |\n{{ output|indent(4 * ' ') }}\n  ...{% endif %}"
    ),
}


class Output(enum.Enum):
    STDOUT: str = "stdout"
    STDERR: str = "stderr"
    COMBINE: str = "combine"

    def __str__(self):
        return self.value.lower()


def run(cmd, number=1, output_type=None, title=None, fmt=None):
    if fmt is None:
        fmt = os.environ.get("failprint_FORMAT", DEFAULT_FORMAT)

    env = Environment(loader=DictLoader(FORMATS))
    env.filters["indent"] = textwrap.indent

    if output_type is not None:
        output_type = Output.COMBINE

    if output_type == Output.COMBINE:
        process = PtyProcessUnicode.spawn(cmd)

        output = []

        while True:
            try:
                output.append(process.read())
            except EOFError:
                break

        process.close()

        output = "".join(output)
        code = process.exitstatus

    else:
        stdout_opt = subprocess.PIPE
        stderr_opt = subprocess.PIPE

        process = subprocess.Popen(cmd, stdin=sys.stdin, stdout=stdout_opt, stderr=stderr_opt)
        stdout, stderr = process.communicate()

        if output_type == Output.STDERR:
            output = stderr
        else:
            output = stdout

        output = output.decode("utf8")
        code = process.returncode

    if title is None:
        title = " ".join(cmd)

    ansiprint(
        env.get_template(fmt).render(
            dict(title=title, code=code, success=code == 0, failure=code != 0, n=number, output=output,)
        )
    )

    return code


def get_parser():
    def allow_custom_format(s):
        if s.startswith("custom="):
            FORMATS["custom"] = s[7:]
            return "custom"
        return s

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--format",
        choices=FORMATS.keys(),
        type=allow_custom_format,
        default=None,
        help="Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. "
        "Available variables: title (command or title passed with -t), code (exit status), "
        "success (boolean), failure (boolean), n (command number passed with -n), "
        "output (command output). Available filters: indent (textwrap.indent).",
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=[m for m in Output],
        type=Output,
        help="Which output to use. Colors are supported with 'combine' only, unless the command has a 'force color' option.",
    )
    parser.add_argument("-n", "--number", type=int, default=1, help="Command number. Useful for the 'tap' format.")
    parser.add_argument("-t", "--title", help="Command title. Default is the command itself.")
    parser.add_argument("COMMAND", nargs="+")
    return parser


def main(args=None):
    parser = get_parser()
    options = parser.parse_args(args)
    return run(
        options.COMMAND, number=options.number, output_type=options.output, title=options.title, fmt=options.format,
    )
