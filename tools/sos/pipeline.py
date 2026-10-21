"""Portfolio view across all Blue Sheets: freshness, coverage, unlinked red flags.

Reads `workspace/accounts/*/deals/*/blue-sheet.md` (and any `blue-sheet*.md`
under workspace/accounts) and prints Markdown or CSV (paste into Google Sheets).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import re
from typing import Dict, List, Optional

from .lint import lint_file
from .skills import Issue


def find_blue_sheets(root: str) -> List[str]:
    base = os.path.join(root, "workspace", "accounts")
    out = []
    if not os.path.isdir(base):
        return out
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if re.match(r"^blue-sheet.*\.md$", f, re.IGNORECASE):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def parse_amount(s: object) -> float:
    m = re.search(r"([\d][\d,]*\.?\d*)\s*([kKmM])?", str(s or ""))
    if not m:
        return 0.0
    try:
        v = float(m.group(1).replace(",", ""))
    except ValueError:
        return 0.0
    mult = {"k": 1e3, "m": 1e6}.get((m.group(2) or "").lower(), 1)
    return v * mult


def collect(root: str, today: dt.date, stale_days: int = 14, best_few_stale_days: int = 7,
            paths: Optional[List[str]] = None) -> List[Dict]:
    rows: List[Dict] = []
    for p in (paths if paths is not None else find_blue_sheets(root)):
        issues, fm, stats = lint_file(p, today=today, stale_days=stale_days, best_few_stale_days=best_few_stale_days)
        errs = [i for i in issues if i.level == "error"]
        warns = [i for i in issues if i.level == "warn"]
        top = (errs + warns)[0] if (errs or warns) else None
        rows.append({
            "account": fm.get("account", ""),
            "opportunity": fm.get("opportunity", ""),
            "owner": fm.get("owner", ""),
            "amount": fm.get("amount", ""),
            "amount_num": parse_amount(fm.get("amount", "")),
            "close_date": fm.get("close_date", ""),
            "zone": fm.get("funnel_zone", ""),
            "status": fm.get("status", ""),
            "position": fm.get("position", ""),
            "days_since_review": stats.get("days_since_review", ""),
            "named_people": stats.get("named_people", 0),
            "eb": "named" if stats.get("eb_named", 0) == 1 else ("CONFLICT" if stats.get("eb_named", 0) > 1 else "UNKNOWN"),
            "coach": "named" if stats.get("coach_named", 0) else "UNKNOWN",
            "red_flags": stats.get("red_flags", 0),
            "red_flags_unlinked": stats.get("red_flags_unlinked", 0),
            "errors": len(errs),
            "warns": len(warns),
            "top_issue": ("%s %s" % (top.code, top.msg)) if top else "",
            "risk": 3 * len(errs) + len(warns),
            "path": os.path.relpath(p, root),
            "issues": issues,
        })
    rows.sort(key=lambda r: (-r["risk"], str(r["account"])))
    return rows


def render_markdown(rows: List[Dict], today: dt.date) -> str:
    active = [r for r in rows if str(r["status"]).lower() in ("active", "")]
    by_zone: Dict[str, List[Dict]] = {}
    for r in active:
        by_zone.setdefault(str(r["zone"]) or "unset", []).append(r)
    out = io.StringIO()
    w = out.write
    w("---\ntype: pipeline-report\ndate: %s\nsheets_scanned: %d\n---\n\n" % (today.isoformat(), len(rows)))
    w("# Pipeline hygiene report, %s\n\n" % today.isoformat())
    if not rows:
        w("No Blue Sheets found under `workspace/accounts/`. Create one with the `mh-blue-sheet` skill.\n")
        return out.getvalue()
    w("## Portfolio\n\n| Zone | Active deals | Value |\n|---|---|---|\n")
    for z in ("best-few", "in", "above", "unset"):
        if z in by_zone:
            w("| %s | %d | %s |\n" % (z, len(by_zone[z]), "{:,.0f}".format(sum(x["amount_num"] for x in by_zone[z]))))
    w("\n## Needs attention\n\n")
    flagged = [r for r in active if r["risk"] > 0]
    if not flagged:
        w("Nothing flagged. Spot check one sheet by hand anyway.\n")
    for r in flagged[:15]:
        w("- **%s / %s** (%s, %s): %d error(s), %d warning(s). %s\n" % (
            r["account"], r["opportunity"], r["owner"], r["zone"] or "zone?", r["errors"], r["warns"], r["top_issue"]))
    w("\n## All sheets\n\n")
    w("| Account | Opportunity | Owner | Zone | Amount | Close | Days since review | EB | Coach | Red flags (unlinked) | Err | Warn | File |\n")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        w("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s (%s) | %d | %d | `%s` |\n" % (
            r["account"], r["opportunity"], r["owner"], r["zone"], r["amount"], r["close_date"],
            r["days_since_review"], r["eb"], r["coach"], r["red_flags"], r["red_flags_unlinked"],
            r["errors"], r["warns"], r["path"]))
    codes: Dict[str, int] = {}
    for r in rows:
        for i in r["issues"]:
            codes[i.code] = codes.get(i.code, 0) + 1
    if codes:
        w("\n## Most common findings\n\n| Code | Count |\n|---|---|\n")
        for c, n in sorted(codes.items(), key=lambda kv: -kv[1])[:10]:
            w("| %s | %d |\n" % (c, n))
    w("\n> Generated by `tools/sos.py pipeline`. Findings are prompts to re-walk the sheet, not a forecast.\n")
    return out.getvalue()


def render_csv(rows: List[Dict]) -> str:
    cols = ["account", "opportunity", "owner", "amount", "close_date", "zone", "status", "position", "days_since_review",
            "named_people", "eb", "coach", "red_flags", "red_flags_unlinked", "errors", "warns", "top_issue", "path"]
    buf = io.StringIO()
    wr = csv.writer(buf)
    wr.writerow(cols)
    for r in rows:
        wr.writerow([r.get(c, "") for c in cols])
    return buf.getvalue()
