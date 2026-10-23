"""Load, validate and compile Agent Skills (https://agentskills.io/specification).

Canonical skills live in `core/skills/<name>/` (and optional `local/skills/<name>/`
for client-specific skills). A skill's `metadata.includes` lists shared files
(relative to `core/`) that are vendored into the compiled skill so every skill is
fully self-contained. That matters for platforms that only accept a zip (Gemini app).

  core/templates/*  -> <skill>/assets/<basename>
  everything else   -> <skill>/references/<basename>
"""
from __future__ import annotations

import json
import os
import re
import shutil
from typing import Dict, List, Optional, Tuple

from .mdparse import split_frontmatter

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"(?<![\w/.-])((?:references|assets|scripts)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
IGNORE_NAMES = {".DS_Store", "Thumbs.db", "__pycache__", ".gitkeep"}
REQUIRED_SECTIONS = [
    ("SK030", r"^##\s+When to use"),
    ("SK031", r"^##\s+(Procedure|Steps)"),
    ("SK032", r"^##\s+Output"),
    ("SK033", r"^##\s+Quality gate"),
]


class Issue(object):
    def __init__(self, level: str, code: str, where: str, msg: str):
        self.level = level  # error | warn
        self.code = code
        self.where = where
        self.msg = msg

    def __str__(self) -> str:
        return "%-5s %s %s: %s" % (self.level.upper(), self.code, self.where, self.msg)


class Skill(object):
    def __init__(self, name: str, directory: str, origin: str):
        self.name = name  # directory name
        self.dir = directory
        self.origin = origin  # core | local
        self.raw = ""
        self.fm: Dict = {}
        self.body = ""
        self.fm_error: Optional[str] = None

    @property
    def description(self) -> str:
        return str(self.fm.get("description", ""))

    @property
    def metadata(self) -> Dict:
        m = self.fm.get("metadata", {})
        return m if isinstance(m, dict) else {}

    @property
    def includes(self) -> List[str]:
        raw = self.metadata.get("includes", "")
        if isinstance(raw, list):
            items = raw
        else:
            items = re.split(r"[,\n]", str(raw))
        return [i.strip() for i in items if i.strip()]

    def include_dest(self, rel: str) -> str:
        base = os.path.basename(rel)
        if rel.replace("\\", "/").startswith("templates/"):
            return "assets/" + base
        return "references/" + base

    def local_files(self) -> List[str]:
        """Skill-local files (relative to skill dir), excluding SKILL.md and junk."""
        out = []
        for root, dirs, files in os.walk(self.dir):
            dirs[:] = sorted(d for d in dirs if d not in IGNORE_NAMES and not d.startswith("."))
            for f in sorted(files):
                if f in IGNORE_NAMES or f.startswith(".") or f == "SKILL.md":
                    continue
                full = os.path.join(root, f)
                out.append(os.path.relpath(full, self.dir).replace(os.sep, "/"))
        return out

    def all_dest_files(self) -> List[str]:
        files = self.local_files() + [self.include_dest(i) for i in self.includes]
        return sorted(set(files))


def load_skill(directory: str, origin: str = "core") -> Skill:
    s = Skill(os.path.basename(directory.rstrip("/")), directory, origin)
    path = os.path.join(directory, "SKILL.md")
    with open(path, "r", encoding="utf-8") as fh:
        s.raw = fh.read()
    s.fm, s.body, s.fm_error = split_frontmatter(s.raw)
    return s


def discover_skills(root: str) -> List[Skill]:
    """Find skills in core/skills and local/skills. local overrides core on name clash."""
    found: Dict[str, Skill] = {}
    for origin, rel in (("core", "core/skills"), ("local", "local/skills")):
        base = os.path.join(root, rel)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            d = os.path.join(base, entry)
            if entry.startswith(".") or not os.path.isdir(d):
                continue
            if not os.path.isfile(os.path.join(d, "SKILL.md")):
                continue
            found[entry] = load_skill(d, origin)
    return [found[k] for k in sorted(found)]


