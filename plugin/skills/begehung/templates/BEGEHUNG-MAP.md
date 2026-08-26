# Begehung MAP — <system name>

Interval: <how stale a row may get before its staleness is itself a
finding; absent this line, the default is the two rounds before this>

## Axes

| axis (what against what) | status | last visited (date · round) | yield | next step |
|---|---|---|---|---|
| <what is checked against what> | dark (modelled) | — | — | <the first probe> |
| CROSS-CUTTING lifecycle — per artifact the system holds: where does it live, who writes it, who reads it | dark (modelled) | — | — | <first artifact to walk> |
| ENFORCER under its own invariants — <what this system demands of others, asked of itself> | dark (modelled) | — | — | <first invariant to test> |

The last two rows are owed rows, not examples: the cross-cutting row
by every system, the enforcer row by any system whose surfaces emit
verdicts about other work. Delete the enforcer row only if this system
emits none.

## Rounds

| round | date | axis | why that axis | read-at | closed-at | reach | class |
|---|---|---|---|---|---|---|---|
| 1 | <YYYY-MM-DD> | <the axis row walked> | darkest / stalest / operator-named | <sha or timestamp> | | | |

`read-at` is filled BEFORE the first search; `closed-at`, `reach` and
`class` at the close. An empty cell is a step not taken — at most one
round row is open at a time.
