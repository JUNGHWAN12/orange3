r"""Helper for translating the Korean message files without editing jaml by hand.

Commands (run from C:\orange3 with .venv-ko\Scripts\python):

    tm.py export canvas [-p PATTERN] [-o FILE]
        List untranslated messages as numbered lines::

            ## application/canvasmain.py
            # class `CanvasMainWindow` > def `setup_ui`
            123	Open
            124=	PCA            (= : Slovenian kept the original)
            125~	more text      (~ : Slovenian left this fragment empty)

        Real newlines inside a message are shown as ⏎.

    tm.py import canvas FILE [--force]
        Read lines "<number><TAB><translation>" or "<number>|<translation>"
        (other lines are ignored) and store them into the repository's
        i18n/ko/msgs.jaml. Special values: @keep (true), @no (false),
        @empty (""), @null (null). Use ⏎ for a real newline. Existing
        translations and `false` marks are only replaced with --force.
        Placeholders ({...}, %s) must match the original; otherwise nothing is
        written.

    tm.py lint [canvas widget orange]
        Check all translations for placeholder mismatches (errors) and
        differences in accelerators and HTML tags (warnings).

    tm.py build-check [canvas widget orange]
        Build the packages with all languages (trubar reports syntax errors
        in translations) and check that Korean f-strings compile.

    tm.py fix-ws [canvas widget orange]
        Give all translations the same trailing whitespace as their originals
        (import does this automatically).

    tm.py fill-same [canvas widget orange]
        Fill untranslated messages whose original text already has exactly one
        translation in any of the three files.

Repository names: canvas (orange-canvas-core), widget (orange-widget-base),
orange (orange3).
"""
import argparse
import collections
import re
import sys

from trubar.messages import MsgNode, dump, load

from _common import REPOS

ALIASES = {"canvas": "orange-canvas-core", "widget": "orange-widget-base",
           "orange": "orange3"}
NEWLINE = "⏎"
SPECIAL = {"@keep": True, "@no": False, "@empty": "", "@null": None}


def repo_for(alias):
    name = ALIASES.get(alias, alias)
    return next(r for r in REPOS if r.name == name)


def leaves(messages, path=()):
    """Yield (path, key, node, parent dict) for all leaves in file order."""
    for key, node in messages.items():
        if isinstance(node.value, dict):
            yield from leaves(node.value, path + (key,))
        else:
            yield path, key, node, messages


def load_ko(repo):
    return load(str(repo.msgs("ko")))


def save_ko(repo, messages):
    dump(messages, str(repo.msgs("ko")))


# Placeholder checks

RE_BRACES = re.compile(r"{{|}}|{[^{}]*}")
# The space flag is not supported: "0% complete" is not a format
RE_PERCENT = re.compile(r"%(?:\([^)]*\))?[-#0+]*(?:\d+|\*)?(?:\.\d+)?[sdifgeEFGxXrc%]")
RE_ACCEL = re.compile(r"(?<!&)&(?!&)(?=[A-Za-z0-9])(?![a-z]+;)")
RE_TAG = re.compile(r"</?([a-zA-Z0-9]+)")


def placeholders(s):
    braces = [m for m in RE_BRACES.findall(s) if m not in ("{{", "}}")]
    return (sorted(braces), sorted(RE_PERCENT.findall(s)))


def trailing_ws(s):
    return s[len(s.rstrip()):]


def leading_ws(s):
    return s[:len(s) - len(s.lstrip())]


def normalize_ws(original, translation):
    """Give the translation the same trailing whitespace as the original.

    Fragments of implicitly concatenated strings usually end with a space,
    which editors tend to strip from translation files."""
    if not isinstance(translation, str) or not translation.strip():
        return translation
    return translation.rstrip() + trailing_ws(original)


def check(original, translation):
    """Return (errors, warnings) for a string translation.

    Braces in the translation must also appear in the original: new ones
    would turn the string into an f-string or break str.format. Braces may be
    dropped (e.g. English plurals, {pl(...)}), which is only reported when
    the dropped one is not a plural."""
    errors, warnings = [], []
    ob, op = placeholders(original)
    tb, tp = placeholders(translation)
    extra = collections.Counter(tb) - collections.Counter(ob)
    missing = collections.Counter(ob) - collections.Counter(tb)
    # A part of an original expression is allowed, e.g. {unit} taken
    # out of {pl(n, unit)}
    inner = [b[1:-1] for b in ob]
    extra = [b for b in extra.elements()
             if not (b[1:-1].strip() and any(b[1:-1] in o for o in inner))]
    if extra:
        errors.append(f"braces not in original: {sorted(extra)}")
    dropped = [b for b in missing.elements() if not b.startswith("{pl(")]
    if dropped:
        warnings.append(f"braces dropped: {dropped}")
    if op != tp:
        errors.append(f"percent {op} != {tp}")
    if len(RE_ACCEL.findall(original)) != len(RE_ACCEL.findall(translation)):
        warnings.append("accelerator (&) count differs")
    if sorted(RE_TAG.findall(original)) != sorted(RE_TAG.findall(translation)):
        warnings.append("HTML tags differ")
    if "'" in translation and '"' in translation:
        warnings.append("both quote types in translation")
    if trailing_ws(original) != trailing_ws(translation):
        errors.append("trailing whitespace differs from original")
    if bool(leading_ws(original)) != bool(leading_ws(translation)):
        warnings.append("leading whitespace differs from original")
    return errors, warnings


