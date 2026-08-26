#!/usr/bin/env python3
"""Regression probe: every PLAN.md Tier-2 signature item still has text
in SKILL.md that could produce it.

Parentage: each anchor below is derived from PLAN.md's statement of the
item — the DEFINITION — never from SKILL.md, which is the artifact on
trial. An anchor read off SKILL.md would move with any cut and stay
green on the loss it exists to catch.

Adding an anchor: key it to the DEMAND PLAN.md states, never to the
sentence SKILL.md currently uses. An anchor whose text could be pasted
out of SKILL.md is the tell — it goes green on any rewrite keeping the
phrase and red on every rewrite that does not, which inverts what the
check is for. Measured here: an anchor quoting `ages by staleness` went
red on a correct repair (dev-notes/OBSERVATIONS.md, 2026-08-26,
"an anchor keyed to WORDING").

Reach, stated: this probe checks that the TEXT survives a cut, and that
a rule SITS in the section governing its moment. It does not measure
behaviour, and a seam anchor does not show a walker REACHES the rule —
only a live round on a system with an existing MAP measures that. A
green here means "no signature item lost its carrier", never "the skill
still works".

Usage: tools/signature_probe.py [path-to-SKILL.md]
Exit 0 = every item carried; 1 = at least one item has no carrier.
"""
import re
import sys
from pathlib import Path

# (item, why it matters, [phrases that must ALL appear])
# Phrases are matched over whitespace-normalized text, case-insensitively:
# SKILL.md is hard-wrapped, so any line-based match returns false zeros on
# a phrase spanning the wrap.
ANCHORS = [
    ("1", "MAP loaded/built before the first search; rows derive from structure",
     ["before the first search command", "enumerate the claim-emission surfaces"]),
    ("2", "the round's lens pre-registered before searching",
     ["pre-register the lens", "before the first search;"]),
    ("3", "coverage counts replace any global done-claim",
     ["k guarded / m prose / j dark of n rows", "in place of any global"]),
    ("4", "every finding exits as mechanism or prose-rest, booked in own carriers",
     ["booked in the system's own carriers", "no third state"]),
    ("5", "rotation answers 'is there more?' by darkest, then stalest",
     ["next round takes the darkest row", "the stalest"]),
    ("6", "findings file appended as findings land; message carries path+counts",
     ["appended as findings land", "carries the findings file's path and its"]),
    ("7", "read-at / closed-at / reach, and supersession",
     ["read-at", "closed-at", "reach", "superseded-by"]),
    ("8", "executed basis or label AT THE HEAD of the basis cell",
     ["at the head of the finding's `basis` cell", "unverified", "modelled"]),
    ("9a", "enforcer row minted, on a loaded map as much as a new one",
     ["enforcer row", "is minted now"]),
    ("9b", "cross-cutting lifecycle row minted, on a loaded map as much as new",
     ["cross-cutting row"]),
    ("10", "class cell records the cross-row read: rows spanned AND property",
     ["the round row's `class` records that read",
      "names the rows read across and the property compared over them"]),
]


# (item, why, heading, [phrases]) — the phrase must appear INSIDE that
# section, not merely somewhere in the file. A rule fires at the seam it
# governs: a rotation rule correct as a sentence but sitting in a section
# the walker reads only on a first run never reaches its moment
# (dev-notes/OBSERVATIONS.md, the amendment-4 incident of 2026-08-26).
# Keyed to the DEMAND, never to one phrasing — an anchor quoting the
# current wording goes green on any rewrite and red on every reword,
# which is the opposite of what it is for.
SECTION_ANCHORS = [
    ("9b-seam", "the rotation seam names the cross-cutting row",
     "## Rotation", ["cross-cutting"]),
]


# Vocabularies live in templates/schema.json (the single home, read by the
# shipped checker) while SKILL.md explains what each value MEANS — so each
# value necessarily appears in both. That is two homes for one fact, which
# drifts silently: a value added to the schema and not to the prose leaves
# the walker filling a cell the skill never taught, and the reverse ships a
# vocabulary the checker rejects. Derived from the schema, never restated:
# a hardcoded list here would age exactly as badly as the one it guards.
SCHEMA_REL = "plugin/skills/begehung/templates/schema.json"


def vocab_values(schema: dict) -> list:
    """Every closed-vocabulary value the schema declares, flattened."""
    out = []
    for section in ("findings", "map"):
        vocabs = schema.get(section, {}).get("vocabularies", {})
        for key, val in vocabs.items():
            if isinstance(val, list):
                out.extend((key, v) for v in val)
    return out


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def section_body(text: str, heading: str) -> str:
    """The text under `heading`, up to the next same-or-higher heading."""
    level = len(heading) - len(heading.lstrip("#"))
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.strip() == heading)
    except StopIteration:
        return ""
    body = []
    for ln in lines[start + 1:]:
        stripped = ln.strip()
        if stripped.startswith("#"):
            if len(stripped) - len(stripped.lstrip("#")) <= level:
                break
        body.append(ln)
    return "\n".join(body)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "plugin/skills/begehung/SKILL.md")
    body = normalize(path.read_text(encoding="utf-8"))

    failures = []
    for item, why, phrases in ANCHORS:
        missing = [p for p in phrases if normalize(p) not in body]
        status = "MISSING" if missing else "carried"
        print(f"  [{status:>7}] item {item:<3} {why}")
        if missing:
            for p in missing:
                print(f"              no carrier for: {p!r}")
            failures.append(item)

    raw = path.read_text(encoding="utf-8")
    for item, why, heading, phrases in SECTION_ANCHORS:
        sect = normalize(section_body(raw, heading))
        if not sect:
            print(f"  [MISSING] item {item:<3} {why}")
            print(f"              section {heading!r} not found")
            failures.append(item)
            continue
        missing = [p for p in phrases if normalize(p) not in sect]
        status = "MISSING" if missing else "carried"
        print(f"  [{status:>7}] item {item:<3} {why}")
        for p in missing:
            print(f"              {heading!r} does not name: {p!r}")
        if missing:
            failures.append(item)

    schema_path = path.parent / "templates" / "schema.json"
    if not schema_path.exists():
        schema_path = Path(SCHEMA_REL)
    if schema_path.exists():
        import json
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        pairs = vocab_values(schema)
        absent = [(k, v) for k, v in pairs if normalize(v) not in body]
        status = "MISSING" if absent else "carried"
        print(f"  [{status:>7}] vocab  every schema vocabulary value is "
              f"explained in SKILL.md ({len(pairs)} values)")
        for key, val in absent:
            print(f"              schema {key} value {val!r} appears in "
                  f"no SKILL.md prose")
        if absent:
            failures.append("vocab")
    else:
        print(f"  [ADVISORY] vocab  schema not found at {schema_path} — "
              f"could not verify, not a pass")

    total = len(ANCHORS) + len(SECTION_ANCHORS) + 1
    print()
    if failures:
        print(f"RED — {len(failures)} of {total} items lost their "
              f"carrier: {', '.join(failures)}")
        return 1
    print(f"GREEN — all {total} Tier-2 signature items carried in "
          f"{path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
