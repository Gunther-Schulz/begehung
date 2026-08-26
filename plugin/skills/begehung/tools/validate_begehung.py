#!/usr/bin/env python3
"""Structural validator for a begehung findings TSV or MAP.md.

Reads plugin/skills/begehung/templates/schema.json at runtime for every
column order and vocabulary it checks against — nothing here restates a
schema value as a literal. A restated copy beside the parser it mirrors
cannot age loudly: the source gains a member and the copy stays green.

Usage:
    validate_begehung.py findings <path> [--grades a,b,c] [--schema PATH]
    validate_begehung.py map <path> [--schema PATH]

`--schema` defaults to ../templates/schema.json resolved relative to
THIS FILE, never the current working directory.

Absence rule: whatever this validator cannot read — a missing column,
a table it cannot find, a cell it cannot classify — is reported as
UNVERIFIED, never as a pass. A file that does not exist or does not
parse exits 2, distinct from a validation failure (exit 1).

Reach, stated: this checks STRUCTURE — column orders, vocabulary
membership, presence of required rows and marks. It does not judge
whether a finding is well-reasoned or a MAP row's status is honest;
only a human reading the content does that.

Exit 0 = every non-advisory check passed. Exit 1 = at least one
check failed. Exit 2 = a named input could not be read or parsed.
"""
import argparse
import json
import re
import sys
from pathlib import Path

STATUS_WIDTH = 10  # widest token below is "UNVERIFIED" (10 chars)


def status_line(status: str, label: str) -> None:
    print(f"  [{status:>{STATUS_WIDTH}}] {label}")


def detail(msg: str) -> None:
    print(f"              {msg}")


class InputError(Exception):
    """A named input could not be read or parsed — exit 2."""


