r"""Shared settings for the Korean translation tools.

The three repositories are expected side by side::

    C:\orange3               (this repository, package Orange)
    C:\orange-canvas-core    (package orangecanvas)
    C:\orange-widget-base    (package orangewidget)

Each must be checked out at the tag that matches the installed Orange.
"""
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ORANGE3_DIR = Path(__file__).resolve().parents[3]
REPOS_ROOT = ORANGE3_DIR.parent

DEFAULT_ORANGE_PYTHON = r"C:\Program Files\Orange\python.exe"

# Languages that the official (conda / PyPI) build is compiled with
OFFICIAL_LANGUAGES = ("en", "si")
MSGS_NAME = "msgs.jaml"


@dataclass(frozen=True)
class Repo:
    name: str          # repository directory
    package: str       # Python package inside the repository
    dist: str          # distribution name (for version lookup)

    @property
    def path(self) -> Path:
        if self.name == "orange3":
            return ORANGE3_DIR
        return REPOS_ROOT / self.name

    @property
    def source(self) -> Path:
        return self.path / self.package

    @property
    def i18n(self) -> Path:
        return self.path / "i18n"

    @property
    def config_file(self) -> Path:
        return self.i18n / "trubar-config.yaml"

    def msgs(self, lang: str) -> Path:
        return self.i18n / lang / MSGS_NAME

    def tag(self) -> str:
        res = subprocess.run(
            ["git", "-C", str(self.path), "describe", "--tags", "--exact-match"],
            capture_output=True, text=True, check=False)
        return res.stdout.strip() if res.returncode == 0 else ""


REPOS = (
    Repo("orange-canvas-core", "orangecanvas", "orange-canvas-core"),
    Repo("orange-widget-base", "orangewidget", "orange-widget-base"),
    Repo("orange3", "Orange", "Orange3"),
)


def installed_packages(orange_python: str) -> dict:
    """Return {package: {"dir": ..., "version": ...}} for the installed Orange.

    Runs outside of any repository and with -P, so that the checkouts
    do not shadow the installed packages."""
    code = (
        "import importlib, importlib.metadata as m, json, os\n"
        f"repos = {[(r.package, r.dist) for r in REPOS]!r}\n"
        "out = {}\n"
        "for pkg, dist in repos:\n"
        "    mod = importlib.import_module(pkg)\n"
        "    out[pkg] = {'dir': os.path.dirname(mod.__file__),\n"
        "                'version': m.version(dist)}\n"
        "print(json.dumps(out))\n")
    res = subprocess.run(
        [orange_python, "-P", "-c", code], capture_output=True, text=True,
        cwd=tempfile.gettempdir(), check=False)
    if res.returncode:
        sys.exit(f"Cannot inspect Orange at {orange_python}:\n{res.stderr}")
    return json.loads(res.stdout)


def build(repo: Repo, dest: Path, languages=None) -> None:
    """Build a multilingual copy of `repo`'s package into `dest`.

    `languages` limits the build to the given language codes (default: all
    languages in the configuration). The build runs in a subprocess because
    trubar keeps its configuration in a module-level singleton."""
    args = [sys.executable, __file__, "--build", repo.name, str(dest)]
    if languages:
        args.append(",".join(languages))
    subprocess.run(args, check=True)


def _build_in_process(repo_name: str, dest: str, languages: str = "") -> None:
    # pylint: disable=import-outside-toplevel
    import yaml
    from trubar import actions
    from trubar.config import config
    from trubar.messages import load
    from trubar.utils import check_any_files

    repo = next(r for r in REPOS if r.name == repo_name)
    config.update_from_file(str(repo.config_file))
    if languages:
        keep = languages.split(",")
        with open(repo.config_file, encoding="utf-8") as f:
            raw = yaml.safe_load(f)["languages"]
        for code in [c for c in config.languages if c not in keep]:
            # Per-language auto-imports cannot be removed after loading
            if "auto-import" in raw[code]:
                sys.exit(f"Cannot exclude language '{code}' with auto-import")
            static = os.path.normpath(os.path.join(config.base_dir, code, "static"))
            config.static_files = tuple(
                p for p in config.static_files if os.path.normpath(p) != static)
            del config.languages[code]

    messages = [
        {} if settings.is_original
        else load(os.path.join(config.base_dir, code, MSGS_NAME))
        for code, settings in config.languages.items()]
    check_any_files(set.union(*(set(m) for m in messages)), str(repo.source))
    actions.translate(messages, str(repo.source), dest, "",
                      verbosity=actions.ReportCritical)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--build":
        _build_in_process(*sys.argv[2:])
    else:
        sys.exit("This module is not meant to be run directly")
