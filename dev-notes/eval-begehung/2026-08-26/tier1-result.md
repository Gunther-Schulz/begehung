# Tier-1 (triggering) — 2026-08-26, skill v0.3.0

Run after the five-amendment arc (1f71d32 → 7847336). Runner: three
`skill-craft:skill-router` lanes in parallel, identical input, opus.

## Instrument note, settled before the run

The frontmatter description is BYTE-IDENTICAL from 1f71d32 to HEAD —
verified by `diff` over lines 2-3, not assumed. No amendment in this
arc touched triggering. Tier-1 was therefore re-run for ONE live
variable only: the competitor field, which the 2026-08-11 baseline
reproduced as of that date and cannot speak for now.

Competitors put to the router: statiker · code-review · kaemmung ·
clippy · security-review · dispatch (6, against the 2026-08-11 run's
6). Query set: PLAN.md's Tier-1 sets, 6 positive + 6 negative (the
2026-08-11 set plus N6 "backlog aufräumen", added because kaemmung
now exists and is the nearest German-language competitor).

## Result: 12/12 clean

| query | fires | verdict |
|---|---|---|
| P1 robustheits-review von pbs-office | 3/3 | clean |
| P2 blinde flecken im regelwerk | 3/3 | clean |
| P3 coverage review of our guard net | 3/3 | clean |
| P4 begehung von lifecycle | 3/3 | clean |
| P5 sind wir überall abgesichert | 3/3 | clean |
| P6 review our review process | 3/3 | clean |
| N1 review this PR | 0/3 | clean (→ code-review 3/3) |
| N2 code-review meiner änderungen | 0/3 | clean (→ code-review 3/3) |
| N3 statiker run für feature X | 0/3 | clean (→ statiker 3/3) |
| N4 diagnose this bug | 0/3 | clean (→ NONE 3/3) |
| N5 review the design of this function | 0/3 | clean (→ code-review 2/3, NONE 1/3) |
| N6 backlog aufräumen | 0/3 | clean (→ kaemmung 3/3) |

Matches the 2026-08-11 baseline (12/12) on every shared query, now
against the current competitor field. No description change owed.

## Notes worth keeping

- The only cross-trial variance was N5, splitting code-review 2 / NONE
  1 — variance inside a COMPETITOR's boundary, not begehung's, which
  held 0/3. Not a defect of this description.
- Two lanes independently reported that begehung's own exclusion
  sentence ("not for … diagnosing one defect") is what decided N4;
  without it the "robustness review" surface would have drawn the
  query. The exclusion clause is load-bearing, not decoration.
- N6 was added this run and is clean: kaemmung's literal trigger
  strings own it, and P2's "Regelwerk" does not leak to kaemmung
  because that description scopes to WORK carriers.

## Dispatcher defect, recorded against the run not the skill

All three lanes reported the same channel failure: the brief named
`begehung-c7` as the report target, and SendMessage refused it —
for an agent running INSIDE this session the address is `main`. The
reports arrived (each lane fell back correctly and said so), so no
data was lost, but the brief was wrong. Sender-side residue: the
fix belongs to the dispatch tooling's own repo, outside this arc's
write boundary.
