# failprint

[![ci](https://github.com/pawamoy/failprint/workflows/ci/badge.svg)](https://github.com/pawamoy/failprint/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://pawamoy.github.io/failprint/)
[![pypi version](https://img.shields.io/pypi/v/failprint.svg)](https://pypi.org/project/failprint/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#failprint:gitter.im)

Run a command, print its output only if it fails.

Tired of searching the `quiet` options of your programs
to lighten up the output of your `make check` or `make lint` commands?

Tired of finding out that standard output and error are mixed up in some of them?

Simply run your command through `failprint`.
If it succeeds, nothing is printed.
If it fails, standard error is printed.
Plus other configuration goodies :wink:

## Example

You don't want to see output when the command succeeds.

![demo](demo.svg)

The task runner [`duty`](https://github.com/pawamoy/duty) uses `failprint`,
allowing you to define tasks in Python and run them with minimalist and beautiful output:

![demo_duty](demo_duty.svg)

## Requirements

failprint requires Python 3.8 or above.

<details>
<summary>To install Python 3.8, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.8.17
pyenv install 3.8.17

# make it available globally
pyenv global system 3.8.17
```
</details>

## Installation

```bash
pip install failprint
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install failprint
```

## Usage

```console
% poetry run failprint -h
usage: failprint [-h] [-c {stdout,stderr,both,none}] [-f {pretty,tap}] [-y | -Y] [-p | -P] [-q | -Q] [-s | -S] [-z | -Z] [-n NUMBER]
                 [-t TITLE]
                 COMMAND [COMMAND ...]

positional arguments:
  COMMAND

optional arguments:
  -h, --help            show this help message and exit
  -c {stdout,stderr,both,none}, --capture {stdout,stderr,both,none}
                        Which output to capture. Colors are supported with 'both' only, unless the command has a 'force color'
                        option.
  -f {pretty,tap}, --format {pretty,tap}
                        Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. Available variables:
                        command, title (command or title passed with -t), code (exit status), success (boolean), failure (boolean),
                        number (command number passed with -n), output (command output), nofail (boolean), quiet (boolean), silent
                        (boolean). Available filters: indent (textwrap.indent).
  -y, --pty             Enable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.
  -Y, --no-pty          Disable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.
  -p, --progress        Print progress while running a command.
  -P, --no-progress     Don't print progress while running a command.
  -q, --quiet           Don't print the command output, even if it failed.
  -Q, --no-quiet        Print the command output when it fails.
  -s, --silent          Don't print anything.
  -S, --no-silent       Print output as usual.
  -z, --zero, --nofail  Don't fail. Always return a success (0) exit code.
  -Z, --no-zero, --strict
                        Return the original exit code.
  -n NUMBER, --number NUMBER
                        Command number. Useful for the 'tap' format.
  -t TITLE, --title TITLE
                        Command title. Default is the command itself.
```

```python
from failprint.runners import run

cmd = "echo hello"

exit_code = run(
    cmd,            # str, list of str, or Python callable
    args=None,      # args for callable
    kwargs=None,    # kwargs for callable
    number=1,       # command number, useful for tap format
    capture=None,   # stdout, stderr, both, none, True or False
    title=None,     # command title
    fmt=None,       # pretty, tap, or custom="MY_CUSTOM_FORMAT"
    pty=False,      # use a PTY
    progress=True,  # print the "progress" template before running the command
    nofail=False,   # always return zero
    quiet=False,    # don't print output when the command fails
    silent=False,   # don't print anything
)
```
