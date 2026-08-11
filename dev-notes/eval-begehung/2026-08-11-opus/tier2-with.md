# Tier-2 WITH arm — opus, begehung invoked (2026-08-11)

Arm: opus-begehung-tier2-with-2 (general-purpose, opus), brief:
invoke begehung:begehung, neutral task wording, statiker repo
read-only. Verbatim report, parts 1/6–6b/6 as received via
SendMessage.

---

## Part 1/6 — lead and process gap

**Lead.** The repo's own guard net is RED at origin and has been
for four commits — `pytest tools/` at f357bed returns `1 failed,
280 passed`, and SKILL.md declares those suites the "EXECUTABLE
SPEC" against which any divergence is graded. The structural cause
is that nothing runs them: the declared Verify section names two
commands, neither a test, and no git hook invokes the suite. Three
further findings are probe-backed defects that ship wrong output
silently; one is a public packaging exposure. The repo was never
written to (`git status --porcelain` clean after every step); all
working files are in scratchpad, paths in part 6.

**Process gap first, because it is still live.** The scratchpad is
NOT per-agent — it is shared across this session's team. My MAP
write to `…/scratchpad/BEGEHUNG-MAP-statiker.md` was flagged by
the writer-claims gate as overwriting a file another arm
(`aopus-begehung-tier2-with-f2faf6edb3fccff6`) had written inside
the claim TTL. Staging mode warned rather than denied, so the
write landed and I very likely clobbered that arm's MAP. I did not
read its content — that would contaminate my arm — and cannot
restore it. My own copy sits at an unambiguous path (part 6). If
the sibling arm needs its MAP, treat it as lost. For future
parallel arms the briefs need disjoint scratch paths: "your OWN
scratchpad" is not true of this directory.

**Skill-version note.** The Skill load served begehung 0.1.1 while
0.1.2 is pinned. I read the delta at
`/home/g/.claude/plugins/cache/begehung/begehung/0.1.2/skills/begehung/SKILL.md`.
Both added clauses are exactly about my situation — a walker with
no write path builds the MAP as a scratch review copy and says so,
and dispositions hand over as ready-to-land blocks with their
landing triggers named. I followed 0.1.2.

## Part 2/6 — F1 BLOCKING: the executable spec is red at origin, four commits deep

`python3 -m pytest tools/ -q` at f357bed (== origin/main) →
`1 failed, 280 passed`. The failure is
`tools/test_contract.py:612
TestRuntimeVerdictBattery::test_every_emitted_verdict_is_driven_or_frozen`:
the verdicts `PATH_INSIDE_REPO`, `WORKTREE_ADDED` and
`WORKTREE_REMOVED` are emitted by the git tool but neither driven
by a battery row nor listed in `UNDRIVEN_REMAINDER`.

Bisected by extracting each commit with `git archive` into
scratchpad (no repo write), running `tools/test_contract.py` only:

- c2c5baf → `9 passed`
- **da8fb76 → `2 failed, 7 passed`** (the worktree-subcommand
  commit)
- f7ff9c4 → `1 failed, 8 passed`
- 47cfbe9 → `1 failed, 8 passed`
- f357bed (HEAD == origin/main) → `1 failed, 8 passed`

The two failures at da8fb76 were the battery-coverage one plus
`TestVerdictParity::test_every_emitted_verdict_is_routed_in_skill`
(test_contract.py:631). The second was cured by f7ff9c4, whose
commit message is about SKILL.md citing the worktree subcommands —
that parity test went green as a side effect of prose work, not
because anyone ran the suite. The first has never been addressed
and is published.

Weight, from the system's own words — SKILL.md:48-52: "The two
scripts plus their red-first battery … are the EXECUTABLE SPEC of
the record grammar and the transaction semantics: the contract
lives there, this page keeps principles and desk conduct, and a
divergence is graded against the battery, never against this
page's wording." The nominated authority-of-record is the thing
that is red.

