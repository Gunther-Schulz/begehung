# Begehung — backlog

Future work graded by decision-completeness (operator-corpus file
roles). PLAN.md stays the design record; SKILL.md clauses stay
fire-born per CLAUDE.md.

## Open

- **READY 2026-08-26 — Tier-2 re-run before the next release.** The
  precipitate change altered process shape (the round now runs a
  checker at forcing point 5), so the repo's "Evaluation before text"
  rule owes a Tier-2 run before release. PLAN's Tier-2 list already
  carries item 11 for it, amended BEFORE any eval ran per PLAN's own
  ordering note. DESIGN, decided: one opus arm on an object with an
  EXISTING map, same brief shape as the 0.3.1 verifier, graded against
  items 1-11. WRITE-SET: dev-notes/eval-begehung/<date>/ plus the
  result record. DONE-CRITERION: item 11 graded present/absent with
  the checker's own output as evidence, and items 1-10 unregressed.
  VERIFIER: the arm's findings file and MAP review copy, plus its
  pasted checker run. Not started — release is the operator's act and
  this gates it.

- **PARKED 2026-08-11 — statiker-framework absorption.** Trigger:
  the statiker-framework exists and begehung has ≥1 certified trial
  run. Until then begehung stays a standalone thin skill (PLAN.md,
  Mission).

## Done

