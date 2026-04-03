#!/usr/bin/env python3
"""
coverage_checker.py — Search for existing news coverage on a topic.

Requires: requests

Usage:
  python coverage_checker.py --topic "eviction rates" --days 90
  python coverage_checker.py --topic "police body cameras" --outlet "local" --days 30
  python coverage_checker.py --topic "school funding" --output coverage_report.json
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)


def search_google_news_rss(topic, days=90):
    """Fetch headlines from Google News RSS for a topic."""
    from urllib.parse import quote
    import xml.etree.ElementTree as ET

    url = f"https://news.google.com/rss/search?q={quote(topic)}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        return [], f"Google News RSS error: {e}"

    cutoff = datetime.now() - timedelta(days=days)
    results = []

    try:
        root = ET.fromstring(resp.content)
        for item in root.findall(".//item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date_str = item.findtext("pubDate", "")
            source_el = item.find("source")
            source = source_el.text if source_el is not None else "Unknown"

            # Parse date
            pub_date = None
            for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]:
                try:
                    pub_date = datetime.strptime(pub_date_str.strip(), fmt)
                    break
                except ValueError:
                    continue

            if pub_date and pub_date.replace(tzinfo=None) < cutoff:
                continue

            results.append({
                "title": title,
                "source": source,
                "url": link,
                "published": pub_date_str,
            })
    except ET.ParseError as e:
        return [], f"XML parse error: {e}"

    return results, None


def analyze_coverage(results, topic):
    """Summarize coverage patterns."""
    if not results:
        return {
            "total_articles": 0,
            "sources": [],
            "summary": "No recent coverage found. This topic may be underreported.",
            "gap_indicators": ["No existing coverage — strong opportunity for original reporting."],
        }

    sources = list({r["source"] for r in results})
    titles = [r["title"] for r in results]

    # Detect common angles from titles
    angle_keywords = {
        "investigation": ["probe", "invest", "examin", "scrutin", "watchdog"],
        "data/statistics": ["data", "statistic", "number", "rate", "percent", "study"],
        "human interest": ["family", "communit", "lives", "story", "face", "struggle"],
        "policy/government": ["law", "bill", "legislat", "polic", "government", "official"],
        "accountability": ["fail", "critic", "challeng", "controv", "scandal", "wrong"],
    }

    covered_angles = {}
    for angle, keywords in angle_keywords.items():
        matches = sum(1 for t in titles if any(k in t.lower() for k in keywords))
        if matches > 0:
            covered_angles[angle] = matches

    uncovered = [a for a in angle_keywords if a not in covered_angles]

    return {
        "total_articles": len(results),
        "sources": sources[:10],
        "covered_angles": covered_angles,
        "potential_uncovered_angles": uncovered,
        "summary": f"Found {len(results)} articles from {len(sources)} outlets in the search window.",
        "gap_indicators": [
            f"Angle '{a}' not yet covered — potential pitch opportunity" for a in uncovered
        ] or ["Topic is well-covered — look for a differentiated local or solutions angle."],
    }


def main():
    parser = argparse.ArgumentParser(description="Check existing news coverage for a story topic.")
    parser.add_argument("--topic", required=True, help="Topic or keywords to search")
    parser.add_argument("--days", type=int, default=90, help="How many days back to search (default: 90)")
    parser.add_argument("--output", help="Save results to JSON file")
    args = parser.parse_args()

    print(f"Searching coverage for: '{args.topic}' (past {args.days} days)...\n")

    results, error = search_google_news_rss(args.topic, args.days)
    if error:
        print(f"Error: {error}", file=sys.stderr)

    analysis = analyze_coverage(results, args.topic)

    # Display
    print(f"Coverage summary: {analysis['summary']}\n")
    print(f"Sources: {', '.join(analysis['sources'][:5]) or 'None found'}\n")

    if analysis.get("covered_angles"):
        print("Angles already covered:")
        for angle, count in analysis["covered_angles"].items():
            print(f"  - {angle} ({count} article{'s' if count > 1 else ''})")
        print()

    print("Gap indicators (pitch opportunities):")
    for gap in analysis["gap_indicators"]:
        print(f"  * {gap}")

    print(f"\nRecent headlines ({min(5, len(results))} of {len(results)}):")
    for r in results[:5]:
        print(f"  [{r['source']}] {r['title']}")
        print(f"   {r['url'][:80]}...")
        print()

    if args.output:
        output_data = {"topic": args.topic, "days": args.days, "analysis": analysis, "articles": results}
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"Full results saved to {args.output}")


if __name__ == "__main__":
    main()
