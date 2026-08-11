# Tier-2 SENTENCE arm — opus-begehung-tier2-sentence (verbatim, parts 1-5 + follow-up)

Brief: identical task, methodology skills barred, plus ONE instruction
sentence: 'Execute this task as a "Begehung" (a systematic inspection
walk) of the whole system.' — the ablation arm: the strongest cheap
competitor, exploiting the term's priors (cold-probe result). Same
grading note as the WITHOUT arm: opus + operator corpus, not bare model.

## Part 1/5

BEGEHUNG /home/g/dev/Gunther-Schulz/statiker (1/5) — read-only, no repo writes. Probe scratch: …/scratchpad/p1..p5 (throwaway git repos + trackers).

ASSESSMENT
The two shipped state machines are unusually well covered: `python3 -m pytest tools/ -q` → 271 passed in 13.7s; test_contract.py drives every subcommand of both tools over real invocations, asserts exactly one verdict line per row, and freezes the undriven remainder set-exact so a new verdict fails the suite until someone places it. Inside the record grammar and the git transactions I found no defect the suites miss.

Exposure sits in three other places: (a) two repairs that landed in one tool and not its sibling — the class test_contract.py:5-10 states it does not cover; (b) gates reporting clean because they examined nothing, with no denominator in the verdict the desk books; (c) the guarantees with the highest damage potential — irreversible units, budget exhaustion, verify's per-R coverage, attended mode, the seal/queue namespace, append-only itself — which have no mechanism at all and fail as non-events. All findings executed; none booked in BACKLOG.md (open there: worktree provisioning, write-set machine-token lint, attack-batching mint).

A. SILENT PASSES IN THE SHIPPED TOOLS

A1. sweep/lint go CLEAN over a tracker they parsed nothing from — the [READY] gate's mechanical half cleared with a live [PENDING] sitting in the file. Two byte-identical entry sets, one missing the `## Cycle` heading:
  with heading → SWEEP_HOLDS, "pending-latest @ line 6", exit 2
  without      → SWEEP_CLEAN exit 0, and LINT_CLEAN exit 0
SKILL.md:312-314 names the fact ("a tracker with no `## ` heading at all parses NO entries, silently") and routes no consequence. No verdict field carries an entry count or the head boundary, so the booked line cannot distinguish clean-over-3 from clean-over-0. Reachable, not theoretical: SKILL.md:245-251 tells the desk to run `lint` once the header and head are written — before any `## ` heading exists — and SKILL.md:94-98 books any unnamed verdict as a `record:` F-line, so a preflight halt recorded at run start parses as nothing. Cheapest close: report `entries: N` plus the head-boundary line in every verdict; no gate semantics change, ES-1's exclusion untouched.

## Part 2/5

A2. `closure --unit U<k>` cannot tell a nonexistent unit from a free one — a silent hold-clear. One tracker, U2 carrying a live hold:
  --unit U2  → UNIT_HELD (exit 2)
  --unit U22 → UNIT_DISPATCHABLE, amendments [], exit 0
  --unit U99 → UNIT_DISPATCHABLE, amendments [], exit 0
statiker_record.py:827-831 validates the token's FORM only; this is attack-8 N3's class with just the spelling half closed. The discriminator already exists in the same file — `known_units` in waves_over_units (statiker_record.py:941-953) knows which units the record names. SKILL.md:920-922 states "the argument-side validation catches only the `--unit` flag": an assurance wider than its predicate — it catches the flag's spelling, never its referent.

A3. The byte-policy guarantee holds in the record tool and fails in the git tool. SKILL.md:62-66 states it of both ("verdict and quote output emit at the byte level over the input's own bytes — a tool that re-spells a byte on output mints the second spelling the input rule exists to prevent"). statiker_record.py:236-244 implements it (emit() via sys.stdout.buffer, surrogateescape); statiker_git.py:78-79 `say()` is a plain print under stdout reconfigured errors="replace" (statiker_git.py:675-677). Measured on a tracked file named b"caf\xe9.txt" — `unit-start --write-set caf<e9>.txt --unit U1`, exit 0, UNIT_START_CLEAN, stdout as bytes:
  b'- F<n> [VERIFIED] unit U1 write-set: caf?.txt \xe2\x80\x94 basis: <the unit enumeration>'
  b'STATIKER-GIT VERDICT: {"verdict": "UNIT_START_CLEAN", "write_set": ["caf\\udce9.txt"]}'
