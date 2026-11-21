#!/usr/bin/env python3
"""Check the animation files in scripts/animations/ before they are merged into the atlas.

Usage: python3 scripts/validate-animations.py [file ...]
With no arguments every .json file in scripts/animations/ is checked.
Exits 1 if any file has a problem.
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "scripts" / "animations"
LAYOUTS = {"bins", "chunks", "doc", "funnel", "gate", "graph", "match", "parallel", "row", "shrink", "stack", "store", "timeline"}
SEV = {"high", "medium", "low"}
TONE = {"ok", "warn", "bad"}
STATE = {"ok", "warn", "bad", "todo", "hit"}


def check(name, data):
    errors = []
    items = data.get("items", [])
    n = len(items)
    if not 4 <= n <= 8:
        errors.append(f"items: need 4 to 8, found {n}")
    if len(set(items)) != n:
        errors.append("items: names must be unique")
    steps = data.get("steps", [])
    if not 3 <= len(steps) <= 6:
        errors.append(f"steps: need 3 to 6, found {len(steps)}")
    for i, st in enumerate(steps, 1):
        where = f"step {i}"
        layout = st.get("layout")
        if layout not in LAYOUTS:
            errors.append(f"{where}: unknown layout {layout!r}")
            continue
        if not st.get("note", "").strip():
            errors.append(f"{where}: note is empty")
        for key in ("drop",):
            if any(not 0 <= x < n for x in st.get(key, [])):
                errors.append(f"{where}: {key} index out of range")
        if layout in ("chunks", "parallel"):
            g = st.get("groups")
            if g is None:
                errors.append(f"{where}: {layout} needs groups")
            elif isinstance(g, list) and len(g) != n:
                errors.append(f"{where}: groups must have {n} entries")
        if layout == "bins":
            bins, binOf = st.get("bins"), st.get("binOf")
            if not bins or binOf is None or len(binOf) != n:
                errors.append(f"{where}: bins needs bins and binOf (one per item)")
            elif any(not 0 <= b < len(bins) for b in binOf):
                errors.append(f"{where}: binOf value out of range")
        if layout == "match":
            targets, pairs = st.get("targets"), st.get("pairs")
            if not targets or pairs is None or len(pairs) != n:
                errors.append(f"{where}: match needs targets and pairs (one per item)")
            elif any(not (p == -1 or 0 <= p < len(targets)) for p in pairs):
                errors.append(f"{where}: pairs value out of range")
        if layout == "gate" and "pass" in st and len(st["pass"]) != n:
            errors.append(f"{where}: pass must have {n} entries")
        if layout == "parallel" and "state" in st and len(st["state"]) != n:
            errors.append(f"{where}: state must have {n} entries")
        for s in st.get("state", []) + st.get("targetState", []):
            if s not in STATE:
                errors.append(f"{where}: unknown state {s!r}")
    out = data.get("outcome")
    if not isinstance(out, dict):
        errors.append("outcome: missing")
    else:
        if out.get("tone") not in TONE:
            errors.append("outcome: tone must be ok, warn or bad")
        if not out.get("verdict"):
            errors.append("outcome: verdict is empty")
        for bar in out.get("bars", []):
            if len(bar) != 3 or bar[2] not in SEV:
                errors.append(f"outcome: bad bar {bar!r}")
        for k, f in enumerate(out.get("findings", []), 1):
            if f.get("sev") not in SEV:
                errors.append(f"finding {k}: sev must be high, medium or low")
            where = f.get("where", "")
            file = where.split(":")[0]
            if file not in items:
                errors.append(f"finding {k}: {file!r} is not one of the items")
        if not out.get("notChecked"):
            errors.append("outcome: notChecked is empty")
    if not data.get("example", "").strip():
        errors.append("example: empty")
    return [f"{name}: {e}" for e in errors]


def main():
    paths = [Path(p) for p in sys.argv[1:]] or [Path(p) for p in sorted(glob.glob(str(DIR / "*.json")))]
    problems = []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            problems.append(f"{p.name}: {err}")
            continue
        problems += check(p.stem, data)
    for line in problems:
        print(line)
    print(f"Checked {len(paths)} file(s); {len(problems)} problem(s).")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
