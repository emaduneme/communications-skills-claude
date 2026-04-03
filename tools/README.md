# Standalone CLI Tools

These are optional Python command-line tools for technical users. **They are not required for any skill to work.**

The journalism skills (story-pitch-planner, information-gathering, field-reporting-interviewing, verification-fact-checking) function fully in Claude Desktop and Claude Code without these scripts — Claude handles the workflows using its own knowledge guided by the SKILL.md instructions.

These tools are for users who want to automate specific parts of their workflow from the terminal (e.g., batch transcription, RSS feed monitoring, persistent story tracking).

---

## Tools by skill

### field-reporting/
| Script | What it does |
|--------|-------------|
| `transcribe.py` | Transcribes audio/video files locally using OpenAI Whisper. Outputs a timestamped transcript. |
| `extract_quotes.py` | Scores sentences in a transcript for quote potential. Filters by topic keywords and outputs a ranked quote list. |

**Requires:** `pip install openai-whisper` + `ffmpeg` (for transcribe), stdlib only (for extract_quotes)

### information-gathering/
| Script | What it does |
|--------|-------------|
| `rss_monitor.py` | Monitors RSS feeds for keyword matches. Maintains a `feeds.json` list and outputs a beat digest. |
| `source_finder.py` | Searches ProPublica (nonprofits), OpenCorporates (companies), and Google News RSS for background research. |

**Requires:** `pip install feedparser requests`

### story-pitch-planner/
| Script | What it does |
|--------|-------------|
| `coverage_checker.py` | Queries Google News RSS for existing coverage on a topic and identifies uncovered angles. |
| `story_tracker.py` | Local JSON-based story assignment tracker. Detects duplicate angles using fuzzy matching. |

**Requires:** `pip install requests` (coverage_checker), stdlib only (story_tracker)

### verification-fact-checking/
| Script | What it does |
|--------|-------------|
| `claim_checker.py` | Decomposes claims into verifiable sub-claims, searches Google Fact Check API and Google News for existing fact-checks, and traces quote attribution. |
| `verification_log.py` | Maintains a persistent verification trail for a story. Tracks claim status (Verified, False, Unverified, etc.) and exports a pre-publication report. |

**Requires:** `pip install requests`. Optional: `GOOGLE_FACTCHECK_API_KEY` env var for the Fact Check API (free key at console.developers.google.com).

---

## Who these are for

- Journalists or researchers comfortable running Python from the terminal
- Newsrooms wanting to automate beat monitoring or story deduplication
- Claude Code users who want Claude to invoke these tools directly via Bash

## Who should ignore these

- Claude Desktop users — the skills work without any scripts
- Anyone who hasn't used a terminal before — the skills in the skill folders are all you need
