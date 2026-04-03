---
name: information-gathering
description: >
  Supports journalists in research, source discovery, and information aggregation.
  Use this skill whenever a journalist or student needs to: monitor RSS feeds or
  news sources for breaking stories, aggregate coverage on a beat, research
  background on a person, organization, or topic, find primary sources and public
  records, identify expert sources for a story, or build a research brief before
  reporting. Also trigger for: "find me background on X", "monitor news about Y",
  "who are experts on Z", "search for public records on", "help me research",
  "what do we know about", or "aggregate recent coverage on". Combines web search,
  RSS feed monitoring, and Python-based source aggregation tools.
---

# Information Gathering & Research Skill

## What this skill does

Equips journalists with structured workflows and tools to:
1. Monitor beats via RSS feeds and keyword alerts
2. Aggregate and summarize recent coverage on a topic
3. Build source lists (experts, officials, affected communities)
4. Find primary sources: public records, datasets, government documents
5. Generate a research brief before field reporting

---

## Workflow

### Step 1 — Define the research scope

Clarify:
- **Topic**: What are you researching?
- **Purpose**: Background context? Source-finding? Breaking news monitoring?
- **Time horizon**: Current (past 7 days) / Recent (past 3 months) / Historical?
- **Geography**: Local, national, international?

### Step 2 — Aggregate current coverage

Run web_search using multiple query types:

```
"[topic]" news [current month year]
"[topic]" site:gov OR site:edu OR site:org
"[topic]" data OR statistics OR report OR study
"[topic]" "according to" OR "spokesperson" OR "official said"
```

For ongoing beat monitoring, use the RSS monitor script:

```bash
python scripts/rss_monitor.py --feeds feeds.json --keywords "keyword1,keyword2" --days 7
```

### Step 3 — Find primary sources

**Public records by category:**

| Source | Type | URL |
|--------|------|-----|
| data.gov | Federal datasets | data.gov |
| PACER | Federal court records | pacer.gov |
| SEC EDGAR | Corporate filings | sec.gov/edgar |
| ProPublica Nonprofit Explorer | 990 tax forms | projects.propublica.org/nonprofits |
| Google Scholar | Academic research | scholar.google.com |
| Bellingcat Toolkit | OSINT/investigation | bellingcat.com |

Use web_search: `"[organization]" site:sec.gov` or `"[topic]" filetype:pdf site:gov`

Run the source finder for nonprofit/corporate lookups:

```bash
python scripts/source_finder.py --type nonprofit --name "Organization Name"
python scripts/source_finder.py --type corporate --name "Company Name"
```

### Step 4 — Build a source list

Every story needs sources across these categories:
1. **Official**: Spokespeople, government agencies, institutions
2. **Expert**: Academics, researchers, think tanks (Google Scholar, university directories)
3. **Affected community**: People directly experiencing the issue
4. **Opposing voices**: Critics, advocates with a different view
5. **Documentary**: Reports, datasets, public records

web_search query for experts: `"[topic]" professor OR researcher "[relevant field]" contact`

### Step 5 — Produce a research brief

```
RESEARCH BRIEF: [Topic]
Date: [Today]
Prepared for: [Story/Reporter]

BACKGROUND (3-5 sentences):
[Context, history, current status]

KEY FACTS:
- [Fact | Source URL]
- [Statistic | Source URL]

PRIMARY SOURCES FOUND:
- [Document name | URL | Why relevant]

EXPERT SOURCES:
- [Name | Affiliation | Why relevant | Contact if found]

COVERAGE GAPS:
- [What has NOT been reported]

SUGGESTED NEXT STEPS:
- [FOIA request for X]
- [Interview Y]
- [Verify Z with dataset]
```

---

## Python Scripts

### scripts/rss_monitor.py
Monitors a configurable list of RSS feeds for keyword matches.
Outputs a digest of matched stories with headlines, sources, and links.

```bash
# First, populate feeds.json with your RSS URLs (see feeds.json.example)
python scripts/rss_monitor.py --feeds feeds.json --keywords "eviction,housing" --days 3
python scripts/rss_monitor.py --feeds feeds.json --keywords "budget cuts" --output digest.txt
```

### scripts/source_finder.py
Searches public databases (ProPublica Nonprofit API, OpenCorporates) for organizational records.

```bash
python scripts/source_finder.py --type nonprofit --name "Red Cross"
python scripts/source_finder.py --type news --query "water contamination" --days 30
```

---

## Notes for the AI

- Always label facts as "needs verification" unless they come from a primary source you have directly examined
- Government (.gov), academic (.edu), and established nonprofit sites have higher baseline credibility than news aggregators
- Present the source URL alongside every fact pulled from web search
- For ongoing beats, recommend setting up the RSS monitor rather than repeating manual searches
- When generating a source list, do not invent contact information — find it or flag it as missing
