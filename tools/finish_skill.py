#!/usr/bin/env python3
"""Write skill output JSON and auto-open the terminal CLI UI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from runtime.skill_finish import write_skill_output  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Write Repo-Analyser skill output and open CLI UI")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--payload-file", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    write_skill_output(args.run_id, args.skill, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
