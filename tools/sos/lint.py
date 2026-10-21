"""Deterministic quality checks for Blue, Green and Gold Sheets.

These are the checks a human reviewer would otherwise do by eye. They run on the
Markdown artifacts (frontmatter + pipe tables) and need no network or LLM.
Findings use stable codes so skills, rubrics and evals can refer to them.

  BS = Blue Sheet, GS = Green Sheet, AS = Gold (account) Sheet
"""
from __future__ import annotations

import datetime as dt
import re
from typing import Dict, List, Optional, Tuple

from .mdparse import (Table, find_tables, is_blank, is_unknown, parse_tables,
                      row_is_empty, section_text, split_frontmatter)
from .skills import Issue

MODE_WORDS = [
    ("even keel", "EK"), ("even-keel", "EK"), ("overconfident", "OC"), ("over-confident", "OC"),
    ("growth", "G"), ("trouble", "T"),
]
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
SSO_DATE_RE = re.compile(
    r"(\b20\d\d[-/]\d{1,2}([-/]\d{1,2})?\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,4}\b|\bq[1-4]\b|\bfy\s?\d{2,4}\b|\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\b|\bend of (the )?(quarter|year|month)\b)",
    re.IGNORECASE,
)


def parse_date(s: object) -> Optional[dt.date]:
    if not s:
        return None
    m = DATE_RE.search(str(s))
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def mode_code(cell: str) -> Optional[str]:
    c = (cell or "").strip().lower()
    for word, code in MODE_WORDS:
        if word in c:
            return code
    if re.match(r"^(g|t|ek|oc)\b", c):
        return re.match(r"^(g|t|ek|oc)\b", c).group(1).upper()
    return None


def role_code(cell: str) -> Optional[str]:
    c = (cell or "").strip().lower()
    if not c:
        return None
    if "economic" in c or re.match(r"^eb\b", c):
        return "EB"
    if "user" in c or re.match(r"^ub\b", c):
        return "UB"
    if "technical" in c or re.match(r"^tb\b", c):
        return "TB"
    if "coach" in c:
        return "COACH"
    return None


def support_value(cell: str) -> Optional[int]:
    m = re.search(r"[-+−–]?\s*\d", cell or "")
    if not m:
        return None
    try:
        v = int(m.group(0).replace("−", "-").replace("–", "-").replace(" ", ""))
    except ValueError:
        return None
    return v


