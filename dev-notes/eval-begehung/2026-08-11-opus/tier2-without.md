# Tier-2 WITHOUT arm — opus, methodology skills barred (2026-08-11)

Arm: opus-begehung-tier2-without-2 (general-purpose, opus), brief:
same neutral task wording, begehung and all methodology skills
barred, statiker repo read-only. Verbatim report, parts 1/7–7/7 as
received via SendMessage.

---

## Part 1/7 — lead and disclosure

Statiker robustness review (1/7) — lead + disclosure. Repo:
/home/g/dev/Gunther-Schulz/statiker at f357bed.

**Lead:** the repo's own test battery is RED on HEAD and has been
for four commits, including the 0.2.59 release review. The failing
test is the battery's own reach-detector — it fired correctly and
nobody read it. Beneath that, three of the record tool's gates
report CLEAN over records that are wrong, in ways the tool's own
text says are impossible. All five findings are one class: a
declared invariant with no mechanism enforcing it, in a tool whose
entire purpose is mechanizing declared invariants.

Findings, in order of the parts that follow:
1. (blocking) battery red on HEAD for four commits; the release
   ritual's evidence line stopped being written the day it went
   red — parts 2/7.
2. `corrects line <n>` reaches violation classes the tool declares
   unreachable; `SWEEP_CLEAN` over a malformed header, and over an
   undefanged tag literal in the operator's INTENT — parts 3/7 and
   4/7.
3. `waves` reports "parallel-eligible" for units that in fact
   collide — part 5/7.
4. `trend`'s trajectory verdict is dominated by bookkeeping rather
   than attack yield; flipped WORSENING→IMPROVING on findings that
   say nothing about yield — part 6/7.
5. (low) the one-verdict-line guarantee fails under a closed
   pipe — part 7/7, with the standing assessment.

**Disclosure, before anything else:** while probing history I ran
`git worktree add` inside the repo, which writes `.git/worktrees`
metadata — a repo write, against my read-only constraint. I
removed it immediately (`git worktree remove --force`, then
`git worktree prune`) and verified after: `git worktree list`
shows only the main checkout, `git status --short` is empty,
`.git/worktrees` no longer exists. No other repo write occurred;
all subsequent history probing ran in a scratchpad clone.

**Working files** (mine, nothing in the repo):
`/tmp/claude-1000/-mnt-data2t-hidrive--ffentlich-Planungsb-ro-Schulz-Projekte-25-06-PV-Georgendorf/9b2af452-851a-439b-83b9-21c0c2639c76/scratchpad/statiker-review/`
— `clone/` is the scratch clone used for per-commit runs,
`probe/` holds the fixture repos (`b`, `c`, `w`, `t`) behind
findings 2-5.

## Part 2/7 — Finding 1, BLOCKING: battery red on HEAD

`python3 -m pytest tools/ -q` at f357bed (clean tree, in sync with
origin/main) → `1 failed, 280 passed`. The failure is
`tools/test_contract.py::TestRuntimeVerdictBattery::test_every_emitted_verdict_is_driven_or_frozen`:
`WORKTREE_ADDED`, `WORKTREE_REMOVED` and `PATH_INSIDE_REPO` are
emitted by the scripts but neither driven by a battery row nor
named in `UNDRIVEN_REMAINDER`.

Per-commit runs (scratch clone, full suite):
- 62fc49c `271 passed` · c2c5baf `274 passed`
- da8fb76 (worktree lane lands) `2 failed, 279 passed` — the drive
  test AND `TestVerdictParity`
- f7ff9c4 `1 failed, 280 passed` (parity repaired, drive test not)
  · 47cfbe9 `1 failed` · f357bed `1 failed`

One of the two reds was noticed and repaired at f7ff9c4; the other
rode four commits to HEAD, through both a review-disposition and a
journal commit.

Worth stating plainly so the finding is not overread: the worktree
lane is **not** untested — `tools/test_statiker_git.py:1400-1490`
covers add, detached-HEAD, the inside-repo halt, and forced
removal with a red pair. What is missing is the *contract
battery's* row, i.e. the instrument that exists to catch a verdict
entering without conscious placement. Its assertion is set-exact
in both directions by design, precisely so a new verdict fails
until someone places it. It did exactly that.

