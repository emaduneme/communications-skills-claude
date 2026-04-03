#!/usr/bin/env python3
"""
claim_checker.py — Verify claims using public fact-check databases and web search.

Modes:
  decompose      — Break a claim into verifiable sub-claims
  factcheck-search — Query Google Fact Check Tools API + Google News
  verify-quote   — Search for the original source of a quote

Requires: requests
Optional: GOOGLE_FACTCHECK_API_KEY env var (free at console.developers.google.com)
          Without a key, falls back to Google Fact Check Explorer scraping.

Usage:
  python claim_checker.py --claim "The crime rate dropped 40%" --mode decompose
  python claim_checker.py --claim "Vaccines cause autism" --mode factcheck-search
  python claim_checker.py --quote "We will not negotiate" --source "Mayor Smith" --mode verify-quote
"""

import argparse
import json
import os
import sys
from datetime import datetime
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)


GOOGLE_API_KEY = os.environ.get("GOOGLE_FACTCHECK_API_KEY", "")


def decompose_claim(claim):
    """Break a complex claim into individually verifiable sub-claims using heuristics."""
    print(f"\nDecomposing claim: '{claim}'\n")

    # Heuristic decomposition markers
    markers = {
        "numerical": r'\d+\.?\d*\s*(%|percent|million|billion|thousand|times|x)',
        "causal": r'\b(because|caused by|due to|led to|result of|after|following)\b',
        "temporal": r'\b(since|after|before|in \d{4}|last year|recently|now)\b',
        "attribution": r'\b(according to|said|claimed|reported by)\b',
        "comparative": r'\b(more than|less than|compared to|versus|higher|lower)\b',
    }

    import re
    flags = {}
    for marker_type, pattern in markers.items():
        if re.search(pattern, claim, re.IGNORECASE):
            flags[marker_type] = True

    # Generate sub-claims based on markers found
    sub_claims = []
    words = claim.split()

    if flags.get("numerical"):
        num_match = re.search(r'\d+\.?\d*\s*(%|percent|million|billion|thousand)', claim, re.IGNORECASE)
        if num_match:
            sub_claims.append({
                "sub_claim": f"The number/statistic '{num_match.group()}' is accurate",
                "how_to_verify": "Find the original data source that produced this figure",
                "source_types": ["Government databases", "Official reports", "Peer-reviewed research"],
            })

    if flags.get("temporal"):
        sub_claims.append({
            "sub_claim": "The timeline/date in the claim is accurate",
            "how_to_verify": "Find contemporaneous records or official announcements for the claimed date",
            "source_types": ["News archives", "Official records", "Court documents"],
        })

    if flags.get("causal"):
        sub_claims.append({
            "sub_claim": "The causal relationship claimed is supported by evidence",
            "how_to_verify": "Look for peer-reviewed research or official analyses establishing causation, not just correlation",
            "source_types": ["Academic studies", "Government analysis", "Expert testimony"],
        })

    if flags.get("attribution"):
        sub_claims.append({
            "sub_claim": "The attributed statement was actually made by the named person/organization",
            "how_to_verify": "Find the original recording, document, or transcript",
            "source_types": ["Official transcripts", "Video/audio recordings", "Press releases"],
        })

    # Always add: existence of the subject
    sub_claims.insert(0, {
        "sub_claim": f"The core factual subject of the claim exists as described",
        "how_to_verify": "Verify that the named program, person, organization, or event actually exists",
        "source_types": ["Official websites", "Public records", "News archives"],
    })

    print(f"Found {len(sub_claims)} verifiable components:\n")
    for i, sc in enumerate(sub_claims, 1):
        print(f"  Sub-claim {i}: {sc['sub_claim']}")
        print(f"  How to verify: {sc['how_to_verify']}")
        print(f"  Sources to check: {', '.join(sc['source_types'])}")
        print()

    print("Verification complexity:", end=" ")
    if len(sub_claims) <= 2:
        print("LOW — straightforward to verify")
    elif len(sub_claims) <= 4:
        print("MEDIUM — requires multiple source types")
    else:
        print("HIGH — complex claim, verify each component independently")

    return sub_claims


