r"""Generate construct.yaml for building the integrated Korean Orange installer.

Usage (with the build-env python, from i18n/ko):
    generate_construct_yaml.py
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]  # i18n/ko
LANGPACK = ROOT / "dist" / "orange-ko-3.40.0"
BUILD_DIR = ROOT / "installer-build"
CHANNEL = ROOT / "channel"
SPECS_FILE = ROOT / "specs.txt"

if not LANGPACK.exists():
    sys.exit(f"Language pack not found at {LANGPACK}. Run build_langpack.py first.")

BUILD_DIR.mkdir(exist_ok=True)

# extra_files: map every translated .py/.json file to a staging area under
# the install prefix; post_install.bat then overlays it onto site-packages
# (guaranteed to run after packages are linked) and deletes the staging copy.
extra_files = []
for pkg_dir_name in ("Orange", "orangecanvas", "orangewidget"):
    pkg_dir = LANGPACK / pkg_dir_name
    for f in pkg_dir.rglob("*"):
        if f.is_file():
            rel = f.relative_to(LANGPACK)
            extra_files.append({str(f): f"_korean_langpack/{rel.as_posix()}"})
print(f"{len(extra_files)} files staged via extra_files")

import json as _json

def load_repodata_names(subdir):
    with open(CHANNEL / subdir / "repodata.json", encoding="utf-8") as f:
        data = _json.load(f)
    names = {}
    for section in ("packages", "packages.conda"):
        for fn, meta in data.get(section, {}).items():
            names[fn] = (meta["name"], meta["version"], meta["build"])
    return names

by_filename = {}
for subdir in ("win-64", "noarch"):
    by_filename.update(load_repodata_names(subdir))

urls = [line.strip() for line in SPECS_FILE.read_text(encoding="utf-8").splitlines()
       if line.strip()]
specs = []
for url in urls:
    fn = url.rsplit("/", 1)[-1]
    name, version, build = by_filename[fn]
    specs.append(f"{name}=={version}={build}")
print(f"{len(specs)} exact package specs (name==version=build)")

config = {
    "name": "Orange3-Korean",
    "version": "3.40.0",
    "company": "Biolab (Korean classroom build)",
    "uninstall_name": "Orange 3.40.0 (Korean)",
    "channels": [f"file:///{CHANNEL.as_posix()}"],
    "specs": specs,
    "installer_type": "exe",
    "keep_pkgs": False,
    "default_prefix": "C:\\Orange",
    "default_prefix_all_users": "C:\\Orange",
    "check_path_spaces": True,
    "post_install": str(ROOT / "tools" / "post_install.bat"),
    "post_install_desc": "Apply the Korean translation",
    "extra_files": extra_files,
    "register_python": False,
    "register_python_default": False,
    "initialize_conda": False,
}

icon = ROOT.parent.parent / "distribute" / "icon-256.png"
if icon.exists():
    config["icon_image"] = str(icon)
    config["welcome_image_text"] = "Orange (Korean)"
    config["header_image_text"] = "Orange (Korean)"

out = BUILD_DIR / "construct.yaml"
with open(out, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False, width=4096)
print(f"wrote {out}")