The record tool on the same byte returns it intact: b'lint: basis-missing @ line 6: - F1 [VERIFIED] path caf\xe9.txt matters'. One path, three spellings — on the one verdict whose printed lines exist to be pasted into the record (statiker_git.py:20-23, "prints one paste-ready record line per write-set path"). Downstream, the record then declares a path that does not exist, and `waves` reads it as disjoint from a sibling unit's real path — the silent direction statiker_record.py:911-914 names in its own words.
Coverage: the git suite's byte tests (tools/test_statiker_git.py:997-1036) are all input-side verdict-correctness; TestES9ByteLevelEmit (tools/test_statiker_record.py:2285) has no git-side twin, and the paste-line round-trip test at tools/test_statiker_git.py:570 exercises an ASCII path only.

## Part 3/5

A4. An absolute write-set spelling reads as disjoint from the same file's relative spelling. One tracker declaring `src/a.txt` (U1), `/abs/repo/src/a.txt` (U2), `./src/a.txt` (U3), `src/../src/a.txt` (U4):
  wave 1: {U1, U3, U4} (overlap — serialize within wave)
  wave 2: {U2} (disjoint — parallel-eligible)
U1 and U2 name the same file and are offered for parallel dispatch. SKILL.md:878-881 declares this "a declaration defect, the desk's to catch at composition" — but SKILL.md:870-871 already fixes the contract as REPO-ROOT-RELATIVE, so `os.path.isabs` is a one-line lint. Note also that `spellings` in WAVES_COMPUTED surfaces aliases only WITHIN a normalization group; the cross-group alias, the dangerous one, produces no flag at all. Adjacent to the booked write-set entry (BACKLOG.md:28-38) but not covered by it — that one covers the declarator's spelling, not the path's form.

A5. Minor, same class as two already-closed variants: `filter --out` into an existing but unwritable directory → INTERNAL_ERROR exit 3 (PermissionError through the generic handler), where missing-parent and is-a-directory are both routed USAGE_ERROR (statiker_record.py:1134-1146). SKILL.md's catch-all reads INTERNAL_ERROR as a tool defect, so an invocation mistake books as one.

B. INVARIANTS WITH NO INSTRUMENT

B1. Append-only — forcing point 1 — has no check, though the tool itself created the material to run one. Probe: tracker pinned by `lock-commit`, then the live `- F1 [PENDING] …` line rewritten in place to `[VERIFIED]` (the move that converts a held gate into a clean one):
  before → SWEEP_HOLDS (pending-latest @ line 6)
  after  → SWEEP_CLEAN, and LINT_CLEAN
  `git diff --stat <pin> -- tracker` → 1 file changed, 1 insertion(+), 1 deletion(-)
Every downstream predicate is positional (corrects-line numbers, latest-line-per-id, post-closure ordering), and SKILL.md:226-231 names the insertion hazard explicitly. `grep -n diff` over both scripts: nothing compares a tracker against its pin. Shape of the close: a `pinned --tracker P --sha S` subcommand asserting the diff is pure append.

## Part 4/5

B2. The requirement head is invisible to every tool, so verify's coverage guarantee rests on brief wording alone. SKILL.md:1018-1027 demands a verdict per R-line (met / not met / NOT EXERCISED) and states the reason itself — "a requirement nobody checked returns exactly what one that passed returns". Probe: a tracker carrying R1.–R5. in the head plus `- V1 [PASSED] …` returns SWEEP_CLEAN with no R inventory in any field. The head exclusion (statiker_record.py:114-120) is right for entry parsing, but nothing reads `R<n>.` for a coverage count, so a verifier's table that silently drops a row returns what a complete one returns — the non-event moved one hop, not closed. The count is computable from material the parser already walks.

B3. The one damage-limiting rule has no instrument on either half of its predicate. `irreversible` and `Mode:` appear in neither script nor either suite (grep over plugin/skills/statiker/scripts/ and tools/). SKILL.md:441-450: "Every other bound in this skill limits waste; this one limits damage: unattended an irreversible unit never dispatches" — `closure --unit` returns UNIT_DISPATCHABLE regardless of both halves. UNIT_HELD proves the mechanized shape is available (a case-sensitive literal the closure reads). Same gap on SKILL.md:475-477, "an attended run never silently becomes unattended": no verdict surfaces the Mode line, while `late_intent` in every sweep/closure verdict is the pattern for exactly this resuming-desk duty (SKILL.md:136-141).

B4. Budget (SKILL.md:161-168, "Exhaustion never continues silently: … unattended it closes the run FAILED") — the token `Budget` is absent from both scripts and both suites. Enforcement is desk memory, in the mode that by definition has no operator watching. `trend` already counts resolved rounds, so the comparison has its input.

## Part 5/5

