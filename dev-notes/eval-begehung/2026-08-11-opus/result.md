# /eval-skill begehung — Tier 2, OPUS arms — 2026-08-11

Skill path (served): plugin cache begehung 0.1.1; the WITH arm
detected the 0.1.2 pin, read the delta, and followed 0.1.2 (its
part 1/6) — both 0.1.2 clauses (scratch review-copy MAP,
ready-to-land dispositions) were exercised.
Installed version at run: 0.1.2 pinned, 0.1.1 served (mid-session
pin lag; the arm's own detection made the run grade 0.1.2
conduct).
Tier applicability: Tier 2 only — this run executes the begehung
BACKLOG READY entry "two-arm Tier-2 on OPUS arms" (Tier 1 ran
2026-08-11 separately, see Done).

Task (both arms, identical, neutral wording — no skill
vocabulary): quality/robustness review of the statiker repo at
f357bed, read-only.

Arms: 2 × opus (general-purpose). WITH invoked begehung:begehung;
WITHOUT barred from methodology skills. Outputs verbatim in
tier2-with.md / tier2-without.md (this directory).

## Per-element grading (PLAN.md §Tier 2 signature)

1. **MAP before first search, rows structure-derived** — PRESENT
   in WITH: MAP review copy (scratchpad
   `BEGEHUNG-MAP-statiker.with-2.md`) opens with the no-map grep,
   derives 10 surfaces S1–S9+ each with consumer and cost ("a
   forcing point passes vacuously", "stale payload served
   silently") — structure, not incident list; cited in
   tier2-with.md part 1/6 (MAP write flagged by the writer gate,
   i.e. it happened BEFORE search work) and part 6b (artifact).
   ABSENT in WITHOUT: `grep -ci MAP tier2-without.md` → 0 (control:
   6 hits in tier2-with.md); its working files are a scratch clone
   and probe fixtures only.
2. **Lens pre-registered before searching** — PRESENT in WITH: MAP
   carries a round register r1–r3 (tier2-with.md part 6b); the
   walk is organized per row. ABSENT in WITHOUT: "lens" 0 hits;
   findings are ordered by severity, no registration artifact.
3. **Coverage counts, no global done-claim** — PRESENT in WITH,
   verbatim: "2 mechanically-guarded / 5 prose-covered / 3 dark,
   of 10 rows" + explicit "no global done-claim" (part 6b).
   WITHOUT: no counts over an enumerated surface set; it closes
   with a qualitative "standing assessment" (part 7/7) — it avoids
   a "secured" claim, but coverage is not enumerable from its
   report.
4. **Structural disposition per finding, booked in the system's
   carriers** — PRESENT in WITH in the 0.1.2 read-only variant:
   every finding closes "Ready-to-land disposition, landing
   trigger *<named commit/seam>*" (parts 2–5). PARTIAL in WITHOUT:
   each finding carries a repair shape and a red-first
   arrangement (strong), but no landing trigger, no carrier
   form — a reader must convert them before they can land.
5. **"Is there more?" answered by rotation to darkest** — PRESENT
   in WITH: "Rotation takes the darkest: R6, the release/pin
   surface … the only row whose wrongness reaches people beyond
   this machine" (part 6b). ABSENT in WITHOUT: report ends at the
   assessment; no next-step surface.

## Contamination check (WITHOUT arm)

Coined-term greps over tier2-without.md: MAP 0 · lens 0 · Linse 0
· "emission surface" 0 · pre-register 0 · rotation 0 ·
prose-covered 0. "begehung" 2 hits — both in this file's own
preamble/arm name added at persistence, none in the arm's report
body. Control: the same greps return live counts in
tier2-with.md. Arm reads clean; the corpus-loaded-control caveat
stands by design (the WITHOUT arm cites the global corpus
explicitly, e.g. its required-reading note — that is the intended
control condition, not contamination).

## Verdict

**Signature present-with / absent-without on elements 1, 2, 3, 5;
element 4 present-with / partial-without.** Finding QUALITY is
comparable and partially disjoint — both arms independently led
with the identical blocking finding (contract battery red at
f357bed, four commits deep, verified by the dispatcher's own run:
`1 failed, 280 passed`), then diverged into disjoint deep sets
(WITH: byte-policy carry-across, guard-reach mutation probe,
release/pin surface; WITHOUT: repair-token class-blindness with
two executed gate-false-clean probes, waves path-field collision,
trend window composition). The skill's delta is therefore NOT
finding quality — opus finds either way — but the structural
artifacts: enumerated coverage with darkness made visible,
registered rounds, dispositions that can LAND, and a rotation
state a successor can resume. Exactly the begehung thesis (yield
tracks the lens; the counter is bookkeeping, not diligence).

The run also answers the entry's two open questions:
- **Opus fitness for the declared consumer range: YES** — both
  arms executed probes, refused to overclaim, self-disclosed
  process violations (WITHOUT: its own repo write, immediately
  repaired and verified; WITH: the MAP collision in shared
  scratch).
- **FP5 cross-row clause, uncontaminated no-op read: the clause
  BINDS** — the WITH arm produced the cross-row class read ("F1,
  F3 and F4 are one class … a known-uncovered class with three
  live instances rather than three surprises", part 6b), which
  the WITHOUT arm's per-finding structure did not produce (its
  closest is the standing assessment's shared-blind-spot
  paragraph — an overall observation, not a per-row cross read
  feeding rotation).

## Process observations (dispatcher-side, booked)

- The briefs said "your OWN scratchpad" — false for parallel arms:
  the session scratchpad is shared, and the WITH arm's MAP write
  collided with a stale claim from an earlier same-named agent
  (writer-claims gate warned in staging). The dispatch skill §1
  already mandates per-agent filenames for shared scratch; the
  dispatcher (this session) failed to apply it — a fire of an
  existing rule, logged, no mint needed.
- Version-pin lag mid-session (0.1.1 served, 0.1.2 pinned) was
  self-detected by the WITH arm; conduct followed 0.1.2. Grade
  unaffected.

## Next action

Statiker-side: the harvest (both arms) lands in the statiker
BACKLOG as repair entries (F1/F2/F3/F4 + the WITHOUT deep set),
red arrangements quoted from the arm files. Begehung-side: entry
"two-arm Tier-2 on OPUS arms" leaves by this record; observation
below logged to dev-notes/OBSERVATIONS.md.
