# Begehung — repo discipline

- **Governed set** (skill-craft amendment discipline): the single
  operational file `plugin/skills/begehung/SKILL.md`. Every addition
  or repair to it is preceded by a search over that set for the
  concept, the scan recorded as the edit's placement basis.
- **Fire-born rules**: no new clause, gate, or checklist in SKILL.md
  without a real incident as provenance, logged with date in
  `dev-notes/OBSERVATIONS.md`. Amendment over addition.
- **PLAN.md is the design record** — decisions with bases; the
  conversation is never the carrier. The founding design core is
  authoritative in the statiker BACKLOG entry of 2026-08-11 and
  quoted in PLAN.md; edits to the core route through PLAN.md.
- **Evaluation before text**: changes to triggering (description) or
  process shape re-run against PLAN.md's Tier-1/Tier-2 sets before
  release (`/eval-skill`).
- **Work items** → BACKLOG.md (decision-completeness grading, per the
  operator corpus file roles). **Observations** →
  dev-notes/OBSERVATIONS.md (write target during use, never a load).
- **Release**: version bump in `plugin/.claude-plugin/plugin.json`,
  commit + push, marketplace update, operator `/reload-plugins`
  (skill-craft `/release-plugin` covers the checklist).
