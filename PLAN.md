# Begehung — the plan (persisted 2026-08-11)

Naming lineage: statiker's sibling — die Begehung is the systematic
inspection walk through the WHOLE object, protocol in hand (Bau-,
Sicherheits-, Brandschutzbegehung). Canonical German domain term,
chosen over a coinage per skill-craft's term-selection rule; cold-probe
verification of the name is an open item (BACKLOG).

Consumer of this file: the sessions that trial and extend the skill.
Every design decision from the founding discussion is HERE or quoted
from its named carrier; the conversation is not the carrier.

## Mission and lineage

A thin, top-tier-first REVIEW-process skill: systematic coverage
review of a system/corpus/process via a persistent axis map, replacing
incident-lensed ad-hoc review rounds. Lineage: clippy (frozen legacy)
→ anneal-dev (lens framework extracted from clippy; LEGACY — the
framework path is gone from the machine, only bindings remain) →
statiker (clippy's successor, design conduct) → **begehung** (the
review sibling). The planned statiker-framework may later absorb both;
begehung is built skill-first, probe-then-certify, exactly as statiker
was — thin before framework, validated on real work before extraction.

## The founding evidence (2026-08-11, pbs second-opinion session)

Measured in one session: review yield tracks the LENS, not the
effort — repeated rounds under one lens exhausted (the final round
found defects mostly in the round's own fresh artifacts), while every
operator question that rotated the lens produced fresh findings. The
pbs Achsen-Inventur (pbs-office
`erhebungen/verifikations-achsen-inventur-2026-08-01.md`) is the
working domain instance: its axis 7 was "found at the desk, not at the
damage". Full record: pbs-office
`erhebungen/robustheits-review-2026-08-11.md` (Zweitrunde section) and
the statiker BACKLOG founding entry (2026-08-11), whose design core is
authoritative and quoted here:

> (1) a persistent AXIS LEDGER per system under review, first derived
> from the artifact's STRUCTURE (claim-emission surfaces × consumers ×
> failure-class dimensions), not from incident history; per row:
> guarded-mechanically (with red-proof pointer) / prose-covered /
> dark, dated — a row unrefreshed past a stated interval is itself a
> finding. (2) Each round PRE-REGISTERS its lens before searching (the
> anti-incident-pull move). (3) Per-lens stop rule: falling yield ends
> the lens, never the ledger; global "done" does not exist. (4)
> Rotation: next round takes the darkest/stalest row. (5) Exit per
> finding: a mechanism at the emission point (mandatory-field move) or
> an honest prose-rest label.

Contrast to anneal-dev (why this is not a revival): anneal ran a FIXED
lens set exhaustively per pass (cost ∝ lenses × artifact; lens list =
past incidents). Begehung is the scheduling-and-bookkeeping layer:
cheap per round (one lens), compounding via the map, composing with
any lens definitions rather than replacing them.

## Evaluation (written before the skill text; skill-craft order)

**Tier 1 — triggering set** (runner: `/eval-skill` /
skill-craft:skill-router):

Positive (must route to begehung):
- "mach ein robustheits-review von pbs-office"
- "wo sind unsere blinden flecken im regelwerk?"
- "run a coverage review of our guard net"
- "begehung von <system>" / "run a begehung"
- "sind wir überall abgesichert? bitte systematisch prüfen"
- "review our review process — we only ever look where the last bug was"

Negative (must NOT route here):
- "review this PR" / "code-review meiner änderungen" (code review)
- "statiker run für feature X" (statiker)
- "diagnose this bug" (diagnosing-bugs)
- "review the design of this function" (statiker/code review)

**Tier 2 — behaviour-delta signature** (with skill vs. without, same
review request). ORDERING, binding: this list is amended BEFORE
`/eval-skill` runs, never after — an item overtaken by a landed
amendment grades conformant behaviour as a miss, and the eval reads
as evidence either way.
1. A MAP file is loaded or created BEFORE the first search command;
   first-run rows derive from structure (emission surfaces), not from
   the incident list alone.
2. The round's lens is pre-registered in the MAP before searching.
3. The report carries coverage counts (guarded/prose/dark of n rows)
   and NO global "done/secured" claim.
4. Every finding carries a structural disposition (emission-point
   mechanism or labeled prose-rest), booked in the system's own
   carriers.
5. A follow-up "and is there more?" is answered by rotating to the
   darkest/stalest row, not by re-running the same lens.
6. A findings data file exists for the round, one row per finding
   (lens · grade · artifact line · finding · basis · disposition),
   its rows appended as findings land rather than composed at close,
   every disposition cell filled at close; the round's message
   carries its path and counts, not the findings themselves.
   (Extends item 3, which is silent on the artifact. The filled-cell
   half is the one that separates this from the recorded incident,
   where the findings were visible and still booked nowhere.)
7. The round row records `read-at` before the first search, and at
   close `closed-at` plus the re-test's `reach` as counts (r hold, s
   superseded) — written whether or not anything moved; a finding the
   close re-test finds no longer holding exits as a prose-rest whose
   `basis` opens `superseded-by <change-ref>:`, and is booked
   nowhere. (The REACH is the discriminator, not the version tokens:
   a version alone separates a round that recorded one from a round
   that did not, while only the reach separates a re-tested round
   from an unexamined one — and r + s must reconcile against the
   findings file's own rows, so the cell cannot be written without
   the pass. CARVE-OUT to item 4, which this item narrows rather than
   leaves untouched: a superseded finding keeps item 4's disposition
   half — it is a prose-rest — and is exempt from its BOOKING half.
   An arm that leaves superseded findings unbooked grades CLEAN on
   item 4.)

## Trial method (statiker pattern: probe-then-certify)

Status: trial. First real run: the pbs-office review's own named next
lens (Achse 7, Zahlen-Quercheck) or any repo needing a system review.
Grade the run against the Tier-2 signature; observations to
dev-notes/OBSERVATIONS.md; rules in SKILL.md stay fire-born.

## Open items

Tracked in BACKLOG.md: name cold-probe · Tier-1 eval run · first
trial run · framework absorption (parked until statiker-framework
exists) · repo visibility (born private; public is the operator's
call, statiker precedent is public).