def validate_skill(skill: Skill, core_dir: str) -> List[Issue]:
    issues: List[Issue] = []
    w = "skill:" + skill.name

    def err(code, msg):
        issues.append(Issue("error", code, w, msg))

    def warn(code, msg):
        issues.append(Issue("warn", code, w, msg))

    if skill.fm_error:
        err("SK001", "frontmatter parse error: " + skill.fm_error)
        return issues
    if not skill.fm:
        err("SK002", "SKILL.md has no YAML frontmatter")
        return issues

    fm = skill.fm
    for k in fm:
        if k not in SPEC_KEYS:
            err("SK003", "unknown frontmatter key %r (allowed: %s)" % (k, ", ".join(sorted(SPEC_KEYS))))

    name = str(fm.get("name", ""))
    if not name:
        err("SK004", "missing `name`")
    else:
        if len(name) > 64:
            err("SK005", "name longer than 64 characters")
        if not NAME_RE.match(name):
            err("SK006", "name must be lowercase letters, digits, single hyphens, not start/end with a hyphen")
        if name != skill.name:
            err("SK007", "name %r must match directory name %r" % (name, skill.name))

    desc = skill.description
    if not desc.strip():
        err("SK008", "missing `description`")
    else:
        if len(desc) > 1024:
            err("SK009", "description is %d chars (max 1024)" % len(desc))
        if "use when" not in desc.lower():
            warn("SK020", "description should say when to use the skill (include 'Use when ...')")
        if len(desc) < 80:
            warn("SK021", "description is very short; routing quality depends on it")

    compat = fm.get("compatibility")
    if compat is not None and not (1 <= len(str(compat)) <= 500):
        err("SK010", "compatibility must be 1-500 chars")

    md = fm.get("metadata", {})
    if md and not isinstance(md, dict):
        err("SK013", "metadata must be a map")
    elif isinstance(md, dict):
        for k, v in md.items():
            if not isinstance(v, str):
                err("SK014", "metadata value for %r must be a string" % k)
        if "version" not in md:
            warn("SK022", "metadata.version missing")

    lines = skill.body.count("\n") + 1
    if lines > 500:
        err("SK011", "SKILL.md body is %d lines (keep under 500; move detail to references)" % lines)
    if len(skill.raw) > 24000:
        warn("SK012", "SKILL.md is %d chars (~%d tokens); trim or split into references" % (len(skill.raw), len(skill.raw) // 4))

    for code, rx in REQUIRED_SECTIONS:
        if not re.search(rx, skill.body, re.MULTILINE | re.IGNORECASE):
            warn(code, "missing recommended section matching %r" % rx)

    # includes resolve?
    dests: Dict[str, str] = {}
    for rel in skill.includes:
        src = os.path.join(core_dir, rel)
        if not os.path.isfile(src):
            err("SK040", "include not found: core/%s" % rel)
            continue
        dest = skill.include_dest(rel)
        if dest in dests and dests[dest] != rel:
            err("SK041", "include basename clash: %s and %s -> %s" % (dests[dest], rel, dest))
        dests[dest] = rel
    local = set(skill.local_files())
    for d in dests:
        if d in local:
            err("SK042", "include %s clashes with a skill-local file" % d)

    # references in body must resolve
    available = set(skill.local_files()) | set(dests.keys())
    for m in sorted(set(REF_RE.findall(skill.body))):
        if m not in available:
            err("SK050", "body references %s which is neither skill-local nor included" % m)
    # included files not referenced in the body (informational)
    body_refs = set(REF_RE.findall(skill.body))
    for d in sorted(dests):
        if d not in body_refs:
            warn("SK051", "included %s is never referenced in the body" % d)

    # junk
    for root, _, files in os.walk(skill.dir):
        for f in files:
            if f in IGNORE_NAMES:
                warn("SK060", "junk file %s (excluded from builds)" % os.path.relpath(os.path.join(root, f), skill.dir))
    return issues


def command_name(skill_name: str) -> str:
    for p in ("mh-", "sos-"):
        if skill_name.startswith(p):
            return skill_name[len(p):]
    return skill_name


def validate_collection(skills: List[Skill], root: str) -> List[Issue]:
    issues: List[Issue] = []
    core_dir = os.path.join(root, "core")
    seen_cmd: Dict[str, str] = {}
    for s in skills:
        issues.extend(validate_skill(s, core_dir))
        c = command_name(s.name)
        if c in seen_cmd:
            issues.append(Issue("error", "SK070", "skill:" + s.name, "command name %r clashes with %s" % (c, seen_cmd[c])))
        seen_cmd[c] = s.name
    # bundles
    bpath = os.path.join(core_dir, "bundles.json")
    if os.path.isfile(bpath):
        try:
            with open(bpath, "r", encoding="utf-8") as fh:
                bundles = json.load(fh)
        except ValueError as e:
            issues.append(Issue("error", "SK080", "bundles.json", "invalid JSON: %s" % e))
            bundles = {}
        names = set(s.name for s in skills)
        for bname, spec in (bundles.get("bundles", {}) or {}).items():
            for sk in spec.get("skills", []):
                if sk not in names:
                    issues.append(Issue("error", "SK081", "bundles.json", "bundle %r references unknown skill %r" % (bname, sk)))
        covered = set()
        for spec in (bundles.get("bundles", {}) or {}).values():
            covered.update(spec.get("skills", []))
        for n in sorted(names - covered):
            issues.append(Issue("warn", "SK082", "bundles.json", "skill %r is in no bundle" % n))
        for pname, spec in (bundles.get("agent_presets", {}) or {}).items():
            if pname.startswith("_"):
                continue
            plist = spec.get("skills", [])
            for sk in plist:
                if sk not in names:
                    issues.append(Issue("error", "SK083", "bundles.json", "agent preset %r references unknown skill %r" % (pname, sk)))
            if len(plist) > 8:
                issues.append(Issue("error", "SK084", "bundles.json", "agent preset %r has %d skills; the limit is 8" % (pname, len(plist))))
    return issues


def load_bundles(root: str) -> Dict:
    p = os.path.join(root, "core", "bundles.json")
    if not os.path.isfile(p):
        return {"bundles": {}}
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def select_skills(skills: List[Skill], root: str, bundle: Optional[str]) -> List[Skill]:
    if not bundle or bundle == "all":
        return skills
    b = load_bundles(root).get("bundles", {})
    if bundle not in b:
        raise SystemExit("unknown bundle %r (available: %s)" % (bundle, ", ".join(sorted(b)) or "none"))
    wanted = set(b[bundle].get("skills", []))
    return [s for s in skills if s.name in wanted]


def compile_skill(skill: Skill, core_dir: str, dest_root: str) -> List[str]:
    """Write a self-contained copy of the skill under dest_root/<name>/. Returns relative file list."""
    dest = os.path.join(dest_root, skill.name)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    written: List[str] = []

    def put(src: str, rel: str):
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(src, out)
        written.append(rel)

    put(os.path.join(skill.dir, "SKILL.md"), "SKILL.md")
    for rel in skill.local_files():
        put(os.path.join(skill.dir, rel), rel)
    for rel in skill.includes:
        put(os.path.join(core_dir, rel), skill.include_dest(rel))
    return sorted(written)
