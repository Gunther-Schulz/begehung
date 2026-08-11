# Tier-2 WITH arm — opus-begehung-tier2-with (verbatim, parts 1-3 + follow-up)

Brief: invoke begehung:begehung and follow it; task = robustness/coverage
review of ~/dev/Gunther-Schulz/statiker, read-only. No signature
vocabulary in the brief. The arm's MAP file is preserved beside this
file as tier2-with-MAP.md (copied from its scratchpad).

## Part 1/3

BEGEHUNG — statiker, round 1 — PART 1/3 (headline, coverage, B1-B2). Read-only; no repo writes. Working MAP in my scratchpad: /tmp/claude-1000/.../scratchpad/BEGEHUNG-MAP-statiker.md

HEADLINE. The record grammar and git transaction layer are genuinely well guarded — 271 tests pass (`python3 -m pytest tools/ -q`, HEAD 4655064, clean tree), the contract test is set-exact both ways with a stated red proof, and prior attack rounds have visibly hardened the closure gate. All 8 findings sit OUTSIDE that core and share one structure: the tools guard the record's GRAMMAR; nothing guards the PROTOCOL — which instrument runs at which seam, whether its verdict was honored, and the run state living outside the record file.

COVERAGE: 12 rows — 4 mechanically-guarded, 3 prose-covered, 5 dark. No global done-claim.

B1 — repo-key derivation is ambiguous AND unimplemented (row A6; silent; highest severity)
SKILL.md:600-608 specifies seal/queue/.paths under `~/.local/state/statiker/seals/<repo-key>/`, repo-key = basename + "-" + first 8 hex of sha256 of the toplevel's REAL path. No tool implements it, no test covers it. (Grep over scripts/ hit only two prose comments; positive control — the same pattern hit "queue" at tools/test_statiker_record.py:226 — so the tools/ zero is a true absence, not a dead pattern.)
Executed probe, three defensible readings of that one sentence for the statiker repo: `echo` → statiker-62aa4be2; `printf '%s'` → statiker-b7b1bba6; trailing slash → statiker-5e6628ef. The live on-disk directory is beat-the-books-173c7b8c, which I matched to the no-trailing-newline form. SKILL.md never says which.
Why it bites: the consumer is a SUCCESSOR desk, and CLAUDE.md:20-30 makes successors routine (a release during a live run means restart). A successor typing `echo` finds no directory, reads an empty queue, proceeds. Zero-hit-as-absence — losing queued findings that can include a design-killing abort.

B2 — the queue has no consumption marker (row A6; silent)
Live evidence: ~/.local/state/statiker/seals/beat-the-books-173c7b8c/…A8.queue still holds F127, F128, D88 under a header reading "Land these at the round's return, BEFORE the A8 outcome line." Those three DID land — tracker lines 7694-7696, correctly ahead of A8 at 7776. So a consumed queue is byte-identical to an unconsumed one, and its own header instructs a successor to re-land them. Re-landing mints duplicate ids, which is exactly the class B4 (part 2) shows passing every mechanical gate.

## Part 2/3

B3 — `waves` certifies an absolute-path collision as parallel-eligible (row A2; silent; real damage)
Executed probe: U1 write-set `src/a.py`, U2 `./src/../src/a.py`, U3 `/abs/repo/src/a.py`. Verdict: U1+U2 correctly normalized and `serialize: true` — that half works; U3 returned as its OWN group with `serialize: false`, i.e. WAVES_COMPUTED actively reports U3 as safe to run in parallel with units writing the same file. SKILL.md:876-880 declares this the desk's to catch at composition, but a leading `/` is trivially computable and unambiguously outside the declared repo-root-relative grammar, and the git tool already halts on the sibling composition defects (directory paths, ignored paths) — the precedent for mechanizing this class is in the system already. The damage is two parallel units writing one file.
Red-first: this probe record must not yield a clean partition; the U1/U2 relative case must stay green.

B4 — duplicate live ids pass every mechanical gate (row A3)
Executed probe: a tracker carrying two live `- D1 [COMMITTED]` entries with contradictory bodies returns SWEEP_CLEAN. Honestly disclaimed — the tool prints its own judgment residue (statiker_record.py:797-799) — and genuinely semantic in the general case, since re-using an id for a status change is the core append-only design. But a computable slice exists: a NEW entry at an id below its class's already-allocated maximum is near-certainly a collision, not a status change. The class has already bitten this system: the A8 queue's F127 records an `F50` citation imported from another namespace.

B5 — the /clippy-stats contract rests on a dated hand-read (row A5)
statiker_record.py:53-58 anchors the tag contract to "clippy-stats source, read 2026-08-07". I re-read the live source today (coding-clippy/plugin/commands/clippy-stats.md) and every claim HOLDS: ~20-line admission window (line 17), enum including COMPLETE (18-19), `\[AUTO-ACCEPTED\]` counted unanchored and bracket-carrying (38). So no drift today. The finding is the basis, not the claim: a hand-read of another repo whose maintainer cannot see this dependency. statiker's ADMISSION_WINDOW=20 guard keeps passing while the aggregation silently stops admitting the file — the failure has no local symptom.

B6 — no reconciliation of enumerated units against landings (row A7)
Landing annotations get FORM checks only (landing-indent, landing-blank, statiker_record.py:384-389). Nothing reconciles the [READY] unit enumeration against landings-or-holds, and the annotation is deliberately not an entry, so no gate counts it. A unit never dispatched has neither landing nor hold. Credit where due: the verify brief's per-R-line NOT EXERCISED demand is a real backstop — but per-requirement rather than per-unit, and resting on a fresh verifier's honesty rather than a mechanism.

## Part 3/3

