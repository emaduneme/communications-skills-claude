#!/usr/bin/env python3
"""
story_tracker.py — Manage story assignments to prevent duplicate coverage.

Usage:
  python story_tracker.py --action list
  python story_tracker.py --action check --topic "Housing prices" --angle "Eviction rates"
  python story_tracker.py --action add --reporter "Jane Smith" --topic "Housing prices" \
      --angle "Eviction rates in low-income neighborhoods" --deadline "2025-02-15"
  python story_tracker.py --action complete --id 3
  python story_tracker.py --action remove --id 3
"""

import argparse
import json
import os
import sys
from datetime import datetime
from difflib import SequenceMatcher


TRACKER_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "story_assignments.json")


def load_tracker():
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    if not os.path.exists(TRACKER_FILE):
        return {"assignments": [], "next_id": 1}
    with open(TRACKER_FILE) as f:
        return json.load(f)


def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def check_duplicates(data, topic, angle):
    """Check for existing assignments that overlap with a new topic/angle."""
    conflicts = []
    for assignment in data["assignments"]:
        if assignment.get("status") == "complete":
            continue
        topic_sim = similarity(topic, assignment["topic"])
        angle_sim = similarity(angle, assignment["angle"]) if angle else 0
        combined = (topic_sim * 0.6) + (angle_sim * 0.4)
        if topic_sim > 0.6 or combined > 0.5:
            conflicts.append({
                "id": assignment["id"],
                "reporter": assignment["reporter"],
                "topic": assignment["topic"],
                "angle": assignment["angle"],
                "deadline": assignment["deadline"],
                "similarity": round(combined, 2),
                "topic_similarity": round(topic_sim, 2),
            })
    return sorted(conflicts, key=lambda x: x["similarity"], reverse=True)


def cmd_check(args):
    data = load_tracker()
    conflicts = check_duplicates(data, args.topic, args.angle or "")
    if not conflicts:
        print(f"No conflicts found for topic: '{args.topic}'")
        print("This angle appears to be available. Proceed with the pitch.")
    else:
        print(f"WARNING: {len(conflicts)} potential conflict(s) found:\n")
        for c in conflicts:
            print(f"  ID {c['id']} | Reporter: {c['reporter']}")
            print(f"  Topic:  {c['topic']}")
            print(f"  Angle:  {c['angle']}")
            print(f"  Deadline: {c['deadline']}")
            print(f"  Overlap score: {c['similarity']} (topic: {c['topic_similarity']})")
            print()


def cmd_add(args):
    data = load_tracker()
    conflicts = check_duplicates(data, args.topic, args.angle or "")
    if conflicts and not args.force:
        print(f"WARNING: {len(conflicts)} conflict(s) found. Use --force to add anyway.")
        for c in conflicts:
            print(f"  ID {c['id']} | {c['reporter']}: {c['topic']} — {c['angle']}")
        sys.exit(1)

    assignment = {
        "id": data["next_id"],
        "reporter": args.reporter,
        "topic": args.topic,
        "angle": args.angle or "",
        "deadline": args.deadline or "TBD",
        "added": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
    }
    data["assignments"].append(assignment)
    data["next_id"] += 1
    save_tracker(data)
    print(f"Story assignment #{assignment['id']} added:")
    print(f"  Reporter: {assignment['reporter']}")
    print(f"  Topic: {assignment['topic']}")
    print(f"  Angle: {assignment['angle']}")
    print(f"  Deadline: {assignment['deadline']}")


def cmd_list(args):
    data = load_tracker()
    active = [a for a in data["assignments"] if a.get("status") != "complete"]
    if not active:
        print("No active story assignments.")
        return
    print(f"Active story assignments ({len(active)}):\n")
    for a in active:
        print(f"  #{a['id']} | {a['reporter']} | Due: {a['deadline']}")
        print(f"  Topic: {a['topic']}")
        print(f"  Angle: {a['angle']}")
        print()


def cmd_complete(args):
    data = load_tracker()
    for a in data["assignments"]:
        if a["id"] == args.id:
            a["status"] = "complete"
            a["completed"] = datetime.now().strftime("%Y-%m-%d")
            save_tracker(data)
            print(f"Assignment #{args.id} marked complete.")
            return
    print(f"Assignment #{args.id} not found.")


def cmd_remove(args):
    data = load_tracker()
    original = len(data["assignments"])
    data["assignments"] = [a for a in data["assignments"] if a["id"] != args.id]
    if len(data["assignments"]) < original:
        save_tracker(data)
        print(f"Assignment #{args.id} removed.")
    else:
        print(f"Assignment #{args.id} not found.")


def main():
    parser = argparse.ArgumentParser(description="Story assignment tracker for newsrooms.")
    parser.add_argument("--action", required=True, choices=["check", "add", "list", "complete", "remove"])
    parser.add_argument("--topic", help="Story topic")
    parser.add_argument("--angle", help="Specific story angle")
    parser.add_argument("--reporter", help="Reporter name")
    parser.add_argument("--deadline", help="Deadline (YYYY-MM-DD or descriptive)")
    parser.add_argument("--id", type=int, help="Assignment ID")
    parser.add_argument("--force", action="store_true", help="Add even if conflicts exist")
    args = parser.parse_args()

    actions = {
        "check": cmd_check,
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "remove": cmd_remove,
    }
    actions[args.action](args)


if __name__ == "__main__":
    main()
