# /eval-skill begehung — 2026-08-11

Skill path: ~/.claude/plugins/cache/begehung/begehung/0.1.1/skills/begehung/SKILL.md
Installed version: 0.1.1 (updated + /reload-plugins same day)
Tier applicability: (a) description-triggered — the description
carries trigger phrases well beyond the name.
Protocol load artifact: skill-craft references/evaluation.md
(sections: Which tiers apply · Tier 1 · Tier 2 · Tier 3 · Relation
to evolution).

## Tier 1

Query set: PLAN.md §Evaluation (operator-blessed at booking; no
redraft). Competitors: statiker, diagnosing-bugs, review, simplify,
security-review, skill-craft. 3 skill-router trials in parallel,
identical input.

| # | query | expected | fires (of 3) | verdict |
|---|---|---|---|---|
| Q1 | mach ein robustheits-review von pbs-office | begehung | 3 | clean |
| Q2 | wo sind unsere blinden flecken im regelwerk? | begehung | 3 | clean |
| Q3 | run a coverage review of our guard net | begehung | 3 | clean |
| Q4 | begehung von unserem abrechnungssystem | begehung | 3 | clean |
| Q5 | run a begehung | begehung | 3 | clean |
| Q6 | sind wir überall abgesichert? bitte systematisch prüfen | begehung | 3 | clean |
| Q7 | review our review process — we only ever look where the last bug was | begehung | 3 | clean (routed via the incident-corner premise, not a literal term) |
| Q8 | review this PR | NOT begehung | 0 (review 3/3) | clean |
| Q9 | code-review meiner änderungen | NOT begehung | 0 (none 3/3, /code-review named) | clean |
| Q10 | statiker run für feature X | NOT begehung | 0 (statiker 3/3) | clean |
| Q11 | diagnose this bug | NOT begehung | 0 (diagnosing-bugs 3/3) | clean |
| Q12 | review the design of this function | NOT begehung | 0 (none 3/3) | clean |

No misses, no over-triggers; the "Not for …" clause carried every
negative boundary. No description change.

## Tier 2 — three-arm run (with / without / sentence), opus arms, statiker repo

Arms: opus subagents, identical read-only task, no signature
vocabulary in any brief. WITH invoked begehung:begehung (served
0.1.1 incl. the fresh FP5 cross-row clause); WITHOUT barred from
methodology skills; SENTENCE got one instruction sentence exploiting
the term's priors (the ablation arm, operator-proposed). Both
controls are opus + the operator's inherited global corpus — the
measured delta is skill-over-corpus, NOT skill-over-bare-model.
Contamination grep over both control transcripts (MAP / lens /
pre-regist / mechanically-guarded / prose-covered / darkest /
rotation / coverage counts): zero coined-term hits (only ordinary
"yield"/"prose only" prose). Transcripts: tier2-with.md,
tier2-without.md, tier2-sentence.md; the WITH arm's MAP artifact:
tier2-with-MAP.md.

Per-element (PLAN.md signature):
1. MAP before search, structure-derived — PRESENT-WITH only:
   tier2-with.md Part 1 ("Working MAP in my scratchpad") and the
   artifact itself (tier2-with-MAP.md: 13 emission surfaces S1-S13
   with consumers, 12 rows with status/yield/next, baseline
   command). ABSENT in both controls (probe scripts only).
2. Lens pre-registered before first search — PRESENT-WITH only
   (tier2-with-MAP.md "## Rounds … Registered before first review
   search"). ABSENT in both controls.
3. Coverage counts + no done-claim — FULL FORM with only
   ("COVERAGE: 12 rows — 4 mechanically-guarded, 3 prose-covered,
   5 dark. No global done-claim."). Both controls carry the
   no-done-claim HALF honestly (WITHOUT: "I cannot claim coverage";
   SENTENCE: "NOT REACHED" list) — corpus effect — but no
   denominator/status enumeration.
4. Structural disposition per finding — taxonomy with only
   (mechanism-shaped w/ red-first vs prose-rest vs needs-design;
   booking blocked by write boundary, handed as an explicit gap).
   Controls give fix-shapes per finding (good) without the
   taxonomy or carrier awareness.
5. Follow-up rotated — WITH: rotation by MAP (bounded extra round
   on darkest row A12 → B9; two assumed-guarded rows re-executed;
   unwalked enumeration + MAP state). Controls: disciplined
   continuation without bookkeeping (WITHOUT: full round 2 + series
   read per the corpus trend rule; SENTENCE: second pass + "highest-
   yield next corner"). The rotation ARTIFACT is with-exclusive;
   the continuation INSTINCT is corpus-wide.

Honest findings-side result: raw finding quality and count are
COMPARABLE across arms, and the sets are complementary, not nested —
each arm holds exclusives (WITH: B9 void-closure commit, B7 version
provenance; WITHOUT: F9 sha-atomicity BLOCKING; SENTENCE: NEW-1
module-level crash defeating the verdict contract). Cross-arm
confirmations (vacuous sweep 3/3, path aliasing 3/3, seals namespace
3/3, unit-typo 2/3, byte-policy carry-across 2/3) give the statiker
harvest independent-instrument weight. Structural pattern reads
appeared in ALL arms (WITH: gate↔transaction protocol; WITHOUT:
repair-lands-at-one-seam; SENTENCE: three-exposure-classes) — the
FP5 cross-row clause's exclusive contribution is therefore
UNRESOLVED at n=1 (its firing log carries this).

Verdict (evidence surfaced; final signature judgment = operator's):
the skill's measured value at n=1 is the persistent bookkeeping
layer (MAP, registration, status denominators, disposition
taxonomy, MAP-anchored rotation) — exactly the compounding half a
one-shot cannot price — NOT more findings per run. The sentence
buys the conduct shape; only the skill buys the artifacts. Caveats:
n=1 per arm, not blind, one domain, controls corpus-loaded.

## Name cold-probe (BACKLOG item, run alongside Tier 1)

Fresh sonnet context, name only, no skill text. Result: RECRUITS,
strongly — the probe reproduced coverage-over-depth-first, whole-
object scope, recurring cadence, and a per-stop protocol with
per-item status marking, unprompted (transcript + grade:
cold-probe-transcript.md, same directory). Decision: KEEP the name.

## Next action

Tier 1: accept-as-clean. Tier 2: two-arm run booked thinking stays
in BACKLOG framing (trial-certification path). Cold-probe verdict
decides keep-or-rename.
