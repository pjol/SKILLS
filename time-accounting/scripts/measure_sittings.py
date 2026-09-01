#!/usr/bin/env python3
"""Measure working time from a Claude Code session transcript.

Transcripts carry a timestamp on every message, so working time is recoverable
exactly rather than estimated. This clusters those timestamps into sittings,
splitting on a gap longer than --gap minutes, and prints each sitting's span
plus the total.

A gap under the threshold is somebody reading a diff, thinking, or fetching
coffee — working time. A gap over it is somebody who left.

Usage:
    measure_sittings.py                        # newest transcript for $PWD
    measure_sittings.py --project ~/code/app   # a different project
    measure_sittings.py --gap 45               # a different sitting threshold
    measure_sittings.py --all                  # every transcript, not just newest
    measure_sittings.py --file path/to.jsonl   # an exact transcript
"""

import argparse
import datetime
import glob
import json
import os
import sys

# Claude Code stores transcripts under a sanitized form of the project path:
# every character outside [A-Za-z0-9] becomes a dash.
PROJECTS_ROOT = os.path.expanduser("~/.claude/projects")


def sanitize(project_path: str) -> str:
    absolute = os.path.abspath(os.path.expanduser(project_path))
    return "".join(c if c.isalnum() else "-" for c in absolute)


def transcripts_for(project_path: str, newest_only: bool) -> list[str]:
    directory = os.path.join(PROJECTS_ROOT, sanitize(project_path))
    found = sorted(glob.glob(os.path.join(directory, "*.jsonl")), key=os.path.getmtime)
    if not found:
        sys.exit(f"No transcripts under {directory}")
    return found if not newest_only else found[-1:]


def timestamps(path: str) -> list[datetime.datetime]:
    stamps = []
    with open(path, errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except (ValueError, TypeError):
                # A partially flushed final line is normal on a live session.
                continue
            raw = record.get("timestamp")
            if not raw:
                continue
            try:
                stamps.append(datetime.datetime.fromisoformat(raw.replace("Z", "+00:00")))
            except ValueError:
                continue
    stamps.sort()
    return stamps


def sittings(stamps, gap_minutes: int):
    """Contiguous runs of activity, split on any gap longer than the threshold."""
    if not stamps:
        return []
    gap = datetime.timedelta(minutes=gap_minutes)
    runs, start, previous = [], stamps[0], stamps[0]
    for when in stamps[1:]:
        if when - previous > gap:
            runs.append((start, previous))
            start = when
        previous = when
    runs.append((start, previous))
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default=os.getcwd(),
                        help="project directory the session ran in (default: cwd)")
    parser.add_argument("--file", help="an exact transcript path, bypassing lookup")
    parser.add_argument("--gap", type=int, default=30,
                        help="minutes of silence that ends a sitting (default: 30)")
    parser.add_argument("--all", action="store_true",
                        help="measure every transcript for the project, not just the newest")
    args = parser.parse_args()

    paths = [args.file] if args.file else transcripts_for(args.project, newest_only=not args.all)

    grand_total = datetime.timedelta()
    for path in paths:
        stamps = timestamps(path)
        if not stamps:
            print(f"{os.path.basename(path)}: no timestamps")
            continue

        runs = sittings(stamps, args.gap)
        total = sum((b - a for a, b in runs), datetime.timedelta())
        grand_total += total

        print(f"\n{os.path.basename(path)}")
        print(f"  {len(stamps)} timestamped records, "
              f"{stamps[0].astimezone():%Y-%m-%d %H:%M} .. {stamps[-1].astimezone():%Y-%m-%d %H:%M}")
        for a, b in runs:
            span = (b - a).total_seconds() / 3600
            print(f"  {a.astimezone():%Y-%m-%d %H:%M} -> {b.astimezone():%H:%M}   {span:5.2f} h")
        print(f"  measured: {total.total_seconds()/3600:.2f} h "
              f"(wall clock {(stamps[-1]-stamps[0]).total_seconds()/3600:.2f} h)")

    if len(paths) > 1:
        print(f"\nall transcripts: {grand_total.total_seconds()/3600:.2f} h")

    print("\nReport the measured figure, rounded to 0.1h, and say it was measured.")


if __name__ == "__main__":
    main()
