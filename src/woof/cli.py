import argparse
import os
import subprocess
import textwrap
from ansimarkup import ansiprint
from jinja2 import Environment, Template, FunctionLoader

DEFAULT_FORMAT = (
    "<bold>{% if success %}<green>✓</green>{% else %}<red>✗</red>{% endif %} {{ cmd }}</bold>{% if failure %} ({{ code }}){% endif %}"
    "{% if failure and stderr %}\n{{ stderr|indent(4 * ' ') }}\n{% endif %}"
)

TAP_FORMAT = (
    "{% if failure %}not {% endif %}ok {{ n }} - {{ cmd }}"
    "{% if failure and stderr %}  ---\nstderr: |\n{{ stderr|indent(4 * ' ') }}\n  ...\n{% endif %}"
)

TEMPLATE = os.environ.get("WOOF_FORMAT", TAP_FORMAT)
ENV = Environment(loader=FunctionLoader(lambda n: TEMPLATE))
ENV.filters["indent"] = textwrap.indent


def run(cmd, n=1):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    code = process.returncode
    stdout, stderr = [s.decode("utf8") for s in (stdout, stderr)]
    return ansiprint(
        ENV.get_template("").render(
            dict(
                cmd=" ".join(cmd),
                code=code,
                success=code == 0,
                failure=code > 0,
                n=n,
                stdout=stdout,
                stderr=stderr,
            )
        )
    )


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--multi", action="store_true", help="Consider each positional argument as a command.")
    parser.add_argument("COMMAND", nargs="+")
    return parser


def main(args=None):
    parser = get_parser()
    options = parser.parse_args(args)

    if options.multi:
        for i, cmd in enumerate(options.COMMAND):
            run(cmd.split(" "), i)
    else:
        run(options.COMMAND)
