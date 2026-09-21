r"""Build the Korean language pack: translated .py files and i18n/*.json for
the three packages, and nothing else (no compiled extensions, no unrelated
files). This is what install_ko.ps1 copies onto an official installation.

Usage (from C:\orange3): .venv-ko\Scripts\python i18n\ko\tools\build_langpack.py [output_dir]
Default output_dir: i18n\ko\dist\orange-ko-<version>
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DEFAULT_ORANGE_PYTHON, REPOS, build, installed_packages  # noqa: E402

VERSION = "3.40.0"  # matches i18n/ko/README.md "기준 버전"


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parents[1] / "dist" / f"orange-ko-{VERSION}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    installed = installed_packages(DEFAULT_ORANGE_PYTHON)
    mismatched = [f"{r.package}: installed {installed[r.package]['version']}, "
                 f"expected {VERSION if r.package == 'Orange3' else '(see README)'}"
                 for r in REPOS if r.package == "Orange3" and installed[r.package]["version"] != VERSION]
    if mismatched:
        sys.exit("Version mismatch, refusing to build:\n" + "\n".join(mismatched))

    manifest = {"version": VERSION, "packages": {}}
    for repo in REPOS:
        dest = out / repo.package
        build(repo, dest)
        n_py = sum(1 for _ in dest.rglob("*.py"))
        n_json = sum(1 for _ in (dest / "i18n").glob("*.json"))
        manifest["packages"][repo.package] = {"py_files": n_py, "json_files": n_json}
        print(f"{repo.package}: {n_py} .py files, {n_json} i18n json files -> {dest}")

    with open(out / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    for name in ("install_ko.ps1", "uninstall_ko.ps1", "install_orange_ko.ps1", "설치.bat"):
        src = Path(__file__).resolve().parent / name
        if src.exists():
            shutil.copy2(src, out / name)

    print(f"\nLanguage pack ready: {out}")
    print("Copy this folder (plus Orange3-3.40.0-x86_64.exe if Orange isn't installed yet) "
          "to the target PC and double-click 설치.bat.")


if __name__ == "__main__":
    main()
