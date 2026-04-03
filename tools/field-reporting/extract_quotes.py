#!/usr/bin/env python3
"""
extract_quotes.py — Extract and score potential key quotes from an interview transcript.

Usage:
  python extract_quotes.py --transcript transcript.txt
  python extract_quotes.py --transcript transcript.txt --topic "housing policy" --output quotes.txt
  python extract_quotes.py --transcript transcript.txt --min-score 3
"""

import argparse
import os
import re
import sys
from datetime import datetime


# Attribution verbs that often precede or follow a direct quote
ATTRIBUTION_VERBS = [
    "said", "says", "stated", "told", "explained", "argued", "noted", "added",
    "emphasized", "warned", "claimed", "admitted", "acknowledged", "insisted",
    "confirmed", "denied", "revealed", "disclosed", "announced", "declared",
    "pointed out", "stressed", "suggested", "indicated",
]

# Words that signal strong statements worth quoting
EMPHATIC_WORDS = [
    "never", "always", "absolutely", "critical", "crisis", "failure", "wrong",
    "illegal", "unconstitutional", "danger", "unacceptable", "urgent", "demand",
    "promise", "guarantee", "refuse", "must", "catastrophe", "historic", "first",
    "last", "only", "directly", "personally", "I", "we", "our",
]

# Words that signal a potential story angle or newsworthiness
NEWSWORTH_PHRASES = [
    "for the first time", "has never", "no one has", "secret", "hidden",
    "internal documents", "previously unreported", "sources say", "exclusively",
    "investigation found", "records show", "according to data",
]


def score_sentence(sentence, topic_keywords):
    """Score a sentence on its quote potential (0-5)."""
    score = 0
    s_lower = sentence.lower()

    # Attribution signals
    if any(v in s_lower for v in ATTRIBUTION_VERBS):
        score += 1

    # Emphatic language
    emphatic_count = sum(1 for w in EMPHATIC_WORDS if w.lower() in s_lower)
    if emphatic_count >= 2:
        score += 2
    elif emphatic_count == 1:
        score += 1

    # Topic relevance
    if topic_keywords:
        kw_matches = sum(1 for k in topic_keywords if k.lower() in s_lower)
        if kw_matches >= 2:
            score += 2
        elif kw_matches == 1:
            score += 1

    # Newsworthiness markers
    if any(phrase in s_lower for phrase in NEWSWORTH_PHRASES):
        score += 2

    # Length filter: very short or very long sentences are often not ideal quotes
    word_count = len(sentence.split())
    if word_count < 8:
        score -= 1
    if word_count > 80:
        score -= 1

    return max(0, score)


def extract_timestamps(line):
    """Extract timestamp from a line like [00:03:42] text..."""
    match = re.match(r"^\[(\d{2}:\d{2}:\d{2})\]\s*(.+)", line.strip())
    if match:
        return match.group(1), match.group(2)
    return None, line.strip()


def extract_quotes(transcript_path, topic_raw="", min_score=2, output_path=None):
    if not os.path.exists(transcript_path):
        print(f"Transcript file not found: {transcript_path}")
        sys.exit(1)

    with open(transcript_path, encoding="utf-8") as f:
        content = f.read()

    topic_keywords = [k.strip() for k in topic_raw.split(",") if k.strip()] if topic_raw else []

    lines = content.split("\n")
    results = []

    for line in lines:
        timestamp, text = extract_timestamps(line)
        if not text or len(text.split()) < 5:
            continue
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            if len(sentence.strip()) < 20:
                continue
            score = score_sentence(sentence, topic_keywords)
            if score >= min_score:
                results.append({
                    "timestamp": timestamp or "",
                    "quote": sentence.strip(),
                    "score": score,
                })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    # Build output
    lines_out = [
        f"QUOTE EXTRACTION REPORT",
        f"Source: {os.path.basename(transcript_path)}",
        f"Topic filter: {topic_raw or 'None (all quotes)'}",
        f"Min score: {min_score}/5 | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Quotes found: {len(results)}",
        "=" * 60,
        "",
    ]

    for i, r in enumerate(results, 1):
        ts = f" [{r['timestamp']}]" if r["timestamp"] else ""
        lines_out.append(f"#{i} | Score: {r['score']}/5{ts}")
        lines_out.append(f'  "{r["quote"]}"')
        lines_out.append("")

    output_text = "\n".join(lines_out)
    print(output_text)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"Quotes saved to: {output_path}")
    else:
        base = os.path.splitext(transcript_path)[0]
        auto_path = f"{base}_quotes.txt"
        with open(auto_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"Quotes saved to: {auto_path}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Extract key quotes from an interview transcript.")
    parser.add_argument("--transcript", required=True, help="Path to transcript text file")
    parser.add_argument("--topic", default="", help="Comma-separated topic keywords to prioritize")
    parser.add_argument("--min-score", type=int, default=2,
                        help="Minimum quote score to include (0-5, default: 2)")
    parser.add_argument("--output", help="Output file for quotes")
    args = parser.parse_args()

    extract_quotes(args.transcript, args.topic, args.min_score, args.output)


if __name__ == "__main__":
    main()
