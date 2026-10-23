"""Instance management: scaffold a client workspace, upgrade it, cut a release, run health checks.

Product vs instance
  product  = this repository: core/ (methodology, skills, templates), tools/, adapters/, docs/, evals/
  instance = a product snapshot + workspace/ (client data) + local/ (client-only skills) + generated platform folders

Upgrades replace product folders and never touch workspace/ or local/.
"""
from __future__ import annotations

import datetime as dt
import errno
import json
import os
import re
import shutil
import sys
import tarfile
from typing import Dict, List, Optional, Tuple

from .build import ALL_TARGETS, build, read_version
from .skills import Issue, discover_skills, validate_collection

PRODUCT_DIRS = ["core", "tools", "adapters", "evals", "tests"]
PRODUCT_FILES = ["AGENTS.md", "CLAUDE.md", "VERSION", ".gitignore"]
PLATFORM_TARGETS = {
    "google": ["agents", "gemini-cli", "gemini-app", "gemini-extension", "notebook", "portable"],
    "claude": ["agents", "claude", "claude-plugin", "portable"],
    "generic": ["agents", "portable"],
    "all": ALL_TARGETS,
}
JUNK = shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc", ".sos-tmp*")


def _targets_for(platforms: List[str]) -> List[str]:
    out: List[str] = []
    for p in platforms:
        for t in PLATFORM_TARGETS.get(p, []):
            if t not in out:
                out.append(t)
    return out or PLATFORM_TARGETS["all"]


def _copy_product(src_root: str, dest_root: str) -> None:
    for d in PRODUCT_DIRS:
        s = os.path.join(src_root, d)
        if os.path.isdir(s):
            t = os.path.join(dest_root, d)
            if os.path.isdir(t):
                shutil.rmtree(t)
            shutil.copytree(s, t, ignore=JUNK)
    for f in PRODUCT_FILES:
        s = os.path.join(src_root, f)
        if os.path.isfile(s):
            shutil.copyfile(s, os.path.join(dest_root, f))
    # docs: product docs only, never legacy or client-specific material
    sd = os.path.join(src_root, "docs")
    if os.path.isdir(sd):
        td = os.path.join(dest_root, "docs")
        if os.path.isdir(td):
            shutil.rmtree(td)
        shutil.copytree(sd, td, ignore=shutil.ignore_patterns("legacy", "__pycache__", ".DS_Store"))
    s = os.path.join(src_root, "CHANGELOG.md")
    if os.path.isfile(s):
        shutil.copyfile(s, os.path.join(dest_root, "CHANGELOG.md"))


EXTENSION_README_HEAD = """# Sales-OS: Gemini CLI extension

Miller Heiman sales skills for Gemini CLI: Blue, Green and Gold Sheets, call debriefs, deal and pipeline reviews, stakeholder lenses, Coach development, buyer-safe drafts and more. 22 skills, one source, tested rules: never invent, tag evidence, approval before anything outward, internal analysis never reaches the buyer.

## Install

```
gemini extensions install https://github.com/Agents4/Sales-OS
```

Restart the CLI, then try `/sos:start` (or just describe the deal). Then `/sos:setup` to fill in company facts, and `/sos:blue-sheet` on a live deal.

Update later with `gemini extensions update sales-os`. For development, link a local checkout: `gemini extensions link <path>`.

Notes:
- Gemini CLI serves enterprise Gemini Code Assist licenses and API-key use. Individual Google AI accounts moved to Antigravity CLI; there, import the extension with `agy plugin import gemini`, or use the skills in `.agents/skills` (see `adapters/google/`). Verify current status in `adapters/google/platform-facts.md`.
- Data stays in your project folder (`workspace/`). The extension never writes into its own folder.
- The Python tools are bundled (Python 3.8+, standard library only). Inside the extension the context file tells the agent how to call them.
- Methodology names belong to their owner; this is an original synthesis. See `core/methodology/fidelity-ledger.md` before marketing under that name.

---

"""