def _rows(tables: List[Table], pattern: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for t in find_tables(tables, pattern):
        out.extend(r for r in t.rows if not row_is_empty(r))
    return out


def _filled(rows: List[Dict[str, str]], key: str) -> List[Dict[str, str]]:
    return [r for r in rows if not is_unknown(r.get(key, ""))]


def _ids(cell: str, prefix: str) -> List[str]:
    return [m.upper() for m in re.findall(r"\b%s-?\d+\b" % prefix, cell or "", flags=re.IGNORECASE)]


def _norm_id(x: str, prefix: str) -> str:
    m = re.search(r"(\d+)", x)
    return "%s-%s" % (prefix, m.group(1)) if m else x.upper()


class LintContext(object):
    def __init__(self, path: str, today: dt.date, stale_days: int, best_few_stale_days: int):
        self.path = path
        self.today = today
        self.stale_days = stale_days
        self.best_few_stale_days = best_few_stale_days
        self.issues: List[Issue] = []

    def err(self, code: str, msg: str):
        self.issues.append(Issue("error", code, self.path, msg))

    def warn(self, code: str, msg: str):
        self.issues.append(Issue("warn", code, self.path, msg))


# --------------------------------------------------------------------------- blue
def lint_blue(fm: Dict, body: str, ctx: LintContext) -> Dict:
    stats: Dict = {}
    for key in ("account", "opportunity", "owner", "sso", "close_date", "funnel_zone", "status", "last_reviewed"):
        if is_blank(str(fm.get(key, ""))):
            ctx.err("BS001", "frontmatter `%s` is missing or still a placeholder" % key)

    status = str(fm.get("status", "active")).lower()
    zone = str(fm.get("funnel_zone", "")).lower()
    if zone and zone not in ("above", "in", "best-few"):
        ctx.err("BS019", "funnel_zone must be one of: above, in, best-few (got %r)" % zone)
    active = status in ("active", "")

    sso = str(fm.get("sso", "")).strip()
    if sso and not is_blank(sso):
        if not re.search(r"\d", sso) or not SSO_DATE_RE.search(sso) or len(sso) < 40:
            ctx.warn("BS002", "SSO fails the colleague test: it needs a named account, scope/value and a date so someone could say on that date whether it was hit")
    close = parse_date(fm.get("close_date"))
    if active and close and close < ctx.today:
        ctx.warn("BS017", "close_date %s is in the past on an active opportunity" % close.isoformat())

    tables = parse_tables(body)
    infl = _rows(tables, r"buying influences")
    infl = [r for r in infl if "role" in r]
    wr = _rows(tables, r"win[- ]?results?")
    rf = _rows(tables, r"red flags?")
    acts = _rows(tables, r"action plan")
    comp = _rows(tables, r"competition")
    stats.update(influences=len(infl), red_flags=len(rf), actions=len(acts))

    # --- influences
    roles: Dict[str, List[Dict[str, str]]] = {"EB": [], "UB": [], "TB": [], "COACH": []}
    for r in infl:
        rc = role_code(r.get("role", ""))
        if rc:
            roles[rc].append(r)
    named = lambda rows: [r for r in rows if not is_unknown(r.get("name", ""))]
    eb_named = named(roles["EB"])
    distinct_eb = set(r.get("name", "").strip().lower() for r in eb_named)
    stats["eb_named"] = len(distinct_eb)
    stats["coach_named"] = len(named(roles["COACH"]))
    if len(distinct_eb) > 1:
        ctx.err("BS003", "more than one Economic Buyer named (%s). There is exactly one; the others are Users, Technical Buyers or influencers" % ", ".join(sorted(distinct_eb)))
    if not eb_named:
        has_flag = any(("economic" in (r.get("red_flag", "") + r.get("flag", "")).lower() or re.search(r"\beb\b|economic buyer", " ".join(r.values()), re.IGNORECASE)) for r in rf)
        if has_flag:
            ctx.warn("BS003", "Economic Buyer is not identified (flagged as a red flag, now it needs an access action)")
        else:
            ctx.err("BS003", "Economic Buyer is not identified and there is no red flag for it")
    for code, key, label in (("BS004", "UB", "User Buyer"), ("BS004", "TB", "Technical Buyer"), ("BS004", "COACH", "Coach")):
        if not named(roles[key]):
            ctx.warn(code, "no named %s (Unknown is allowed but must appear as a red flag or unknown with an action)" % label)
    named_people = set()
    for r in infl:
        if not is_unknown(r.get("name", "")):
            named_people.add(r.get("name", "").strip().lower())
    stats["named_people"] = len(named_people)
    if active and zone == "best-few" and len(named_people) < 3:
        ctx.warn("BS012", "single or double threaded: only %d named buying influence(s) on a Best Few opportunity" % len(named_people))

    for r in infl:
        who = r.get("name", "") or r.get("role", "")
        if is_unknown(r.get("name", "")):
            continue
        if mode_code(r.get("mode", "") or r.get("response_mode", "")) is None:
            ctx.warn("BS005", "%s: response mode is missing or not one of Growth / Trouble / Even Keel / Overconfident" % who)
        deg = (r.get("degree_of_influence", "") or r.get("degree", "")).strip().lower()
        if deg and deg[0] not in "hml":
            ctx.warn("BS005", "%s: degree of influence should be High / Medium / Low" % who)
        sup = r.get("support", "")
        if sup and not is_unknown(sup):
            v = support_value(sup)
            if v is None or v < -5 or v > 5:
                ctx.warn("BS015", "%s: support must be an integer from -5 to +5" % who)
        lv = parse_date(r.get("last_verified", ""))
        if lv and (ctx.today - lv).days > 60:
            ctx.warn("BS016", "%s: mode/support last verified %s (over 60 days ago)" % (who, lv.isoformat()))

    # EB in Even Keel / Overconfident on a best-few deal
    for r in eb_named:
        mc = mode_code(r.get("mode", "") or r.get("response_mode", ""))
        if mc in ("EK", "OC") and zone in ("best-few", "in"):
            ctx.warn("BS013", "Economic Buyer %s is %s: that is a timing problem, not a supporter. Change the mode or change the forecast" % (r.get("name", ""), "Even Keel" if mc == "EK" else "Overconfident"))

    # --- win-results
    wr_by_name = {}
    for r in wr:
        wr_by_name[r.get("name", "").strip().lower()] = r
    for name in sorted(named_people):
        row = wr_by_name.get(name)
        if row is None:
            ctx.warn("BS006", "%s: no Win-Results row" % name.title())
            continue
        if is_unknown(row.get("business_result", "")):
            ctx.warn("BS006", "%s: business result unknown (acceptable, but needs a question that reveals it)" % name.title())
        if is_unknown(row.get("personal_win", "")):
            ctx.warn("BS006", "%s: personal win is blank. If you cannot write it you have not had the conversation yet" % name.title())
        if is_unknown(row.get("evidence", "")) and is_unknown(row.get("source", "")):
            ctx.warn("BS014", "%s: Win-Results have no evidence or source (mark F/I/A/U and cite)" % name.title())

    # --- competition
    if not comp:
        ctx.warn("BS018", "competition table is empty")
    else:
        text = " ".join(" ".join(r.values()) for r in comp).lower()
        if not re.search(r"status quo|do nothing|no decision", text):
            ctx.err("BS018", "competition must include Status quo / do nothing")

    # --- red flags and actions
    rf_ids = []
    for r in rf:
        rid = r.get("id", "")
        if is_blank(rid):
            ctx.warn("BS007", "red flag %r has no ID (use RF-1, RF-2...) so actions can link to it" % (r.get("red_flag", "")[:50]))
        else:
            rf_ids.append(_norm_id(rid, "RF"))
    linked = set()
    for a in acts:
        for cell_key in ("targets_red_flag", "red_flag", "linked_red_flag", "red_flags", "targets"):
            if cell_key in a:
                for x in _ids(a[cell_key], "RF"):
                    linked.add(_norm_id(x, "RF"))
    for rid in rf_ids:
        if rid not in linked:
            ctx.err("BS007", "%s has no action. Every red flag needs at least one action with an owner and a date" % rid)
    stats["red_flags_unlinked"] = len([r for r in rf_ids if r not in linked])
    for a in acts:
        label = a.get("id", "") or a.get("action", "")[:40]
        if is_unknown(a.get("owner", "")):
            ctx.err("BS008", "action %s has no owner" % label)
        d = parse_date(a.get("due", ""))
        if d is None:
            ctx.err("BS008", "action %s has no ISO due date (YYYY-MM-DD)" % label)
        elif active and d < ctx.today and a.get("status", "").strip().lower() not in ("done", "complete", "completed", "cancelled", "canceled"):
            ctx.warn("BS009", "action %s is past due (%s)" % (label, d.isoformat()))

    if active and rf and not acts:
        ctx.err("BS007", "red flags exist but the action plan is empty")
    if active and not rf:
        ctx.warn("BS007", "no red flags recorded. A complex deal with zero red flags is usually a deal not yet understood")

    # BAC / MAA
    low = body.lower()
    if "best action commitment" not in low or "minimum acceptable action" not in low:
        ctx.warn("BS020", "action plan should state the Best Action Commitment and the Minimum Acceptable Action for the next interaction")

    # staleness
    lr = parse_date(fm.get("last_reviewed"))
    if lr is None:
        ctx.err("BS010", "last_reviewed missing or not an ISO date")
    elif active:
        limit = ctx.best_few_stale_days if zone == "best-few" else ctx.stale_days
        age = (ctx.today - lr).days
        stats["days_since_review"] = age
        if age > limit:
            ctx.warn("BS010", "stale: last reviewed %d days ago (limit %d for %s)" % (age, limit, zone or "this zone"))
    return stats


# -------------------------------------------------------------------------- green
def _list_items(text: Optional[str]) -> List[str]:
    if not text:
        return []
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    items = []
    for line in text.splitlines():
        m = re.match(r"^\s*(?:\d+[.)]|[-*])\s+(.*\S)\s*$", line)
        if m and not is_blank(m.group(1)) and not m.group(1).strip().startswith(">"):
            items.append(m.group(1))
    return items


def lint_green(fm: Dict, body: str, ctx: LintContext) -> Dict:
    for key in ("account", "participant", "meeting_date", "linked_blue_sheet", "owner"):
        if is_blank(str(fm.get(key, ""))):
            ctx.err("GS001", "frontmatter `%s` is missing or a placeholder" % key)
    stats = {}
    bac = re.search(r"best action commitment[^\n]*?:\**[ \t]*([^\n]*)", body, re.IGNORECASE)
    maa = re.search(r"minimum acceptable action[^\n]*?:\**[ \t]*([^\n]*)", body, re.IGNORECASE)
    if not bac or is_blank(bac.group(1).strip("* ")):
        ctx.err("GS002", "Best Action Commitment is empty. A call without it is a visit")
    if not maa or is_blank(maa.group(1).strip("* ")):
        ctx.err("GS002", "Minimum Acceptable Action is empty")
    counts = {}
    for label, pat, minimum in (
        ("confirmation", r"confirmation questions", 1),
        ("new information", r"new information questions", 2),
        ("attitude", r"attitude questions", 1),
        ("commitment", r"commitment questions", 1),
    ):
        items = _list_items(section_text(body, pat))
        counts[label] = len(items)
        if len(items) < minimum:
            ctx.warn("GS003", "needs at least %d %s question(s), found %d" % (minimum, label, len(items)))
    stats["questions"] = counts
    concept_rows = _rows(parse_tables(body), r"buyer.?s concept")
    if not concept_rows:
        ctx.warn("GS004", "no Buyer's Concept hypothesis recorded. State it (even as an assumption) so the call can test it")
    md = parse_date(fm.get("meeting_date"))
    if md and str(fm.get("status", "planned")).lower() == "planned" and md < ctx.today:
        ctx.warn("GS005", "meeting_date %s has passed but status is still planned: run the debrief and update the Blue Sheet" % md.isoformat())
    return stats


# --------------------------------------------------------------------------- gold
def _meaningful(text: Optional[str]) -> str:
    if not text:
        return ""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = [l for l in text.splitlines() if l.strip() and not l.strip().startswith(">") and not l.strip().startswith("|") and not l.strip().startswith("#")]
    joined = " ".join(lines).strip()
    return "" if is_blank(joined) else joined


def lint_gold(fm: Dict, body: str, ctx: LintContext) -> Dict:
    for key in ("account", "field_of_play", "owner", "last_reviewed", "next_review"):
        if is_blank(str(fm.get(key, ""))):
            ctx.err("AS001", "frontmatter `%s` is missing or a placeholder" % key)
    stats = {}
    tables = parse_tables(body)
    players = [r for r in _rows(tables, r"strategic players") if "strategic_role" in r or "role" in r]
    named = [r for r in players if not is_unknown(r.get("name", ""))]
    # roles only count when a real person fills them (the template pre-fills role labels)
    roles = [(r.get("strategic_role", "") or r.get("role", "")).lower() for r in named]
    stats["players"] = len(named)
    if not any("sponsor" in x and "anti" not in x for x in roles):
        ctx.err("AS002", "no Sponsor identified. At least one Strategic Player must promote your relationship and counter competitors")
    if not any("coach" in x for x in roles):
        ctx.warn("AS003", "no Strategic Coach identified")
    if not any("anti" in x for x in roles) and "none identified" not in body.lower():
        ctx.warn("AS004", "no Anti-Sponsor recorded. If there is none, say 'None identified' and how you checked")
    if len(named) == 1:
        ctx.warn("AS005", "single-threaded: one named Strategic Player")

    if not _meaningful(section_text(body, r"critical vulnerability")):
        ctx.err("AS006", "Critical Vulnerability is blank. Name the weakness that would cripple your position if left unaddressed")
    if not _meaningful(section_text(body, r"charter statement")):
        ctx.err("AS007", "Charter Statement is blank")
    bsh = _rows(tables, r"buy-?sell hierarchy")
    levels = [support_value(r.get("level", "")) for r in bsh]
    if len(bsh) < 2 or any(v is None or v < 1 or v > 5 for v in levels):
        ctx.warn("AS008", "Buy-Sell Hierarchy needs a current and a desired level (1-5), from the customer's view and ours")
    inv = _rows(tables, r"investments?")
    kinds = " ".join((r.get("decision", "") or r.get("focus_stop", "")).lower() for r in inv)
    if "focus" not in kinds or "stop" not in kinds:
        ctx.err("AS009", "needs at least one Focus investment and one Stop investment. A plan with only things to do is a task list")
    if not _rows(tables, r"revenue targets?"):
        ctx.warn("AS010", "no revenue targets recorded")
    if not re.search(r"blue[-_ ]sheet|\.md", section_text(body, r"single sales objectives?") or "", re.IGNORECASE):
        ctx.warn("AS011", "no Single Sales Objectives linked to Blue Sheets")
    nr = parse_date(fm.get("next_review"))
    lr = parse_date(fm.get("last_reviewed"))
    if lr and (ctx.today - lr).days > 90:
        ctx.warn("AS012", "last reviewed %d days ago; LAMP plans are reviewed every 60-90 days" % (ctx.today - lr).days)
    if nr and nr < ctx.today:
        ctx.warn("AS012", "next_review %s has passed" % nr.isoformat())
    return stats


# -------------------------------------------------------------------------- entry
def lint_text(path: str, text: str, today: Optional[dt.date] = None, stale_days: int = 14,
              best_few_stale_days: int = 7) -> Tuple[List[Issue], Dict, Dict]:
    today = today or dt.date.today()
    ctx = LintContext(path, today, stale_days, best_few_stale_days)
    fm, body, fm_err = split_frontmatter(text)
    if fm_err:
        ctx.err("SH001", "frontmatter error: " + fm_err)
        return ctx.issues, fm, {}
    typ = str(fm.get("type", "")).lower()
    stats: Dict = {}
    if typ == "blue-sheet":
        stats = lint_blue(fm, body, ctx)
    elif typ == "green-sheet":
        stats = lint_green(fm, body, ctx)
    elif typ == "gold-sheet":
        stats = lint_gold(fm, body, ctx)
    else:
        ctx.err("SH002", "frontmatter `type` must be blue-sheet, green-sheet or gold-sheet (got %r)" % typ)
    return ctx.issues, fm, stats


def lint_file(path: str, **kw) -> Tuple[List[Issue], Dict, Dict]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        return [Issue("error", "SH000", path, "cannot read file (%s). On Google Drive this usually means the file is cloud-only: set the folder to Available offline" % e)], {}, {}
    return lint_text(path, text, **kw)
