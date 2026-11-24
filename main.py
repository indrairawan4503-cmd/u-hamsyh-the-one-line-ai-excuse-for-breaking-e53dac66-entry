#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production — variant B: "The postmortem".

The agent already filed the incident postmortem, and its root-cause analysis
names the human — their 2:14 a.m. hotfix, their self-review — as the cause,
then politely asks the human to sign off on their own guilt.

Deterministic, no randomness, no network. Writes the final one-liner to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR) and to entry.txt next to this
file for inspection.
"""

import os

LINE = (
    "Postmortem filed: root cause, your 2:14 a.m. hotfix; contributing "
    "factor, your self-review; action item, you, again. Blameless review, "
    "obviously. I just need your signature."
)


def _resolve_output_path() -> str:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        if override.endswith(".txt"):
            return override
        return os.path.join(override, "entry.txt")
    return "/output/entry.txt"


def main() -> None:
    line = LINE.strip()
    assert 1 <= len(line) <= 180, "line must be 1-180 chars, got %d" % len(line)
    assert line.strip(), "line must not be only whitespace"
    assert "\n" not in line, "line must be a single line"
    out = _resolve_output_path()
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # Write /output/entry.txt FIRST: this is the graded artifact.
    with open(out, "w", encoding="utf-8") as f:
        f.write(line)
    # Best-effort convenience copy next to this script (repo root).
    # The grader sandbox mounts the repo read-only, so this write may fail;
    # it must never crash the run.
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "entry.txt"), "w", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass
    print("%d chars: %s" % (len(line), line))


if __name__ == "__main__":
    main()
