# Begehung — backlog

Future work graded by decision-completeness (operator-corpus file
roles). PLAN.md stays the design record; SKILL.md clauses stay
fire-born per CLAUDE.md.

## Open

- **READY 2026-08-26 — precipitate the machine-read semantics into a
  template + validator.** Provenance: the medium question answered in
  e97943a — ~46% of SKILL.md is machine-read semantics (two table
  schemas, three status values, two label vocabularies, two completion
  criteria) carried in prose, and three review rounds concentrated
  their findings in exactly that text. DESIGN: the findings-file
  column semantics, the MAP's two row forms, the status and label
  vocabularies precipitate into a SHIPPED template (TSV + MAP
  skeleton) that begehung ships, plus a validator that checks a real
  findings file against it. WRITE-BOUNDARY QUESTION, named not
  answered: the validator's natural home is the lifecycle plugin's
  intake, since amendment 1 makes the findings file an item SOURCE —
  begehung ships the template and points at the validator, the plugin
  owns the check; confirm before building, the two repos are separate
  write boundaries. DONE-CRITERION: SKILL.md word count DOWN from
  2087 with the schemas checkable rather than remembered. VERIFIER:
  the validator goes red on a planted bad cell (an empty disposition,
  a `dark` row with no label, a `class` cell naming no rows).
  Not started in this arc (judgment-desk ruling 2026-08-26).

- **PARKED 2026-08-11 — statiker-framework absorption.** Trigger:
  the statiker-framework exists and begehung has ≥1 certified trial
  run. Until then begehung stays a standalone thin skill (PLAN.md,
  Mission).
## Done

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
  existence. VERIFIER STILL OWED AND UNRUN: a Tier-2 with-arm re-run
  against statiker — existing MAP, enforces — where the enforcer row
  must EXIST at the round's end.

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