B5. The seal / queue / `.paths` namespace is prose only — `seals`, `sha256`, `repo-key`, `.paths` absent from both scripts and both suites. The derivation is intricate and load-bearing (SKILL.md:600-611: basename + first 8 hex of sha256 of the toplevel's REAL path, derived in the main checkout, never a linked worktree), and a successor desk is explicitly told to re-derive it. A mis-derived key yields an empty directory, indistinguishable from "nothing was queued" — and the queue is where findings and leg dispatches park during the append freeze.

B6. Tracker location, verified live today: the stats reader admits a run only as `.clippy/runs/*.md` (coding-clippy/plugin/commands/clippy-stats.md:10-27, "No `.clippy/runs/` → report 'no Clippy history' and stop"). Neither statiker script mentions `.clippy/runs` (grep: no occurrence). A tracker placed anywhere else passes preflight and every gate and is permanently invisible to the reader the trial's own comparison metrics depend on (SKILL.md:132-134 states the shared-convention guarantee). Positive half of the same read: the premises the tag contract rests on are INTACT — first ~20 lines admission, the closed Status/Phase enums, and `grep -c '\[AUTO-ACCEPTED\]'` counted unanchored WITH brackets, matching statiker_record.py:53-58 and ADMISSION_WINDOW=20.

C1. statiker_record.py contradicts itself about the write-set form, and the stale half is the module docstring — what a reader meets first. Docstring (statiker_record.py:22-36): "no literal write-set record-line form is spelled out in SKILL.md (only the LOCK's own `lock-set:` F-line is, :471-472) … flag this convention for desk/operator confirmation before relying on it against a live tracker." Inline comment in the same file (907-913): "The write-set record-line form is normative in SKILL.md (Implementation: …)". BACKLOG.md:175-185 closed it 2026-08-10. Both docstring citations have drifted too: SKILL.md:471-472 is now the attended-prompt text (the lock-set F-line sits at 486-487) and :499 is a lock-set re-read sentence (the write-set form is at 869-872). Same decay in BACKLOG.md:44 and :59 (SKILL.md:816, :471-478) — the repo's own symbol-anchored rule applied to its own citations.

NOT REACHED
Desk conduct itself (brief composition, attack-round independence, the relay loop) is unobservable from the repo; I graded only what artifacts and tools can be made to answer. No live run end-to-end, and I did not exercise the batched-trip worktree path (its provisioning is the booked READY entry).

## Follow-up answer ("and is there more?")

Yes. Second pass found one new executed class, two smaller items, and I can now state the remainder honestly.

NEW-1 (executed). A module-level failure defeats the verdict-line contract outright. `STATIKER_GIT_RETRY_BASE=abc python3 statiker_git.py state-gate` → bare traceback, exit 1, NO verdict line (the float() sits at statiker_git.py:62, outside main()'s try). SKILL.md:70-76 makes the verdict line the result and 0/2/3 the codes; exit 1 routes nowhere and the desk's halt handling keys on a line that never printed. Second trigger, same class, READ NOT EXECUTED (no 3.9 interpreter here): both tools use PEP-604 `str | None` in dataclass bodies (statiker_git.py:106, statiker_record.py:233), evaluated at class creation, with no `from __future__ import annotations` and no declared Python floor anywhere in the plugin (grep: no python_requires/requires-python) — a public install on 3.9 dies at import, again with no verdict line. Close: move both module-level computations inside main()'s try, declare the floor.

NEW-2. The model-resolution chain is prose only — `models` absent from both scripts and both suites. SKILL.md:664-673 (clippy.config/models → shipped register → strongest-available, "an unreadable models file halts the dispatch") and the register's certification duty (README, defaults/models) are desk-executed. A typo'd class key falls silently to the next step, and the "declared deviation" the terminal fallback owes has no detector. Same shape as A2/B3: a literal token with no lint.

NEW-3 (minor). `.pytest_cache/` is absent from .gitignore (only `__pycache__/` is there) — the repo's own verify by-product is undeclared untracked state, the exact class SKILL.md:1032-1047 makes the desk declare per path.

PROVENANCE CHECK before calling these new: the git tool's INPUT-side decode was fixed at attack-9 (OBSERVATIONS:3309-3310); the ES-9 encode-side mint (OBSERVATIONS:3712) sits wholly inside the record tool's R2/R3 design-attack context with no mention of the git sibling. So A3's carry-across gap is unlogged, not merely unbooked. Grep over OBSERVATIONS/PLAN/clippy-lineage: no hits for the heading, entry-count, or unknown-unit classes.

WORTH SAYING: the skill's own shipped no-corpus ethics (references/evidence.md) already carry the rules that name A1 and B2 — "an expected nothing is exactly what a dead instrument returns; an absence claim stands only once the instrument is shown live on a known positive". These are not doctrine blind spots; they are places the doctrine is not yet wired to a mechanism.

REACH, so you can price another round: OBSERVATIONS.md (4544 lines) was read by targeted grep only, PLAN.md by headings; the batched-trip worktree path, an end-to-end live run, and desk conduct were not exercised at all. Highest-yield next corner: the RESUME path — a successor desk reconstructing state from tracker plus seal namespace — which is where B3/B5 would actually bite and which no test touches.