- **precipitate the machine-read semantics into a template + validator**
  — built 2026-08-26, commits 92faae9 (schema + templates), 6b535b2 +
  d4fb620 (the shipped checker, dispatched lane), 072aab9 (role keys,
  exit contract), and this one (the self-review's 16 findings).
  DELIVERED against the RESTATED criterion: both completion criteria
  are executable — `tools/validate_begehung.py findings|map` — and the
  vocabularies have one home, `templates/schema.json`, which both
  tools read rather than restate.
  NOT DELIVERED, and the entry's original criterion was wrong to ask:
  SKILL.md went UP, 2094 → ~2160 words. What is extractable is the
  ENUMERATION of legal values; what stays is the SEMANTICS, and prose
  explaining a vocabulary does not shrink when the vocabulary moves.
  The ~46% figure from e97943a measured what the text IS, never what
  can leave (recorded: dev-notes/OBSERVATIONS.md, same date).
  VERIFIER RUN: the entry named three planted bad cells. Two existed
  and passed; the third — a `class` cell naming no rows — did NOT
  exist and was built in this commit, red-first (empty class on a
  closed round → exit 1; class naming no axis row → exit 1; class
  naming one → exit 0). Also proven: the German-worded owed row that
  a hardcoded token failed now passes with one schema line changed.
  PRE-COMMIT SELF-REVIEW: 4 blocking, 8 notable, 4 nits — all fixed,
  none deferred, every one reproduced by the dispatcher before repair.
  SURVIVOR, booked below: the Tier-2 re-run this entry's own GATE line
  defers to before release.

- **two clause cuts the arc measured but did not take** — built
  2026-08-26, this commit. Cut (a), the FP5 cross-row RATIONALE, taken
  as designed. Cut (b), the Rotation paragraph, taken but NOT to the
  booked destination.
  DEVIATION from the booked design, with basis: the entry prescribed
  relocating the staleness clause into MAP derivation step 5. The
  pre-commit self-review blocked it — step 5 sits under "First run
  derives rows from the system's STRUCTURE", and rotation only matters
  from round 2 on, when first-run derivation does not run. That is the
  amendment-4 class recurring one commit after its own repair
  (dev-notes/OBSERVATIONS.md, second-firing note). The rule instead
  stays at its seam as one sentence in `## Rotation` — still a cut,
  four lines down to one.
  TWO FURTHER REPAIRS the review bought: the removed FP5 clause was
  also binding FP4's "the emission point" for a class row spanning n
  axis rows, restored to the single definition home (the MAP `class`
  sentence); and the booked basis "MEASURED no-op" was itself wrong —
  the clause's firing log reads FIRED, and the cut now rests on the
  record's n=1 ambiguity instead (both corrections in OBSERVATIONS).
  VERIFIER: the booked one named a "regression probe set" that existed
  in no committed file — an unbound slot, booked as its own instrument
  lesson. Built as `tools/signature_probe.py`, expectations derived
  from PLAN.md rather than from SKILL.md. Red-first proof: GREEN on
  pre-change HEAD; RED on each of three mutants, each on its own item
  only (naive Rotation cut → 9b-seam; `class` demand removed → 10;
  staleness anchor → 9b); GREEN after repair, 12/12.
  DONE-CRITERION met: 2132 → 2094 words, lint exit 0 / 0 blocking,
  frontmatter byte-identical so Tier-1 carries no delta.

- **move the enforcer/cross-cutting row trigger to forcing point 1** —
  booked READY and built the same day, 9c10c08 (v0.3.1). Provenance:
  the Tier-2 run of 2026-08-26
  (dev-notes/eval-begehung/2026-08-26/result.md) — amendment 4
  produced NO row in either arm, because a walker loading an existing
  MAP never executes first-run derivation and the completion
  criterion's "at every invocation" sentence sat inside that same
  conditional section. Built rather than left booked on the
  judgment-desk ruling: designed fix, named verifier, live session,
  and a lap carrying the first evidence to reach the artifact.
  DEVIATION from the booked design, with basis: the entry said the
  requirement "produces or demands both rows"; the self-review showed
  detection-only leaves the measured failure unfixed, so forcing point
  1 MINTS the row and Tier-2 item 9a's discriminator went back to
  existence. VERIFIER RUN AND PASSED, 2026-08-26 (record:
  dev-notes/eval-begehung/2026-08-26/verify-031-*): one opus arm, the
  0.3.0 brief unchanged, statiker's existing 13-row map. Pre-state
  established before the run — 13 axis rows, ZERO enforcer or
  cross-cutting rows. After: both rows MINTED and present, each also
  recorded as a finding of the round, both carrying `dark (modelled)`.
  Control holds: the live map is untouched at 13 rows, 0 enforcer
  (`git status` empty, HEAD 680cdba). Same brief and object as the
  0.3.0 arm that produced neither row, so the skill text is the only
  changed variable.

- **two-arm Tier-2 on OPUS arms** — run 2026-08-11, 2 × opus
  (with/without), statiker repo as the review object. Verdict:
  signature present-with/absent-without (4 of 5 elements; the
  fifth present vs partial); opus fitness confirmed; FP5
  cross-row clause binds uncontaminated. Record:
  dev-notes/eval-begehung/2026-08-11-opus/ (arm files verbatim +
  result.md); observation in dev-notes/OBSERVATIONS.md same date.


- **repo visibility** — operator word 2026-08-11: public (statiker
  precedent). Executed same day: `gh repo edit --visibility public`,
  verified PUBLIC. Commit: this one.
- **name cold-probe** — run 2026-08-11, fresh sonnet context, word
  only: RECRUITS strongly (coverage-over-depth-first, whole-object
  scope, cadence, per-stop protocol — all unprompted). KEEP the
  name. Transcript + grade:
  dev-notes/eval-begehung/2026-08-11/cold-probe-transcript.md.
  Commit: this one.
- **Tier-1 triggering eval** — run 2026-08-11 via /eval-skill, 3×
  skill-router against 6 competitors: 12/12 clean (7 positives fire
  3/3 incl. the no-keyword boundary query; 5 negatives zero fires,
  each at its right owner). No description change. Record:
  dev-notes/eval-begehung/2026-08-11/result.md. Commit: this one.
- **round-close cross-row class read** — parked 132086e, minted same
  day into forcing point 5 (this commit) on operator GO. The parking
  basis did not survive one question: the "fails the no-op test"
  verdict rested on trial run 1's unprompted cross-row read, but that
  run executed in the session that had just discovered the class —
  contaminated evidence, undecidable from there. Provenance (founding
  day, label-over-body across ≥4 surfaces, one structural cure)
  satisfies fire-born; no-op status now validated by use — cut
  candidate if fresh-session rounds show the read is default.
  TRIGGER FIRED, dispositioned 2026-08-26 (bundle 3-5): two fresh opus
  rounds BOTH performed the cross-row read unprompted, so the READ is
  default and mandating it would be a no-op. NOT cut — reduced instead:
  amendment 5 keeps the clause and adds the round row's `class` cell,
  the recording being what the arms did not do by default. The cut
  trigger asked whether the rule earns its place; the answer is that
  its visibility half does and its mandate half did not.
- **first trial run (probe-then-certify)** — run 2026-08-11 on
  pbs-office (Achse 7 Zahlen-Quercheck), graded 5/5 against the
  Tier-2 signature with one recorded deviation (parallel-ownership
  case, no rule minted — fire-born pending a second occurrence);
  record in dev-notes/OBSERVATIONS.md "trial run 1". Commit: this
  one.
