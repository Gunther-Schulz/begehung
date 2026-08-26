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
UNVERIFIED, never as a pass. That holds at the EXIT CODE too, which is
the only layer a script reads: any UNVERIFIED check exits 3 (AMBER)
even when nothing failed, because "could not verify" is not "clean".
Exit 0 clean · 1 a check failed · 2 a named input is missing or does
not parse · 3 nothing failed but something could not be verified.
ADVISORY results never move the exit code: they report a judgment this
tool cannot make rather than something it could not read.

Reach, stated: this checks STRUCTURE — column orders, vocabulary
membership, presence of required rows and marks. It does not judge
whether a finding is well-reasoned or a MAP row's status is honest;
only the walker reading the content does that.
"""
import argparse
import json
import re
import sys
from pathlib import Path

STATUS_WIDTH = 10  # widest token below is "UNVERIFIED" (10 chars)


_UNVERIFIED_COUNT = [0]


def status_line(status: str, label: str) -> None:
    """Print one check's result, and COUNT the could-not-verify ones.

    An UNVERIFIED check must not leave the process exiting 0. The text
    saying "could not verify" while the exit code says "pass" is the
    absence rule holding in the prose and breaking at the only layer a
    script reads: `validate && deploy` would treat a check that
    verified nothing as clean. ADVISORY is different by design — it
    reports a judgment this tool cannot make, so it never touches the
    exit code.
    """
    if status.strip().upper() == "UNVERIFIED":
        _UNVERIFIED_COUNT[0] += 1
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


def schema_row_token(map_section: dict, row_key: str):
    """The token an owed MAP row is RECOGNIZED by, from schema.json's
    map.required_rows.<row_key>.match. Returns None when the schema
    declares no usable token, so the caller degrades to UNVERIFIED
    rather than falling back to a spelling of its own.

    Recognizing a row by token is a real limitation, not an oversight:
    a faithfully-built row worded differently — another language, a
    house phrasing — is invisible to it, and a decoy row merely
    containing the token passes. Keeping the token in the schema is
    what makes that limitation a ONE-LINE repair for the system being
    walked, instead of a checker defect nobody can fix from outside.
    """
    entry = ((map_section.get("required_rows") or {}).get(row_key) or {})
    if not isinstance(entry, dict):
        return None
    token = entry.get("match")
    return token if isinstance(token, str) and token.strip() else None


def schema_role_value(section: dict, vocab_list, role_key: str):
    """The member of an UNORDERED schema vocabulary that a check must
    single out by MEANING — "the status meaning absence", "the
    disposition a superseded row takes". The caller names the ROLE
    (`role_key`); schema.json's `roles` map owns the spelling, so a
    renamed value is followed automatically and no second home for it
    exists in this file.

    Returns None — so the caller degrades LOUDLY to UNVERIFIED rather
    than matching nothing while reporting OK — in both failure
    directions, which are different bugs and both silent otherwise:
    the schema declares no such role, or it declares one whose value
    its own vocabulary no longer lists (a stale `roles` entry left
    behind by a rename that touched only the vocabulary).

    Unlike column names (schema_column_index, below), position carries
    no declared meaning in an unordered vocabulary, so nothing is
    derived positionally here.
    """
    value = (section.get("roles") or {}).get(role_key)
    if value is None or value not in vocab_list:
        return None
    return value


def schema_column_index(header, schema_columns, col_name: str):
    """Index of `col_name` in `header`, where `col_name` is drawn from
    `schema_columns` — the schema's own ordered column list, the single
    home for column layout. Returns None (never a guessed position)
    when the schema no longer declares that column, or the header
    (already schema-verified elsewhere, but re-checked here rather than
    assumed) does not carry it — the caller reports UNVERIFIED rather
    than crashing on `.index()` or silently defaulting to a position.
    """
    if col_name not in schema_columns or col_name not in header:
        return None
    return header.index(col_name)


# ---------------------------------------------------------------------------
# findings subcommand
# ---------------------------------------------------------------------------

def run_findings(path: Path, schema: dict, grades_override) -> int:
    findings_schema = schema.get("findings", {})
    schema_cols = findings_schema.get("columns", [])
    vocab = findings_schema.get("vocabularies", {})
    # N8: these two schema keys are READ, not assumed. An inert key inside
    # the file declared "the single home" reads as authority it does not have.
    overridable = vocab.get("grade_overridable", True)
    refused_override = grades_override is not None and not overridable
    if refused_override:
        status_line(
            "FAIL",
            "check 5: --grades was given, but schema.json sets "
            "findings.vocabularies.grade_overridable false — the schema "
            "forbids a per-run grade vocabulary here",
        )
        grade_vocab = vocab.get("grade", [])
        grades_override = None
    else:
        grade_vocab = grades_override if grades_override is not None else vocab.get("grade", [])
    disposition_vocab = vocab.get("disposition", [])
    basis_labels = vocab.get("basis_labels", [])
    marks = findings_schema.get("marks", {})
    ready_mark = marks.get("ready_to_land")
    superseded_mark = marks.get("superseded")

    raw = read_raw(path)
    rows, newline_hits = parse_tsv(raw)
    if not rows:
        raise InputError(f"{path} has no rows at all (not even a header)")

    header = rows[0]
    data_rows = rows[1:]

    failed = refused_override

    # Check 1: header
    n = len(schema_cols)
    if len(header) >= n and header[:n] == schema_cols:
        extra = header[n:]
        minimum = schema.get("findings", {}).get("columns_are_minimum", True)
        if extra and not minimum:
            failed = True
            status_line(
                "FAIL",
                f"check 1: {len(extra)} extra trailing column(s) {extra}, and "
                "schema.json sets findings.columns_are_minimum false",
            )
        else:
            status_line("OK", f"check 1: header matches schema columns ({n} columns)")
            if extra:
                detail(f"{len(extra)} extra trailing column(s) — allowed, "
                       f"schema says the column list is a minimum: {extra}")
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
        if ready_mark is None:
            status_line(
                "UNVERIFIED",
                "check 6: disposition — schema.json declares no "
                "findings.marks.ready_to_land, so a marked cell cannot be "
                "stripped and its value cannot be graded",
            )
        for i, r in enumerate(data_rows):
            cell = r[idx] if idx < len(r) else ""
            has_mark, remainder = strip_ready_to_land(cell, ready_mark or "\0\0")
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
        if superseded_mark is None:
            status_line(
                "UNVERIFIED",
                "check 7: basis — schema.json declares no "
                "findings.marks.superseded, so a superseded mark cannot be "
                "recognized and check 8 cannot run faithfully",
            )
        for i, r in enumerate(data_rows):
            cell = r[idx] if idx < len(r) else ""
            has_super, ref, remainder = strip_superseded(cell, superseded_mark or "\0\0")
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
    prose_rest = schema_role_value(
        schema.get("findings", {}), disposition_vocab, "superseded_disposition")
    if col_index.get("basis") is None or col_index.get("disposition") is None:
        status_line(
            "UNVERIFIED",
            "check 8: superseded rows are prose-rest with no ready-to-land mark "
            "— basis and/or disposition column not found",
        )
    elif prose_rest is None:
        status_line(
            "UNVERIFIED",
            "check 8: superseded rows take the superseded disposition with no "
            "ready-to-land mark — schema.json declares no usable "
            "findings.roles.superseded_disposition, or names one its own "
            "findings.vocabularies.disposition no longer lists",
        )
    else:
        bad = []
        for i in range(len(data_rows)):
            has_super = basis_info.get(i, (False, None, ""))[0]
            if not has_super:
                continue
            has_mark, remainder = disp_stripped.get(i, (False, ""))
            if has_mark or remainder != prose_rest:
                bad.append((i, has_mark, remainder))
        if bad:
            failed = True
            status_line(
                "FAIL",
                f"check 8: a superseded-by row's disposition must be exactly "
                f"{prose_rest!r} and carry no ready-to-land mark",
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
    status_line("COUNTS", "check 9: counts (informational, never a pass/fail)")
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
        status_idx = schema_column_index(axis_table["header"], axis_cols, "status")
        if status_idx is None:
            failed = True
            status_line(
                "FAIL",
                "check 3: every axis-row status cell in schema's status vocabulary "
                "— 'status' column not found via map.axis_columns",
            )
            status_line(
                "UNVERIFIED",
                "check 4: dark rows carry a label or pointer — 'status' column not found",
            )
        else:
            dark = schema_role_value(
                schema.get("map", {}), status_vocab, "absence_status")
            bad_vocab = []
            bad_dark = []
            dark_count = 0
            for i, row in enumerate(axis_table["rows"]):
                cell = row[status_idx] if status_idx < len(row) else ""
                token, rest = leading_token(cell)
                if token not in status_vocab:
                    bad_vocab.append((i, cell))
                    continue
                if dark is not None and token == dark:
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

            if dark is None:
                status_line(
                    "UNVERIFIED",
                    "check 4: the absence status carries SOMETHING after the token — "
                    "schema.json declares no usable map.roles.absence_status, "
                    "or names one its own map.vocabularies.status no longer "
                    "lists",
                )
            elif bad_dark:
                failed = True
                status_line("FAIL", f"check 4: every {dark!r} status cell carries 'modelled' or a pointer")
                for i, cell in bad_dark[:20]:
                    detail(f"axis row {i}: status={cell!r} — no label/pointer after {dark!r}")
            else:
                status_line("OK", f"check 4: all {dark_count} dark row(s) carry a label or pointer")

    axis_name_col = axis_cols[0] if axis_cols else None
    axis_idx = (
        schema_column_index(axis_table["header"], axis_cols, axis_name_col)
        if axis_table is not None and axis_name_col is not None
        else None
    )

    # Check 5: cross-cutting row present
    if axis_table is None:
        status_line("UNVERIFIED", "check 5: cross-cutting row present — axis table not found")
    elif axis_idx is None:
        status_line(
            "UNVERIFIED",
            "check 5: cross-cutting row present — map.axis_columns[0] not found "
            "in the axis table header",
        )
    else:
        token = schema_row_token(map_schema, "cross_cutting")
        if token is None:
            status_line(
                "UNVERIFIED",
                "check 5: cross-cutting row present — schema.json declares no "
                "map.required_rows.cross_cutting.match token to recognize it by",
            )
        else:
            found = any(
                token.lower() in (row[axis_idx] if axis_idx < len(row) else "").lower()
                for row in axis_table["rows"]
            )
            if found:
                status_line("OK", f"check 5: an axis row carries the schema's "
                                  f"cross-cutting token {token!r}")
            else:
                failed = True
                status_line("FAIL", f"check 5: no axis row carries the schema's "
                                    f"cross-cutting token {token!r}")
                detail("this recognizes the row by TOKEN, not by meaning: a "
                       "faithful row worded otherwise fails here, and the cure "
                       "is schema.json's match token, not a reworded row")

    # Check 6: enforcer row — ADVISORY, never fails exit code
    if axis_table is None:
        status_line("UNVERIFIED", "check 6: enforcer row present — axis table not found (advisory)")
    elif axis_idx is None:
        status_line(
            "UNVERIFIED",
            "check 6: enforcer row present — map.axis_columns[0] not found "
            "in the axis table header (advisory)",
        )
    else:
        token = schema_row_token(map_schema, "enforcer")
        if token is None:
            status_line(
                "UNVERIFIED",
                "check 6: enforcer row — schema.json declares no "
                "map.required_rows.enforcer.match token to recognize it by",
            )
        else:
            found = any(
                token.lower() in (row[axis_idx] if axis_idx < len(row) else "").lower()
                for row in axis_table["rows"]
            )
            status_line(
                "ADVISORY",
                f"check 6: a row carrying the schema's enforcer token {token!r} is "
                f"{'present' if found else 'ABSENT'} — whether one is OWED depends on "
                "this system emitting verdicts about other work, a judgment this "
                "checker cannot make; never affects exit code",
            )

    # Check 7: at most one empty closed-at, and it is the last round row
    if round_table is None:
        status_line("UNVERIFIED", "check 7: at most one open round row, and it is last — round table not found")
    else:
        closed_idx = schema_column_index(round_table["header"], round_cols, "closed-at")
        if closed_idx is None:
            failed = True
            status_line(
                "FAIL",
                "check 7: at most one open round row, and it is last "
                "— 'closed-at' column not found via map.round_columns",
            )
        else:
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

    # Check 8: a CLOSED round row carries a class cell, and a named class
    # names at least one axis row. PLAN item 10 calls the property compared
    # over the rows "the half a walker cannot fake"; the row NAMES are
    # copyable from the table above, so naming one is the part a checker can
    # verify — that it was compared at all stays the walker's to answer.
    if round_table is None or axis_table is None:
        status_line(
            "UNVERIFIED",
            "check 8: closed round rows carry a class naming axis rows — "
            "round and/or axis table not found",
        )
    else:
        closed_idx = schema_column_index(
            round_table["header"], round_cols, "closed-at")
        class_idx = schema_column_index(
            round_table["header"], round_cols, "class")
        axis_i = schema_column_index(
            axis_table["header"], axis_cols, axis_cols[0] if axis_cols else "")
        none_token = schema_role_value(
            map_schema, map_schema.get("vocabularies", {}).get("class", ["none"]),
            "empty_class") or "none"
        if closed_idx is None or class_idx is None or axis_i is None:
            status_line(
                "UNVERIFIED",
                "check 8: closed round rows carry a class naming axis rows — "
                "schema no longer declares one of closed-at / class / the "
                "axis-name column",
            )
        else:
            axis_names = [
                (r[axis_i] if axis_i < len(r) else "").strip().lower()
                for r in axis_table["rows"]
            ]
            empty_class, unnamed = [], []
            for i, r in enumerate(round_table["rows"]):
                closed = (r[closed_idx] if closed_idx < len(r) else "").strip()
                if not closed:
                    continue  # an open round has not made its cross-row read yet
                cls = (r[class_idx] if class_idx < len(r) else "").strip()
                if not cls:
                    empty_class.append(i)
                    continue
                if cls.strip().lower() == none_token.lower():
                    continue
                hit = any(
                    name and any(
                        w for w in name.split() if len(w) > 3 and w in cls.lower())
                    for name in axis_names
                )
                if not hit:
                    unnamed.append((i, cls))
            if empty_class or unnamed:
                failed = True
                status_line(
                    "FAIL",
                    "check 8: every CLOSED round row carries a class, and a "
                    f"class other than {none_token!r} names an axis row")
                for i in empty_class:
                    detail(f"round row {i}: closed-at filled but class empty "
                           "— a skipped close")
                for i, cls in unnamed:
                    detail(f"round row {i}: class={cls!r} names no axis row "
                           "from the table above")
            else:
                status_line(
                    "OK",
                    "check 8: every closed round row carries a class, each "
                    "naming an axis row or the none-token")

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
    unverified = _UNVERIFIED_COUNT[0]
    if exit_code != 0:
        print(f"RED — one or more checks failed"
              + (f"; {unverified} could not be verified" if unverified else ""))
        return exit_code
    if unverified:
        print(f"AMBER — no check failed, but {unverified} could NOT be "
              f"verified. This is not a pass: exit 3.")
        return 3
    print("GREEN — all non-advisory checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
