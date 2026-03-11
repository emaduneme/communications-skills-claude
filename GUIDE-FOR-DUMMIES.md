# How to Install and Use These Claude Skills

No technical experience required.

---

## Before You Start

**You need a Claude account.** These skills work with any paid Claude plan (Pro, Team, or higher). The free tier has limited context — skills may still work, but attaching your own reference files works best on a paid plan.

**You don't need to know how to code.** Everything here is copy-paste.

---

## What Is a "Skill"?

A skill is a set of instructions you give Claude once — and it follows them every time.

Without a skill, you'd have to explain your needs from scratch every conversation: *"Write this in AP style, use an inverted pyramid, include a boilerplate, ask me who to quote before starting..."*

With a skill, Claude already knows all of that. You just say *"write a press release for our grant announcement"* and it does the right thing.

The 8 skills in this collection are those instruction sets — professionally written, ready to paste in.

---

## Which Skills Work Right Away

Some skills need no setup at all. Start with one of these:

| Skill | Folder | Good for |
|-------|--------|----------|
| Press Release & Crisis Comms | `04-press-release/` | Any organizational announcement or public statement |
| Content Calendar | `05-content-calendar/` | Planning social media and editorial schedules |
| Brand Voice Guide | `06-brand-voice/` | Defining how your org should sound in writing |
| Media Pitch | `07-media-pitch/` | Getting press coverage, pitching op-eds, booking podcasts |
| Internal Communications | `08-internal-comms/` | Staff memos, change announcements, leadership messages |

The other three (Cover Letter, Manuscript Review, Email Drafting) work better when you add your own writing samples — see [Personalizing Skills](#personalizing-skills-1-3) below.

---

## Step 1: Get the Files

### If you're on GitHub

Click the green **Code** button at the top of the repo, then **Download ZIP**. Unzip it anywhere on your computer.

### If someone sent you the folder directly

You already have the files. Open the folder — you'll see directories named `01-cover-letter-gen`, `02-manuscript-review`, and so on.

---

## Step 2: Pick a Skill

Decide which skill you want to install. You'll upload just that skill's folder (not the entire collection).

---

## Step 3: Install the Skill in Claude

### Option A: Upload via Claude.ai (recommended)

This is the official installation method. Skills are uploaded as a zipped folder through Claude's Skills interface.

1. Find the skill folder you want (e.g., `04-press-release/`)
2. Zip that folder:
   - **Mac**: Right-click the folder → Compress
   - **Windows**: Right-click the folder → Send to → Compressed (zipped) folder
3. Open [claude.ai](https://claude.ai) in your browser
4. Go to **Settings → Capabilities → Skills**
5. Click **Upload skill** and select the `.zip` file you just made
6. The skill will appear in your skills list — toggle it on
7. Start a new conversation — Claude will now use the skill automatically when relevant

> You can upload all 8 skills individually and toggle them on or off as needed.

### Option B: Claude Code (developer tool)

```bash
# Place the skill folder in your Claude skills directory
cp -r 04-press-release/ ~/.claude/skills/

# In any Claude Code session, invoke it
/04-press-release
```

### Option C: Project Instructions (manual, no upload required)

If the Skills upload interface isn't available in your region or plan, you can manually paste the skill instructions:

1. Open the skill folder and open `SKILL.md` in any text editor
2. Select all the text (Cmd+A / Ctrl+A) and copy it
3. In Claude, create a **New Project** (left sidebar)
4. Open **Project Instructions** and paste the `SKILL.md` text
5. Save — every conversation in that project will follow the skill

> This works but bypasses the official Skills infrastructure. The upload method (Option A) is preferred.

---

## Step 4: Use It

Once the skill is loaded, just describe what you need in plain language. Claude will ask any clarifying questions it needs, then produce the output.

**Examples of what to say:**

| Skill | Say something like... |
|-------|-----------------------|
| Press Release | "Write a press release announcing our new research grant. The lead researcher is Dr. Maria Chen." |
| Media Pitch | "I published a study on AI in newsrooms. Help me pitch it to a reporter at Nieman Lab." |
| Brand Voice | "Help me define the brand voice for our nonprofit. We focus on environmental health in low-income communities." |
| Internal Comms | "I need to tell my team that we're restructuring two departments and one team lead is being reassigned." |
| Content Calendar | "Build me a month of LinkedIn content for a journalism professor who studies misinformation." |

Claude will never fabricate details — if it needs something it doesn't have, it will ask.

---

## Personalizing Skills 1–3

The Cover Letter, Email Drafting, and Manuscript Review skills work out of the box — but they get much better when you give them your own materials.

### What to add and where

Each of those skill folders has a `references/` subfolder with placeholder files. Open each file — they explain exactly what to add. Then do one of the following:

**In a Claude Project (recommended):**
Upload the filled-in reference files directly to the project. Claude will reference them automatically.

**In a regular conversation:**
Paste the content of the reference file directly into the chat when you start. For example, paste your CV text before asking for a cover letter.

### What each skill benefits from

| Skill | What to provide |
|-------|----------------|
| Cover Letter (`01`) | Your CV/resume, 2–3 cover letters you've sent before |
| Manuscript Review (`02`) | A sample of your writing voice (optional but helpful) |
| Email Drafting (`03`) | 3–4 emails you've sent that you're happy with, your preferred sign-offs |

---

## Troubleshooting

**The skill isn't loading automatically.**
Check that the skill is toggled on in Settings → Capabilities → Skills. Start a fresh conversation after enabling it — skills don't activate mid-conversation.

**It doesn't sound like me.**
Add your voice samples. For Email Drafting, add `references/voice-samples.md` with 3–4 emails you've written. For Cover Letter, add 2–3 letters you've sent. Upload the filled-in file to the same skill zip or attach it to your Claude project.

**I want to use multiple skills at once.**
Upload each skill individually and toggle them all on. Claude can use multiple active skills simultaneously.

**I want to edit a skill.**
Open `SKILL.md` in any text editor, make your changes, re-zip the folder, and re-upload it via Settings → Capabilities → Skills.

**I updated a skill file. Do I need to reinstall?**
Yes — re-zip the updated folder and upload it again to replace the previous version.

**Is my CV or writing data stored anywhere?**
Your data goes to Claude (Anthropic) as part of your conversation. It follows Anthropic's standard privacy policy and is not stored in this repo. If you have concerns, use summarized or anonymized versions of sensitive documents.

---

## Still Stuck?

Open an issue on this GitHub repository. Include: which skill you're trying to use, which step you got stuck on, and what happened (or didn't happen).
