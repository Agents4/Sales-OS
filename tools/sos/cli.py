"""Command line interface for Sales-OS tooling."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from typing import Dict, List, Optional

from . import __version__
from .build import ALL_TARGETS, build
from .instance import doctor, new_instance, release, upgrade_instance
from .lint import lint_file, parse_date
from .mdparse import split_frontmatter
from .notebook import build_account_pack, build_company_pack
from .pipeline import collect, render_csv, render_markdown
from .skills import Issue, discover_skills, validate_collection

LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#|<)([^)\s]+?)(?:#[^)\s]*)?\)")


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))  # tools/sos
    return os.path.abspath(os.path.join(here, "..", ".."))


def workspace_root(args) -> str:
    """Folder that contains `workspace/`. Order: --workspace, the current folder if it has a
    workspace/, else the product folder. This lets the tools serve a user's project when
    Sales-OS is installed elsewhere (for example as a Gemini CLI extension)."""
    given = getattr(args, "workspace", None)
    if given:
        return os.path.abspath(given)
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "workspace")):
        return cwd
    return repo_root()


def _today(args) -> dt.date:
    if getattr(args, "today", None):
        d = parse_date(args.today)
        if d is None:
            raise SystemExit("--today must be YYYY-MM-DD")
        return d
    return dt.date.today()


def _print_issues(issues: List[Issue], strict: bool = False) -> int:
    errs = [i for i in issues if i.level == "error"]
    warns = [i for i in issues if i.level == "warn"]
    for i in errs + warns:
        print(str(i))
    print("\n%d error(s), %d warning(s)" % (len(errs), len(warns)))
    return 1 if errs or (strict and warns) else 0


# ------------------------------------------------------------------- validate
def check_links(root: str) -> List[Issue]:
    issues: List[Issue] = []
    scan = ["AGENTS.md", "README.md", "core", "adapters", "docs", "evals"]
    for item in scan:
        p = os.path.join(root, item)
        files = []
        if os.path.isfile(p):
            files = [p]
        elif os.path.isdir(p):
            for dirpath, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in ("legacy", "scaffold", "__pycache__")]
                files += [os.path.join(dirpath, f) for f in fs if f.endswith(".md")]
        for f in files:
            try:
                text = open(f, "r", encoding="utf-8").read()
            except OSError as e:
                issues.append(Issue("error", "LK000", os.path.relpath(f, root), "unreadable: %s" % e))
                continue
            in_fence = False
            for n, line in enumerate(text.splitlines(), start=1):
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                if in_fence:
                    continue
                for m in LINK_RE.finditer(line):
                    target = m.group(1)
                    if target.startswith(("references/", "assets/")) or "{{" in target:
                        continue
                    full = os.path.normpath(os.path.join(os.path.dirname(f), target))
                    if not os.path.exists(full):
                        issues.append(Issue("error", "LK001", "%s:%d" % (os.path.relpath(f, root), n), "broken link: %s" % target))
    return issues


def cmd_validate(args) -> int:
    root = repo_root()
    skills = discover_skills(root)
    issues = validate_collection(skills, root)
    if not args.skip_links:
        issues += check_links(root)
    # eval cases complete?
    cases = os.path.join(root, "evals", "cases")
    if os.path.isdir(cases):
        for c in sorted(os.listdir(cases)):
            d = os.path.join(cases, c)
            if os.path.isdir(d):
                for need in ("input.md", "expected.md"):
                    if not os.path.isfile(os.path.join(d, need)):
                        issues.append(Issue("error", "EV001", "evals/cases/" + c, "missing " + need))
    print("%d skills checked" % len(skills))
    return _print_issues(issues, args.strict)


def cmd_build(args) -> int:
    root = repo_root()
    targets = args.target or None
    return build(root, bundle=args.bundle, targets=targets, check=args.check)


# ----------------------------------------------------------------------- lint
def sheet_files(root: str) -> List[str]:
    base = os.path.join(root, "workspace", "accounts")
    out = []
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            try:
                head = open(p, "r", encoding="utf-8").read(600)
            except OSError:
                out.append(p)
                continue
            if re.search(r"^type:\s*(blue|green|gold)-sheet", head, re.MULTILINE):
                out.append(p)
    return sorted(out)


def cmd_lint(args) -> int:
    root = workspace_root(args)
    today = _today(args)
    paths = args.paths or sheet_files(root)
    if not paths:
        print("no sheets found (looked in workspace/accounts). Pass a path, or create a sheet with the mh-blue-sheet skill.")
        return 0
    all_issues: List[Issue] = []
    payload = []
    for p in paths:
        issues, fm, stats = lint_file(p, today=today, stale_days=args.stale_days, best_few_stale_days=args.best_few_stale_days)
        all_issues += issues
        payload.append({"file": p, "type": fm.get("type"), "stats": stats, "issues": [{"level": i.level, "code": i.code, "message": i.msg} for i in issues]})
        if not args.json:
            print("== %s [%s]" % (os.path.relpath(p, root) if p.startswith(root) else p, fm.get("type", "?")))
            for i in issues:
                print("   %-5s %s  %s" % (i.level.upper(), i.code, i.msg))
            if not issues:
                print("   clean")
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
        errs = sum(1 for i in all_issues if i.level == "error")
        return 1 if errs else 0
    errs = sum(1 for i in all_issues if i.level == "error")
    warns = sum(1 for i in all_issues if i.level == "warn")
    print("\n%d sheet(s): %d error(s), %d warning(s)" % (len(paths), errs, warns))
    return 1 if errs or (args.strict and warns) else 0


def cmd_pipeline(args) -> int:
    root = workspace_root(args)
    today = _today(args)
    rows = collect(root, today, args.stale_days, args.best_few_stale_days)
    text = render_csv(rows) if args.format == "csv" else render_markdown(rows, today)
    if args.out:
        out = args.out
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote %s (%d sheets)" % (out, len(rows)))
    else:
        sys.stdout.write(text)
    return 0


def cmd_notebook_pack(args) -> int:
    root = workspace_root(args)
    if args.account:
        out = args.out or os.path.join(root, "dist", "notebook-packs", "deal-room-" + args.account)
        written = build_account_pack(root, args.account, out, with_method=not args.no_method, product=repo_root())
    elif args.company:
        out = args.out or os.path.join(root, "dist", "notebook-packs", "company-playbook")
        written = build_company_pack(root, out, product=repo_root())
    else:
        print("choose --account <slug> or --company")
        return 1
    print("wrote %d source file(s) to %s" % (len(written), out))
    for fn, w in written:
        print("  %-48s %7d words" % (fn, w))
    return 0


def cmd_new_instance(args) -> int:
    return new_instance(repo_root(), args.dest, args.client, args.platforms, args.bundle)


def cmd_upgrade(args) -> int:
    return upgrade_instance(repo_root(), args.dest)


def cmd_release(args) -> int:
    p = release(repo_root(), args.out)
    print("wrote " + p)
    return 0


def cmd_export_extension(args) -> int:
    from .instance import export_extension_repo
    return export_extension_repo(repo_root(), args.dest)


def cmd_list(args) -> int:
    root = repo_root()
    skills = discover_skills(root)
    for s in skills:
        md = s.metadata
        print("%-26s %-8s %s" % (s.name, md.get("layer", ""), (s.description[:90] + "...") if len(s.description) > 90 else s.description))
    print("\n%d skills" % len(skills))
    return 0


def cmd_doctor(args) -> int:
    return doctor(repo_root())


# ------------------------------------------------------------------- selftest
def cmd_selftest(args) -> int:
    root = repo_root()
    fx = os.path.join(root, "tests", "fixtures")
    exp_path = os.path.join(fx, "expected.json")
    if not os.path.isfile(exp_path):
        print("tests/fixtures/expected.json missing")
        return 1
    expected = json.load(open(exp_path, "r", encoding="utf-8"))
    today = dt.date(2026, 10, 17)
    failures = 0
    for fn, spec in sorted(expected.items()):
        issues, fm, stats = lint_file(os.path.join(root, fn), today=today)
        got = sorted(set(i.code for i in issues if i.level == "error"))
        got_w = sorted(set(i.code for i in issues if i.level == "warn"))
        want = sorted(spec.get("errors", []))
        want_w = sorted(spec.get("warnings_include", []))
        ok = got == want and all(w in got_w for w in want_w)
        print("%s %-28s errors=%s%s" % ("PASS" if ok else "FAIL", fn, got, "" if ok else "  expected errors=%s warnings_include=%s got warnings=%s" % (want, want_w, got_w)))
        if not ok:
            failures += 1
    # parser sanity
    fm, body, err = split_frontmatter("---\nname: x\nmetadata:\n  a: \"b\"\n  c: [1, 2]\n---\nbody")
    parser_ok = err is None and fm.get("name") == "x" and fm["metadata"]["a"] == "b" and body == "body" and fm["metadata"]["c"] == ["1", "2"]
    print("%s frontmatter parser" % ("PASS" if parser_ok else "FAIL"))
    failures += 0 if parser_ok else 1
    # pipeline on fixtures
    rows = collect(root, today, paths=[os.path.join(root, f) for f in sorted(expected) if "blue-" in os.path.basename(f)])
    print("%s pipeline collects %d fixture sheet(s)" % ("PASS" if rows else "FAIL", len(rows)))
    failures += 0 if rows else 1
    print("\n%s" % ("all selftests passed" if not failures else "%d selftest failure(s)" % failures))
    return 1 if failures else 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="sos.py", description="Sales-OS tooling (v%s)" % __version__)
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    s = sub.add_parser("validate", help="validate skills against the Agent Skills spec, plus links and eval cases")
    s.add_argument("--strict", action="store_true", help="treat warnings as errors")
    s.add_argument("--skip-links", action="store_true")
    s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("build", help="compile skills into platform outputs")
    s.add_argument("--bundle", help="only this bundle (see core/bundles.json)")
    s.add_argument("--target", action="append", choices=ALL_TARGETS, help="limit to a target (repeatable)")
    s.add_argument("--check", action="store_true", help="fail if generated outputs are out of date")
    s.set_defaults(fn=cmd_build)

    s = sub.add_parser("lint", help="lint Blue, Green and Gold Sheets")
    s.add_argument("paths", nargs="*")
    s.add_argument("--today", help="YYYY-MM-DD (for reproducible runs)")
    s.add_argument("--stale-days", type=int, default=14)
    s.add_argument("--best-few-stale-days", type=int, default=7)
    s.add_argument("--strict", action="store_true")
    s.add_argument("--json", action="store_true")
    s.add_argument("--workspace", help="folder that contains workspace/ (default: current folder if it has one, else this product folder)")
    s.set_defaults(fn=cmd_lint)

    s = sub.add_parser("pipeline", help="portfolio hygiene report across all Blue Sheets")
    s.add_argument("--format", choices=["md", "csv"], default="md")
    s.add_argument("--out")
    s.add_argument("--today")
    s.add_argument("--stale-days", type=int, default=14)
    s.add_argument("--best-few-stale-days", type=int, default=7)
    s.add_argument("--workspace", help="folder that contains workspace/ (default: current folder if it has one, else this product folder)")
    s.set_defaults(fn=cmd_pipeline)

    s = sub.add_parser("notebook-pack", help="compile a Gemini Notebook source pack from the workspace")
    s.add_argument("--account", help="account folder slug under workspace/accounts")
    s.add_argument("--company", action="store_true", help="company playbook from workspace/context-library")
    s.add_argument("--out")
    s.add_argument("--no-method", action="store_true", help="do not append the method reference sources")
    s.add_argument("--workspace", help="folder that contains workspace/ (default: current folder if it has one, else this product folder)")
    s.set_defaults(fn=cmd_notebook_pack)

    s = sub.add_parser("new-instance", help="scaffold a client instance")
    s.add_argument("dest")
    s.add_argument("--client", required=True)
    s.add_argument("--platforms", nargs="+", default=["google"], choices=["google", "microsoft", "claude", "generic", "all"])
    s.add_argument("--bundle", help="restrict to a skill bundle")
    s.set_defaults(fn=cmd_new_instance)

    s = sub.add_parser("upgrade-instance", help="upgrade an instance from this product checkout (keeps workspace/ and local/)")
    s.add_argument("dest")
    s.set_defaults(fn=cmd_upgrade)

    s = sub.add_parser("release", help="write dist/releases/sales-os-<version>.tar.gz (no client data)")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_release)

    s = sub.add_parser("export-extension", help="assemble a git-ready Gemini CLI extension repository (extension at the repository root)")
    s.add_argument("dest")
    s.set_defaults(fn=cmd_export_extension)

    s = sub.add_parser("list", help="list skills")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("doctor", help="health check (readability, drift, structure)")
    s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("selftest", help="run the linter and parser against tests/fixtures")
    s.set_defaults(fn=cmd_selftest)

    args = p.parse_args(argv)
    return args.fn(args)