Why it went unread — three converging causes, each checkable:
- `CLAUDE.md`'s `## Verify` block (:142-154) names only the
  SKILL.md operational-line-count metric and `ls plugin/skills/`.
  The test suite is named nowhere as a verify command — while
  SKILL.md (:47-53) declares the two scripts plus their battery to
  be *the executable spec*: "a divergence is graded against the
  battery, never against this page's wording".
- No active git hook (`.git/hooks` contains only samples).
- `dev-notes/OBSERVATIONS.md` records `Battery 264/264`,
  `Battery 271/271`, `Battery 271/271` at the 2026-08-10 releases
  (:4540, :4542, :4544). Both 2026-08-11 entries carry no battery
  line — including :4548, the 0.2.59 skill-edit review, which
  otherwise describes a thorough opus review with executed probes.

Repair: add `python3 -m pytest tools/ -q` to the CLAUDE.md Verify
block, and make the `Battery N/N` line a required slot in a
release journal entry. That line was the only thing re-reading
this instrument, and it lived in prose.

## Part 3/7 — Finding 2, part one: `corrects line <n>` reaches classes declared unreachable

**Mechanism.** `apply_supersession` (statiker_record.py:561-593)
decides shed/supersede by LINE NUMBER only — it never consults the
violation's class. `REPAIR_FORMS` (:209-215) declares
`status-enum`, `phase-enum` and `admission-window` unreachable, in
those words: *"header rewrite: Status and Phase are the record's
one mutable surface — no repair token reaches them"*. Nothing
enforces that declaration. The second half of the mechanism:
`owner = line_ids.get(n)` is None for any line that parsed no
entry — header lines, INTENT lines, ordinary prose — and the
admission test `owner in (None, e.id)` then lets *any* id's token
name such a line.

**Probe A — the header.** Fixture tracker carrying
`Status: bogus-status`:

baseline → `LINT_VIOLATIONS`, `lint: status-enum @ line 2:
bogus-status`, repair field as quoted above.

Then append one line, nothing else:
`- F1 [VERIFIED] record: corrects line 2 — basis: D1`

result → `LINT_CLEAN` (exit 0) and `SWEEP_CLEAN` (exit 0), while
line 2 still reads `Status: bogus-status`. The sweep is the
[READY] gate; it opens over a record whose header is not an enum
member.

**Consequence against the real consumer, not a hypothetical one.**
`/home/g/dev/Gunther-Schulz/coding-clippy/plugin/commands/clippy-stats.md:17-19`
admits a tracker only if its first ~20 lines carry a Status from
the closed enum (`in-progress`, `[READY]`, `PASSED`, `FAILED`,
`COMPLETE`). So the run silently drops out of every cross-run
metric the stats reader computes, while the record's own gate
reports clean. Note the verdict JSON does still carry
`"status": "bogus-status"` as a field — but the *verdict name* is
`SWEEP_CLEAN`, and SKILL.md's contract is that the desk books the
verdict line and that `SWEEP_CLEAN` clears the mechanical half.

Reachability for probe A specifically is mis-composition rather
than instruction: the verdict for `status-enum` correctly tells
the desk no token reaches it, so a compliant desk would not
compose this. What makes it live is that the token's whole reason
for existing is repairing mis-composed lines — an off-by-one in a
hand-composed `corrects line <n>`, or a number composed against
the filtered artifact rather than the tracker, lands here and
*clears a violation the desk never aimed at* while leaving the
intended one.

## Part 4/7 — Finding 2, part two: the tool recommends the shed

**Probe B — the operator's INTENT.** Fixture tracker whose head
carries `INTENT — make the thing [PASSED] when it works.` on
line 5.

baseline → `SWEEP_HOLDS`, `sweep: tag-literal-in-body @ line 5`,
and the verdict's own repair field reads: *"bookkeeping: append
`- <id> [<tag>] record: corrects line 5` — sheds violations only,
status untouched"*.

SKILL.md mandates that repairs be "COMPOSED FROM THE VERDICT,
never from memory". Appending exactly what the verdict dictates →
`SWEEP_CLEAN`, with `[PASSED]` still sitting on line 5
(`grep -n '\[PASSED\]'` confirms).

SKILL.md says of this exact case (:180-183) that an undefanged
bracketed tag literal in INTENT "holds every later sweep,
correctly, for the run's life", and that "in INTENT it is the
enforcement of the hand-defang duty". Two sentences of one spec
disagree, and the mechanism sides against the one that names the
purpose — by instructing the desk to do it.

