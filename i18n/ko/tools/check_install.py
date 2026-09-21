r"""Check that the source checkouts match the installed Orange.

The three packages are built with the languages of the official build
(English and Slovenian) and compared with the installed files. If they are
identical, Korean files built from the same checkouts can safely replace
the installed ones.

Usage (from C:\orange3)::

    .venv-ko\Scripts\python i18n\ko\tools\check_install.py
    .venv-ko\Scripts\python i18n\ko\tools\check_install.py --orange-python D:\Orange\python.exe
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

from _common import DEFAULT_ORANGE_PYTHON, OFFICIAL_LANGUAGES, REPOS, \
    build, installed_packages


def read_text(path: Path) -> str:
    # Checkouts may have CRLF line endings (core.autocrlf)
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def compare(built: Path, installed: Path):
    same, different, not_installed = [], [], []
    for path in sorted(built.rglob("*")):
        rel = path.relative_to(built)
        is_json = rel.parts[0] == "i18n" and path.suffix == ".json"
        if path.suffix != ".py" and not is_json:
            continue
        target = installed / rel
        if not target.exists():
            not_installed.append(rel)
        elif is_json:
            with open(path, encoding="utf-8") as f1, \
                    open(target, encoding="utf-8") as f2:
                (same if json.load(f1) == json.load(f2) else different).append(rel)
        else:
            (same if read_text(path) == read_text(target) else different).append(rel)
    built_py = {p.relative_to(built) for p in built.rglob("*.py")}
    only_installed = sorted(
        rel for rel in (p.relative_to(installed) for p in installed.rglob("*.py"))
        if rel not in built_py)
    return same, different, not_installed, only_installed


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--orange-python", default=DEFAULT_ORANGE_PYTHON,
                        help="python.exe of the installed Orange")
    args = parser.parse_args()

    installed = installed_packages(args.orange_python)
    ok = True
    with tempfile.TemporaryDirectory(prefix="orange-ko-check-") as tmp:
        for repo in REPOS:
            info = installed[repo.package]
            tag = repo.tag()
            print(f"\n=== {repo.package}: installed {info['version']}, "
                  f"checkout {tag or '(not at a tag)'}")
            if tag != info["version"]:
                print("  !! version mismatch")
                ok = False
            dest = Path(tmp, repo.package)
            build(repo, dest, OFFICIAL_LANGUAGES)
            same, different, not_installed, only_installed = \
                compare(dest, Path(info["dir"]))
            print(f"  identical: {len(same)}")
            for title, files in (("DIFFERENT", different),
                                 ("not installed", not_installed),
                                 ("only in installation", only_installed)):
                if files:
                    print(f"  {title}: {len(files)}")
                    for rel in files[:15]:
                        print(f"    {rel}")
                    if len(files) > 15:
                        print("    ...")
            ok = ok and not different

    print("\nRESULT:", "OK - checkouts match the installation" if ok
          else "MISMATCH - do not overwrite the installation")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