# Source analysis: where a string literal is used in code

USAGE_FLAGS = {
    "R": "old signal name in replaces=[...]: keep",
    "S": "default value of a Setting: check how it is stored",
    "C": "compared with == / in: translate consistently or keep",
    "K": "dict key, subscript or .get() argument",
}


def string_usages(filename):
    """Return {string: set of flags} for string constants in a source file."""
    # pylint: disable=import-outside-toplevel
    import ast

    try:
        with open(filename, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (OSError, SyntaxError):
        return {}
    usages = collections.defaultdict(set)

    def strings(node):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                yield sub.value
            elif isinstance(sub, ast.JoinedStr):
                yield from ()  # f-strings are never keys

    def mark(node, flag):
        for s in strings(node):
            usages[s].add(flag)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            fname = func.attr if isinstance(func, ast.Attribute) else \
                getattr(func, "id", "")
            for kw in node.keywords:
                if kw.arg == "replaces":
                    mark(kw.value, "R")
            if fname in ("Setting", "ContextSetting", "SettingProvider") \
                    and node.args:
                mark(node.args[0], "S")
            if fname in ("get", "pop", "setdefault") and node.args:
                mark(node.args[0], "K")
        elif isinstance(node, ast.Compare):
            for sub in [node.left] + node.comparators:
                if not isinstance(sub, ast.JoinedStr):
                    mark(sub, "C")
        elif isinstance(node, ast.Dict):
            for key in node.keys:
                if key is not None:
                    mark(key, "K")
        elif isinstance(node, ast.Subscript):
            mark(node.slice, "K")
    return usages


def usage_marks(repo, relpath, cache={}):  # pylint: disable=dangerous-default-value
    key = (repo.name, relpath)
    if key not in cache:
        cache[key] = string_usages(str(repo.source / relpath))
    return cache[key]


# Commands

def cmd_export(args):
    repo = repo_for(args.repo)
    ko = load_ko(repo)
    si = load(str(repo.msgs("si")))
    out = []
    last_file = last_ctx = None
    for idx, (path, key, node, _) in enumerate(leaves(ko)):
        if node.value is not None or args.pattern not in path[0]:
            continue
        if path[0] != last_file:
            out.append(f"\n## {path[0]}")
            last_file, last_ctx = path[0], None
        ctx = " > ".join(path[1:])
        if ctx != last_ctx:
            out.append(f"# {ctx or '(module)'}")
            last_ctx = ctx
        mark = ""
        sinode = si
        try:
            for p in path:
                sinode = sinode[p].value
            sival = sinode[key].value
        except (KeyError, AttributeError, TypeError):
            sival = None
        if sival is True:
            mark = "="
        elif sival == "":
            mark = "~"
        # Keys are source representations; compare with unescaped text too
        try:
            text = key.encode("latin-1", "backslashreplace") \
                .decode("unicode-escape")
        except UnicodeDecodeError:
            text = key
        flags = usage_marks(repo, path[0]).get(text, ())
        if flags:
            mark += "[" + "".join(sorted(flags)) + "]"
        out.append(f"{idx}{mark}\t{key.replace(chr(10), NEWLINE)}")
    text = "\n".join(out).lstrip("\n") + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        n = sum(1 for line in out if line[:1].isdigit())
        print(f"{n} messages written to {args.output}")
    else:
        sys.stdout.write(text)


def parse_translations(filename):
    trans = {}
    with open(filename, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip("\r\n")
            mo = re.match(r"(\d+)[=~]?(?:\t|\|)(.*)$", line)
            if not mo:
                continue
            idx, value = int(mo.group(1)), mo.group(2)
            if idx in trans:
                sys.exit(f"{filename}:{lineno}: duplicate number {idx}")
            if value in SPECIAL:
                value = SPECIAL[value]
            else:
                value = value.replace(NEWLINE, "\n")
            trans[idx] = (lineno, value)
    return trans


def cmd_import(args):
    repo = repo_for(args.repo)
    ko = load_ko(repo)
    trans = parse_translations(args.file)
    entries = list(leaves(ko))
    errors, warnings, updates = [], [], []
    for idx, (lineno, value) in sorted(trans.items()):
        if idx >= len(entries):
            errors.append(f"line {lineno}: no message number {idx}")
            continue
        path, key, node, parent = entries[idx]
        value = normalize_ws(key, value)
        where = f"line {lineno} (#{idx} {path[0]}: {key[:50]!r})"
        if node.value is False and value is not False and not args.force:
            errors.append(f"{where}: message is marked as not translatable")
            continue
        if node.value is not None and node.value != value and not args.force:
            errors.append(f"{where}: already translated as {node.value!r}")
            continue
        if isinstance(value, str) and value:
            errs, warns = check(key, value)
            errors += [f"{where}: {e}" for e in errs]
            warnings += [f"{where}: {w}" for w in warns]
        updates.append((parent, key, value))
    for w in warnings:
        print("warning:", w)
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        sys.exit("Nothing written.")
    for parent, key, value in updates:
        parent[key] = MsgNode(value, parent[key].comments)
    save_ko(repo, ko)
    print(f"{len(updates)} messages stored in {repo.msgs('ko')}")


def all_repos(names):
    return [repo_for(n) for n in (names or ALIASES)]


def cmd_lint(args):
    n_err = n_warn = 0
    for repo in all_repos(args.repos):
        for idx, (path, key, node, _) in enumerate(leaves(load_ko(repo))):
            if not isinstance(node.value, str) or not node.value:
                continue
            errs, warns = check(key, node.value)
            for kind, msgs in (("ERROR", errs), ("warning", warns)):
                for m in msgs:
                    print(f"{kind}: {repo.name} #{idx} {path[0]}: "
                          f"{key[:50]!r}: {m}")
            n_err += len(errs)
            n_warn += len(warns)
    print(f"{n_err} errors, {n_warn} warnings")
    return 1 if n_err else 0


def cmd_build_check(args):
    """Build packages with all languages and check the Korean message table."""
    # pylint: disable=import-outside-toplevel
    import json
    import tempfile
    from pathlib import Path
    from _common import build

    ok = True
    with tempfile.TemporaryDirectory(prefix="orange-ko-build-") as tmp:
        for repo in all_repos(args.repos):
            dest = Path(tmp, repo.package)
            try:
                build(repo, dest)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"{repo.name}: BUILD FAILED: {exc}")
                ok = False
                continue
            tables = {}
            for name in ("English", "Korean"):
                with open(dest / "i18n" / f"{name}.json", encoding="utf-8") as f:
                    tables[name] = json.load(f)
            en, ko = tables["English"], tables["Korean"]
            bad = []
            for idx, (e, k) in enumerate(zip(en, ko)):
                if idx < 2 or not isinstance(e, str):
                    continue
                if re.match(r"[a-zA-Z]*f[a-zA-Z]*['\"]", e):
                    try:
                        compile(k, "<ko>", "eval")
                    except SyntaxError as exc:
                        bad.append((idx, k, exc))
            changed = sum(a != b for a, b in zip(en[2:], ko[2:]))
            print(f"{repo.name}: {len(ko)} entries, {changed} differ from "
                  f"English, {len(bad)} invalid f-strings")
            for idx, k, exc in bad:
                print(f"  #{idx}: {k!r}: {exc}")
            ok = ok and len(en) == len(ko) and not bad
    print("OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


def cmd_fix_ws(args):
    for repo in all_repos(args.repos):
        ko = load_ko(repo)
        fixed = 0
        for _, key, node, parent in leaves(ko):
            value = normalize_ws(key, node.value)
            if value != node.value:
                parent[key] = MsgNode(value, node.comments)
                fixed += 1
        if fixed:
            save_ko(repo, ko)
        print(f"{repo.name}: fixed trailing whitespace in {fixed} messages")


def cmd_fill_same(args):
    repos = all_repos(args.repos)
    files = {repo.name: load_ko(repo) for repo in all_repos(None)}
    known = collections.defaultdict(set)
    for ko in files.values():
        for _, key, node, _ in leaves(ko):
            if isinstance(node.value, str) or node.value is True:
                known[key].add(node.value)
    for repo in repos:
        ko = files[repo.name]
        filled = []
        for path, key, node, parent in leaves(ko):
            if node.value is None and len(known.get(key, ())) == 1:
                value = next(iter(known[key]))
                parent[key] = MsgNode(value, node.comments)
                filled.append((path[0], key, value))
        if filled:
            save_ko(repo, ko)
        print(f"{repo.name}: filled {len(filled)}")
        for fname, key, value in filled:
            print(f"  {fname}: {key[:60]!r} -> {value!r}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("export")
    p.add_argument("repo")
    p.add_argument("-p", "--pattern", default="")
    p.add_argument("-o", "--output")
    p = sub.add_parser("import")
    p.add_argument("repo")
    p.add_argument("file")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("lint")
    p.add_argument("repos", nargs="*")
    p = sub.add_parser("fill-same")
    p.add_argument("repos", nargs="*")
    p = sub.add_parser("fix-ws")
    p.add_argument("repos", nargs="*")
    p = sub.add_parser("build-check")
    p.add_argument("repos", nargs="*")
    args = parser.parse_args()
    return {"export": cmd_export, "import": cmd_import, "lint": cmd_lint,
            "fill-same": cmd_fill_same, "fix-ws": cmd_fix_ws,
            "build-check": cmd_build_check}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
