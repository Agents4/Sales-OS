"""Source packs for Gemini Notebook (formerly NotebookLM).

A notebook cannot run skills, so we give it the next best thing: well-structured
source documents plus a chat-instruction block and a Studio prompt cookbook.

Static packs (methodology, etc.) are defined in core/notebook-packs/<name>/pack.json.
Workspace packs are compiled from live data:
    sos.py notebook-pack --account acme      -> a deal room for one account
    sos.py notebook-pack --company           -> company playbook from context-library
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from typing import Dict, List, Optional, Tuple

DEFAULT_MAX_WORDS = 120000
CHAT_INSTRUCTION_SOFT_LIMIT = 3000  # chars; the product limit has changed over time, stay well under it
LIMITS_NOTE = ("Source limits (verify on Google's usage-limits page): consumer Gemini Notebook is roughly 50 sources "
               "per notebook on the standard tier; Gemini Notebook Enterprise is 300 sources, 500,000 words or 500 MB each.")


def words(text: str) -> int:
    return len(text.split())


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)


def split_by_words(text: str, max_words: int) -> List[str]:
    if words(text) <= max_words:
        return [text]
    parts, cur, count = [], [], 0
    for para in re.split(r"\n{2,}", text):
        w = words(para)
        if cur and count + w > max_words:
            parts.append("\n\n".join(cur))
            cur, count = [], 0
        cur.append(para)
        count += w
    if cur:
        parts.append("\n\n".join(cur))
    return parts


def assemble(title: str, chunks: List[Tuple[str, str]], note: str = "") -> str:
    out = ["# %s" % title, ""]
    if note:
        out += [note, ""]
    for label, text in chunks:
        out += ["---", "", "## Document: %s" % label, "", _strip_frontmatter(text).strip(), ""]
    return "\n".join(out).rstrip() + "\n"


def write_sources(out_dir: str, sources: List[Tuple[str, str]], max_words: int) -> List[Tuple[str, int]]:
    """sources: list of (title, text). Writes numbered files, splitting long ones. Returns (filename, words)."""
    os.makedirs(os.path.join(out_dir, "sources"), exist_ok=True)
    written: List[Tuple[str, int]] = []
    n = 0
    for title, text in sources:
        parts = split_by_words(text, max_words)
        for i, part in enumerate(parts, start=1):
            n += 1
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "source"
            suffix = "" if len(parts) == 1 else "-part%d" % i
            fn = "%02d-%s%s.md" % (n, slug, suffix)
            with open(os.path.join(out_dir, "sources", fn), "w", encoding="utf-8") as fh:
                fh.write(part)
            written.append((fn, words(part)))
    return written


def write_readme(out_dir: str, title: str, description: str, written: List[Tuple[str, int]],
                 chat_file: Optional[str], studio_file: Optional[str]) -> None:
    lines = ["# %s" % title, "", description, "", "## Upload steps", "",
             "1. Create a new notebook in Gemini Notebook (or Gemini Notebook Enterprise).",
             "2. Add everything in `sources/` as sources (upload files, or import them to Google Docs first so you can use **Sync with Drive** when they change).",
             "3. Open the chat settings (Configure chat), choose a custom / conversational-style prompt, and paste the contents of `chat-instructions.txt`.",
             "4. Use `studio-prompts.md` for Audio / Video Overviews, Reports, Slide decks, Mind maps, Flashcards and Quizzes.", "",
             "## Sources in this pack (%d)" % len(written), "", "| File | Words |", "|---|---|"]
    for fn, w in written:
        lines.append("| `%s` | %d |" % (fn, w))
    lines += ["", LIMITS_NOTE, "",
              "Refresh rule: regenerate this pack after meaningful changes (`python3 tools/sos.py notebook-pack ...`) and re-upload only the sources that changed. Notebook sources are static copies unless they are Google Docs/Slides synced from Drive.", ""]
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def _copy_text(src: str, dest: str, subst: Optional[Dict[str, str]] = None) -> int:
    text = _read(src)
    for k, v in (subst or {}).items():
        text = text.replace("{{%s}}" % k, v)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    return len(text)


# ------------------------------------------------------------------ static packs
def build_static_packs(root: str, stage_dir: str) -> List[str]:
    base = os.path.join(root, "core", "notebook-packs")
    core = os.path.join(root, "core")
    names: List[str] = []
    if not os.path.isdir(base):
        return names
    for entry in sorted(os.listdir(base)):
        pdir = os.path.join(base, entry)
        pj = os.path.join(pdir, "pack.json")
        if not os.path.isfile(pj):
            continue
        spec = json.load(open(pj, "r", encoding="utf-8"))
        if spec.get("dynamic"):
            continue  # template-only packs (account room, company playbook)
        out_dir = os.path.join(stage_dir, entry)
        sources = []
        for s in spec.get("sources", []):
            chunks = [(f, _read(os.path.join(core, f))) for f in s["files"]]
            sources.append((s["title"], assemble(s["title"], chunks, s.get("note", ""))))
        written = write_sources(out_dir, sources, spec.get("max_words", DEFAULT_MAX_WORDS))
        chat = spec.get("chat_instructions")
        studio = spec.get("studio_prompts")
        if chat:
            n = _copy_text(os.path.join(pdir, chat), os.path.join(out_dir, "chat-instructions.txt"))
            if n > CHAT_INSTRUCTION_SOFT_LIMIT:
                print("  warn: %s chat instructions are %d chars (soft limit %d)" % (entry, n, CHAT_INSTRUCTION_SOFT_LIMIT))
        if studio:
            _copy_text(os.path.join(pdir, studio), os.path.join(out_dir, "studio-prompts.md"))
        write_readme(out_dir, spec.get("title", entry), spec.get("description", ""), written, chat, studio)
        names.append(entry)
    return names


# ---------------------------------------------------------------- workspace packs
def _collect_files(base: str, pattern: str) -> List[str]:
    out = []
    if not os.path.isdir(base):
        return out
    rx = re.compile(pattern, re.IGNORECASE)
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(files):
            if rx.search(f) and not f.startswith(".") and f.lower() != "readme.md":
                out.append(os.path.join(dirpath, f))
    return out


def build_account_pack(root: str, account: str, out_dir: str, with_method: bool = True,
                       max_words: int = DEFAULT_MAX_WORDS, product: Optional[str] = None) -> List[Tuple[str, int]]:
    acct_dir = os.path.join(root, "workspace", "accounts", account)
    if not os.path.isdir(acct_dir):
        raise SystemExit("account folder not found: workspace/accounts/%s" % account)
    core = os.path.join(product or root, "core")
    rel = lambda p: os.path.relpath(p, acct_dir)
    today = dt.date.today().isoformat()

    def group(title: str, files: List[str]) -> Optional[Tuple[str, str]]:
        if not files:
            return None
        return (title, assemble("%s: %s" % (account, title), [(rel(f), _read(f)) for f in files],
                                "Compiled %s from workspace/accounts/%s. Newest information is at the end of each section where dated." % (today, account)))

    gold = _collect_files(acct_dir, r"^gold-sheet.*\.md$") + _collect_files(acct_dir, r"^(profile|account-profile).*\.md$")
    blue = [f for f in _collect_files(acct_dir, r"^blue-sheet.*\.md$")]
    green = sorted(_collect_files(acct_dir, r"^\d{4}-\d{2}-\d{2}.*green.*\.md$") + _collect_files(os.path.join(acct_dir, "green-sheets"), r"\.md$"))
    notes = sorted(set(_collect_files(os.path.join(acct_dir, "call-notes"), r"\.md$")))
    research = _collect_files(os.path.join(acct_dir, "research"), r"\.md$")
    sources = [g for g in (
        group("Account plan and profile", gold), group("Blue Sheets (deal strategy)", blue),
        group("Green Sheets (call plans)", sorted(set(green))), group("Call notes and debriefs", notes),
        group("Research", research)) if g]
    if with_method:
        chunks = [(f, _read(os.path.join(core, f))) for f in (
            "methodology/strategic-selling.md", "methodology/conceptual-selling.md", "methodology/lamp.md",
            "methodology/glossary.md", "methodology/failure-modes.md")]
        sources.append(("Method reference", assemble("Miller Heiman method reference", chunks)))
    written = write_sources(out_dir, sources, max_words)
    pdir = os.path.join(core, "notebook-packs", "account-room")
    subst = {"account": account.replace("-", " ").title(), "date": today}
    chat = os.path.join(pdir, "chat-instructions.txt")
    studio = os.path.join(pdir, "studio-prompts.md")
    if os.path.isfile(chat):
        _copy_text(chat, os.path.join(out_dir, "chat-instructions.txt"), subst)
    if os.path.isfile(studio):
        _copy_text(studio, os.path.join(out_dir, "studio-prompts.md"), subst)
    write_readme(out_dir, "Deal room: %s" % subst["account"],
                 "Account deal room for Gemini Notebook, compiled %s. Contains the account plan, Blue and Green Sheets, call notes and the method reference, so the notebook can answer questions about this account with citations." % today,
                 written, "chat-instructions.txt", "studio-prompts.md")
    return written


def build_company_pack(root: str, out_dir: str, max_words: int = DEFAULT_MAX_WORDS,
                       product: Optional[str] = None) -> List[Tuple[str, int]]:
    cl = os.path.join(root, "workspace", "context-library")
    if not os.path.isdir(cl):
        raise SystemExit("workspace/context-library not found")
    top = sorted(f for f in os.listdir(cl) if f.endswith(".md") and not f.startswith("."))
    rel = lambda p: os.path.relpath(p, cl)
    sources = []
    if top:
        sources.append(("Company context", assemble("Company context", [(f, _read(os.path.join(cl, f))) for f in top])))
    for sub, title in (("competitors", "Competitive intelligence"), ("proof", "Proof points and case studies"),
                       ("objections", "Objection library"), ("playbooks", "Playbooks")):
        files = _collect_files(os.path.join(cl, sub), r"\.md$")
        if files:
            sources.append((title, assemble(title, [(rel(f), _read(f)) for f in files])))
    if not sources:
        raise SystemExit("no markdown found in workspace/context-library")
    written = write_sources(out_dir, sources, max_words)
    pdir = os.path.join(product or root, "core", "notebook-packs", "company-playbook")
    for fn, dest in (("chat-instructions.txt", "chat-instructions.txt"), ("studio-prompts.md", "studio-prompts.md")):
        src = os.path.join(pdir, fn)
        if os.path.isfile(src):
            _copy_text(src, os.path.join(out_dir, dest))
    write_readme(out_dir, "Company playbook", "Company-level sales context for enablement Q&A and onboarding.", written,
                 "chat-instructions.txt", "studio-prompts.md")
    return written
