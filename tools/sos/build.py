"""Compile the canonical skill library into per-platform outputs.

Canonical source : core/skills/*  (+ local/skills/*), core/shared, core/templates ...
Generated outputs:

  .agents/skills/            Gemini CLI, Antigravity CLI, Codex and other Agent Skills clients (workspace scope)
  .claude/skills/            Claude Code
  .gemini/commands/sos/      Gemini CLI slash commands (/sos:blue-sheet ...)
  .gemini/settings.json      created once if missing: makes Gemini CLI read AGENTS.md
  dist/gemini-app/           one zip per skill for upload in the Gemini app / Workspace / Gemini Enterprise
  dist/gemini-extension/     Gemini CLI extension (also importable by Antigravity: `agy plugin import gemini`)
  dist/claude-plugin/        Claude Code plugin
  dist/portable/             single-file prompts for tools without skill support (custom GPTs, Grok, Copilot...)
  dist/notebook-packs/       Gemini Notebook source packs (static packs)

Generated files are never edited by hand. `sos.py build --check` fails if they drift.
"""
from __future__ import annotations

import filecmp
import json
import os
import re
import shutil
import tempfile
import zipfile
from typing import Dict, List, Optional

from . import __version__
from .notebook import build_static_packs
from .skills import (Skill, command_name, compile_skill, discover_skills,
                     select_skills, validate_collection, load_bundles)

ALL_TARGETS = ["agents", "claude", "gemini-cli", "gemini-app", "gemini-extension", "extension-root", "claude-plugin", "portable", "notebook"]

# When the repository root is itself a Gemini CLI extension (gemini-extension.json at the root),
# these root files are generated from dist/gemini-extension so a GitHub install never goes stale.
EXTENSION_ROOT_MARKER = "gemini-extension.json"
EXTENSION_ROOT_FILES = ("gemini-extension.json", "GEMINI.md")
EXTENSION_ROOT_DIRS = ("skills", "commands")
MANIFEST = ".sales-os-managed.json"
ZIP_DATE = (2026, 1, 1, 0, 0, 0)
REPO_ONLY_RE = re.compile(r"<!--\s*repo-only:start\s*-->.*?<!--\s*repo-only:end\s*-->\s*", re.DOTALL)


def read_version(root: str) -> str:
    p = os.path.join(root, "VERSION")
    if os.path.isfile(p):
        return open(p, "r", encoding="utf-8").read().strip() or __version__
    return __version__


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _toml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=True)


def _dir_files(path: str) -> Dict[str, str]:
    out = {}
    for dirpath, _, files in os.walk(path):
        for f in files:
            full = os.path.join(dirpath, f)
            out[os.path.relpath(full, path).replace(os.sep, "/")] = full
    return out


def diff_trees(a: str, b: str) -> List[str]:
    """Differences between expected tree `a` and actual tree `b`."""
    problems: List[str] = []
    fa = _dir_files(a) if os.path.isdir(a) else {}
    fb = _dir_files(b) if os.path.isdir(b) else {}
    for rel in sorted(set(fa) | set(fb)):
        if rel not in fb:
            problems.append("missing: %s" % rel)
        elif rel not in fa:
            problems.append("unexpected: %s" % rel)
        elif not filecmp.cmp(fa[rel], fb[rel], shallow=False):
            problems.append("changed: %s" % rel)
    return problems


# --------------------------------------------------------------------- generators
def gen_skill_dir(stage: str, rel: str, skills: List[Skill], core_dir: str, version: str) -> None:
    base = os.path.join(stage, rel)
    os.makedirs(base, exist_ok=True)
    for s in skills:
        compile_skill(s, core_dir, base)
    _write(os.path.join(base, MANIFEST), json.dumps(
        {"generator": "sales-os", "version": version, "skills": sorted(s.name for s in skills)}, indent=2) + "\n")


def command_toml(skill: Skill, mode: str) -> str:
    desc = skill.description.strip()
    short = desc if len(desc) <= 160 else desc[:157].rstrip() + "..."
    if mode == "project":
        body = (
            "Run the Sales-OS skill `%s`.\n\n"
            "Follow these instructions exactly. Relative paths (references/, assets/) resolve against `.agents/skills/%s/`.\n\n"
            "@{.agents/skills/%s/SKILL.md}\n\n"
            "Request and inputs from the user:\n{{args}}\n" % (skill.name, skill.name, skill.name))
    else:
        body = (
            "Activate and follow the Sales-OS skill `%s` (use the activate_skill tool if it is not already active). "
            "Relative paths (references/, assets/) resolve against the skill's own folder.\n\n"
            "Request and inputs from the user:\n{{args}}\n" % skill.name)
    return "description = %s\nprompt = \"\"\"\n%s\"\"\"\n" % (_toml_str(short), body)


