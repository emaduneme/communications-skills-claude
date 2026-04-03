#!/usr/bin/env python3
"""
rss_monitor.py — Monitor RSS feeds for keyword matches on your beat.

Requires: feedparser, requests

Install: pip install feedparser requests

Usage:
  python rss_monitor.py --feeds feeds.json --keywords "housing,eviction" --days 7
  python rss_monitor.py --feeds feeds.json --keywords "school budget" --output digest.txt
  python rss_monitor.py --add-feed "AP News" "https://rsshub.app/apnews/topics/apf-topnews"

feeds.json example:
  {
    "feeds": [
      {"name": "AP Top News", "url": "https://rsshub.app/apnews/topics/apf-topnews"},
      {"name": "Reuters", "url": "https://feeds.reuters.com/reuters/topNews"},
      {"name": "NPR News", "url": "https://feeds.npr.org/1001/rss.xml"}
    ]
  }
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

try:
    import feedparser
except ImportError:
    print("Install feedparser: pip install feedparser")
    sys.exit(1)

FEEDS_FILE_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data", "feeds.json")


def load_feeds(path):
    if not os.path.exists(path):
        return {"feeds": []}
    with open(path) as f:
        return json.load(f)


def save_feeds(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def parse_date(entry):
    """Try to parse a feedparser entry's published date."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    return None


def matches_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw.strip().lower() in text_lower for kw in keywords)


def monitor_feeds(feeds_path, keywords_raw, days=7, output_file=None):
    data = load_feeds(feeds_path)
    feeds = data.get("feeds", [])

    if not feeds:
        print("No feeds configured. Add feeds with --add-feed or edit feeds.json.")
        return

    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    print(f"Monitoring {len(feeds)} feeds for keywords: {keywords}")
    print(f"Looking back {days} days (since {cutoff.strftime('%Y-%m-%d')})\n")

    all_matches = []

    for feed_config in feeds:
        name = feed_config.get("name", "Unknown")
        url = feed_config.get("url", "")
        if not url:
            continue

        try:
            parsed = feedparser.parse(url)
        except Exception as e:
            print(f"  [Error] {name}: {e}")
            continue

        feed_matches = []
        for entry in parsed.entries:
            title = getattr(entry, "title", "")
            summary = getattr(entry, "summary", "")
            link = getattr(entry, "link", "")
            text = f"{title} {summary}"

            pub_date = parse_date(entry)
            if pub_date and pub_date < cutoff:
                continue

            if not keywords or matches_keywords(text, keywords):
                feed_matches.append({
                    "source": name,
                    "title": title,
                    "url": link,
                    "published": pub_date.strftime("%Y-%m-%d %H:%M") if pub_date else "Unknown",
                    "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                })

        print(f"  [{name}]: {len(feed_matches)} match{'es' if len(feed_matches) != 1 else ''}")
        all_matches.extend(feed_matches)

    # Sort by date (newest first)
    all_matches.sort(key=lambda x: x["published"], reverse=True)

    output_lines = [
        f"\nBEAT DIGEST — Keywords: {', '.join(keywords)}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total matches: {len(all_matches)}\n",
        "=" * 60,
    ]

    for item in all_matches:
        output_lines.append(f"\n[{item['source']}] {item['published']}")
        output_lines.append(f"  {item['title']}")
        output_lines.append(f"  {item['url']}")
        if item["summary"]:
            output_lines.append(f"  Summary: {item['summary']}")

    output_text = "\n".join(output_lines)
    print(output_text)

    if output_file:
        with open(output_file, "w") as f:
            f.write(output_text)
        print(f"\nDigest saved to: {output_file}")

    return all_matches


def add_feed(feeds_path, name, url):
    data = load_feeds(feeds_path)
    for f in data["feeds"]:
        if f["url"] == url:
            print(f"Feed already exists: {name}")
            return
    data["feeds"].append({"name": name, "url": url})
    save_feeds(data, feeds_path)
    print(f"Added feed: {name} ({url})")


def list_feeds(feeds_path):
    data = load_feeds(feeds_path)
    feeds = data.get("feeds", [])
    if not feeds:
        print("No feeds configured.")
        return
    print(f"Configured feeds ({len(feeds)}):")
    for f in feeds:
        print(f"  - {f['name']}: {f['url']}")


def main():
    parser = argparse.ArgumentParser(description="Monitor RSS feeds for your beat.")
    parser.add_argument("--feeds", default=FEEDS_FILE_DEFAULT, help="Path to feeds.json")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords to match")
    parser.add_argument("--days", type=int, default=7, help="Days to look back (default: 7)")
    parser.add_argument("--output", help="Save digest to file")
    parser.add_argument("--add-feed", nargs=2, metavar=("NAME", "URL"), help="Add a new RSS feed")
    parser.add_argument("--list-feeds", action="store_true", help="List all configured feeds")
    args = parser.parse_args()

    if args.add_feed:
        add_feed(args.feeds, args.add_feed[0], args.add_feed[1])
    elif args.list_feeds:
        list_feeds(args.feeds)
    else:
        monitor_feeds(args.feeds, args.keywords, args.days, args.output)


if __name__ == "__main__":
    main()
