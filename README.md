# failprint

[![ci](https://github.com/pawamoy/failprint/workflows/ci/badge.svg)](https://github.com/pawamoy/failprint/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/failprint/)
[![pypi version](https://img.shields.io/pypi/v/failprint.svg)](https://pypi.org/project/failprint/)

Run a command, print its output only if it fails.

Tired of searching the `quiet` options of your programs
to lighten up the output of your `make check` or `make lint` commands?

Tired of finding out that standard output and error are mixed up in some of them?

Simply run your command through `failprint`.
If it succeeds, nothing is printed.
If it fails, standard error is printed.
Plus other configuration goodies :wink:

## Example

Some tools output a lot of things. You don't want to see it when the command succeeds.

Without `failprint`:

- `poetry run bandit -s B404 -r src/`
- `poetry run black --check $(PY_SRC)`

![basic](https://user-images.githubusercontent.com/3999221/79385294-a2a0e080-7f68-11ea-827d-f72134a02eef.png)

With `failprint`:

- `poetry run failprint -- bandit -s B404 -r src/`
- `poetry run failprint -- black --check $(PY_SRC)`

![failprint_fail](https://user-images.githubusercontent.com/3999221/79385302-a5033a80-7f68-11ea-98cd-1f4148629724.png)

It's already better, no? Much more readable!

And when everything passes, it's even better:

![failprint_success](https://user-images.githubusercontent.com/3999221/79385308-a59bd100-7f68-11ea-8012-90cbe9e0ac08.png)

## Requirements

failprint requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.12

# make it available globally
pyenv global system 3.6.12
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install failprint
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 failprint
```

## Usage

```
usage: failprint [-h] [-f {custom,pretty,tap}] [-o {stdout,stderr,combine}] [-n NUMBER] [-t TITLE] COMMAND [COMMAND ...]

positional arguments:
  COMMAND

optional arguments:
  -h, --help            show this help message and exit
  -f {custom,pretty,tap}, --format {custom,pretty,tap}
                        Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'.
                        Available variables: title (command or title passed with -t), code (exit status), success (boolean), failure (boolean),
                        n (command number passed with -n), output (command output). Available filters: indent (textwrap.indent).
  -o {stdout,stderr,combine}, --output {stdout,stderr,combine}
                        Which output to use. Colors are supported with 'combine' only, unless the command has a 'force color' option.
  -n NUMBER, --number NUMBER
                        Command number. Useful for the 'tap' format.
  -t TITLE, --title TITLE
                        Command title. Default is the command itself.
```
