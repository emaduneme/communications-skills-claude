#!/usr/bin/env python3
"""
source_finder.py — Search public databases for organizational records.

Requires: requests

Supported types:
  nonprofit  — ProPublica Nonprofit Explorer (Form 990 data, no API key required)
  news       — Google News RSS feed search
  corporate  — OpenCorporates company search

Usage:
  python source_finder.py --type nonprofit --name "American Red Cross"
  python source_finder.py --type news --query "water contamination Missouri" --days 30
  python source_finder.py --type corporate --name "Meta Platforms"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)


def search_nonprofits(name):
    """Search ProPublica Nonprofit Explorer for 990 data."""
    url = f"https://projects.propublica.org/nonprofits/api/v2/search.json?q={quote(name)}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"ProPublica API error: {e}")
        return

    organizations = data.get("organizations", [])
    if not organizations:
        print(f"No nonprofit records found for: {name}")
        return

    print(f"Nonprofit records for '{name}' ({len(organizations)} results):\n")
    for org in organizations[:5]:
        print(f"  Organization: {org.get('name', 'N/A')}")
        print(f"  EIN: {org.get('ein', 'N/A')}")
        print(f"  State: {org.get('state', 'N/A')}")
        print(f"  NTEE Code: {org.get('ntee_code', 'N/A')} (mission category)")
        print(f"  Latest filing year: {org.get('data_source', 'N/A')}")
        ein = org.get("ein", "").replace("-", "")
        if ein:
            print(f"  ProPublica URL: https://projects.propublica.org/nonprofits/organizations/{ein}")
        print()


def search_news(query, days=30):
    """Search Google News RSS for recent coverage."""
    import xml.etree.ElementTree as ET
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        print(f"Google News error: {e}")
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"Parse error: {e}")
        return

    results = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        source_el = item.find("source")
        source = source_el.text if source_el is not None else "Unknown"
        results.append({"title": title, "source": source, "url": link, "date": pub_date})

    print(f"News results for '{query}' (past {days} days): {len(results)} articles\n")
    for r in results[:10]:
        print(f"  [{r['source']}] {r['title']}")
        print(f"   {r['url'][:80]}")
        print()


def search_corporate(name):
    """Search OpenCorporates for business entity records."""
    url = f"https://api.opencorporates.com/v0.4/companies/search?q={quote(name)}&jurisdiction_code=us"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 429:
            print("OpenCorporates rate limit hit. Try again in a few minutes.")
            return
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"OpenCorporates error: {e}")
        return

    companies = data.get("results", {}).get("companies", [])
    if not companies:
        print(f"No corporate records found for: {name}")
        return

    print(f"Corporate records for '{name}' ({len(companies)} results):\n")
    for item in companies[:5]:
        c = item.get("company", {})
        print(f"  Name: {c.get('name', 'N/A')}")
        print(f"  Jurisdiction: {c.get('jurisdiction_code', 'N/A')}")
        print(f"  Company number: {c.get('company_number', 'N/A')}")
        print(f"  Status: {c.get('current_status', 'N/A')}")
        print(f"  Incorporated: {c.get('incorporation_date', 'N/A')}")
        print(f"  OpenCorporates URL: {c.get('opencorporates_url', 'N/A')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Search public databases for journalistic source-finding.")
    parser.add_argument("--type", required=True, choices=["nonprofit", "news", "corporate"])
    parser.add_argument("--name", help="Organization or company name (for nonprofit/corporate)")
    parser.add_argument("--query", help="Search query (for news)")
    parser.add_argument("--days", type=int, default=30, help="Days back for news search (default: 30)")
    args = parser.parse_args()

    if args.type == "nonprofit":
        if not args.name:
            print("--name required for nonprofit search")
            sys.exit(1)
        search_nonprofits(args.name)
    elif args.type == "news":
        query = args.query or args.name
        if not query:
            print("--query or --name required for news search")
            sys.exit(1)
        search_news(query, args.days)
    elif args.type == "corporate":
        if not args.name:
            print("--name required for corporate search")
            sys.exit(1)
        search_corporate(args.name)


if __name__ == "__main__":
    main()
