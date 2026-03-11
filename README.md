![Communications Skills for Claude](git-image.png)

# Communications Professional Skills for Claude

A collection of 8 Claude skills for communications researchers, PR professionals, journalists, and academic communicators. Each skill is a ready-to-use prompt template that extends Claude with specialized expertise for your communication workflows.

**Works with Claude Desktop and Claude Code.**

> **First time here?** Read [GUIDE-FOR-DUMMIES.md](GUIDE-FOR-DUMMIES.md) — it explains everything from scratch in plain English.

These skills were built following Anthropic's official methodology. If you want to build your own skills or understand how these are structured, refer to the Skills and Best Practices guides in the Anthropic developer documentation.

---

## Skills

### Personal Skills — Require Your Own Materials

These skills are designed around *you*. They work best when you add your CV, writing samples, or preferences. Each skill folder includes placeholder files with step-by-step instructions on what to provide.

| # | Skill | Folder | What It Does | Setup Needed |
|---|-------|--------|-------------|--------------|
| 1 | Cover Letter Generator | [`01-cover-letter-gen/`](01-cover-letter-gen/) | Tailored cover letters from a job posting + your CV. Handles academic, industry, and hybrid roles. | Add your CV, voice samples + letter template |
| 2 | Manuscript Review | [`02-manuscript-review/`](02-manuscript-review/) | Multi-pass review catching citation errors, statistical issues, copy-paste artifacts, and style inconsistencies. Fixes presented 1–2 at a time. | Add writing sample (optional) |
| 3 | Email Drafting | [`03-email-drafting/`](03-email-drafting/) | Context-aware professional emails calibrated to relationship and purpose. Covers academic, administrative, networking, and career contexts. | Add voice samples + sign-offs |

### General Skills — Ready To Use Immediately

These work out of the box with no setup required. Skills 4, 6, 7, and 8 also include optional reference files — placeholder templates you can fill with your organization's specific materials to get more tailored outputs.

| # | Skill | Folder | What It Does | Optional Customization |
|---|-------|--------|-------------|------------------------|
| 4 | Press Release & Crisis Comms | [`04-press-release/`](04-press-release/) | AP-style press releases, crisis statements, media advisories, and position statements. | Add org boilerplate |
| 5 | Content Calendar | [`05-content-calendar/`](05-content-calendar/) | Content strategies with pillar definitions, platform selection, and posting schedules with specific content prompts. | None |
| 6 | Brand Voice Guide | [`06-brand-voice/`](06-brand-voice/) | Brand voice documentation with "but not" qualifiers, do/don't examples, tone spectrums, and platform-specific guidelines. | Voice discovery worksheet + one-pager template |
| 7 | Media Pitch | [`07-media-pitch/`](07-media-pitch/) | Targeted pitches for journalists, editors, and podcast hosts. Covers research translation, op-eds, and expert sourcing. | Add your media contacts + past successful pitches |
| 8 | Internal Communications | [`08-internal-comms/`](08-internal-comms/) | Organizational announcements, change management messages, and difficult news communications. | FAQ builder, talking points + comms plan templates |

---

## Quick Install

### Claude Desktop (no coding required)

1. Open the skill folder you want (e.g., `04-press-release/`)
2. Open `SKILL.md` and copy all the text
3. In Claude Desktop, go to **Settings → Profile → Custom Instructions** and paste it in
4. Start a new conversation and use the trigger phrase listed in the skill's README

> For personal skills (1–3): also read the skill's README to see what reference files to add.

### Claude Code

```bash
# Copy a skill folder to your Claude skills directory
cp -r 04-press-release/ ~/.claude/skills/press-release/

# Then invoke it in any Claude Code session
/press-release
```

---

## Not Sure Where to Start?

- **Just want something that works right now?** → Skill 4 (Press Release) or Skill 8 (Internal Comms). Paste and go.
- **Want emails that actually sound like you?** → Skill 3 (Email Drafting).
- **Academic or researcher?** → Skill 2 (Manuscript Review) or Skill 7 (Media Pitch).
- **Building a brand or content presence?** → Skill 6 (Brand Voice), then Skill 5 (Content Calendar).

---

## Skill Dependencies

These skills can produce output for other skills, but those skills are **separate products** — they are not included here. Install them independently via Claude Desktop or Claude Code.

| This skill | Works with (external) | For |
|------------|----------------------|-----|
| Skill 2 (Manuscript Review) | `academic-research` skill | Statistical write-up templates, results section rewrites |
| Skill 4 (Press Release) | `docx` skill | Formatted Word document output |
| Skill 5 (Content Calendar) | `xlsx` skill | Spreadsheet-format editorial calendar |
| Skill 6 (Brand Voice) | `docx`, `pptx`, or `pdf` skill | Team-ready formatted guide, slide deck, or PDF |

---

## Questions / Issues

Found a bug or have a suggestion? Open an issue on this repository.

---

## License

Open for use, modification, and redistribution. Attribution appreciated but not required.
