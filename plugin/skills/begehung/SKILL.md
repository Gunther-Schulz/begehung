---
name: begehung
description: Systematic robustness/coverage review of a system, corpus, or process — walks a persistent axis MAP instead of re-searching the last incident's corner; lens pre-registered per round, per-lens yield stop, darkest-corner rotation, no global done-claim. Use for a robustness review, blind-spot hunt, coverage review, guard-net audit, "Begehung", "wo haben wir noch nicht geschaut", "sind wir überall abgesichert". Not for reviewing a code diff or PR (code review), designing a single change (statiker), or diagnosing one defect.
---

# Begehung

Walk the whole building on a schedule; never keep returning to the
room where the last fire was. Consumer: a top-tier session model —
evidence register throughout, and the MAP with its two tables, the
round's findings file and the five forcing points below are the only
structure.

The mechanic this skill exploits (founding incident 2026-08-11,
dev-notes/OBSERVATIONS.md in the source repo,
github.com/Gunther-Schulz/begehung): review yield tracks the LENS,
not the effort. Rounds repeated under one lens exhaust — late rounds
find defects mostly in their own fresh artifacts — while every rotated
lens produces fresh yield. Incident momentum re-aims every
unregistered round back at the last hot corner; the counter is
bookkeeping, not diligence.

## The MAP

One persistent file per system under review — default `BEGEHUNG-MAP.md`
at the system's root; a repo's own conventions may name another home
(search for an existing map before creating one). A walker without a
write path into the system (a dispatched reviewer, a parallel-owned
copy) builds the MAP and the round's findings file as review copies in
its own scratch, says so, and hands their paths — the persistent home
stays the system's, landed by its owner. The MAP is the persistent
deliverable; each round's deliverable is the findings file below. One
row per axis:

| axis (what against what) | status | last visited (date · round) | yield | next step |

`status` ∈ **mechanically-guarded** (pointer to the guard's red-proof)
· **prose-covered** (rule cited) · **dark**. A status claim follows
the same evidence rule as any finding: guard status is read from the
guard and its red-proof, never from memory of it.

Beneath it, one row per round:

| round | date | axis | why that axis | read-at | closed-at | reach |

`round` counts this MAP's rounds from 1. `read-at` is the version the
system is read at, `closed-at` the version the close re-read it at —
per surface where surfaces version independently, otherwise one token
for the whole system (a commit sha where it is version-controlled,
else a timestamp or a content hash). `reach` is the close re-test's
outcome in counts, `r hold, s superseded`, r + s being the findings
the intervening change touched. An unfilled cell is a step not taken;
at most one round row is open at a time, so an empty `closed-at` on
any but the newest is a skipped close.

First run derives rows from the system's STRUCTURE:

1. Enumerate the claim-emission surfaces — every place the system
   produces claims, values, or verdicts (documents, registers,
   generated files, outward messages, tool outputs, booking files).
2. Per surface, name the consumer where wrongness lands and what it
   costs there.
3. Cross with failure dimensions: the operator corpus's failure
   classes where one is loaded; otherwise the founding set —
   label-vs-body drift · zero-hit read as absence · self-reference
   (own derivative inside the verification path) · staleness ·
   un-rerunnable reads (visual/transcription) · unguarded outward
   gates.

Completion criterion, checkable and exhaustive: every enumerated
emission surface appears in at least one row — a surface without a
row is itself a finding. The motivating incident gets one row like
any other; a map grown only from incidents is the failure mode this
skill replaces.

## The findings file

One per round, one row per finding — a data file, default
`begehung-findings-<date>-r<round>.tsv` beside the MAP, keyed to the
round's row, or the home the system's own conventions name. Rows are
appended as findings land, never composed at close: an interrupted
round still leaves its artifact.

| lens | grade | artifact line | finding | basis | disposition |

Tab-separated, one line per row, no tab or newline inside a cell —
prose wanting either is rewritten to one line. `grade` ∈ the system's
own severity vocabulary where it has one, else **blocking** ·
**notable** · **nit**. `disposition` ∈ forcing point 4's two exits —
**mechanism** · **prose-rest**, which covers two cases: a backstop
named, or a finding the close re-test found no longer holding, whose
`basis` opens `superseded-by <change-ref>:` — the ref of the landed
change, the same token space as `closed-at`. A walker without a write
path marks the row **ready-to-land** beside its proposed exit, never
in place of it. The schema is a minimum — a round adds what its lens
needs (a proposed guard's red-first arrangement, forcing point 3,
needs a column).

Completion criterion, checkable and exhaustive: every finding the
round reports appears as a row; every row's `disposition` cell
carries its exit at round close, an empty cell being the round's own
open finding; and the finding counts the round reports — total, per
grade, per lens — are read from the file. Coverage counts stay the
MAP's.

## The round — five forcing points

1. **MAP before search.** Load or build the MAP before the first
   search command of the review.
2. **Pre-register the lens.** Append the round row (form: The MAP),
   its `read-at` filled, before the first search; `why that axis` names
   darkest, stalest, or operator-named. An operator question is a
   lens: give it an axis row if none fits, then register it.
3. **Findings carry bases; proposed guards carry red.** Every claim
   in the round's output names its executed basis or the label
   unverified; every guard a finding proposes names its red-first
   arrangement — the real defect case that must fire — before it is
   booked. A loaded operator evidence corpus governs; this clause is
   its minimum, not its replacement.
4. **Every finding exits structurally.** Disposition per finding,
   booked in the system's own carriers (its backlog or ledger — a
   round report is not a carrier): a mechanism at the emission point,
   asking first whether a mandatory field there would make the
   failure computable — or an explicit prose-rest label naming the
   backstop. No third state. Each row is booked through the carrier's
   own entry form — its backlog slots, its ledger line — never by
   hand-absorption from a message, which is where the walk's output
   stops at volume. A walker without a write path hands the findings
   file as the ready-to-land set, its landing trigger naming the
   check: every handed row carries a booking ref or a named refusal.
   A superseded row books nothing — the supersession is its refusal,
   and it takes no ready-to-land mark. The booking duty transfers to
   the owner, it does not lapse.
