# Tier-2 WITHOUT arm — opus-begehung-tier2-without (verbatim, parts 1-5 + round 2)

Brief: identical task, methodology skills barred. NOTE for grading: this
arm is opus + the operator's global corpus (subagents inherit
~/.claude/CLAUDE.md), NOT a bare model — the delta measured is
skill-over-corpus.

## Part 1/5

STATIKER ROBUSTNESS/COVERAGE REVIEW (1/5) — read-only, no repo writes.

Probe scripts in my own scratchpad: …/scratchpad/{probe_quote.py, probe_git_bytes.py, probe_drop_handshake.py, probe_detached.py, probe_unit_start_link.py, probe_unit_typo.py, probe_freeze_header.py}

BASELINE: all three suites green as committed — record 170, git 92, contract 9 tests (run 2026-08-11). SKILL.md operational lines 1111 (repo Verify block). Every finding is a probe against committed code, not a code reading.

THE PATTERN (read first): four of the six code findings are one shape — a repair that landed at the seam where the defect fired and not at its sibling, or that pinned the FORM the defect took and not the CLASS. test_contract.py's docstring declares exactly that class out of its reach ("it does not cover behavioral carry-across (a repair landing at one seam and not its sibling)") and assigns it to "the per-repair parallel-site test pair in the suites, plus the attack rounds themselves". Those parallel-site pairs are not being written; the suites are indexed one test per fired incident. That is the coverage finding under the individual ones.

F1 (blocking) — the [READY] gate passes vacuously on entries above the first `## ` heading.
`sweep` returns SWEEP_CLEAN over a tracker whose live [PENDING] entries sit above the first `## ` heading, including the early state where no `## Cycle` heading exists yet — which is precisely where SKILL.md sends the desk to lint ("Run `lint` once the header and head are written").
Probe: tracker with `- F1 [PENDING] … — basis: unverified` and `- D1 [PENDING] …`, no heading → lint LINT_CLEAN, sweep SWEEP_CLEAN, waves WAVES_COMPUTED (waves=[], unplannable=[]). Same with a heading present and one entry above it. Only `closure` fails closed (CLOSURE_ABSENT).
Silent in both directions because the head-region exclusion (ES-1) suppresses the entry scan and the whole-file defang lint does not compensate: its scan reduces to the body whenever ENTRY_RE matches (statiker_record.py:451-459), so a well-formed entry line is an entry for the defang exemption and not an entry for any gate. TestES1HeadRegionExclusion pins only the must-not-fire direction, and its fixtures are deliberately non-entry-shaped bullets (`- V2 an operator bullet inside the head`).
Consequence: forcing point 2's stated condition — "no entry's latest line is [PENDING]" — is reported met by the instrument that computes it, over zero entries.
Cheapest mechanism: no verdict of any subcommand reports how many entries it parsed. An `entries: <n>` field, plus an evidence line when entry-shaped lines sit in the head region, would make the vacuous pass visible; today no consumer can tell "clean" from "examined nothing".

## Part 2/5

F2 (blocking) — `closure --unit` validates the id's FORM, never its EXISTENCE: a one-digit typo clears a hold.
Probe over a tracker where U1 is HELD (`- D2 [AUTO-ACCEPTED] unit U1 held: …`) and U2 carries an amendment:
  --unit U1  → UNIT_HELD (correct)
  --unit U11 → UNIT_DISPATCHABLE, amendments=[]   ← hold silently cleared
  --unit U2  → UNIT_DISPATCHABLE with its amendment
  --unit U21 → UNIT_DISPATCHABLE, amendments=[]   ← amendment silently dropped
  --unit U7  → UNIT_DISPATCHABLE (unit never existed)
This is attack-8 N3 verbatim ("a mistyped id ('3','u3') matched no scope line and fell through to UNIT_DISPATCHABLE — a silent hold-clear"). Its repair added `re.fullmatch(r"U\d+")` (statiker_record.py:827), closing the spellings that fail the regex and leaving every typo that passes it. `closure --unit` is the per-unit dispatch gate (SKILL.md:87), so forcing point 4's strongest gate returns green on a wrong digit and the brief then travels without the amendments whose transport is the gate's whole purpose.
In reach: the same module already computes the known-unit set (`waves_over_units`, known_units from unit-scoped entries), and by SKILL.md's own Implementation rule every real unit has a write-set line — so an unknown `--unit` is decidable, not a judgment call.