def export_extension_repo(src_root: str, dest: str) -> int:
    """Assemble a git-ready repository whose root IS a Gemini CLI extension
    (gemini-extension.json, GEMINI.md, skills/, commands/) next to the full product source.
    Gemini CLI installs extensions from a GitHub repository root, so this layout is required."""
    dest = os.path.abspath(dest)
    if os.path.isdir(dest) and any(n != ".git" for n in os.listdir(dest)):
        print("destination %s exists and is not empty" % dest)
        return 1
    rc = build(src_root, targets=["gemini-extension"], quiet=True)
    if rc != 0:
        print("build failed; fix validation errors first")
        return rc
    os.makedirs(dest, exist_ok=True)
    _copy_product(src_root, dest)
    ext = os.path.join(src_root, "dist", "gemini-extension")
    for name in ("gemini-extension.json", "GEMINI.md"):
        shutil.copyfile(os.path.join(ext, name), os.path.join(dest, name))
    for d in ("skills", "commands"):
        shutil.copytree(os.path.join(ext, d), os.path.join(dest, d), ignore=JUNK)
    readme = os.path.join(src_root, "README.md")
    body = open(readme, "r", encoding="utf-8").read() if os.path.isfile(readme) else ""
    with open(os.path.join(dest, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(EXTENSION_README_HEAD + body)
    print("extension repository ready: %s (version %s)" % (dest, read_version(src_root)))
    return 0


def _scaffold_workspace(src_root: str, dest_root: str, client: str) -> None:
    scaf = os.path.join(src_root, "core", "scaffold", "workspace")
    today = dt.date.today().isoformat()
    for dirpath, dirs, files in os.walk(scaf):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",)]
        for f in files:
            if f == ".DS_Store":
                continue
            s = os.path.join(dirpath, f)
            rel = os.path.relpath(s, scaf)
            t = os.path.join(dest_root, "workspace", rel)
            os.makedirs(os.path.dirname(t), exist_ok=True)
            if os.path.exists(t):
                continue  # never overwrite client data
            try:
                text = open(s, "r", encoding="utf-8").read()
            except UnicodeDecodeError:
                shutil.copyfile(s, t)
                continue
            text = text.replace("{{client}}", client).replace("{{date}}", today)
            with open(t, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
    for d in ("accounts", "outputs", "context-library"):
        os.makedirs(os.path.join(dest_root, "workspace", d), exist_ok=True)


def new_instance(src_root: str, dest: str, client: str, platforms: List[str], bundle: Optional[str]) -> int:
    dest = os.path.abspath(dest)
    if os.path.exists(dest) and os.listdir(dest):
        print("destination %s exists and is not empty" % dest)
        return 1
    os.makedirs(dest, exist_ok=True)
    _copy_product(src_root, dest)
    os.makedirs(os.path.join(dest, "local", "skills"), exist_ok=True)
    with open(os.path.join(dest, "local", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# local/\n\nClient-only skills go in `local/skills/<name>/SKILL.md`. They are compiled with the core skills and survive upgrades.\nSee `docs/skill-authoring-guide.md`.\n")
    _scaffold_workspace(src_root, dest, client)
    meta = {
        "client": client,
        "created": dt.date.today().isoformat(),
        "product_version": read_version(src_root),
        "platforms": platforms,
        "bundle": bundle or "all",
    }
    with open(os.path.join(dest, ".sales-os-instance.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    rc = build(dest, bundle=bundle, targets=_targets_for(platforms))
    if rc == 0:
        print("\ninstance ready: %s\nnext: open it in your agent and say \"set up Sales-OS\" (runs the sos-setup skill)." % dest)
    return rc


def upgrade_instance(src_root: str, dest: str) -> int:
    dest = os.path.abspath(dest)
    meta_path = os.path.join(dest, ".sales-os-instance.json")
    if not os.path.isfile(meta_path):
        print("%s is not a Sales-OS instance (no .sales-os-instance.json)" % dest)
        return 1
    meta = json.load(open(meta_path, "r", encoding="utf-8"))
    agents = os.path.join(dest, "AGENTS.md")
    if os.path.isfile(agents):
        shutil.copyfile(agents, agents + ".bak-" + dt.date.today().isoformat())
    _copy_product(src_root, dest)
    _scaffold_workspace(src_root, dest, meta.get("client", "Client"))  # adds new scaffold files only
    old = meta.get("product_version")
    meta["product_version"] = read_version(src_root)
    meta["upgraded"] = dt.date.today().isoformat()
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    print("upgraded %s: %s -> %s (workspace/ and local/ untouched; old AGENTS.md saved as .bak)" % (dest, old, meta["product_version"]))
    return build(dest, bundle=None if meta.get("bundle") in (None, "all") else meta["bundle"],
                 targets=_targets_for(meta.get("platforms", ["all"])))


def release(root: str, out_dir: Optional[str] = None) -> str:
    version = read_version(root)
    out_dir = out_dir or os.path.join(root, "dist", "releases")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "sales-os-%s.tar.gz" % version)
    include = PRODUCT_DIRS + ["docs"] + PRODUCT_FILES + ["README.md", "CHANGELOG.md"]

    def keep(ti: tarfile.TarInfo):
        parts = ti.name.split("/")
        if any(p in ("__pycache__", ".DS_Store", "legacy") for p in parts) or ti.name.endswith(".pyc"):
            return None
        ti.uid = ti.gid = 0
        ti.uname = ti.gname = ""
        ti.mtime = 0
        return ti

    with tarfile.open(path, "w:gz") as tar:
        for item in sorted(include):
            p = os.path.join(root, item)
            if os.path.exists(p):
                tar.add(p, arcname="sales-os-%s/%s" % (version, item), filter=lambda ti: keep(ti))
    return path


# ---------------------------------------------------------------------------- registries
def check_registries(root: str, skills) -> Tuple[List[str], List[str]]:
    """Check the registries declared in os.manifest.json. Returns (problems, notes).
    A registry is a hand-maintained file that must change when a skill is added.
    check = lists_skills: every product skill name appears in the file.
    check = skill_count: every number matched by `pattern` equals the product skill count."""
    mp = os.path.join(root, "os.manifest.json")
    if not os.path.isfile(mp):
        return [], []
    try:
        with open(mp, "r", encoding="utf-8") as fh:
            man = json.load(fh)
    except (OSError, ValueError) as e:
        return ["os.manifest.json is not valid JSON (%s)" % e], []
    names = sorted(s.name for s in skills if getattr(s, "origin", "core") == "core")
    problems: List[str] = []
    notes: List[str] = []
    for reg in man.get("registries", []):
        kind = reg.get("check")
        if not kind:
            continue
        rel = reg.get("file", "")
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            notes.append("registry %s not found" % rel)
            continue
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        if kind == "lists_skills":
            missing = [n for n in names if not re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), text)]
            if missing:
                problems.append("%s does not mention: %s. %s" % (rel, ", ".join(missing), reg.get("update", "")))
        elif kind == "skill_count":
            found = re.findall(reg.get("pattern", r"(\d+) skills"), text)
            wrong = sorted(set(f for f in found if int(f) != len(names)))
            if not found:
                notes.append("%s: no skill count found by pattern %s" % (rel, reg.get("pattern")))
            elif wrong:
                problems.append("%s states %s skills; there are %d. %s" % (rel, "/".join(wrong), len(names), reg.get("update", "")))
        else:
            notes.append("registry %s: unknown check '%s'" % (rel, kind))
    return problems, notes


# ---------------------------------------------------------------------------- doctor
def doctor(root: str) -> int:
    problems = 0
    warn = 0

    def ok(m):
        print("  ok    " + m)

    def bad(m):
        nonlocal problems
        problems += 1
        print("  FAIL  " + m)

    def note(m):
        nonlocal warn
        warn += 1
        print("  warn  " + m)

    print("Sales-OS doctor  (%s)" % root)
    if sys.version_info < (3, 8):
        bad("Python 3.8+ required, found %s" % sys.version.split()[0])
    else:
        ok("python %s" % sys.version.split()[0])
    for rel in ("AGENTS.md", "core/skills", "core/methodology", "core/templates", "tools/sos.py", "VERSION"):
        (ok if os.path.exists(os.path.join(root, rel)) else bad)(rel + (" present" if os.path.exists(os.path.join(root, rel)) else " missing"))

    unreadable: List[Tuple[str, str]] = []
    count = 0
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
        for f in files:
            p = os.path.join(dirpath, f)
            count += 1
            try:
                with open(p, "rb") as fh:
                    fh.read(1024)
            except OSError as e:
                unreadable.append((os.path.relpath(p, root), "%s (errno %s)" % (e.strerror, e.errno)))
    if unreadable:
        bad("%d file(s) cannot be read. On Google Drive for desktop this means the files are cloud-only placeholders:" % len(unreadable))
        for rel, why in unreadable[:20]:
            print("          - %s: %s" % (rel, why))
        print("          Fix: in Drive for desktop set this folder to 'Available offline' (or use Mirror files), then re-run.")
    else:
        ok("all %d files readable" % count)

    junk = []
    for base in (".agents", ".claude", "dist", "core"):
        for dirpath, _, files in os.walk(os.path.join(root, base)):
            junk += [os.path.join(dirpath, f) for f in files if f == ".DS_Store"]
    (note if junk else ok)(".DS_Store files in skills/dist: %d (the Gemini app upload rejects hidden binary files; zips exclude them)" % len(junk) if junk else "no .DS_Store in skills/dist")

    skills = discover_skills(root)
    issues = validate_collection(skills, root)
    e = [i for i in issues if i.level == "error"]
    w = [i for i in issues if i.level == "warn"]
    (bad if e else ok)("%d skills, %d error(s), %d warning(s)" % (len(skills), len(e), len(w)))
    for i in e[:10]:
        print("          " + str(i))

    reg_problems, reg_notes = check_registries(root, skills)
    if os.path.isfile(os.path.join(root, "os.manifest.json")):
        if reg_problems:
            for m in reg_problems:
                bad("registry: " + m)
        else:
            ok("registries in os.manifest.json are consistent with the skills")
        for m in reg_notes:
            note(m)

    a = os.path.join(root, "AGENTS.md")
    if os.path.isfile(a):
        n = len(open(a, "r", encoding="utf-8").read().splitlines())
        (note if n > 220 else ok)("AGENTS.md is %d lines%s" % (n, " (keep it a router, under ~200 lines)" if n > 220 else ""))

    meta_path = os.path.join(root, ".sales-os-instance.json")
    check_targets = None
    check_bundle = None
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as fh:
                meta = json.load(fh)
            check_targets = _targets_for(meta.get("platforms", ["all"]))
            check_bundle = None if meta.get("bundle") in (None, "all") else meta["bundle"]
        except (OSError, ValueError):
            note("could not read .sales-os-instance.json; checking all targets")
    rc = build(root, bundle=check_bundle, targets=check_targets, check=True, quiet=True)
    if rc == 0:
        ok("generated platform outputs are current")
    elif rc == 2:
        note("generated outputs are out of date: run `python3 tools/sos.py build`")
    else:
        bad("build check failed (validation errors)")
    gs = os.path.join(root, ".gemini", "settings.json")
    if os.path.isfile(gs):
        (ok if "AGENTS.md" in open(gs, "r", encoding="utf-8").read() else note)(".gemini/settings.json %s" % ("reads AGENTS.md" if "AGENTS.md" in open(gs, "r", encoding="utf-8").read() else "does not list AGENTS.md in context.fileName (Gemini CLI would miss it)"))
    print("\n%d problem(s), %d warning(s)" % (problems, warn))
    return 1 if problems else 0