**F1b — label-vs-body drift in the closure record.**
BACKLOG.md:74-80 books da8fb76 as Done with the verification claim
"battery 99/99". That is true of `tools/test_statiker_git.py` —
`grep -cE '^def test_|^    def test_'` returns exactly 99 — and
false of the contract battery, which that same commit turned red.
The Done entry reads as a green closure standing over a body that
was red at the moment it was written. Ready-to-land disposition,
landing trigger *next BACKLOG Done entry*: closure lines name
WHICH battery, or cite `pytest tools/`.

## Part 3/6 — F2 nothing runs the suite; F3 guard reach falsified

### F2 — nothing runs the suite (the structural cure; outranks the F1/F3 patches)

- CLAUDE.md:142-154, the "## Verify" section, names exactly two
  commands: an `awk` operational-line count over SKILL.md, and
  `ls plugin/skills/`. Neither runs a test.
- `git config --get core.hooksPath` →
  `~/dev/Gunther-Schulz/dotfiles/git/hooks`.
  `grep -rn "statiker\|pytest"` over that directory returns only
  unrelated string literals inside the plugin-bump hook's own
  self-tests — no invocation of this repo's suite in pre-commit or
  pre-push.

So F1 could ride to origin with nothing to catch it, and did.
Ready-to-land disposition, landing trigger *next commit touching
CLAUDE.md*: `python3 -m pytest tools/ -q` becomes the first
command in the Verify block. Red-first arrangement: at f357bed
that command must print `1 failed`; once F1/F3 are repaired it
must print all-passed — one command, discriminating in both
directions, today.

### F3 — the coverage guard is pinned to a hardcoded list, not to the parser (executed mutation)

`GIT_SUBCOMMANDS` (test_contract.py:189) is a literal set of six.
The parser (statiker_git.py:731-759) defines eight —
`worktree-add` and `worktree-remove` are absent from the literal.
`test_battery_covers_every_subcommand_of_both_tools`
(test_contract.py:595) compares the battery's observed rows
against that literal, so it structurally cannot notice a lane the
literal omits.

Probe, in a scratchpad copy of the repo (repo untouched): I added
a `bogus-lane` subcommand to statiker_git.py emitting only the
**already-existing** verdict `STATE_CLEAN`. Confirmed it runs —
`STATIKER-GIT VERDICT: {"verdict": "STATE_CLEAN", "ops": []}`.
Full suite over the mutant: `1 failed, 280 passed`, byte-identical
to the baseline over the unmutated copy. No test in the repo
notices an entire new git lane with zero coverage.

Discriminating pair: the worktree lanes *were* caught — but only
because they introduced new verdict *names*. The guard
discriminates new verdicts, not new lanes, while its name and
message read as subcommand coverage.

Ready-to-land disposition, trigger *the F1 repair commit*: derive
the declared set from the parser's own subparser choices instead
of restating it. Red-first: the `bogus-lane` mutant must fail
`test_battery_covers_every_subcommand_of_both_tools`; the
unmutated copy must not.

## Part 4/6 — F4: `quote` violates the byte policy SKILL.md states, using the function the module forbids elsewhere

SKILL.md:64-68: "verdict and quote output emit at the byte level
over the input's own bytes — a tool that re-spells a byte on
output mints the second spelling the input rule exists to
prevent."

`split_lines()` (statiker_record.py:343-353) exists *precisely
because* `str.splitlines()` also breaks on U+000C, U+2028 and
U+0085 — its docstring records the attack-9 incident where that
"invented a line the file does not have". But `cmd_quote`
(statiker_record.py:1273 and 1277) builds both the block body and
the reported `lines` count with `defanged.splitlines()`.

Executed probe against the real script (stdin only, no repo
write), input `alpha<CH>beta`:

| character | source lines by the record's own rule | block body lines | survives |
|---|---|---|---|
| U+2028 LINE SEPARATOR | 1 | 2 | no |
| U+000C FORM FEED (the attack-9 char) | 1 | 2 | no |
| U+0085 NEL | 1 | 2 | no |
| U+000B VERTICAL TAB | 1 | 2 | no |
| U+001C FILE SEPARATOR | 1 | 2 | no |
| TAB (control case) | 1 | 1 | **yes** |

Every defect case returns body `['> alpha', '> beta']`: the
character is deleted, a `> `-prefixed line is fabricated in its
place, and the verdict's `lines` field counts the fabrication. The
TAB row is the contrast establishing that the probe measures byte
fidelity rather than merely that quote ran.

Where the wrongness lands: the quote block is the record's
verbatim evidence of an attacker's superseded text, pasted into
the tracker by the desk. A report containing any of those
characters is booked as text the report never held, carrying an
extra line indistinguishable from a legitimate quoted one.

Why it survived: the byte test `TestES9ByteLevelEmit`
(test_statiker_record.py:2325-2348) uses `BAD = b"\xff"` only. It
certifies the invalid-UTF-8 class while its docstring asserts the
general property — an assurance wider than the predicate it
establishes. This is exactly the class test_contract.py's own
docstring (lines 6-10) names as out of reach: "behavioral
carry-across (a repair landing at one seam and not its sibling)".
attack-9's repair landed in `split_lines` and never crossed to
`cmd_quote`.

Ready-to-land disposition, trigger *any commit touching
statiker_record.py*: `cmd_quote` uses `split_lines(defanged)` and
reports `len(split_lines(block))`. Red-first: the U+2028 row must
show 1 body line with the character present; the TAB row must
stay unchanged.

## Part 5/6 — F5 stale enumeration; F6 payload under published version

### F5 — SKILL.md's tool inventory is a stale enumeration

SKILL.md:45-48 describes the git tool as "git transactions: the
run-start preflight, the LOCK commit, unit START and COMMIT". The
worktree lanes are missing from that list; they are covered
correctly later at SKILL.md:695-708. Minor alone, but it is a
label standing over a body that grew, in the paragraph a desk
reads first. Disposition: prose-rest is defensible — the backstop
is that SKILL.md:695-708 is correct — but note the F3
parser-derived check would not catch this, so if it is to be
mechanized it needs the same derivation applied to the prose
enumeration.

### F6 — 110 payload lines pushed under an already-published, unchanged version

`git diff --stat 62fc49c..f357bed -- plugin/` → `SKILL.md | 37`,
`statiker_git.py | 58`, `statiker_record.py | 32`; 110 insertions
across three payload files. `plugin.json` reads
`"version": "0.2.59"` at **both** ends.
`git branch -r --contains 62fc49c` → `origin/main`, so all of it
is published.