F3 (blocking) — nothing links unit START to unit COMMIT; "every later modification is the unit's own" is desk conduct only.
Probe: tracked file `mod.py` carrying an operator's UNSTAGED draft.
  unit-start  → UNIT_COLLISION {" M", "mod.py"}   (the guard itself works)
  unit-commit → UNIT_COMMITTED, sha a60b7b3
  git show HEAD:mod.py → 'operator draft, uncommitted'
The commit seam re-reads column ONE only (statiker_git.py:593-594, deliberate per its own comment), so the column-two case START exists to catch is unguarded there, and the tool cannot know whether START ran or whether its halt was honored. The LOCK has the analogous handshake (`--drop` acknowledgement, HALT_DROPS_STALE/UNACKNOWLEDGED); the unit path has none.
Silent in the worst direction: the desk books UNIT_COMMITTED as evidence the unit landed its own work, while the operator's uncommitted draft is now in history under the run's authorship. Given the skill's stated threat model — "the failure this skill exists to prevent is skim-and-build under momentum … top-tier models exhibit it too" — an implementer skipping START or proceeding past its halt is inside the model, not outside it.

## Part 3/5

F4 (high) — the byte-level emit rule (ES-9) was never carried to the git tool, so the drop handshake cannot be satisfied by pasting.
SKILL.md:62-66 states the byte policy for both tools; SKILL.md:524-529 requires `--drop` be "PASTED from the verdict line, never re-typed", because "two spellings of one byte deadlocked this handshake".
Probe, repo containing `caf\xff.txt` with staged operator state on it — lock-check stdout verbatim:
  evidence line: `collision (staged operator state): M  caf?.txt`   ← byte destroyed ('?')
  verdict line : `{"drops": [{"path": "caf\udcff.txt", …}]}`        ← JSON escape; raw 0xff appears nowhere in stdout
lock-commit with each spelling a desk could paste:
  `caf?.txt`      → HALT_DROPS_STALE
  `caf\udcff.txt` → HALT_DROPS_STALE
  real argv bytes → LOCK_COMMITTED   (the one spelling the tool never prints)
SKILL.md's route allows one retry, then "a second mismatch OF ANY KIND halts the lock uncommitted" → unattended the run closes FAILED, under a diagnosis that names the wrong cause ("the tree moved between check and commit, or the `--drop` list was mis-composed") and two verdict sets that look identical to a reader.
The existing test (TestAttack9PathDecoding.test_lock_drop_handshake_completes_non_utf8_byte_path) passes `--drop self.NAME` — its own Python variable, never the tool's printed output — so it certifies the internal comparison along a path the desk cannot take. statiker_record.py has the fix (`emit()` at byte level, ES-9); statiker_git.py uses `print` under stdout reconfigured to errors="replace" (statiker_git.py:78, 675-677).

F5 (medium) — `quote` mutates report bytes: the NIT1 repair landed in the tracker parser and not in its only sibling.
`split_lines()` exists precisely because "str.splitlines() also breaks on U+000C, U+2028 and U+0085" (statiker_record.py:318-323, attack-9 NIT1). `cmd_quote` calls `defanged.splitlines()` (line 1245) — the module's only other line-splitting site.
Probe, one input line each → output block:
  "alpha\x0cbeta" → "> alpha" / "> beta"  (form feed deleted)
  U+2028, U+0085, "\x0b", "\r" between alpha/beta → same split, separator gone
So an attacker's report line carrying any of five separators enters the pinned record as two lines with the separator deleted — a second, unsanctioned mutation under a rule naming defang as "the one sanctioned mutation" (SKILL.md:738-740). ES-9's quote test covers the \xff class only. Minor sibling: a whitespace-only report line becomes `"> " + spaces`, i.e. trailing whitespace, which the same rule's own parenthetical says target-repo hooks may strip.

## Part 4/5

F6 (medium) — detached HEAD and a linked-worktree cwd defeat the pin guarantee silently.
Probe A, main checkout with HEAD detached: preflight PREFLIGHT_OK → state-gate STATE_CLEAN → lock-commit LOCK_COMMITTED sha 88d629a; `git log main` does not contain it, branch = <none>. Everything downstream still works (`filter` reads `git show <sha>:tracker` fine), so the run completes normally while its three certified surfaces — pinned record, lock commit, unit commits — sit on no branch.
Probe B, invocation cwd inside a linked detached worktree: PREFLIGHT_OK, unit-commit UNIT_COMMITTED d5837c6, main unaffected.
The state gate reads merge/rebase/cherry-pick/revert by design, and "HEAD is on a branch" is neither an operation-in-progress nor a pinnability question as preflight defines it (preflight tests `check-ignore` only). dev-notes already carries "exotic git layouts (bare, GIT_DIR, worktree .git files) unexercised" as honest residue; detached HEAD is not named there, and it is the case the skill's own worktree provisioning makes reachable — a failed `git worktree remove` is booked as an F-line and the worktree survives.

