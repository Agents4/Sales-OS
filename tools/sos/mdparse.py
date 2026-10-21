"""Tiny Markdown + frontmatter helpers (no third-party dependencies).

Frontmatter support is intentionally a YAML *subset*:
  - top-level `key: value` scalars (quotes optional)
  - one level of nesting: `key:` followed by indented `sub: value` lines
  - inline lists: `key: [a, b, c]`
That is all the Agent Skills spec and our sheet schemas need.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

FM_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        inner = v[1:-1]
        if v[0] == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner
    return v


def _scalar(v: str) -> Any:
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_unquote(x) for x in _split_csv(inner)]
    return _unquote(v)


def _split_csv(s: str) -> List[str]:
    out, cur, q = [], [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur.append(ch)
        elif ch == ",":
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur).strip())
    return out


def split_frontmatter(text: str) -> Tuple[Dict[str, Any], str, Optional[str]]:
    """Return (frontmatter dict, body, error)."""
    m = FM_RE.match(text)
    if not m:
        return {}, text, None
    raw = m.group(1)
    body = text[m.end():]
    fm: Dict[str, Any] = {}
    current: Optional[str] = None
    for i, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line[:1] in (" ", "\t")
        if indented:
            if current is None or not isinstance(fm.get(current), dict):
                return fm, body, "line %d: unexpected indentation" % i
            if ":" not in line:
                return fm, body, "line %d: expected `key: value`" % i
            k, _, v = line.strip().partition(":")
            fm[current][k.strip()] = _scalar(v)
            continue
        if ":" not in line:
            return fm, body, "line %d: expected `key: value`" % i
        k, _, v = line.partition(":")
        k = k.strip()
        if v.strip() == "":
            fm[k] = {}
            current = k
        else:
            fm[k] = _scalar(v)
            current = None
    # collapse empty maps that never got children into ""
    for k, v in list(fm.items()):
        if v == {}:
            fm[k] = ""
    return fm, body, None


def norm(s: str) -> str:
    """Normalise a table header or label to snake_case."""
    s = re.sub(r"\(.*?\)", "", s)  # drop parentheticals
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.strip().lower())
    return s.strip("_")


class Table(object):
    def __init__(self, heading: str, header: List[str], rows: List[Dict[str, str]], line: int):
        self.heading = heading
        self.header = header
        self.rows = rows
        self.line = line

    def __repr__(self) -> str:  # pragma: no cover
        return "<Table %r %d rows>" % (self.heading, len(self.rows))


def _split_row(line: str) -> List[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    line = line.replace("\\|", "\u0000")
    return [c.replace("\u0000", "|").strip() for c in line.split("|")]


SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def parse_tables(body: str) -> List[Table]:
    lines = body.splitlines()
    tables: List[Table] = []
    heading = ""
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        hm = HEAD_RE.match(line)
        if hm:
            heading = hm.group(2).strip()
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]) and "|" in lines[i + 1]:
            header_raw = _split_row(line)
            header = [norm(h) for h in header_raw]
            rows: List[Dict[str, str]] = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = _split_row(lines[j])
                while len(cells) < len(header):
                    cells.append("")
                rows.append(dict(zip(header, cells[: len(header)])))
                j += 1
            tables.append(Table(heading, header, rows, i + 1))
            i = j
            continue
        i += 1
    return tables


def find_tables(tables: List[Table], heading_pattern: str) -> List[Table]:
    rx = re.compile(heading_pattern, re.IGNORECASE)
    return [t for t in tables if rx.search(t.heading)]


def section_text(body: str, heading_pattern: str) -> Optional[str]:
    """Return the text under the first heading matching the pattern (until next heading of same/higher level)."""
    rx = re.compile(heading_pattern, re.IGNORECASE)
    lines = body.splitlines()
    start = None
    level = 0
    in_fence = False
    for idx, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        hm = HEAD_RE.match(line)
        if hm and start is None and rx.search(hm.group(2)):
            start = idx + 1
            level = len(hm.group(1))
            continue
        if hm and start is not None and len(hm.group(1)) <= level:
            return "\n".join(lines[start:idx])
    if start is not None:
        return "\n".join(lines[start:])
    return None


PLACEHOLDER_RE = re.compile(r"^(?:<[^>]*>|\[[^\]]*\]|\.\.\.|…|tbd|n/?a|-|—|–)?$", re.IGNORECASE)


def is_blank(v: Optional[str]) -> bool:
    """True if a cell is empty or an unfilled placeholder like <name> or [..]."""
    if v is None:
        return True
    v = v.strip()
    return bool(PLACEHOLDER_RE.match(v))


def row_is_empty(row: Dict[str, str]) -> bool:
    return all(is_blank(v) for v in row.values())


def is_unknown(v: Optional[str]) -> bool:
    if v is None:
        return True
    s = v.strip().lower()
    return s in ("", "unknown", "unk", "u", "tbd", "?", "none identified", "not identified", "n/a") or is_blank(v)
