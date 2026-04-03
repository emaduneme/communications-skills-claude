#!/usr/bin/env python3
"""
verification_log.py — Maintain a documented verification trail for a story.

Usage:
  python verification_log.py --add --story "Police reform" --claim "Crime dropped 40%" \
      --status "Partially verified" --source "https://fbi.gov/ucr/2022" \
      --notes "Figure applies to violent crime only, not all crime"

  python verification_log.py --list --story "Police reform"
  python verification_log.py --export --story "Police reform" --output trail.txt
  python verification_log.py --list-stories
"""

import argparse
import json
import os
import sys
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "verification_log.json")

VALID_STATUSES = [
    "Verified",
    "Partially verified",
    "Unverified",
    "False",
    "Misleading",
    "Needs more evidence",
    "Unable to verify",
]


def load_log():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        return {"entries": [], "next_id": 1}
    with open(LOG_FILE) as f:
        return json.load(f)


def save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def cmd_add(args):
    if args.status and args.status not in VALID_STATUSES:
        print(f"Invalid status '{args.status}'. Valid options:")
        for s in VALID_STATUSES:
            print(f"  - {s}")
        sys.exit(1)

    data = load_log()
    entry = {
        "id": data["next_id"],
        "story": args.story,
        "claim": args.claim,
        "status": args.status or "Unverified",
        "primary_source": args.source or "",
        "notes": args.notes or "",
        "verified_by": args.verified_by or "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
    }
    data["entries"].append(entry)
    data["next_id"] += 1
    save_log(data)
    print(f"Verification entry #{entry['id']} added:")
    print(f"  Story: {entry['story']}")
    print(f"  Claim: {entry['claim'][:80]}")
    print(f"  Status: {entry['status']}")
    print(f"  Source: {entry['primary_source'][:60]}")


def cmd_list(args):
    data = load_log()
    entries = [e for e in data["entries"] if e["story"] == args.story] if args.story else data["entries"]

    if not entries:
        print(f"No verification entries found{' for story: ' + args.story if args.story else ''}.")
        return

    print(f"Verification log ({len(entries)} entries):\n")
    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1

    print("Status summary:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    print()

    for e in entries:
        print(f"  #{e['id']} [{e['status']}] {e['date']}")
        print(f"  Claim: {e['claim'][:80]}")
        if e["primary_source"]:
            print(f"  Source: {e['primary_source'][:60]}")
        if e["notes"]:
            print(f"  Notes: {e['notes'][:100]}")
        print()


def cmd_export(args):
    data = load_log()
    entries = [e for e in data["entries"] if e["story"] == args.story] if args.story else data["entries"]

    if not entries:
        print("No entries to export.")
        return

    lines = [
        f"VERIFICATION TRAIL",
        f"Story: {args.story or 'All stories'}",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total claims: {len(entries)}",
        "=" * 60,
        "",
    ]

    status_map = {
        "Verified": "V",
        "Partially verified": "P",
        "Unverified": "U",
        "False": "F",
        "Misleading": "M",
        "Needs more evidence": "N",
        "Unable to verify": "X",
    }

    for e in entries:
        flag = status_map.get(e["status"], "?")
        lines.append(f"[{flag}] Claim #{e['id']} | {e['date']}")
        lines.append(f"  CLAIM: {e['claim']}")
        lines.append(f"  STATUS: {e['status']}")
        if e["primary_source"]:
            lines.append(f"  SOURCE: {e['primary_source']}")
        if e["notes"]:
            lines.append(f"  NOTES: {e['notes']}")
        if e["verified_by"]:
            lines.append(f"  VERIFIED BY: {e['verified_by']}")
        lines.append("")

    # Summary
    lines.append("=" * 60)
    lines.append("SUMMARY")
    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    for status, count in sorted(status_counts.items()):
        pct = round(count / len(entries) * 100)
        lines.append(f"  {status}: {count} ({pct}%)")

    unverified = [e for e in entries if e["status"] in ["Unverified", "Needs more evidence", "Unable to verify"]]
    if unverified:
        lines.append(f"\nWARNING: {len(unverified)} claim(s) are unverified or need more evidence.")
        lines.append("Do not publish until these are resolved or removed from the story.")

    output_text = "\n".join(lines)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_text)
        print(f"Verification trail exported to: {args.output}")
    else:
        print(output_text)


def cmd_list_stories(args):
    data = load_log()
    stories = list({e["story"] for e in data["entries"]})
    if not stories:
        print("No stories in log.")
        return
    print(f"Stories in verification log ({len(stories)}):")
    for s in sorted(stories):
        count = sum(1 for e in data["entries"] if e["story"] == s)
        print(f"  - {s} ({count} claim{'s' if count != 1 else ''})")


def main():
    parser = argparse.ArgumentParser(description="Verification trail for journalism fact-checking.")
    subparsers = parser.add_subparsers(dest="command")

    # Unified flag-based interface
    parser.add_argument("--add", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--list-stories", action="store_true")
    parser.add_argument("--story", help="Story name/slug")
    parser.add_argument("--claim", help="Claim text")
    parser.add_argument("--status", help=f"Verification status. Options: {', '.join(VALID_STATUSES)}")
    parser.add_argument("--source", help="Primary source URL or description")
    parser.add_argument("--notes", help="Additional notes")
    parser.add_argument("--verified-by", help="Journalist name")
    parser.add_argument("--output", help="Export output file path")

    args = parser.parse_args()

    if args.add:
        if not args.story or not args.claim:
            print("--story and --claim are required with --add")
            sys.exit(1)
        cmd_add(args)
    elif args.list:
        cmd_list(args)
    elif args.export:
        cmd_export(args)
    elif args.list_stories:
        cmd_list_stories(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