def load_schema(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"could not read schema {path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputError(f"schema {path} does not parse as JSON: {exc}") from exc


def read_raw(path: Path) -> str:
    """Read a file preserving its exact line-ending bytes (newline='')."""
    try:
        return path.read_text(encoding="utf-8", newline="")
    except OSError as exc:
        raise InputError(f"could not read {path}: {exc}") from exc


# ---------------------------------------------------------------------------
# TSV parsing
# ---------------------------------------------------------------------------

def parse_tsv(raw: str):
    """Split on literal '\\n' only, so a lone embedded '\\r' inside a cell
    (not part of a trailing CRLF) survives into the cell instead of being
    silently absorbed as a line break by str.splitlines(). Returns
    (rows, newline_hits) where rows is a list of list-of-cells (CRLF
    trailing '\\r' stripped) and newline_hits is [(row_idx, col_idx), ...]
    for any cell that still carries an embedded '\\r' after that strip —
    the only newline shape this row-splitting scheme can detect, since a
    raw '\\n' cannot survive inside a cell by construction (it IS the row
    separator here).
    """
    pieces = raw.split("\n")
    # A trailing '' from a final '\n' is not a row.
    if pieces and pieces[-1] == "":
        pieces = pieces[:-1]
    rows = []
    newline_hits = []
    for r_idx, piece in enumerate(pieces):
        if piece.endswith("\r"):
            piece = piece[:-1]
        cells = piece.split("\t")
        for c_idx, cell in enumerate(cells):
            if "\r" in cell or "\n" in cell:
                newline_hits.append((r_idx, c_idx))
        rows.append(cells)
    return rows, newline_hits


# ---------------------------------------------------------------------------
# Markdown pipe-table parsing
# ---------------------------------------------------------------------------

def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and len(s) >= 2


def _is_separator_row(line: str) -> bool:
    s = line.strip()
    if not _is_table_row(s):
        return False
    inner = s[1:-1]
    cells = inner.split("|")
    if not cells:
        return False
    return all(re.fullmatch(r"\s*:?-{1,}:?\s*", c) for c in cells)


def _split_row(line: str):
    s = line.strip()
    inner = s[1:-1] if _is_table_row(s) else s
    return [c.strip() for c in inner.split("|")]


def parse_markdown_tables(text: str):
    lines = text.splitlines()
    tables = []
    i = 0
    n = len(lines)
    while i < n:
        if _is_table_row(lines[i]) and i + 1 < n and _is_separator_row(lines[i + 1]):
            header = _split_row(lines[i])
            j = i + 2
            rows = []
            while j < n and _is_table_row(lines[j]):
                rows.append(_split_row(lines[j]))
                j += 1
            tables.append({"header": header, "rows": rows, "line": i + 1})
            i = j
        else:
            i += 1
    return tables


def find_table_with_header(tables, expected_header):
    for t in tables:
        if t["header"] == expected_header:
            return t
    return None


# ---------------------------------------------------------------------------
# Findings-cell parsing helpers
# ---------------------------------------------------------------------------

def strip_ready_to_land(cell: str, mark: str):
    """Returns (has_mark, remainder) — remainder has the mark and any
    leading '·'/whitespace separator stripped, then stripped itself."""
    s = cell.strip()
    if s.startswith(mark):
        rest = s[len(mark):].lstrip()
        while rest.startswith("·"):
            rest = rest[1:].lstrip()
        return True, rest.strip()
    return False, s


def strip_superseded(cell: str, mark: str):
    """Returns (has_mark, ref_or_None, remainder)."""
    s = cell.strip()
    pattern = re.escape(mark) + r"\s+([^:]+):\s*"
    m = re.match(pattern, s)
    if m:
        return True, m.group(1).strip(), s[m.end():].strip()
    return False, None, s


def classify_basis_remainder(remainder: str, labels):
    if not remainder:
        return "empty"
    for lbl in labels:
        if remainder == lbl or (
            remainder.startswith(lbl)
            and (len(remainder) == len(lbl) or not remainder[len(lbl)].isalnum())
        ):
            return f"label:{lbl}"
    return "executed"


def leading_token(cell: str):
    s = cell.strip()
    if not s:
        return "", ""
    m = re.match(r"^(\S+)(.*)$", s, re.DOTALL)
    return m.group(1), m.group(2).strip()


# ---------------------------------------------------------------------------
# findings subcommand
# ---------------------------------------------------------------------------

def run_findings(path: Path, schema: dict, grades_override) -> int:
    findings_schema = schema.get("findings", {})
    schema_cols = findings_schema.get("columns", [])
    vocab = findings_schema.get("vocabularies", {})
    grade_vocab = grades_override if grades_override is not None else vocab.get("grade", [])
    disposition_vocab = vocab.get("disposition", [])
    basis_labels = vocab.get("basis_labels", [])
    marks = findings_schema.get("marks", {})
    ready_mark = marks.get("ready_to_land", "ready-to-land")
    superseded_mark = marks.get("superseded", "superseded-by")

    raw = read_raw(path)
    rows, newline_hits = parse_tsv(raw)
    if not rows:
        raise InputError(f"{path} has no rows at all (not even a header)")

    header = rows[0]
    data_rows = rows[1:]

    failed = False

    # Check 1: header
    n = len(schema_cols)
    if len(header) >= n and header[:n] == schema_cols:
        extra = header[n:]
        status_line("OK", f"check 1: header matches schema columns ({n} columns)")
        if extra:
            detail(f"{len(extra)} extra trailing column(s): {extra}")
        else:
            detail("no extra columns")
    else:
        failed = True
        status_line("FAIL", "check 1: header does not equal schema findings.columns")
        detail(f"expected (prefix): {schema_cols}")
        detail(f"actual header     : {header}")

    col_index = {}
    for col in schema_cols:
        col_index[col] = header.index(col) if col in header else None
        if col_index[col] is None:
            detail(f"column {col!r} not found in header — dependent checks UNVERIFIED")

    # Check 2: row length
    short_rows = [i for i, r in enumerate(data_rows) if len(r) < len(header)]
    if short_rows:
        failed = True
        status_line("FAIL", "check 2: every data row has at least as many cells as header")
        detail(f"{len(short_rows)} short row(s), 0-indexed data rows: {short_rows[:20]}")
    else:
        status_line("OK", f"check 2: all {len(data_rows)} data row(s) have >= {len(header)} cells")

    # Check 3: no newline inside a cell
    if newline_hits:
        failed = True
        status_line("FAIL", "check 3: no cell contains a newline")
        for r_idx, c_idx in newline_hits[:20]:
            detail(f"row {r_idx} (0=header), cell {c_idx}: embedded CR/LF")
    else:
        status_line("OK", "check 3: no cell contains an embedded newline")

    # Check 4: lens non-empty
    if col_index.get("lens") is None:
        status_line("UNVERIFIED", "check 4: lens non-empty — 'lens' column not found")
    else:
        idx = col_index["lens"]
        empties = [i for i, r in enumerate(data_rows) if idx >= len(r) or not r[idx].strip()]
        if empties:
            failed = True
            status_line("FAIL", "check 4: lens non-empty on every row")
            detail(f"empty on data row(s): {empties[:20]}")
        else:
            status_line("OK", f"check 4: lens non-empty on all {len(data_rows)} row(s)")

    # Check 5: grade in vocabulary
    if col_index.get("grade") is None:
        status_line("UNVERIFIED", "check 5: grade in vocabulary — 'grade' column not found")
    else:
        idx = col_index["grade"]
        bad = []
        for i, r in enumerate(data_rows):
            val = r[idx].strip() if idx < len(r) else ""
            if val not in grade_vocab:
                bad.append((i, val))
        if bad:
            failed = True
            status_line("FAIL", f"check 5: grade in vocabulary {grade_vocab}")
            for i, val in bad[:20]:
                detail(f"data row {i}: grade={val!r}")
        else:
            status_line("OK", f"check 5: all grades in {grade_vocab}")

    # Check 6: disposition non-empty and (post-mark-strip) in vocabulary
    disp_stripped = {}
    if col_index.get("disposition") is None:
        status_line("UNVERIFIED", "check 6: disposition — 'disposition' column not found")
    else:
        idx = col_index["disposition"]
        bad = []
        for i, r in enumerate(data_rows):
            cell = r[idx] if idx < len(r) else ""
            has_mark, remainder = strip_ready_to_land(cell, ready_mark)
            disp_stripped[i] = (has_mark, remainder)
            if not cell.strip() or remainder not in disposition_vocab:
                bad.append((i, cell, remainder))
        if bad:
            failed = True
            status_line(
                "FAIL",
                f"check 6: disposition non-empty and in vocabulary {disposition_vocab} "
                "(after stripping a leading ready-to-land mark)",
            )
            for i, cell, remainder in bad[:20]:
                detail(f"data row {i}: raw={cell!r} -> stripped={remainder!r}")
        else:
            status_line("OK", f"check 6: disposition valid on all {len(data_rows)} row(s)")

    # Check 7: basis non-empty; label vs executed
    basis_info = {}
    if col_index.get("basis") is None:
        status_line("UNVERIFIED", "check 7: basis — 'basis' column not found")
    else:
        idx = col_index["basis"]
        bad = []
        label_rows = []
        executed_rows = []
        for i, r in enumerate(data_rows):
            cell = r[idx] if idx < len(r) else ""
            has_super, ref, remainder = strip_superseded(cell, superseded_mark)
            basis_info[i] = (has_super, ref, remainder)
            kind = classify_basis_remainder(remainder, basis_labels)
            if not cell.strip() or kind == "empty":
                bad.append((i, cell))
            elif kind.startswith("label:"):
                label_rows.append((i, kind[6:]))
            else:
                executed_rows.append(i)
        if bad:
            failed = True
            status_line("FAIL", "check 7: basis non-empty (after optional superseded-by strip)")
            for i, cell in bad[:20]:
                detail(f"data row {i}: raw={cell!r}")
        else:
            status_line("OK", f"check 7: basis non-empty on all {len(data_rows)} row(s)")
        detail(f"{len(label_rows)} row(s) carry a basis_labels label: {label_rows[:20]}")
        detail(f"{len(executed_rows)} row(s) carry an executed basis: {executed_rows[:20]}")

    # Check 8: cross-cell — superseded rows are prose-rest, no ready-to-land
    if col_index.get("basis") is None or col_index.get("disposition") is None:
        status_line(
            "UNVERIFIED",
            "check 8: superseded rows are prose-rest with no ready-to-land mark "
            "— basis and/or disposition column not found",
        )
    else:
        bad = []
        for i in range(len(data_rows)):
            has_super = basis_info.get(i, (False, None, ""))[0]
            if not has_super:
                continue
            has_mark, remainder = disp_stripped.get(i, (False, ""))
            if has_mark or remainder != "prose-rest":
                bad.append((i, has_mark, remainder))
        if bad:
            failed = True
            status_line(
                "FAIL",
                "check 8: a superseded-by row's disposition must be exactly "
                "'prose-rest' and carry no ready-to-land mark",
            )
            for i, has_mark, remainder in bad[:20]:
                detail(
                    f"data row {i}: ready-to-land present={has_mark}, "
                    f"disposition={remainder!r}"
                )
        else:
            n_super = sum(1 for i in range(len(data_rows)) if basis_info.get(i, (False,))[0])
            status_line("OK", f"check 8: {n_super} superseded-by row(s), all prose-rest/no-mark")

    # Check 9: counts — always printed
    status_line("OK", "check 9: counts (informational, always printed)")
    detail(f"total data rows: {len(data_rows)}")
    if col_index.get("grade") is not None:
        idx = col_index["grade"]
        counts = {}
        for r in data_rows:
            val = r[idx].strip() if idx < len(r) else ""
            counts[val] = counts.get(val, 0) + 1
        detail(f"count per grade: {counts}")
    else:
        detail("count per grade: UNVERIFIED — 'grade' column not found")
    if col_index.get("lens") is not None:
        idx = col_index["lens"]
        counts = {}
        for r in data_rows:
            val = r[idx].strip() if idx < len(r) else ""
            counts[val] = counts.get(val, 0) + 1
        detail(f"count per lens: {counts}")
    else:
        detail("count per lens: UNVERIFIED — 'lens' column not found")

    return 1 if failed else 0


# ---------------------------------------------------------------------------
# map subcommand
# ---------------------------------------------------------------------------

def run_map(path: Path, schema: dict) -> int:
    map_schema = schema.get("map", {})
    axis_cols = map_schema.get("axis_columns", [])
    round_cols = map_schema.get("round_columns", [])
    status_vocab = map_schema.get("vocabularies", {}).get("status", [])

    text = read_raw(path)
    tables = parse_markdown_tables(text)

    failed = False

    axis_table = find_table_with_header(tables, axis_cols)
    if axis_table is None:
        failed = True
        status_line("FAIL", "check 1: an axis table is present whose header equals map.axis_columns")
        detail(f"expected header: {axis_cols}")
        detail(f"tables found (headers): {[t['header'] for t in tables]}")
    else:
        status_line("OK", f"check 1: axis table found at line {axis_table['line']}")

    round_table = find_table_with_header(tables, round_cols)
    if round_table is None:
        failed = True
        status_line("FAIL", "check 2: a round table is present whose header equals map.round_columns")
        detail(f"expected header: {round_cols}")
        detail(f"tables found (headers): {[t['header'] for t in tables]}")
    else:
        status_line("OK", f"check 2: round table found at line {round_table['line']}")

    # Check 3 & 4: status vocabulary + dark rows carry a label/pointer
    if axis_table is None:
        status_line("UNVERIFIED", "check 3: status cell vocabulary — axis table not found")
        status_line("UNVERIFIED", "check 4: dark rows carry a label or pointer — axis table not found")
    else:
        status_idx = axis_table["header"].index("status")
        bad_vocab = []
        bad_dark = []
        dark_count = 0
        for i, row in enumerate(axis_table["rows"]):
            cell = row[status_idx] if status_idx < len(row) else ""
            token, rest = leading_token(cell)
            if token not in status_vocab:
                bad_vocab.append((i, cell))
                continue
            if token == "dark":
                dark_count += 1
                if not rest:
                    bad_dark.append((i, cell))
        if bad_vocab:
            failed = True
            status_line("FAIL", f"check 3: every axis-row status cell in {status_vocab}")
            for i, cell in bad_vocab[:20]:
                detail(f"axis row {i}: status={cell!r}")
        else:
            status_line("OK", f"check 3: all {len(axis_table['rows'])} axis-row status cell(s) valid")

        if bad_dark:
            failed = True
            status_line("FAIL", "check 4: every 'dark' status cell carries 'modelled' or a pointer")
            for i, cell in bad_dark[:20]:
                detail(f"axis row {i}: status={cell!r} — no label/pointer after 'dark'")
        else:
            status_line("OK", f"check 4: all {dark_count} dark row(s) carry a label or pointer")

    # Check 5: cross-cutting row present
    if axis_table is None:
        status_line("UNVERIFIED", "check 5: cross-cutting row present — axis table not found")
    else:
        axis_idx = axis_table["header"].index("axis (what against what)") \
            if "axis (what against what)" in axis_table["header"] else 0
        found = any(
            "cross-cutting" in (row[axis_idx] if axis_idx < len(row) else "").lower()
            for row in axis_table["rows"]
        )
        if found:
            status_line("OK", "check 5: cross-cutting row present")
        else:
            failed = True
            status_line("FAIL", "check 5: cross-cutting row present")
            detail("no axis cell contains 'CROSS-CUTTING' (case-insensitive)")

    # Check 6: enforcer row — ADVISORY, never fails exit code
    if axis_table is None:
        status_line("UNVERIFIED", "check 6: enforcer row present — axis table not found (advisory)")
    else:
        axis_idx = axis_table["header"].index("axis (what against what)") \
            if "axis (what against what)" in axis_table["header"] else 0
        found = any(
            "enforcer" in (row[axis_idx] if axis_idx < len(row) else "").lower()
            for row in axis_table["rows"]
        )
        status_line(
            "ADVISORY",
            f"check 6: enforcer row {'present' if found else 'absent'} — owed only where "
            "this system's surfaces emit verdicts about other work, a judgment this "
            "checker cannot make; never affects exit code",
        )

    # Check 7: at most one empty closed-at, and it is the last round row
    if round_table is None:
        status_line("UNVERIFIED", "check 7: at most one open round row, and it is last — round table not found")
    else:
        closed_idx = round_table["header"].index("closed-at")
        empties = [
            i for i, row in enumerate(round_table["rows"])
            if not (row[closed_idx].strip() if closed_idx < len(row) else "")
        ]
        n_rows = len(round_table["rows"])
        if len(empties) > 1:
            failed = True
            status_line("FAIL", "check 7: at most one round row has an empty closed-at")
            detail(f"empty closed-at at round-table row indices: {empties}")
        elif len(empties) == 1 and empties[0] != n_rows - 1:
            failed = True
            status_line("FAIL", "check 7: the one open round row must be the LAST round row")
            detail(f"open row index {empties[0]}, last index is {n_rows - 1}")
        else:
            status_line("OK", f"check 7: {len(empties)} open round row(s), position valid")

    return 1 if failed else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def default_schema_path() -> Path:
    return Path(__file__).resolve().parent.parent / "templates" / "schema.json"


def main() -> int:
    parser = argparse.ArgumentParser(prog="validate_begehung.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_find = sub.add_parser("findings")
    p_find.add_argument("path")
    p_find.add_argument("--grades", default=None, help="comma-separated grade vocabulary override")
    p_find.add_argument("--schema", default=None)

    p_map = sub.add_parser("map")
    p_map.add_argument("path")
    p_map.add_argument("--schema", default=None)

    args = parser.parse_args()

    schema_path = Path(args.schema) if args.schema else default_schema_path()

    try:
        schema = load_schema(schema_path)
        target = Path(args.path)
        if not target.exists():
            raise InputError(f"{target} does not exist")

        if args.command == "findings":
            grades_override = None
            if args.grades is not None:
                grades_override = [g.strip() for g in args.grades.split(",") if g.strip()]
            exit_code = run_findings(target, schema, grades_override)
        else:
            exit_code = run_map(target, schema)
    except InputError as exc:
        print(f"ERROR: {exc}")
        return 2

    print()
    if exit_code == 0:
        print("GREEN — all non-advisory checks passed")
    else:
        print("RED — one or more checks failed")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
