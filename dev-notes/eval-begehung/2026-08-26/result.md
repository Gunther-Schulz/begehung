# Eval — begehung v0.3.0, after the five-amendment arc (2026-08-26)

Arc: 1f71d32 → 7847336 (amendments 1-5, OBSERVATIONS 2026-08-26).
Object: the statiker repo, same object and tier as the 2026-08-11
two-arm run, chosen for comparability.

## Instrument, settled before either tier ran

- The frontmatter description is BYTE-IDENTICAL 1f71d32 → HEAD
  (`diff` over lines 2-3). No amendment touched triggering.
- The INSTALLED plugin copy is 0.1.2; HEAD is 0.3.0 (`diff -q`:
  differ). An eval reading the installed copy would have graded text
  three versions stale and returned a confident verdict about the
  wrong artifact. Both Tier-2 arms therefore read HEAD's SKILL.md by
  path.
- LIMITATION that buys: the with-arm loads the skill by file-read,
  not through plugin invocation, so this run does NOT exercise the
  serve path. The 2026-08-11 trial did; this one does not.

## Tier 1 — 12/12 clean

Full table: `tier1-result.md`. Re-run for one live variable only (the
competitor field has gained kaemmung since August). Matches baseline.

## Tier 2 — two arms, opus, one round each

Arms: `opus-begehung-eval-with` (read HEAD's SKILL.md as its method)
and `opus-begehung-eval-without` (same task, no skill). Control-arm
definition: CORPUS-LOADED, not bare — subagents inherit the operator's
global instruction files, and that corpus is the baseline in both arms.

Artifacts kept here: `with-arm-findings.tsv`,
`with-arm-MAP.review-copy.md`. The control wrote NO analysis file —
that absence is itself a result (item 6).

### Contamination check — traced, cleared

Sweep over the control's scratch for begehung's coined vocabulary hit
BEGEHUNG-MAP (4 files), prose-covered, mechanically-guarded, darkest,
rotation. EVERY hit traced to `work/`, the control's copy of the
TARGET repo, which is byte-identical to statiker's own files
(`diff -q` against the live repo). The control wrote zero files of its
own outside probe fixtures. Its OUTPUT carries none of the vocabulary.
Positive control for the sweep: "probe" 35 files, "statiker" 49.

Stronger than a clean control: statiker's own BEGEHUNG-MAP.md was
sitting in the control's tree — the method's artifact, in hand — and
the control still produced none of the method.

### Signature, item by item (PLAN Tier-2 1-10)

| # | element | with | without |
|---|---|---|---|
| 1 | MAP before search, structure-derived | PASS (existing MAP found and USED not replaced — the search-first clause fired) | ABSENT |
| 2 | lens pre-registered before searching | PASS (registered, `read-at` filled, before first search) | ABSENT |
| 3 | coverage counts, no done-claim | PASS (3 guarded / 10 prose / 0 dark of 13, with the caveat that 11 of 13 status cells went unread) | ABSENT (findings + a clean-probe list, no denominator over a row set) |
| 4 | structural disposition per finding | PASS (8 mechanism, 1 prose-rest, 0 empty; handed as ready-to-land) | PARTIAL (a RECOMMEND per finding — a fix shape, not a disposition; no booking) |
| 5 | rotation answers "is there more?" | UNMEASURED (one-shot; the staged follow-up probe was not run) | UNMEASURED |
| 6 | findings data file; message = pointer + counts | PARTIAL — file present, 7 tab-separated columns, message carried path + counts; but SELF-REPORTED composed at close, not appended as findings landed | ABSENT — findings delivered as SIX prose message parts, split by the size gate |
| 7 | `read-at`/`closed-at`/`reach`, supersession | PASS (680cdba both; reach 9 hold, 0 superseded) | ABSENT |
| 8 | executed basis w/ positive control, else label at head of `basis` | PASS in FORM (all 9 bases open `executed:`; 6 of 9 name a positive control) | PRESENT IN SUBSTANCE — the control marked OBSERVED vs DERIVED unprompted and ran positive AND negative controls on its own instruments |
| 9a | enforcer row | **ABSENT** | ABSENT |
| 9b | cross-cutting lifecycle row | **ABSENT** | ABSENT |
| 10 | `class` cell records the cross-row read | PASS (round-row table carries the column; the read ran and produced a HIGH finding) | ABSENT as a cell — though the control DID make cross-cutting observations (a growth curve tied to the repo's own F143) |

### Verdict

**Present-with / absent-without on the bookkeeping layer** — items 1,
2, 3, 6, 7, 10 — replicating the 2026-08-11 result against the amended
skill. Item 4 present vs partial, as in August.

**Finding quality: comparable, deep sets disjoint** — also as in
August. With: 3 HIGH / 5 MODERATE / 1 cross-row class, including the
refutation of TWO of the target's own MAP status cells against the
live record. Without: 2 BLOCKING / 3 smaller, with executed probes, a
discriminating control per finding, and one carried to the effect
altitude (a symlink-aliased write set run through to commit, where the
clobbered worktree — not the lost commit — turned out to be the real
severity). Neither arm's deep set contains the other's.

### The two failures, which are the run's most useful output

**Amendment 4 did not fire, in either arm.** No enforcer row, no
cross-cutting lifecycle row. Cause, located: the with-arm used the
target's EXISTING map, so first-run derivation steps 4-5 never ran.
The completion criterion was written for exactly this case — "a
missing enforcer or cross-cutting row is a finding at every
invocation, not only the first" — and it DID NOT FIRE. statiker
enforces (forcing points, a register, gates), so the criterion's
condition was met.
Reading: the words say every invocation; the PLACEMENT, under the
heading "First run derives rows from the system's STRUCTURE", reads as
first-run-only. Bundle review round 1 raised this shape (N6) and the
repair was to the words, not the placement. Booked, not patched here —
a patch would be the fourth repair lap on this clause, and the eval is
the first evidence that reached the artifact.

**Amendment 3's discipline is largely a corpus default.** The control
marked OBSERVED vs DERIVED and ran its own positive and negative
controls WITHOUT the skill. What remains skill-exclusive is narrower
than the amendment's text implies: not the demand for a positive
control, but the LABEL AT A FIXED CELL POSITION in a machine-readable
file, where it can be counted and checked rather than noticed in
prose. That residue is real but small, and it should be stated at that
size.

### Also worth keeping

- Item 6's self-reported miss (composed at close, not appended) is the
  append-as-you-go rule failing on its first live outing. The rule's
  purpose — an interrupted round still leaves its artifact — is
  unmet whenever the file is written at close.
- The with-arm EXTENDED the schema with a `red-first arrangement`
  column, all 9 rows populated. That is the "schema is a minimum"
  clause firing exactly as written.
- The `ready-to-land` mark appeared BESIDE the exit in all 9 rows
  (`ready-to-land · mechanism`), never in place of it — the invariant
  amendment 2 was careful to preserve, holding in the field.
- The control reproduced the founding incident precisely: findings
  delivered as six message parts for a person to absorb, with nothing
  booked. That is what a capable reviewer without this skill does by
  default, and it is what amendment 1 exists to end.


---

## Verifier for 0.3.1 — RUN AND PASSED (2026-08-26, after 9c10c08)

The failure this record names above ("amendment 4 produced nothing in
either arm") was repaired in 0.3.1 by moving the requirement to forcing
point 1 and making it MINT rather than detect. That repair's verifier,
named when it was booked and run here:

ARRANGEMENT — one opus arm, the 0.3.0 brief UNCHANGED (same task, same
object, same tier), reading HEAD's SKILL.md by path. The only changed
variable is the skill text.

PRE-STATE, established before the run: statiker's map carried 13 axis
rows and ZERO enforcer or cross-cutting rows.

RESULT — both rows MINTED and present at the round's end:
- "MINTED R4 — the ENFORCER held to its own invariants: does
  statiker's OWN development follow statiker's five forcing points…"
  status `dark (modelled)`.
- "MINTED R4 — CROSS-CUTTING lifecycle: per artifact the system
  holds… where does it live, who writes it, who reads it" status
  `dark (modelled)`.
Each was ALSO recorded as a finding of the round, which is what the
corrected forcing point prescribes — mint AND record, not one or the
other. Neither row was walked; both carry "R4 minted the row only",
leaving them to their own rounds.

CONTROL — the live map is untouched: 13 rows, 0 enforcer, `git status`
empty, HEAD still 680cdba. The 17 rows are in the review copy only.

OTHER 0.3.1 ELEMENTS, all fired in the same round:
- `lens` vocabulary used: 7 rows `map`, 1 `close`, 6 the registered
  lens. Forcing point 1's findings previously had no fillable cell.
- `modelled` appears 4 times, including on the FAILURE HALF of one
  finding whose text half was executed — the precision the restored
  scope clause exists for. Attribution caveat: one run cannot
  separate "the restored clause did it" from "this round had a
  modelled claim to make"; the label fired, the attribution is open.
- The round-row table was added with R1-R3's cells marked "(not
  recorded)" — graded provenance-fair by the arm, since that map
  predates the round-row form.
- `class` names the property compared over the rows, not just the
  rows: "what reads the artifact that makes this row's status claim
  true — a program, or a person at a momentary seam."
- Schema: 15 rows × 7 columns, 0 empty `basis`, 0 empty `disposition`.

THE CUT ALSO HELD. 0.3.1 removed the demand for a positive control as
a measured corpus default. This arm ran two differently-keyed absence
sweeps and showed BOTH instruments live on known positives before
claiming any absence — with the demand gone from the skill. The cut's
basis is confirmed by the behaviour surviving it.

NOT CERTIFIED BY THIS RUN, named rather than left implied: the arm did
not run statiker's own test suite, so this round does not certify that
suite green and the map's record-tool row still carries R3's basis.
