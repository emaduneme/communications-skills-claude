---
name: verification-fact-checking
description: >
  Helps journalists verify claims, quotes, statistics, and sources before
  publication. Use this skill when a journalist or student needs to: fact-check
  a specific claim or statistic, verify a quote or source attribution, check
  whether a data point is accurate, identify the original source of a claim,
  check an image or video for manipulation, verify a source's identity or
  credentials, or build a verification trail for a story. Also trigger for:
  "is this true", "verify this claim", "where does this statistic come from",
  "check this quote", "who said this originally", "is this image real",
  "how do I verify X", or "fact-check this". Combines web search, the
  Google Fact Check API, claim decomposition, and Python verification tools.
---

# Verification & Fact-Checking Skill

## What this skill does

Provides journalists with a structured verification pipeline:
1. Decompose complex claims into individually verifiable sub-claims
2. Search for prior fact-checks on a claim
3. Find primary sources for statistics and data
4. Check quote attribution and accuracy
5. Flag red flags in images, videos, or documents
6. Build a documented verification trail

---

## Core principle

**Verification is documentation.** For every fact you publish, you need to be able to answer:
- Who said or produced it?
- Where can I point a reader to see it themselves?
- What would change my mind?

---

## Workflow

### Step 1 — Decompose the claim

Break any complex claim into the smallest individually verifiable units.

Example claim: "The city's crime rate dropped 40% after the new police program launched in 2022."

Sub-claims:
1. There is a police program that launched in 2022. (Verifiable: check city records)
2. Crime rate dropped 40%. (Verifiable: check official crime statistics)
3. The drop is causally linked to the program. (Harder — requires analysis)

Run decomposition automatically:

```bash
python scripts/claim_checker.py --claim "The city's crime rate dropped 40% after the new program" --mode decompose
```

### Step 2 — Search for existing fact-checks

Use web_search:
```
"[claim keywords]" fact check OR debunked OR verified
"[claim keywords]" site:snopes.com OR site:politifact.com OR site:factcheck.org
```

Or run the fact-check search tool:

```bash
python scripts/claim_checker.py --claim "Claim text here" --mode factcheck-search
```

This queries:
- Google Fact Check API (aggregates Snopes, PolitiFact, FactCheck.org, AP Fact Check, Reuters Fact Check)
- Google News for recent debunks

### Step 3 — Find primary sources

For **statistics**: Go to the original producing organization, not the news article that reported them.

Common primary source categories:

| Claim type | Go here first |
|-----------|---------------|
| Crime statistics | FBI UCR, local PD annual reports |
| Health/medical | CDC, NIH, peer-reviewed journals (PubMed) |
| Economic data | BLS, Census Bureau, Federal Reserve |
| Environmental | EPA, NOAA, peer-reviewed science |
| Corporate claims | SEC filings, company annual reports |
| Government claims | Official agency websites, FOIA records |
| Historical events | Library of Congress, National Archives |

web_search pattern: `"[statistic]" site:cdc.gov` or `"[claim]" site:bls.gov filetype:pdf`

### Step 4 — Verify the quote

For attributed quotes:
1. Do you have a recording? Use that — do not rely on notes alone.
2. Does the quote appear in a prior published source? Find the original, not a republication.
3. Search: `"[exact quote phrase]"` — Google will surface the original publication if it's widely reported.
4. For social media quotes: archive the post before it can be deleted.

```bash
python scripts/claim_checker.py --mode verify-quote --quote "Exact quote text" --source "Name"
```

### Step 5 — Image/video verification

**Quick checks (no tools needed):**
- Reverse image search: drag into Google Images or TinEye
- Check image metadata: use ExifTool (`exiftool image.jpg`)
- Look for inconsistencies: shadows, edges, lighting, duplicated textures

**For deeper investigation:**
- InVID/WeVerify browser extension: video frame analysis
- FotoForensics.com: error level analysis (free, upload required)
- AI-generated image detection: Hive Moderation, AI or Not

```bash
python scripts/verify_media.py --image photo.jpg --check-metadata --check-exif
```

### Step 6 — Build the verification trail

For every verified claim, document:

```
CLAIM: "[Exact claim text]"
STATUS: [Verified / Unverified / False / Partially true / Needs more evidence]
PRIMARY SOURCE: [URL or document name]
ACCESSED: [Date]
NOTES: [What you found, any caveats or context]
VERIFIED BY: [Reporter name]
```

Save the full trail:

```bash
python scripts/verification_log.py --add --claim "Crime rate dropped 40%" \
  --status "Partially verified" \
  --source "https://fbi.gov/crime-data/2022" \
  --notes "40% figure applies only to violent crime, not overall crime rate"
```

### Step 7 — Pre-publication checklist

Before sending the story to an editor:

- [ ] Every statistic has a named primary source
- [ ] Every quote is from a recording or contemporaneous document
- [ ] Every claim with a named person has been given opportunity to respond
- [ ] Contested or contested claims are labeled as such in the story
- [ ] Images and video have been reverse-searched
- [ ] Verification trail is saved and accessible

---

## Python Scripts

### scripts/claim_checker.py
Three modes:
- `decompose`: Breaks a claim into sub-claims
- `factcheck-search`: Queries Google Fact Check Tools API + Google News
- `verify-quote`: Searches for the original source of a quote

```bash
python scripts/claim_checker.py --claim "TEXT" --mode decompose
python scripts/claim_checker.py --claim "TEXT" --mode factcheck-search
python scripts/claim_checker.py --quote "QUOTE TEXT" --source "Person Name" --mode verify-quote
```

### scripts/verification_log.py
Maintains a JSON log of verification decisions for a story.
Produces a clean verification trail that can be shared with editors.

```bash
python scripts/verification_log.py --add --claim "TEXT" --status "Verified" --source "URL"
python scripts/verification_log.py --list --story "Story name"
python scripts/verification_log.py --export --story "Story name" --output trail.txt
```

### scripts/verify_media.py
Checks image/video file metadata (EXIF) for signs of manipulation or misdating.
Requires: `pip install Pillow`

```bash
python scripts/verify_media.py --image photo.jpg
python scripts/verify_media.py --image photo.jpg --check-exif --verbose
```

---

## Notes for the AI

- Never present a web search result as verification — it is a lead, not proof
- If a claim cannot be verified with available tools, say so explicitly and suggest what would be needed
- Distinguish between: (a) "we found no evidence this is true" and (b) "we found evidence this is false" — these are different conclusions
- When using the fact-check API, cross-reference at least 2 independent fact-checkers before calling something debunked
- For contested empirical claims (policy effectiveness, causality), note the range of expert opinion, not just one side
- Always flag when a primary source has a potential conflict of interest