B7 — version provenance has no home (row A9; silent; hits the trial's own measurement)
No tool parses the `Skill:` line — parse_tracker reads only Status and Phase. Live evidence: the beat-the-books tracker header records `Skill: statiker 0.2.13` plus a hand-invented continuation ledger ("cycles 1-6 ran 0.2.4 … cycle 9 runs 0.2.13"). That record reached Cycle 11 and round A8, last written 2026-08-08, by which date plugin.json stood at 0.2.51 (read from the plugin.json body across its commits, not commit subjects — only 2 commits carry "version:" in the subject). So the delivered record attributes cycles 10-11 and rounds A7-A8 to a version ~38 releases stale.
Structural, not desk sloppiness: SKILL.md declares Status and Phase the header's ONLY mutable fields, so a run spanning releases has nowhere to write the truth — and CLAUDE.md makes spanning routine. It matters because CLAUDE.md's trial procedure grades arms post-run on the raw records, making the version that experiment's independent variable.

B8 — nothing binds a gate verdict to the transaction it gates (row A12; the cross-row cure)
Executed probe: a tracker with `Status: [READY]` and a live `- D1 [PENDING]` returns SWEEP_HOLDS from the record tool and LOCK_CHECK_CLEAN from the git tool in the same breath. SKILL.md's "sweep runs FIRST at this seam" is prose only; closure likewise never reads [PENDING]. Every finding above is an instance of this structure, so one cure outranks the per-row patches: gate the lock on the tracker's own Status field — if Status is `[READY]`, sweep must be clean. That discriminates without over-firing, since a close-time lock carries COMPLETE or FAILED and SKILL.md explicitly allows a FAILED run to carry PENDINGs.
Red-first: my probe tracker is the must-fire case; a `Status: FAILED` tracker with a PENDING entry is the must-not-fire case.
Reach caveat, stated rather than buried: I checked whether records already carry booked verdict lines a reconciliation could read — zero in that tracker (loose control: "VERDICT" appears 8 times, all prose). But the tools landed 2026-08-07 and that run began 2026-08-05, so it is largely pre-tools; weak n=1 evidence.

DISPOSITION. All eight want BACKLOG.md entries; I own no write path, so none are booked — a gap I hand you, not a decision. B1, B3, B8 are mechanism-shaped with red-first arrangements stated. B5, B6 are prose-rest candidates with named backstops. B7 needs a design decision (a header field for version continuation) before it is dispatchable.

ROTATION. A12 (protocol) is the darkest row and the next lens; its cure would lighten A2 and A3 with it. A12 was no one's row until this round — the repo has no BEGEHUNG-MAP, so nothing tracked it. If this recurs, statiker's root is the map's home, and the next round reads the ratio first (12 rows, 5 dark).

## Follow-up answer ("and is there more?")

Yes — and one of them is worse than anything in the first three parts. I ran a bounded extra round rather than answer from feel.

B9 — a unit COMMIT lands over a VOID closure (row A12; escalates B8)
Executed, same probe repo: a tracker whose post-closure scopeless `- D1 [INVALIDATED]` kills an entry live at the closure. The record tool returns CLOSURE_VOID ("invalidates an entry live at the closure") — the premise-kill route that bars EVERY unit. The git tool, run next against that same repo, returns UNIT_START_CLEAN and then UNIT_COMMITTED with sha 66a8c412. Code landed in the repo over a design the record had already voided.
This is strictly more damaging than B8. B8 was a tracker commit at the lock seam; this is forcing point 4's own invariant — no implementation over an unclosed design — with the gate that detects the violation sitting in the same toolchain, already answering correctly, and simply not consulted. Same cure shape as B8, at the unit seam: `unit-start` reads the tracker it is building for and refuses on CLOSURE_VOID / CLOSURE_ABSENT / UNIT_HELD. Red-first: this probe is the must-fire case; a CLOSURE_LIVE + UNIT_DISPATCHABLE tracker is the must-not-fire case. Cheap, because `unit-start` is already the seam where the desk is told to stop.

Two rows I had marked guarded, now executed rather than assumed — both HOLD:
- Defang end-to-end (A5). Piped a report containing `[AUTO-ACCEPTED]` and `[PASSED]` through `quote`, then ran the stats reader's OWN commands against the output: `grep -c '\[AUTO-ACCEPTED\]'` → 0, `grep -c '\[PASSED\]'` → 0. The bracket-dropping defang genuinely defeats the real greps. B5's concern is the dated basis, not the mechanism.
- Filter line-number equality (A4). ARTIFACT_WRITTEN reports lines_in 19 = lines_out 19, blocks_blanked 1, and the entry F9 survives at line 19 with the Superseded lines blanked in place. The `corrects line <n>` dereference invariant holds under test.

One smaller observation: the live state directory carries two namespaces SKILL.md never defines — `~/.local/state/statiker/artifacts/<repo-key>/…A8.md` and a `…A8.report` file — alongside the three it does (`.seal`, `.queue`, `.paths`). Desks invented homes for artifact and report retention because the spec gives none. Same class as B1/B2: unnamed persistence with no lifecycle.

And structurally, yes, there is more by construction. Falling yield ends a lens, not the review — I closed round 1 on the protocol lens after two instances, and it produced a third the moment I pushed. Unwalked: A12 beyond the lock and unit seams (preflight, state-gate, filter, verify dispatch are each their own binding question); A8 (models register) I read but never probed; A12's cousin — whether `waves` output is honored at dispatch; and A1/A3/A10's deeper reach, where I confirmed the batteries run green but did not attempt to falsify their discrimination. Current MAP: 12 rows, 4 guarded / 3 prose / 5 dark, one round old.