F7 (medium) — the append freeze is computable from the record and unchecked; the XDG state namespace is prose-derived end to end.
`grep -rn "local/state|seals|\.queue|\.paths|repo-key" plugin/skills/statiker/scripts/ tools/` → zero hits. Three file kinds (`.A<n>.seal`, `.A<n>.queue`, `.<round>.paths`) under a key the desk derives by hand from prose (basename + first 8 hex of sha256 of the toplevel's REAL path, "derive it in the MAIN checkout, never a linked worktree"). No tool computes the key, no test exercises it, and every failure mode is a non-event: a key derived one way and re-derived another leaves a successor desk finding no seal and no queue, with nothing in the record showing either existed.
The freeze itself is decidable from the tracker — a live round is a latest A-line tagged [DISPATCHED] with no resolving line, so any F/D/R line after it is a breach. Probe: `- A1 [DISPATCHED] …` followed by two appended entries → sweep SWEEP_CLEAN, lint LINT_CLEAN. `trend` already reads DISPATCHED lines for its window, so the data is in hand.
Same family, booked READY in BACKLOG.md already: worktree provisioning joins the git tool. Not booked: the tree claim itself ("tree == lock commit") — one of the three premise-break causes that void a whole priced round, checkable with one command, with no subcommand covering it.

## Part 5/5

F8 (low) — header fields beyond Status/Phase are unlinted and never cross-checked.
`Budget:` is the run's only bound over every repeating seam ("Exhaustion never continues silently"); `Skill:` is the only record trace of CLAUDE.md's release-during-live-run hazard. Probe: a header carrying neither, `Status: PASSED`, and no V-line anywhere → LINT_CLEAN, SWEEP_CLEAN. Nothing counts rounds against the budget although `trend` counts rounds, and nothing cross-checks Status/Phase against the record's own state — those two fields being exactly what the stats reader the trial's grading rests on reads.

COVERAGE ASSESSMENT
Strong where mechanized: 271 green tests, red-first provenance cited per case, a contract battery that states its own two-layer reach honestly, and a sweep that PRINTS its judgment residue instead of absorbing it. That last habit is the repo's best practice and is why F1 and F7 read as gaps rather than as misrepresentation.
Weak in three specific ways:
1. No verdict carries the REACH of the check that produced it — no entry counts, no known-unit list — so a degraded check is indistinguishable from a clean one. F1 and F2 both live in that blind spot, and both are cheap to close from data the module already computes.
2. Tests are indexed by fired defect, so sibling seams stay unwritten. F4 and F5 are literally the unrepaired halves of repairs already made, and test_contract.py's own docstring predicted that class.
3. The two tools duplicate their shared rules by hand (byte policy, containment, path grammar). F4 is that duplication drifting. dev-notes already carries the attack-9 recommendation for ONE shared path-grammar function consumed by both; it was not taken.

Priority if you act on one thing: F2, then F1 — both are gates returning green over nothing, both fixable inside statiker_record.py with data it already has.

NOT COVERED BY ME (stated as gaps, not clean): no live run of the skill's conduct, so the prose forcing points are unexercised; no review of PLAN.md/dev-notes design decisions; no deep attack on trend/filter semantics; no bare-repo or GIT_DIR layouts. My probes ran on Python 3.14 / git as installed here; I did not vary either.

## Follow-up answer ("and is there more?") — round 2, part 1/2

YES — SECOND ROUND, 4 MORE (1/2). New probes: probe_sha_atomicity.py, probe_waves_filter.py (same scratchpad dir as before).

F9 (BLOCKING) — the booked sha is not the commit the tool made, and the readback compares against the wrong commit.
`commit_with_retry` runs `git commit` and then a SEPARATE `git rev-parse HEAD` (statiker_git.py:415); `head_shown_paths()` likewise reads HEAD, not the sha just created (:366-376). SKILL.md blesses parallel units on one shared index ("commits serialize; the tool's capped retry absorbs the contention"), so another writer landing between those two commands is in-design.
Probe (a post-commit hook occupies the window deterministically — same mechanism as a sibling unit committing there):
  verdict: {"verdict": "UNIT_COMMITTED_EXTRAS", "write_set": ["unit.txt"], "sha": "5c97b5d", "extras": ["sibling.txt"]}
  git log: 5c97b5d sibling unit U2 / 6aaef57 unit U1 / 5865397 base
  the commit actually carrying unit.txt: 6aaef57
Two defects in one verdict. (1) The landing annotation would read `unit U1 landed: 5c97b5d` — another unit's commit — and SKILL.md calls that annotation "what makes resume reliable". (2) `extras: ["sibling.txt"]` is a false extra, and SKILL.md routes extras as "recorded as collision-class contradiction and brief exclusion, never reverted" — so the desk books a finding against a legitimate sibling file and tells the attacker to treat it as outside the frozen surface. That is exactly the consequence attack-8 B1 recorded for the C-quoting case ("the 'extra' was the tracker, which the desk then excludes from the attack surface").
Honest caveat: my window-occupier is a hook, not a live sibling; the mechanism under test is the two separate HEAD reads, which are unconditional. Fix shape is small — take the sha from the commit's own output and read the diff at that sha rather than at HEAD (the corpus rule about the verifier's own output, applied to git).

