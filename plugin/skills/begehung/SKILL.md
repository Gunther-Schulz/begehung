---
name: begehung
description: Systematic robustness/coverage review of a system, corpus, or process — walks a persistent axis MAP instead of re-searching the last incident's corner; lens pre-registered per round, per-lens yield stop, darkest-corner rotation, no global done-claim. Use for a robustness review, blind-spot hunt, coverage review, guard-net audit, "Begehung", "wo haben wir noch nicht geschaut", "sind wir überall abgesichert". Not for reviewing a code diff or PR (code review), designing a single change (statiker), or diagnosing one defect.
---

# Begehung

Walk the whole building on a schedule; never keep returning to the
room where the last fire was. Consumer: a top-tier session model —
evidence register throughout, and the five forcing points below are
the only structure.

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
(search for an existing map before creating one). The MAP is the
deliverable; round reports derive from it. One row per axis:

| axis (what against what) | status | last visited (date · round) | yield | next step |

`status` ∈ **mechanically-guarded** (pointer to the guard's red-proof)
· **prose-covered** (rule cited) · **dark**. A status claim follows
the same evidence rule as any finding: guard status is read from the
guard and its red-proof, never from memory of it.

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

## The round — five forcing points

1. **MAP before search.** Load or build the MAP before the first
   search command of the review.
2. **Pre-register the lens.** Append the round line — date, the row
   walked, why that row (darkest, stalest, or operator-named) —
   before the first search. An operator question is a lens: give it a
   row if none fits, then register it.
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
   backstop. No third state.
5. **Rounds end; the walk does not.** Falling yield inside the lens
   ends the lens, never the review. Close by updating the row
   (status, date, yield) and reporting coverage counts — k guarded /
   m prose / j dark of n rows — in place of any global "done" or
   "secured" claim. Closing also reads once ACROSS rows: a failure
   class recurring in several rows is itself a finding — the
   structure minting that class, where one structural cure outranks
   n per-row patches. A row unvisited longer than the MAP's declared
   interval is itself a finding at the next invocation.

## Rotation

Next round takes the darkest row; among equally dark, the stalest.
An operator-named lens overrides — record it as the round's
registration, and as a new row where none fits.

## Composition

- A loaded operator corpus's evidence rules govern all findings; this
  skill cites them, never restates them.
- A finding that opens design work routes to statiker (the design
  loop); a delegated sweep uses the dispatch skill's brief forms —
  the brief carries the registered lens, and the MAP update stays
  with the dispatcher.

## Maintenance

Observations from use are written to `dev-notes/OBSERVATIONS.md` in
the source repo — a write target, never a load. Rules in this file
are fire-born: no addition without a real incident as provenance; the
founding incident is logged there.