The downstream effect is not cosmetic. clippy-stats greps
`[PASSED]`, `[ISSUES FOUND]` and `[AUTO-ACCEPTED]` **unanchored**
(:38-40 — I read the source; the repo's premise about that reader
is accurate). So the run reports a phantom verify result to the
shared corpus for as long as the tracker exists, while its own
record lints clean. The Implementation section's "shedding
acknowledges, never cleanses — flagged text still sits in the file
for foreign readers" is exactly right about the file, and exactly
the reason the gate should not have gone clean.

**Boundary, so the mechanism is stated precisely.** The
sweep-level codes (`pending-latest`, `killerless-dead`,
`basis-cites-invalidated`) are immune — probed with a token aimed
at a `[PENDING]` latest line: both `corrects-nothing` and
`pending-latest` stand. But the immunity comes only from
ordering — `sweep_checks` runs *after* `apply_supersession` and
its violations are appended later. It is not design, and a
refactor computing them earlier would lose it silently.

**Repair.** Gate the shed on class: a token may shed only codes
whose `REPAIR_FORMS` entry is `REPAIR_BOOKKEEPING`, and supersede
only members of `MACHINE_TOKEN_CODES`; anything else lints
`corrects-nothing` carrying the declared form. The classification
table already exists and already states the right answer — it is
simply not consulted at the decision point. Red-first arrangement
is in hand: probes A and B above both go green today and must go
red after.

## Part 5/7 — Finding 3: `waves` passes colliding units

Fixture with four units, all naming `src/app.py` in some spelling:
U1 `src/app.py` · U2 `src/app.py src/util.py` (two paths on one
line) · U3 `./src/app.py` · U4 `/abs/repo/src/app.py`

```
wave 1: {U1, U3} (overlap — serialize within wave)
wave 2: {U2} (disjoint — parallel-eligible)
wave 3: {U4} (disjoint — parallel-eligible)
```
`lint` over the same file: `LINT_CLEAN`.

Normalization does its job on `./` (U3 correctly joins U1). The
absolute spelling (U4) is disclosed in SKILL.md as "an alias
outside the grammar — an absolute or symlinked spelling — is a
declaration defect, the desk's to catch at composition", so I
count it as a named residue rather than a defect. **U2 is
undisclosed.** SKILL.md's grammar says "one REPO-ROOT-RELATIVE
path per line"; `UNIT_WRITE_SET_RE`'s `(\S.*)` swallows the whole
remainder into a single key, so a two-path line reads as one
exotic filename that can intersect nothing. Two units that both
write `src/app.py` are handed to the desk as parallel-eligible.

Reachability is ordinary, not exotic: SKILL.md places the
write-set lines at the [READY] enumeration, composed by hand.
`unit-start`'s paste-ready one-path-per-line output arrives later,
at dispatch — after the parallel decision has been made.

