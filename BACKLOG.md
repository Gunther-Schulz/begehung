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
  findings file against it.
  WRITE-BOUNDARY QUESTION — ANSWERED 2026-08-26, against the premise
  booked here. The premise was that the validator's natural home is
  the lifecycle plugin's intake. REFUTED at the interface: lifecycle's
  intake is `items add`, one item at a time through named CLI slots
  (`--requirement`, `--goal`, `--write-set`, `--done-criterion`,
  `--evidence`), with no file-ingest path — it never reads a findings
  file and so has nothing to check against begehung's schema (basis:
  lifecycle/plugin/cli/lifecycle_core/cli.py, the `items add` parser,
  read 2026-08-26). These are two checks with different questions, not
  one check in two homes: "is this findings file well-formed?" is
  begehung's, at round close; "can this become an item?" is
  lifecycle's, at booking. The validator is begehung's, built in this
  repo, no cross-repo coordination.
  DESIGN ADDITION: the validator's invocation anchors at forcing point
  5's close, where the round's counts are reported — an un-fakeable
  artifact at a moment that observably produces one, rather than a
  pointer the walker may not reach.
  DONE-CRITERION, RESTATED with basis: the original ("word count DOWN
  from 2087") rests on e97943a's ~46% figure. That figure is right
  about what the text IS and wrong about what can LEAVE — column lists
  and vocabularies move, but the semantics of judgment-bearing cells
  cannot (the `class` cell's "the property is not copyable" is the
  un-fakeable half a template cannot carry). Realistic movement
  250-400 words, not 900. Criterion: both completion criteria
  EXECUTABLE, and every vocabulary with exactly one home — word count
  down is a side effect, not the target.
  VERIFIER: the validator goes red on a planted bad cell (an empty
  disposition, a `dark` row with no label, a `class` cell naming no
  rows), each red shown beside a green on the same file with only that
  cell repaired.
  GATE: process-shape change, so the repo's "Evaluation before text"
  rule puts a Tier-2 re-run between this and RELEASE (not between it
  and commit); PLAN's Tier-2 list is amended BEFORE that eval runs,
  per PLAN's own ordering note.
  Not started in this arc (judgment-desk ruling 2026-08-26).

- **PARKED 2026-08-11 — statiker-framework absorption.** Trigger:
  the statiker-framework exists and begehung has ≥1 certified trial
  run. Until then begehung stays a standalone thin skill (PLAN.md,
  Mission).
## Done

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