def gen_gemini_commands(stage: str, rel: str, skills: List[Skill], mode: str) -> None:
    base = os.path.join(stage, rel)
    for s in skills:
        _write(os.path.join(base, command_name(s.name) + ".toml"), command_toml(s, mode))


def write_zip(path: str, files: Dict[str, bytes]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for arc in sorted(files):
            zi = zipfile.ZipInfo(arc, date_time=ZIP_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, files[arc])


def gen_gemini_app(stage: str, skills: List[Skill], core_dir: str, root: str, version: str) -> None:
    base = os.path.join(stage, "dist", "gemini-app")
    tmp = tempfile.mkdtemp()
    sizes = {}
    try:
        for s in skills:
            files = compile_skill(s, core_dir, tmp)
            data = {}
            for rel in files:
                data[rel] = open(os.path.join(tmp, s.name, rel), "rb").read()
            zp = os.path.join(base, "zips", s.name + ".zip")
            write_zip(zp, data)
            sizes[s.name] = os.path.getsize(zp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bundles = load_bundles(root).get("bundles", {})
    lines = ["# Upload these skills to the Gemini app, Workspace and Gemini Enterprise", "",
             "Version %s. Generated by `python3 tools/sos.py build`. Do not edit." % version, "",
             "## How", "",
             "- **Gemini app** (gemini.google.com or the Mac app): Skills page > create > upload. Choose one `.zip` from `zips/`. SKILL.md sits at the zip root. Review, then Create.",
             "- **Gemini Enterprise**: an admin first turns on *skills* and *skill sharing* in Feature Management; then users upload and share the same zips.",
             "- If a zip is rejected, upload the matching folder from `.agents/skills/<name>/` instead.",
             "- Only 100 skills can be active at once in the Gemini app. Activate a bundle, not everything.",
             "- Uploads: plain-text files only, max 100 MB combined; scripts cannot reach the internet. These zips contain Markdown only.",
             "- Skills do not sync between the Gemini app and Workspace apps (Docs, Gmail...). Upload in each place you want them.", "",
             "## Bundles (activate these sets)", ""]
    for bname in sorted(bundles):
        b = bundles[bname]
        lines.append("### %s" % bname)
        lines.append(b.get("description", ""))
        lines.append("")
        for sk in b.get("skills", []):
            lines.append("- `%s`" % sk)
        lines.append("")
    lines += ["## All skills", "", "| Zip | Size |", "|---|---|"]
    for n in sorted(sizes):
        lines.append("| `zips/%s.zip` | %.1f KB |" % (n, sizes[n] / 1024.0))
    lines.append("")
    _write(os.path.join(base, "INSTALL.md"), "\n".join(lines))


EXTENSION_NOTE = """
## Running as a Gemini CLI extension

This context file ships with the Sales-OS extension. Your project folder is the working folder; the extension itself lives in `~/.gemini/extensions/sales-os/` (a linked install lives wherever it was linked).

- Skills are active by name. Slash commands are `/sos:start`, `/sos:blue-sheet`, `/sos:green-sheet` and so on.
- The Python tools are bundled. Wherever a skill says `python3 tools/sos.py <command>`, run `python3 ~/.gemini/extensions/sales-os/tools/sos.py <command>` instead. Run it from your project folder: `lint` and `pipeline` read `workspace/` in the current folder, or pass explicit file paths or `--workspace <folder>`.
- Your data stays in your project: `workspace/context-library/`, `workspace/accounts/`, `workspace/outputs/`. Run `sos-setup` to create and fill the context library. Nothing is written into the extension folder.
- Rule files referenced as `core/shared/...` are included inside each skill as `references/...`.
"""


def agents_md_for_extension(root: str) -> str:
    text = _read(os.path.join(root, "AGENTS.md"))
    text = REPO_ONLY_RE.sub("", text)
    text = text.replace("Full rules: `core/shared/operating-rules.md`.",
                        "Full rules: `references/operating-rules.md` inside any skill.")
    text = text.replace("See `core/shared/capabilities.md`.", "See `references/capabilities.md` inside any skill.")
    text = text.replace("method files in `core/methodology/`", "method references inside the skills")
    return text.rstrip() + "\n" + EXTENSION_NOTE


def gen_extension(stage: str, skills: List[Skill], core_dir: str, root: str, version: str) -> None:
    base = os.path.join(stage, "dist", "gemini-extension")
    manifest = {
        "name": "sales-os",
        "version": version,
        "description": "Miller Heiman sales operating system: Blue, Green and Gold Sheet skills, reviews and routines.",
        "contextFileName": "GEMINI.md",
    }
    _write(os.path.join(base, "gemini-extension.json"), json.dumps(manifest, indent=2) + "\n")
    _write(os.path.join(base, "GEMINI.md"), agents_md_for_extension(root))
    for s in skills:
        compile_skill(s, core_dir, os.path.join(base, "skills"))
    gen_gemini_commands(base, "commands/sos", skills, "extension")
    _write(os.path.join(base, "README.md"),
           "# Sales-OS Gemini CLI extension\n\n"
           "Install from this folder:\n\n```\ngemini extensions install <path-to-this-folder>\n```\n\n"
           "or link it while developing: `gemini extensions link <path>`. Restart the CLI afterwards.\n\n"
           "Antigravity CLI: `agy plugin import gemini` converts installed Gemini CLI extensions into plugins.\n\n"
           "Generated by `python3 tools/sos.py build`. Do not edit.\n")


def gen_claude_plugin(stage: str, skills: List[Skill], core_dir: str, version: str) -> None:
    base = os.path.join(stage, "dist", "claude-plugin")
    manifest = {
        "name": "sales-os",
        "version": version,
        "description": "Miller Heiman sales operating system: Blue, Green and Gold Sheet skills, reviews and routines.",
        "author": {"name": "Sales-OS"},
        "keywords": ["sales", "miller-heiman", "strategic-selling", "blue-sheet"],
    }
    _write(os.path.join(base, ".claude-plugin", "plugin.json"), json.dumps(manifest, indent=2) + "\n")
    for s in skills:
        compile_skill(s, core_dir, os.path.join(base, "skills"))
    _write(os.path.join(base, "README.md"),
           "# Sales-OS Claude Code plugin\n\nAdd this folder as a local plugin (or publish it to a plugin marketplace). Skills appear namespaced as `sales-os:<skill>`.\n\nGenerated by `python3 tools/sos.py build`. Do not edit.\n")


def gen_portable(stage: str, skills: List[Skill], core_dir: str, root: str, version: str) -> List[str]:
    base = os.path.join(stage, "dist", "portable")
    notes: List[str] = []
    sp = os.path.join(core_dir, "shared", "portable-system-prompt.md")
    if os.path.isfile(sp):
        txt = _read(sp)
        _write(os.path.join(base, "system-prompt.md"), txt)
        if len(txt) > 8000:
            notes.append("portable system prompt is %d chars (>8000: some chat tools truncate custom instructions)" % len(txt))
    for s in skills:
        parts = ["# Skill: %s" % s.name, "", "> %s" % s.description.strip(), "", s.body.strip(), ""]
        for rel in s.all_dest_files():
            src = None
            if rel in s.local_files():
                src = os.path.join(s.dir, rel)
            else:
                for inc in s.includes:
                    if s.include_dest(inc) == rel:
                        src = os.path.join(core_dir, inc)
            if src and rel.lower().endswith((".md", ".txt", ".json", ".csv", ".toml", ".yaml", ".yml")):
                parts += ["", "---", "", "## Attached file: %s" % rel, "", re.sub(r"\A---\s*\n.*?\n---\s*\n", "", _read(src), flags=re.DOTALL).strip(), ""]
        _write(os.path.join(base, "skills", s.name + ".md"), "\n".join(parts).rstrip() + "\n")
    _write(os.path.join(base, "README.md"),
           "# Portable prompts\n\nFor tools without Agent Skills support (custom GPTs, Grok, Copilot, plain chat).\n\n"
           "1. Paste `system-prompt.md` as the custom instructions / system prompt.\n"
           "2. Attach the needed `skills/<name>.md` files as knowledge, or paste one into the chat when you need it. Each file is self-contained (instructions, references and templates inlined).\n"
           "3. Version %s. Generated by `python3 tools/sos.py build`.\n" % version)
    return notes


# ------------------------------------------------------------------------ driver
def build(root: str, bundle: Optional[str] = None, targets: Optional[List[str]] = None,
          check: bool = False, quiet: bool = False) -> int:
    say = (lambda *a: None) if quiet else print
    targets = targets or ALL_TARGETS
    skills_all = discover_skills(root)
    issues = validate_collection(skills_all, root)
    errors = [i for i in issues if i.level == "error"]
    for i in issues:
        if i.level == "warn" and not quiet:
            say(str(i))
    if errors:
        for i in errors:
            say(str(i))
        say("\nbuild aborted: %d validation error(s). Fix them or run `sos.py validate`." % len(errors))
        return 1
    skills = select_skills(skills_all, root, bundle)
    core_dir = os.path.join(root, "core")
    version = read_version(root)
    stage = tempfile.mkdtemp(prefix="sos-stage-")
    notes: List[str] = []
    try:
        if "agents" in targets:
            gen_skill_dir(stage, ".agents/skills", skills, core_dir, version)
        if "claude" in targets:
            gen_skill_dir(stage, ".claude/skills", skills, core_dir, version)
        if "gemini-cli" in targets:
            gen_gemini_commands(stage, ".gemini/commands/sos", skills, "project")
        if "gemini-app" in targets:
            gen_gemini_app(stage, skills, core_dir, root, version)
        root_ext = "extension-root" in targets and os.path.isfile(os.path.join(root, EXTENSION_ROOT_MARKER))
        if "gemini-extension" in targets or root_ext:
            gen_extension(stage, skills, core_dir, root, version)
        if "claude-plugin" in targets:
            gen_claude_plugin(stage, skills, core_dir, version)
        if "portable" in targets:
            notes += gen_portable(stage, skills, core_dir, root, version)
        if "notebook" in targets:
            build_static_packs(root, os.path.join(stage, "dist", "notebook-packs"))

        # ---- sync or check
        managed_skill_dirs = [r for t, r in (("agents", ".agents/skills"), ("claude", ".claude/skills")) if t in targets]
        whole_dirs = []
        if "gemini-cli" in targets:
            whole_dirs.append(".gemini/commands/sos")
        for t, r in (("gemini-app", "dist/gemini-app"), ("gemini-extension", "dist/gemini-extension"),
                     ("claude-plugin", "dist/claude-plugin"), ("portable", "dist/portable"),
                     ("notebook", "dist/notebook-packs")):
            if t in targets:
                whole_dirs.append(r)

        if root_ext:
            whole_dirs += list(EXTENSION_ROOT_DIRS)
        drift: List[str] = []
        if root_ext:
            ext_stage = os.path.join(stage, "dist", "gemini-extension")
            for name in EXTENSION_ROOT_FILES:
                new_f = os.path.join(ext_stage, name)
                cur_f = os.path.join(root, name)
                if check:
                    if not os.path.isfile(cur_f) or open(new_f, "rb").read() != open(cur_f, "rb").read():
                        drift.append("%s: differs from generated extension file" % name)
                else:
                    shutil.copyfile(new_f, cur_f)
        for rel in managed_skill_dirs:
            new = os.path.join(stage, rel)
            cur = os.path.join(root, rel)
            old_names = set()
            mp = os.path.join(cur, MANIFEST)
            if os.path.isfile(mp):
                try:
                    old_names = set(json.load(open(mp, "r", encoding="utf-8")).get("skills", []))
                except ValueError:
                    pass
            new_names = set(s.name for s in skills)
            if check:
                for n in sorted(new_names):
                    for p in diff_trees(os.path.join(new, n), os.path.join(cur, n)):
                        drift.append("%s/%s: %s" % (rel, n, p))
                for n in sorted(old_names - new_names):
                    drift.append("%s/%s: stale skill no longer in source" % (rel, n))
                if not os.path.isfile(mp):
                    drift.append("%s: not generated yet" % rel)
            else:
                os.makedirs(cur, exist_ok=True)
                for n in old_names - new_names:
                    shutil.rmtree(os.path.join(cur, n), ignore_errors=True)
                for n in new_names:
                    d = os.path.join(cur, n)
                    if os.path.isdir(d):
                        shutil.rmtree(d)
                    shutil.copytree(os.path.join(new, n), d)
                shutil.copyfile(os.path.join(new, MANIFEST), mp)
        for rel in whole_dirs:
            new = os.path.join(stage, "dist", "gemini-extension", rel) if rel in EXTENSION_ROOT_DIRS else os.path.join(stage, rel)
            cur = os.path.join(root, rel)
            if check:
                for p in diff_trees(new, cur):
                    drift.append("%s: %s" % (rel, p))
            else:
                if os.path.isdir(cur):
                    shutil.rmtree(cur)
                os.makedirs(os.path.dirname(cur), exist_ok=True)
                if os.path.isdir(new):
                    shutil.copytree(new, cur)

        if "gemini-cli" in targets and not check:
            sp = os.path.join(root, ".gemini", "settings.json")
            if not os.path.exists(sp):
                _write(sp, json.dumps({"context": {"fileName": ["AGENTS.md"]}}, indent=2) + "\n")
                say("created .gemini/settings.json (Gemini CLI will read AGENTS.md)")
            else:
                say("kept existing .gemini/settings.json. Make sure context.fileName includes \"AGENTS.md\".")
        for n in notes:
            say("note: " + n)
        if check:
            if drift:
                say("generated outputs are out of date (%d differences). Run: python3 tools/sos.py build" % len(drift))
                for d in drift[:40]:
                    say("  " + d)
                return 2
            say("ok: generated outputs match source (%d skills)" % len(skills))
            return 0
        say("built %d skills -> %s" % (len(skills), ", ".join(managed_skill_dirs + whole_dirs)))
        return 0
    finally:
        shutil.rmtree(stage, ignore_errors=True)