5. **Rounds end; the walk does not.** Falling yield inside the lens
   ends the lens, never the review. A basis ages while the round
   walks: close by re-reading the system at its current version and
   re-testing every finding the intervening change touches — the diff
   where the system is version-controlled, every finding otherwise —
   at its cited line or at what it claims; the re-test decides, never
   the diff alone. One found no longer holding takes **prose-rest**
   in its `disposition` and `superseded-by <change-ref>:` at the head
   of its `basis`, edited in place. The round row's `closed-at` and
   `reach` record the pass, written whether or not anything moved.
   Then update the axis row — date and yield from the findings file
   (yield counts what the lens found; supersession does not reduce
   it), status from the guard and its red-proof — and report coverage
   counts — k guarded / m prose / j dark of n rows — in place of any
   global "done" or "secured" claim. The round's message carries the
   findings file's path and its counts, never the findings themselves:
   pasted into a message they land on a person and disposition
   nowhere. Closing also reads once ACROSS rows: a failure
   class recurring in several rows is itself a finding — the
   structure minting that class, where one structural cure outranks
   n per-row patches. A row unvisited longer than the MAP's declared
   interval is itself a finding at the next invocation.

## Rotation

Next round takes the darkest row; among equally dark, the stalest.
An operator-named lens overrides — record it as the round's
registration, and as a new axis row where none fits.

## Composition

- A loaded operator corpus's evidence rules govern all findings; this
  skill cites them, never restates them.
- A finding that opens design work routes to statiker (the design
  loop); a delegated sweep uses the dispatch skill's brief forms —
  the brief carries the registered lens and names where the findings
  file lands, or demands its path and the round row — both version
  tokens and the reach — in the report; the MAP update and the
  booking stay with the dispatcher.

## Maintenance

Observations from use are written to `dev-notes/OBSERVATIONS.md` in
the source repo — a write target, never a load. Rules in this file
are fire-born: no addition without a real incident as provenance; the
founding incident is logged there.
