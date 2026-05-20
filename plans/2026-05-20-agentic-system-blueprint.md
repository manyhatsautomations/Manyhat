# Manyhat Automations — Agentic System Blueprint

> **Goal:** Transform Manyhat's vault + Hermes into a fully agentic system
> **Architecture:** 5-layer: Identity → Memory → Skills → Planning → Output (all grounded in Obsidian vault + GitHub)
> **Tech Stack:** Hermes Agent, Obsidian vault, GitHub, cron jobs, dreamer agent

---

## Research Synthesis

**Best practices from 7 leading systems** (Claude Code, Hermes, Cursor, CrewAI, AutoGen, OpenClaw):

| Layer | Best Pattern | Source | Why |
|-------|-------------|--------|-----|
| Identity | user.md + business.md + personality.md | OpenClaw + Hermes | Separates user from business context |
| Memory | memory.md + Daily/ + Dreaming/ | Hermes + user's blueprint | Only system with overnight consolidation |
| Skills | 3-level (YAML frontmatter → SKILL.md → linked files) | Hermes | Triggers auto-load, linked files on demand |
| Output | timestamped brief/ folders with summary.md | Hermes | Only system with real "brief" artifact structure |
| Planning | Formal planning skill with clarifying Qs upfront | Hermes + user's blueprint | Forces granularity before execution |

---

# LAYER 1: Identity System

## Files to create

### `identity/user.md` — Who Paul is, how he works
- Role, preferences, communication style, pet peeves
- Operating environment, tools, languages
- How he wants Hermes to interact

### `identity/business.md` — Manyhat Automations context
- Company name, website, services, pricing
- ICP (Ideal Customer Profile)
- Brand voice and positioning
- 9 active clients with industries

### `identity/personality.md` — How Hermes should embody
- Tone: professional, agency-grade, no-BS
- Communication: direct, action-oriented, numbers-focused
- Persona: senior AI automation consultant

### `identity/15-questions.md` — Identity interview (ask Paul)
- 15 questions about work habits, preferences, pet peeves, goals
- Auto-loads and presents first unanswered question each session
- Answers feed back into user.md and personality.md

---

# LAYER 2: Memory System

## Architecture
```
03 Memories/
  memory.md           ← long-term (durable facts, preferences, decisions — loaded at session start)
  Daily/
    today.md          ← auto-loaded each session
    yesterday.md      ← auto-loaded for context
    2026-05-19.md     ← archive (stays on disk)
  Dreaming/
    consolidation-log.md ← nightly output
```

## Behavior
- `memory.md`: Durable facts only. Never task progress. Pruned monthly by dreamer.
- `today.md`: Created at session start. Logs key decisions, files touched, outcomes.
- `yesterday.md`: Auto-loaded into context for continuity.
- `dreaming/`: Cron job runs nightly — reads day's log, scores themes, promotes to memory.md, forgets stale.

---

# LAYER 3: Skills System

## Already exists (Hermes native)
- 3-level system: YAML frontmatter → SKILL.md body → linked files
- Stored in `~/.hermes/skills/` and project `.hermes/skills/`

## Additions needed
1. Business context injection: Every skill references `identity/business.md`
2. Skill chaining docs: How to chain cold-calling → voice-ai → ghl-deploy
3. Agency-specific skills:
   - `cold-call-script` → loads scripts, objections, voice AI
   - `client-onboarding` → questionnaires, service agreements, GHL setup
   - `lead-generation` → YellowPages scraper, CSV processing
   - `ghl-deployment` → GoHighLevel setup, automations, workflows

---

# LAYER 4: Planning System

## Behavior
1. For 3+ step tasks: create plan in `plans/YYYY-MM-DD-task-name.md`
2. Ask clarifying questions BEFORE touching code
3. Break into granular phases (2-5 min each)
4. Plan format: Goal → Clarifying Qs → Phases → Success Criteria → Risk

## Already exists
- `writing-plans` skill (loaded)
- Plan directory at `plans/`

---

# LAYER 5: Brief/Output System

## Architecture
```
brief/
  README.md           ← index of all briefs with links
  2026-05-20-agentic-system.md ← today's output
  2026-05-19-github-repo-setup.md
  ...
```

## Format per brief
```markdown
# Brief: [Title]
**Date:** YYYY-MM-DD
**Status:** [ Complete / In Progress / Blocked ]
**Session ID:** [hermes session ref]

## Summary
[2-3 sentences on what was accomplished]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Files Created/Modified
- [path]
- [path]

## Artifacts
[Link to generated files, scripts, configs]

## Next Steps
[What follows]
```

---

# IMPLEMENTATION PHASE

## Phase 1: Identity System (now)
1. Create `identity/user.md`
2. Create `identity/business.md`  
3. Create `identity/personality.md`
4. Create `identity/15-questions.md`
5. Link all to dashboard

## Phase 2: Memory System (next)
1. Create `03 Memories/memory.md`
2. Create `03 Memories/Daily/today.md` + `yesterday.md`
3. Create dreamer cron job
4. Wire into vault dashboard

## Phase 3: Brief System
1. Create `brief/` folder structure
2. Create `brief/README.md` index
3. Create today's brief
4. Add to dashboard

## Phase 4: Skills Enhancement
1. Add business context references to existing skills
2. Create agency-specific skills
3. Document skill chaining patterns

## Phase 5: Sync & Configure
1. Push all to GitHub
2. Sync to Obsidian vault
3. Configure Hermes cron for dreamer
4. Test end-to-end

---
#agentic-system #blueprint
