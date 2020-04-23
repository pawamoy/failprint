# failprint

Print only on failure.

*:warning: Work in progress!*

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