def search_fact_checks(claim):
    """Query Google Fact Check Tools API for existing fact-checks."""
    print(f"\nSearching fact-check databases for: '{claim}'\n")

    results = []

    # Google Fact Check Tools API
    if GOOGLE_API_KEY:
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {"query": claim, "key": GOOGLE_API_KEY, "pageSize": 10}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            claims = data.get("claims", [])
            for c in claims:
                for review in c.get("claimReview", []):
                    results.append({
                        "claim_text": c.get("text", ""),
                        "claimant": c.get("claimant", "Unknown"),
                        "rating": review.get("textualRating", "N/A"),
                        "reviewer": review.get("publisher", {}).get("name", "Unknown"),
                        "url": review.get("url", ""),
                        "date": review.get("reviewDate", ""),
                    })
        except Exception as e:
            print(f"Google Fact Check API error: {e}")
    else:
        print("Note: Set GOOGLE_FACTCHECK_API_KEY env var for Google Fact Check API access.")
        print("Free key at: https://developers.google.com/fact-check/tools/api/reference/rest\n")

    # Google News RSS search for fact-checks
    news_url = f"https://news.google.com/rss/search?q={quote(claim + ' fact check')}&hl=en-US&gl=US&ceid=US:en"
    import xml.etree.ElementTree as ET
    try:
        resp = requests.get(news_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(resp.content)
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            source_el = item.find("source")
            source = source_el.text if source_el is not None else "Unknown"
            if any(fc in title.lower() for fc in ["fact check", "fact-check", "debunk", "false", "true", "mislead"]):
                results.append({
                    "claim_text": title,
                    "claimant": "N/A",
                    "rating": "See article",
                    "reviewer": source,
                    "url": link,
                    "date": item.findtext("pubDate", ""),
                })
    except Exception as e:
        print(f"Google News search error: {e}")

    if not results:
        print("No existing fact-checks found in databases.")
        print("This does not mean the claim is true — it may not have been checked yet.")
        print("\nRecommended manual sources:")
        print("  - snopes.com")
        print("  - politifact.com")
        print("  - factcheck.org")
        print("  - apnews.com/hub/ap-fact-check")
        print("  - reuters.com/fact-check")
        return []

    print(f"Found {len(results)} fact-check result(s):\n")
    for r in results:
        print(f"  Rating: {r['rating']}")
        print(f"  Reviewer: {r['reviewer']}")
        print(f"  Claim: {r['claim_text'][:100]}")
        print(f"  URL: {r['url'][:80]}")
        print(f"  Date: {r['date'][:20] if r['date'] else 'N/A'}")
        print()

    return results


def verify_quote(quote_text, source_name):
    """Search for the original source of a quote."""
    print(f"\nVerifying quote: '{quote_text[:80]}...' (attributed to {source_name})\n")

    # Search strategies
    searches = [
        f'"{quote_text[:60]}"',
        f'"{source_name}" said "{quote_text[:40]}"',
        f'"{source_name}" "{quote_text[:30]}" original',
    ]

    import xml.etree.ElementTree as ET
    found_sources = []

    for search_query in searches[:2]:  # Limit to 2 searches
        url = f"https://news.google.com/rss/search?q={quote(search_query)}&hl=en-US&gl=US&ceid=US:en"
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:3]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                source_el = item.find("source")
                outlet = source_el.text if source_el is not None else "Unknown"
                pub_date = item.findtext("pubDate", "")
                found_sources.append({
                    "headline": title,
                    "outlet": outlet,
                    "url": link,
                    "date": pub_date,
                })
        except Exception:
            pass

    if found_sources:
        print(f"Potential original sources ({len(found_sources)} found):\n")
        for s in found_sources[:5]:
            print(f"  [{s['outlet']}] {s['headline'][:80]}")
            print(f"   {s['url'][:80]}")
            print(f"   Date: {s['date'][:20] if s['date'] else 'N/A'}")
            print()
        print("Next step: Visit the earliest-dated source and verify the exact wording.")
    else:
        print("No published sources found for this quote.")
        print("Recommendation: Obtain primary documentation (recording, transcript, press release).")

    print("\nQuote verification checklist:")
    print("  [ ] Quote appears in recording/transcript")
    print("  [ ] Quote is not taken out of context — read surrounding paragraphs")
    print("  [ ] Date and setting of the quote are accurate")
    print(f"  [ ] {source_name} has been given opportunity to confirm or correct")

    return found_sources


def main():
    parser = argparse.ArgumentParser(description="Verify claims and quotes for journalism.")
    parser.add_argument("--claim", help="Claim text to verify or decompose")
    parser.add_argument("--quote", help="Quote text to verify (use with --source)")
    parser.add_argument("--source", help="Person attributed with the quote")
    parser.add_argument("--mode", required=True,
                        choices=["decompose", "factcheck-search", "verify-quote"],
                        help="Verification mode")
    args = parser.parse_args()

    if args.mode == "decompose":
        if not args.claim:
            print("--claim required for decompose mode")
            sys.exit(1)
        decompose_claim(args.claim)

    elif args.mode == "factcheck-search":
        if not args.claim:
            print("--claim required for factcheck-search mode")
            sys.exit(1)
        search_fact_checks(args.claim)

    elif args.mode == "verify-quote":
        if not args.quote:
            print("--quote required for verify-quote mode")
            sys.exit(1)
        verify_quote(args.quote, args.source or "Unknown")


if __name__ == "__main__":
    main()
