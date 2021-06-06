"""Generate the credits page."""

import functools
import re
import urllib
from itertools import chain
from pathlib import Path

import mkdocs_gen_files
import toml
from jinja2 import StrictUndefined
from jinja2.sandbox import SandboxedEnvironment
from pip._internal.commands.show import search_packages_info  # noqa: WPS436 (no other way?)


def get_credits_data() -> dict:
    """Return data used to generate the credits file.

    Returns:
        Data required to render the credits template.
    """
    project_dir = Path(__file__).parent.parent
    metadata = toml.load(project_dir / "pyproject.toml")["project"]
    metadata_pdm = toml.load(project_dir / "pyproject.toml")["tool"]["pdm"]
    lock_data = toml.load(project_dir / "pdm.lock")
    project_name = metadata["name"]

    all_dependencies = chain(
        metadata.get("dependencies", []),
        chain(*metadata.get("optional-dependencies", {}).values()),
        chain(*metadata_pdm.get("dev-dependencies", {}).values()),
    )
    direct_dependencies = {re.sub(r"[^\w-].*$", "", dep) for dep in all_dependencies}
    direct_dependencies = {dep.lower() for dep in direct_dependencies}
    indirect_dependencies = {pkg["name"].lower() for pkg in lock_data["package"]}
    indirect_dependencies -= direct_dependencies

    packages = {}
    for pkg in search_packages_info(sorted(direct_dependencies | indirect_dependencies)):
        pkg = {_: pkg[_] for _ in ("name", "home-page")}
        packages[pkg["name"].lower()] = pkg

    # all packages might not be credited,
    # like the ones that are now part of the standard library
    # or the ones that are only used on other operating systems,
    # and therefore are not installed,
    # but it's not that important

    return {
        "project_name": project_name,
        "direct_dependencies": sorted(direct_dependencies),
        "indirect_dependencies": sorted(indirect_dependencies),
        "package_info": packages,
        "more_credits": "http://pawamoy.github.io/credits/",
    }


@functools.lru_cache(maxsize=None)
def get_credits():
    """Return credits as Markdown.

    Returns:
        The credits page Markdown.
    """
    jinja_env = SandboxedEnvironment(undefined=StrictUndefined)
    commit = "c2bcf23338e648bcbe32d6735d623b9e0a45f43f"
    template_url = f"https://raw.githubusercontent.com/pawamoy/jinja-templates/{commit}/credits.md"
    template_data = get_credits_data()
    template_text = urllib.request.urlopen(template_url).read().decode("utf8")  # noqa: S310
    return jinja_env.from_string(template_text).render(**template_data)


with mkdocs_gen_files.open("credits.md", "w") as fd:
    fd.write(get_credits())
mkdocs_gen_files.set_edit_path("credits.md", "gen_credits.py")