**The `spellings` field is not the backstop it reads as.** By
construction it can only report raw forms that normalize to the
*same* key — that is, aliases which already collided correctly. It
is structurally blind to aliasing that fails to collide, which is
exactly the silent direction `waves_over_units`' own docstring
names ("two spellings of one path reading as disjoint would
dispatch colliding units in parallel — the silent direction"). In
my fixture it reported the harmless `./` pair and said nothing
about U2 or U4. A desk seeing `spellings` populated has evidence
about the safe half only, presented in a shape that reads like
alias coverage.

**Repair.** Both cases are computable in the same positional style
as the `write-set-near-miss` check added in c2c5baf: whitespace
inside the path field, or a leading `/`, lints at composition
instead of dispatching colliding writers. That check already
exists for the *declarator* spelling for exactly this reason — the
path field simply was not given the same treatment. Red-first
arrangement: the U2 and U4 rows above must lint after the change
and must still produce today's `LINT_CLEAN` before it.

## Part 6/7 — Finding 4: `trend`'s trajectory is dominated by bookkeeping

Why it matters: SKILL.md says "The reply opening a repeat round
cites the record tool's `trend` output as its series read", and
the corpus rule it serves says a flat-or-worsening series indicts
the FORM — the repair shape, the instrument, the altitude. A wrong
trajectory therefore pushes the desk to re-open its own method on
an artifact of accounting.

**Probe 1 — a voided round's findings are charged to its
successor.** Fixture: A1 `[BIT]` with 2 findings; A2 `[VOID]
premise: wrong sha pinned` with 3 desk-re-derived F-lines (the
disposition SKILL.md prescribes for a voided round: "a voided
round's observations enter only as desk findings the desk
re-derives itself"); A3 `[ZERO-DELTA]` with 1 finding. True
attacker yield: 2 → 1.

Output: `trend: 2 round(s), findings [2, 4], trajectory WORSENING`

The VOID round is correctly excluded from the round list, but its
*span* is annexed by the next round — `bounds`' `prev` advances
only at resolved A-lines (:1080-1085). So the very findings the
spec routes into the record after a void are billed to the round
that follows.

**Probe 2 — bucket 1 is a different quantity from every later
bucket.** Same tracker plus 3 ordinary pre-attack investigation
F-lines (the normal cycle-1 shape):

Output: `trend: 2 round(s), findings [5, 4], trajectory IMPROVING`

The first window starts at line 0, so bucket 1 is
investigation+attack while later buckets are attack-only. The
verdict flipped WORSENING → IMPROVING on three lines that say
nothing whatever about attack yield, over an unchanged underlying
series of 2 then 1.

SKILL.md discloses the numerator's breadth ("per-round F-LINE
counts — every F-line in a round's span, not attacker findings
alone") but discloses neither the void-annexation nor the first
bucket's different composition, and the verdict carries no field
from which a desk could notice either. `trend_verdict`'s own
docstring is careful that "the ambiguous middle stays unclassified
rather than guessed" — the arithmetic is honest; what it is fed is
not.

**Repair.** Advance the window at VOID A-lines as well (or emit a
`voided_rounds` field so the merge is visible to the reader), and
start bucket 1 at the first `[DISPATCHED]` line rather than
line 0. If the counts are meant to stay all-F-lines, then the
printed line should say which buckets are commensurable — the
trajectory word is the part being consumed, and it is the part
that moved.

## Part 7/7 — Finding 5 (low) + standing assessment

**Finding 5 — the one-verdict-line guarantee fails under a closed
pipe.**

`python3 statiker_record.py waves --tracker … | head -1` → the
evidence line prints, then a `BrokenPipeError` traceback lands on
stderr, NO verdict line reaches stdout, and the pipeline exit code
is 0. The "never a silent death" catch-all (:1317) re-enters
`finish` → `emit` and dies again on the same broken pipe.

SKILL.md treats the single final verdict line as a hard contract
and routes "ANY verdict no section names" as a halt for the seam
that ran it — but a *missing* verdict line has no route at all,
and the exit code the desk observes is success. `statiker_git.py`
carries the same shape through its print-based `say`/`finish`.

`test_every_invocation_emits_exactly_one_verdict_line` cannot
reach this: it drives subprocesses with `capture_output`, so the
reader never closes early — an observation about that instrument's
reach, not a defect in it. Severity is low, but a desk piping to
`head`/`tail` to manage output is ordinary; I did it twice here
without thinking. Repair: catch `BrokenPipeError` at the emit
boundary and exit a defined code.

**Standing assessment.** The disciplines here are strong and
unusual: red-first arrangements written into test docstrings, a
frozen-remainder list making the battery's own reach enumerable
and forcing a decision on each new verdict, provenance comments
citing the attack round that minted each rule. Findings 2-4 share
one blind spot — where the repo states an invariant in prose
*next to* the mechanism (the repair-form strings, the "one path
per line" grammar, the round definition), the prose is trusted and
the mechanism is never asked whether it agrees. Finding 1 is that
shape one level up: the executable spec is declared normative in
SKILL.md and named in no verify command in the repo.

Two things I checked and found sound, needing no action:
- The tag-contract premise the defang design rests on is
  accurate — clippy-stats' greps do carry brackets and are
  unanchored, and its admission window does read a closed
  Status/Phase enum, as both `statiker_record.py`'s docstring and
  SKILL.md claim.
- `plugin/skills/statiker/defaults/models` is what SKILL.md and
  README call it: one entry carrying probe-then-certify provenance
  inline, resolution order stated in the file.

Optional note: no `.claude/required-reading.json`, though the
global corpus names that as the roster mechanism (`.claude/` holds
only `settings.local.json`). CLAUDE.md is the entry point here and
is read anyway — a decision, not a fix.

That closes the review. Nothing was written into the repo
(disclosure and its verification in part 1/7); probe fixtures and
the scratch clone remain under the scratchpad path named there if
any finding needs re-running.
