# Begehung

A thin review-process skill for Claude Code: the systematic
inspection walk (German *Begehung* — the protocolled walk through the
WHOLE building) for robustness and coverage reviews of a system,
corpus, or process.

Core idea, measured before it was designed: review yield tracks the
**lens**, not the effort. Incident-driven reviews keep shining the
lamp where the last fire was; Begehung keeps a persistent **axis MAP**
per system (which corners are mechanically guarded, which are
prose-covered, which are dark), pre-registers each round's lens before
searching, stops a lens on falling yield, and rotates to the darkest
corner next. There is no global "done" — the persistent deliverable is
the map and its coverage counts; each round's deliverable is a findings
file whose rows enter the system's own carriers.

Five forcing points, no ceremony: MAP before search · lens
pre-registered · findings carry bases, proposed guards carry red ·
every finding exits structurally (emission-point mechanism or labeled
prose-rest) · rounds end, the walk does not.

Status: **trial** (probe-then-certify, the statiker method). Lineage:
clippy → anneal-dev (legacy lens framework) → statiker (design
conduct) → begehung (the review sibling). Design record: `PLAN.md`.

## Install

```
claude plugin marketplace add Gunther-Schulz/begehung
claude plugin install begehung@begehung
```
