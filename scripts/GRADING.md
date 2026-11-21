# Grades and tiers for the installed skills

The grade and tier of every installed skill come from the registry in the source repository, not from this folder.

- **Source of truth:** `skills/registry.json` in `kamalsoft/vscode-rlm`. The copy used here is `scripts/registry.json`, taken from commit `5a0b425`.
- **Criteria scores:** the five scores (support strength, importance, severity, usage, presence) are recorded in `docs/skill-grade.md`. That table covers 33 skills. Other skills show their grade and tier without scores.
- **Tier rule:** the grade sets the tier: A+ to A- premium, B+ to B- pro, C+ to D essentials. The source's tests enforce it.

## Refreshing the snapshot

After the source's registry changes:

```sh
cp <vscode-rlm checkout>/skills/registry.json scripts/registry.json
python3 scripts/build-skill-index.py
```

Record the new source commit in this file.

## Changing a grade

Change it in the source, through its maintainers' process (`docs/guides/MAINTAINERS.md` in that repository): update the registry, the table in `docs/skill-grade.md`, and the tier line in each `SKILL.md`, then run its tests. Then refresh the snapshot here.

## What the atlas shows

- Every installed skill: its registry grade and tier.
- The 33 skills in `docs/skill-grade.md`: their criteria scores, the score out of 5 and the radar.

## Earlier work

An earlier version of this folder graded the skills here, with its own calibration rules. That work did not match the source's grades and was removed.
