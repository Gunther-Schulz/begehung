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

## Tier 2

Signature spec: PLAN.md §Evaluation (written before the skill text).
Status: WITH-arm evidence exists — trial run 1 on pbs-office
(OBSERVATIONS.md, 5/5 with one deviation) — but graded in the
authoring session; per evaluation.md ("a control arm in a session
that has read the candidate is not a control") a clean two-arm run
needs fresh subagents on a neutral system. Not run today (minimum-
tier rule; the trial covers the serving path). Proposed: two-arm
run on a neutral small system when the next real round is due.

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
