#!/usr/bin/env python3
"""Write docs/skills-index.js from the skills installed in a folder.

Usage: python3 scripts/build-skill-index.py [skills-folder]
Default folder: .claude/skills in this repository.

Grades and tiers come from scripts/registry.json, a snapshot of skills/registry.json in the
vscode-rlm source (commit recorded in scripts/GRADING.md). The five criteria scores come from
docs/skill-grade.md where a skill is listed there. The atlas (docs/skill-atlas.html) loads the output.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "skills-index.js"
ANIMATIONS = ROOT / "scripts" / "animations"
REGISTRY = ROOT / "scripts" / "registry.json"
GRADE_DOC = ROOT / "docs" / "skill-grade.md"
TIER = re.compile(r"<!--\s*tier:\s*(\w+)\s*-->")
BAND_ORDER = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D"]


def frontmatter(text):
    # Only the single-line `key: value` pairs the skills use.
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip('"\'')
    return fields


def first_sentence(text, limit=110):
    head = re.split(r"(?<=\.)\s", text, maxsplit=1)[0]
    return head if len(head) <= limit else head[: limit - 1].rstrip() + "…"


def protocol(text):
    # Numbered steps under "## Protocol", as "1. **Title.** text" with optional wrapped lines.
    steps, body, inside = [], [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Protocol"
            continue
        if inside:
            body.append(line)
    for line in body:
        match = re.match(r"^\d+\.\s+\*\*(.+?)\*\*\s*(.*)$", line)
        if match:
            steps.append({"title": match.group(1).rstrip("."), "text": match.group(2)})
        elif steps and line.strip():
            steps[-1]["text"] += " " + line.strip()
    return steps



# Shared walkthrough for installed skills with no hand-written animation: each of the first six
# protocol steps is drawn with one of these layouts, over six placeholder items.
GENERIC_LAYOUTS = ["row", "chunks", "parallel", "funnel", "gate", "doc"]
GENERIC_ITEMS = [f"input-{i}" for i in range(1, 7)]


def generic_animation(steps):
    out = []
    for i, step in enumerate(steps[:6]):
        layout = GENERIC_LAYOUTS[i]
        first = re.split(r"(?<=\.)\s", step["text"], maxsplit=1)[0]
        note = f"{step['title']}. {first}".strip()
        st = {"layout": layout, "note": note}
        if layout in ("chunks", "parallel"):
            st["groups"] = [0, 0, 1, 1, 2, 2]
        if layout == "parallel":
            st["state"] = ["ok"] * 6
        if layout == "gate":
            st["pass"] = [True, True, True, True, True, False]
        if layout == "doc":
            st["docLabel"] = "report"
        out.append(st)
    return {"items": GENERIC_ITEMS, "steps": out, "outcome": None}


def registry_grades():
    """skillName -> {grade, tier, folder} from the registry snapshot."""
    return {r["skillName"]: {"grade": r["grade"], "tier": r["tier"], "folder": r["folder"]} for r in json.loads(REGISTRY.read_text(encoding="utf-8"))}


def criteria_scores(registry):
    """skillName -> {score, scores} from the table in docs/skill-grade.md (33 skills)."""
    found = {}
    for line in GRADE_DOC.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\d+\s*\|\s*`([^`]+)`\s*\|.*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*([\d.]+)\s*\|", line)
        if not m:
            continue
        name = m.group(1) if m.group(1) in registry else "rlm-" + m.group(1)
        if name in registry:
            found[name] = {"scores": [int(m.group(i)) for i in range(2, 7)], "score": m.group(7)}
    return found


def skill_entry(folder, grades, criteria):
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    meta = frontmatter(text)
    name = meta.get("name", folder.name)
    description = meta.get("description", "")
    steps = protocol(text)
    registered = grades.get(name)
    entry = {
        "id": name,
        "goal": first_sentence(description),
        "cat": "Installed",
        "on": False,
        "use": description,
        "prompt": f"Use the {name} skill.",
        "input": "",
        "output": "",
        "pros": [],
        "cons": [],
        "items": [],
        "steps": [],
        "outcome": None,
        "idea": "",
        "why": "",
        "protocol": steps,
        "path": folder.relative_to(ROOT).as_posix() if folder.is_relative_to(ROOT) else str(folder),
    }
    if registered:
        extra = criteria.get(name, {})
        entry["grade"] = {"grade": registered["grade"], "tier": registered["tier"], "score": extra.get("score"), "scores": extra.get("scores")}
        entry["tier"] = registered["tier"]
    else:
        entry["grade"] = None
        entry["tier"] = ""
    animation = ANIMATIONS / f"{name}.json"
    if animation.is_file():
        # Hand-written animation: items, steps, outcome and example.
        entry.update(json.loads(animation.read_text(encoding="utf-8")))
    elif len(steps) >= 3:
        entry.update(generic_animation(steps))
    return entry


def rank(skills):
    """Order by grade band, then by score where one is recorded. The rank is the position in that order."""
    def key(s):
        g = s["grade"]
        score = float(g["score"]) if g and g.get("score") else -1
        return (BAND_ORDER.index(g["grade"]) if g else len(BAND_ORDER), -score, s["id"])
    for position, s in enumerate(sorted(skills, key=key), 1):
        if s["grade"]:
            s["grade"]["rank"] = position


def main():
    source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / ".claude" / "skills"
    if not source.is_dir():
        sys.exit(f"Not a folder: {source}")
    registry = registry_grades()
    criteria = criteria_scores(registry)
    folders = sorted(p for p in source.iterdir() if (p / "SKILL.md").is_file())
    skills = [skill_entry(p, registry, criteria) for p in folders]
    rank(skills)
    missing = [s["id"] for s in skills if not s["grade"]]
    OUT.write_text("window.SKILL_INDEX = " + json.dumps({"skills": skills}, indent=1) + ";\n", encoding="utf-8")
    print(f"Wrote {len(skills)} skills from {source} to {OUT}")
    if missing:
        print(f"Not in the registry snapshot: {len(missing)} ({', '.join(missing[:5])}...)")


if __name__ == "__main__":
    main()
