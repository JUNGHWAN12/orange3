r"""Build a local conda channel from the .conda/.tar.bz2 files extracted from
the official Orange installer, so `constructor` can rebuild an equivalent
installer without hitting the network.

Usage (with the build-env python): build_local_channel.py SRC_PKGS_DIR CHANNEL_DIR
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import conda_package_handling.api as cph

src, channel = Path(sys.argv[1]), Path(sys.argv[2])
channel.mkdir(parents=True, exist_ok=True)


def read_subdir(path: Path) -> str:
    """Peek at a .conda or .tar.bz2 package's info/index.json for its subdir."""
    with tempfile.TemporaryDirectory() as tmp:
        cph.extract(str(path), dest_dir=tmp, components=["info"])
        with open(Path(tmp, "info", "index.json"), encoding="utf-8") as f:
            return json.load(f)["subdir"]


counts = {}
for pkg in sorted(src.iterdir()):
    if pkg.suffix not in (".conda",) and not pkg.name.endswith(".tar.bz2"):
        continue
    try:
        subdir = read_subdir(pkg)
    except Exception as exc:
        print(f"SKIP {pkg.name}: {exc}")
        continue
    dest_dir = channel / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pkg, dest_dir / pkg.name)
    counts[subdir] = counts.get(subdir, 0) + 1

for subdir, n in counts.items():
    print(f"{subdir}: {n} packages")
print(f"Local channel populated at {channel}")