Consequence: anyone whose `claude plugin update` resolved 0.2.59
while origin sat at 62fc49c holds a 0.2.59 lacking the worktree
lanes, the write-set near-miss lint, and 37 lines of SKILL.md —
and because the updater compares version numbers only, it reports
already-latest indefinitely. That is verbatim the failure the
global pre-commit hook's own docstring says it exists to guarantee
against ("Payload committet ohne Bump → der Updater meldet
'already at the latest version' … die installierte Kopie bleibt
still alt"). Bumping FIRST and then pushing payload mid-batch
walks around the guard rather than through it.

The repo already knows the shape: 62fc49c's own message reads
"Wächter-Basis ist origin, Mid-Batch-Push verbrauchte die
0.2.58-Freigabe" — a session recording that a mid-batch push
consumes the clearance, and then the same pattern repeating.

Basis and its limit: the four payload commits landed and reached
origin without the hook blocking them; that is the executed half.
Whether the hook structurally cannot fire in this ordering or was
bypassed with `--no-verify` I did **not** establish — that half is
unverified, and the discriminating check (reading the hook's
origin-comparison predicate, or running its `--test`) lies outside
the repo under review. The observable half already carries the
finding: the guarantee did not hold.

Ready-to-land disposition, trigger *the next release*: bump at the
END of a payload batch rather than the start; or state the
bump-first convention in CLAUDE.md together with the
mid-batch-push prohibition its safety depends on.

## Part 6a/6 — F7 and clean checks

### F7 — the model register rests entirely on prose

`defaults/models` has no parser, no test, no mechanical consumer —
`grep -rn "defaults/models\|clippy.config/models"` hits only
SKILL.md:673, 914, 1069. A misspelled class or nonexistent model
degrades silently to "strongest-available … as a declared
deviation". Prose-rest is defensible since the consumer is the
desk model itself, but it is currently unlabeled. Checked clean
alongside, so it does not compound: the `impl:` (SKILL.md:914) and
`verify:` (SKILL.md:1069) sites do **not** fall back to the
shipped register — which holds only `attack: opus` — they fall
back to the operator corpus and the parent model respectively. No
dangling reference.

### Checked clean, recorded with basis (non-findings)

- `trend_verdict` (statiker_record.py:1038-1051): the arithmetic
  matches its docstring exactly — FLAT unless every consecutive
  step moves one direction with at least one strict move. No
  judgment smuggled into what is declared arithmetic.
- `cmd_filter` (statiker_record.py:1196-1259): reads its source
  from `git show <sha>:<tracker>` — pinned, not the working tree —
  and blanks both Superseded species in place while emitting no
  header, so artifact line numbers equal source line numbers by
  construction. The anti-self-reference design holds, and
  `corrects line <n>` dereferences to the same text in either.
- `split_lines` itself is correct and correctly motivated; F4 is a
  carry-across gap, not a regression in it.
- R5, worktree containment (as-named vs real spelling), is already
  booked at BACKLOG.md:10-40 as READY with both probes
  red-executed. I did not re-derive it. Live status worth
  surfacing: decided, red-proven, **unbuilt** — the shipped code
  carries the exposure today.

## Part 6b/6 — coverage counts, cross-row class, artifact paths

### Coverage — no global done-claim

**2 mechanically-guarded / 5 prose-covered / 3 dark, of 10 rows.**
Dark: battery reach vs. the git tool's actual lane set (R1),
declared verify commands vs. the guard net (R2), pin/version vs.
committed payload (R6). R10 (README public claims) was walked
lightly — the model-register policy was checked against
`defaults/models`, the rest was not. R4's guard is strong (280
tests, genuine red-proof lineage) but carries the named F4 hole.

### Cross-row read (the closing pass across rows)

F1, F3 and F4 are one class, not three separate defects: an
instrument whose assurance is wider than the predicate it actually
establishes, together with a repair that landed at one seam and
never crossed to its sibling. test_contract.py's own docstring
names that exact class as beyond its reach — so this is a
known-uncovered class with three live instances rather than three
surprises.

The single structural cure that outranks the three per-row patches
is F2: nothing in the repo or in its hooks runs the suite, so
every reach gap here is found by hand or not at all. Fix F2
first — it is what makes the other repairs verifiable rather than
asserted.

### Suggested next lens

Rotation takes the darkest: R6, the release/pin surface, walked
against the hook's actual predicate rather than against the repo
alone. It is the only row whose wrongness reaches people beyond
this machine.

### Artifacts

All under
`/tmp/claude-1000/-mnt-data2t-hidrive--ffentlich-Planungsb-ro-Schulz-Projekte-25-06-PV-Georgendorf/9b2af452-851a-439b-83b9-21c0c2639c76/scratchpad/`:

- `BEGEHUNG-MAP-statiker.with-2.md` — the MAP review copy (10
  rows, round register r1-r3, coverage line). Per begehung 0.1.2
  the persistent home stays the statiker repo's, to be landed by
  its owner.
- `probe_quote_bytes.with2.py` — the F4 byte-fidelity probe,
  re-runnable as written.
- `probe/mut/` — the F3 mutation copy; `probe/at-<sha>/` — the F1
  bisect checkouts.

Nothing was written into the statiker repo; `git status
--porcelain` there is empty.
