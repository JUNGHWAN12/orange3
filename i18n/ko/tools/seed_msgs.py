r"""Create i18n/ko/msgs.jaml in each repository from the Slovenian file.

Strings that Slovenian marks as `false` (must not be translated: identifiers,
regular expressions, file names ...) keep this mark. Everything else becomes
`null` (untranslated). Slovenian comments are dropped. The result is then
synchronized with the sources with `trubar collect`.

Existing Korean files are never overwritten unless --force is given.

Usage (from C:\orange3)::

    .venv-ko\Scripts\python i18n\ko\tools\seed_msgs.py
"""
import argparse
import subprocess
import sys

from trubar.messages import MsgNode, dump, load

from _common import REPOS


def seed(messages):
    seeded = {}
    for msg, node in messages.items():
        if isinstance(node.value, dict):
            seeded[msg] = MsgNode(seed(node.value))
        else:
            seeded[msg] = MsgNode(False if node.value is False else None)
    return seeded


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing Korean message files")
    args = parser.parse_args()

    for repo in REPOS:
        target = repo.msgs("ko")
        if target.exists() and not args.force:
            print(f"{target}: exists, skipped")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        dump(seed(load(str(repo.msgs("si")))), str(target))
        before = target.read_bytes()
        subprocess.run(
            [sys.executable, "-m", "trubar", "--conf", str(repo.config_file),
             "collect", "-q", "-s", str(repo.source), str(target)],
            check=True)
        changed = "changed by collect" if target.read_bytes() != before \
            else "already in sync with sources"
        print(f"{target}: created ({changed})")


if __name__ == "__main__":
    main()
