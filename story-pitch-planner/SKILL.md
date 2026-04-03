---
name: story-pitch-planner
description: >
  Helps journalists develop, evaluate, and track story pitches. Use this skill
  whenever a journalist or student asks to pitch a story, develop an angle, find
  a news hook, check if a story has already been covered, brainstorm story ideas
  from a topic or beat, assess newsworthiness, or plan resource requirements for
  a story. Also trigger for requests like "help me pitch this to my editor",
  "what angle should I take on X", "has this been covered", "generate story ideas
  about Y", or "is this newsworthy". Coordinates web search (for existing coverage),
  AI angle analysis, and a local story tracker (to prevent duplicate assignments).
---

# Story Pitching & Planning Skill

## What this skill does

Helps journalists and students:
1. Develop strong, differentiated angles on a topic
2. Evaluate newsworthiness using the 5 news values
3. Check existing coverage to avoid duplication
4. Estimate resource requirements (time, sources, data needs)
5. Track active story assignments to prevent overlap

---

## Workflow

### Step 1 — Clarify the request

Ask (if not already clear):
- **Topic/beat**: What is the story about?
- **Audience**: Who is the outlet serving?
- **Mode**: (a) developing a new angle, (b) evaluating an existing pitch, or (c) checking for duplicate coverage?

### Step 2 — Check existing coverage

Use web_search with: `[topic] news [current month/year]` AND `[topic] investigation OR report`

Look for:
- Stories published in the past 30-90 days
- Similar angles taken by competitors
- Investigations already completed

Summarize the gap — what has NOT been done? That is the pitch space.

### Step 3 — Develop or evaluate the angle

**For new angles**, apply the ANGLE MATRIX:

| Dimension | Questions |
|-----------|-----------|
| Who is harmed or helped? | Are they underrepresented? |
| What changed recently? | New law, data, event, study? |
| What is the proximity hook? | How does this affect the specific audience? |
| What is the accountability or solutions frame? | Who is responsible? What can change? |
| What data can anchor this? | Is there a document, dataset, or record? |

Generate 3 distinct angles: (1) hard news, (2) feature/human angle, (3) data/accountability.

**For pitch evaluation**, score:

```
Timeliness     (1-5): Is there a news peg right now?
Proximity      (1-5): Does it affect the target audience directly?
Impact         (1-5): How many people affected, and how severely?
Novelty        (1-5): Has this specific angle been published?
Feasibility    (1-5): Can it be reported in the available timeframe?
TOTAL          /25
```

20+ = strong pitch. 15-19 = viable with refinement. Below 15 = rethink the angle.

### Step 4 — Resource planning

Estimate for the editor:
- **Sources needed**: e.g., 2 on-record, 1 data source, 1 expert
- **Time estimate**: Breaking (same day) / Short-turn (3-5 days) / Feature (2-4 weeks) / Investigation (1-3 months)
- **Data/documents**: FOIA requests, public records, datasets
- **Obstacles**: source access, embargoes, legal sensitivity

### Step 5 — Log to story tracker

Run the tracker to check for and log active assignments:

```bash
python scripts/story_tracker.py --action check --topic "TOPIC" --angle "ANGLE"
python scripts/story_tracker.py --action add --reporter "NAME" --topic "TOPIC" --angle "ANGLE" --deadline "DATE"
python scripts/story_tracker.py --action list
```

### Step 6 — Draft the pitch

```
STORY PITCH

Headline (working): [One-line, present tense]
Angle: [One sentence — what makes this different from existing coverage]
News peg: [Why now?]
Impact: [Who is affected and how]
Key sources: [3-5 source types]
Resource needs: [Time, travel, data access]
Newsworthiness score: [X/25]
```

---

## Python Scripts

### scripts/story_tracker.py
Manages a local JSON-based assignment log to prevent duplicate angle coverage.

### scripts/coverage_checker.py
Runs structured web searches and returns a summary of what has already been reported on a topic.

Read the scripts for full usage — they are self-documenting via --help.

---

## Notes for the AI

- Always search the web before declaring a topic "uncovered" — training data is not current
- When generating angles, always produce all 3 types (hard news, feature, data/accountability)
- Flag stories with legal sensitivity proactively (defamation, privacy, court orders)
- Consider solutions journalism framing as a fourth angle when relevant
- Be specific about source types, not generic ("local health official" not just "expert")
