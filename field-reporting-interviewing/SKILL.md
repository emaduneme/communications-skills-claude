---
name: field-reporting-interviewing
description: >
  Helps journalists prepare for and conduct field reporting and interviews.
  Use this skill when a journalist or student needs to: prepare interview
  questions for a specific source or story, build a pre-interview research brief,
  organize and structure interview notes, transcribe or summarize recorded
  interviews, draft a source contact message or interview request, or develop
  a field reporting checklist. Also trigger for: "help me prepare for an
  interview with X", "what questions should I ask about Y", "organize my
  interview notes", "help me contact this source", "I have an interview transcript,
  help me find the key quotes", or "build me a field checklist". Includes
  Python tools for transcription workflow and notes organization.
---

# Field Reporting & Interviewing Skill

## What this skill does

Prepares reporters for the field and helps them extract maximum value from interviews:
1. Pre-interview research and question development
2. Source contact drafting (interview request emails/messages)
3. Field reporting checklists
4. Interview notes organization and quote extraction
5. Transcription workflow (via Whisper)

---

## Workflow

### Step 1 — Pre-interview preparation

Before any interview, do the following research:

**Web search:**
```
"[Source name]" biography OR background OR "has said"
"[Source name]" past statements OR quotes OR testimony
"[topic]" recent developments [current month year]
```

**Build a source profile:**
- What is their role/expertise?
- What have they said publicly before? (Look for consistency or contradictions)
- What is their potential bias or stake in the story?
- What do critics say about their position?

### Step 2 — Question development

Structure questions across 4 tiers:

**Tier 1 — Context (warm-up, build rapport):**
Open, biographical, easy to answer. Do not start here with hard accusations.
Example: "Can you walk me through how you got involved with this issue?"

**Tier 2 — Facts and timeline:**
What happened, when, and who was involved?
Example: "When did your organization first become aware of X?"

**Tier 3 — Accountability and conflict:**
The harder questions — contradictions, responsibility, failures.
Example: "Documents show that on [date] your office received a report about X. Why wasn't action taken sooner?"

**Tier 4 — Forward-looking and human:**
What should happen? What would you say to those affected?
Example: "What would you tell families who lost [X] because of this?"

Always end with: "Is there anything I haven't asked that you think is important?"

**Question rules:**
- One question at a time — never bundle
- Follow silence — wait after an answer before jumping in
- Have 30% more questions than you need
- Put your most important questions in the middle, not the end

### Step 3 — Interview request drafting

Use the message_compose skill or draft directly:

```
Subject: Interview Request — [Brief topic description]

Dear [Name],

I'm [name], a reporter with [outlet]. I'm working on a story about [topic] and 
your perspective as [role] would be valuable.

I'm hoping to speak with you for approximately [time]. The interview would 
focus on [2-3 specific topics].

I'm available [dates/times]. Please let me know what works for you, or if 
you'd prefer I speak with someone else in your office.

[Name] | [Contact info] | Deadline: [date]
```

### Step 4 — Field checklist

Before leaving for the field:

```bash
python scripts/field_checklist.py --story "Story name" --interview-count 3
```

Or manually verify:
- [ ] Recording device charged and tested (and backup — phone)
- [ ] Extra storage/batteries
- [ ] Notebook and multiple pens
- [ ] Press credentials
- [ ] Source contact information (phone + email offline)
- [ ] Pre-interview research brief printed or saved offline
- [ ] Questions printed (in order of priority)
- [ ] Consent disclosure ready ("I'm recording this, do you consent?")
- [ ] Location confirmed and directions downloaded
- [ ] Editor knows your location and expected return time

### Step 5 — Post-interview: notes and transcription

**For recorded interviews:**

```bash
# Transcribe with OpenAI Whisper (requires: pip install openai-whisper)
python scripts/transcribe.py --audio interview.mp3 --output transcript.txt

# Extract key quotes from a transcript
python scripts/extract_quotes.py --transcript transcript.txt --topic "housing policy"
```

**For handwritten notes:**

Organize immediately after the interview — do not wait. Use this format:

```
INTERVIEW: [Source name, title]
Date/time: [Date]
Location/medium: [In person / Phone / Zoom]
Recorder: [Yes/No — consent obtained: Yes/No]

KEY QUOTES (verbatim):
Q1: "[Exact words]"
Q2: "[Exact words]"

PARAPHRASES (attributed but not verbatim):
- [Source] said X in response to question about Y

FOLLOW-UP NEEDED:
- Verify claim that [X]
- Obtain document [Y]
- Contact [Z] for corroboration

OFF THE RECORD / NOT FOR ATTRIBUTION:
[Do not write verbatim — note topics discussed and agreed restrictions]
```

### Step 6 — Quote verification

Before publishing any quote:
1. Cross-reference with recording — do not rely on memory
2. For long quotes: read back to source if time allows
3. Never alter a quote to change its meaning — paraphrase instead
4. Label paraphrases as paraphrases in your notes

---

## Python Scripts

### scripts/transcribe.py
Transcribes audio files using OpenAI Whisper (runs locally, free).
Requires: `pip install openai-whisper` and FFmpeg.

```bash
python scripts/transcribe.py --audio interview.mp3
python scripts/transcribe.py --audio interview.mp4 --model medium --output transcript.txt
```

### scripts/extract_quotes.py
Scans a transcript for potential key quotes based on topic keywords.
Flags sentences with attribution verbs and emotional/emphatic language.

```bash
python scripts/extract_quotes.py --transcript transcript.txt --topic "budget cuts"
```

### scripts/field_checklist.py
Generates a pre-field checklist and saves it as a text file.

```bash
python scripts/field_checklist.py --story "City council vote" --interview-count 2
```

---

## Notes for the AI

- When developing questions, always tailor them to the specific source's known positions — generic questions produce generic answers
- Flag when a source has previously made conflicting statements on record — this is interview ammunition
- For hostile or defensive sources, sequence is critical: do not lead with accusations
- Always remind reporters to state recording consent out loud on the tape itself, not just before pressing record
- When extracting quotes from notes, flag any quote that appears to be paraphrased rather than verbatim