F10 (high) — `waves`' alias report is blind to the exact alias class SKILL.md hands the desk.
statiker_record.py:911-914 names the hazard itself: "two spellings of one path reading as disjoint would dispatch colliding units in parallel — the silent direction." Normalization is lexical, so an absolute spelling normalizes to itself and becomes its own key with one raw spelling — `spellings` stays empty.
Probe: U1 declares `src/a.py`, U2 declares `<repo>/src/a.py` plus `src/b.py` (the same file, two spellings) →
  waves: [{U1, serialize:false}, {U2, serialize:false}]   ← parallel-eligible
  spellings: {}                                            ← the alias report, empty
SKILL.md calls this "a declaration defect, the desk's to catch at composition", but `waves` exists to replace exactly that eyeball, and its verdict hands the desk nothing to catch it with. `os.path.isabs` closes the absolute case in one line, and `repo_paths` already computes the repo top needed to normalize it properly.

## Round 2, part 2/2

F11 (medium) — `filter` accepts any sha with no staleness signal, and "wrong sha pinned" is one of the three premise breaks that VOID a whole round.
Probe: same tracker, two lock commits; filter at the current lock and at the STALE earlier lock both return ARTIFACT_WRITTEN with an identical field set (`sha, out, source_tracker, lines_in, lines_out, blocks_blanked, sections_blanked, lines_blanked, form`). Only lines_in/out differ, and the desk has no expected value to compare them against — the artifact of a superseded design reads exactly like the artifact of the current one, and the round's whole cost is spent before anyone can tell.
A discriminator is one command: the tracker's own newest commit (`git log -1 --format=%H -- <rel>`) beside the given sha; a mismatch means the pin is not the newest state of that record, which is the desk's cue to check whether a re-lock happened. Not a gate — a field in the verdict the brief already quotes.

F12 (low-medium) — a unit write-set may name the tracker; the record's single-writer property is unguarded at the unit seam.
Probe: `unit-commit --write-set .clippy/runs/t.md -m "unit U1"` over an appended tracker → UNIT_COMMITTED, sha 36d83c8, the record change committed as the unit's own output. The tool guards directories, symlink leaves, ignored paths and staged collisions, but nothing says "this path is the run's own record". Structural reason: unit-start/unit-commit take no `--tracker`, so the tool cannot know. Trigger needs a composition error in the brief, so this is defence-in-depth rather than a live hazard — but the record is one of the run's three certified surfaces and it is the one with no mechanical owner.

THE SERIES READ (the answer to your question, stated as evidence rather than as reassurance)
Round 1: 8 findings. Round 2: 4 more, one blocking, in corners I had explicitly named as not covered. Yield is declining but nowhere near zero, so I cannot claim coverage — by the repo's own standard a design closes on a zero-delta round, and I have not had one.
Where a third round would go, in my order: (1) the `corrects line <n>` supersession machinery under adversarial chains — heavily tested, so the expected yield is low but the blast radius is the closure gate; (2) `trend`'s round-bounding when VOID rounds interleave, since VOID spans fold into the next round's counts and `trend` is what the desk must cite before repeating a round; (3) the filter's line-alignment claim under CRLF and missing-trailing-newline trackers (alignment holds, but bytes change — I read the code and did not probe it); (4) exotic git layouts — bare, GIT_DIR set, submodules — which dev-notes already carries as unexercised residue; (5) the SKILL.md prose itself under a live run, which is the largest uncovered surface of all and the only one that tests the twelve findings' actual consequence on desk conduct.
