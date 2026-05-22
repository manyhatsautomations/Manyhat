---
name: Manyhat Agent Roster
updated: 2026-05-21
total_agents: 17
---

# Manyhat Automations — Complete Agent Roster

All Hermes cron agents running the business.

## Full Daily Schedule

| Time | Agent | Category | Silent? |
|------|-------|----------|---------|
| Every 1m | **Telegram Command Handler** | Real-Time | Script-only |
| Every 5m | **PWM API Watchdog** | Infra | Local |
| 2:00am | **Dream Memory Consolidation** | Memory | Local |
| 3:00am | **Dreamer — Nightly Consolidation** | Memory | Telegram |
| 6:00am | **Social Media Research & Script Gen** | Marketing | Telegram |
| 7:00am | **Morning Briefing** | Accountability | Telegram |
| 8am-6pm | **Lead Enrichment Watcher** (every 30m) | Pipeline | Silent if none |
| 10:00am | **GHL Pipeline Watcher** | Pipeline | Silent if none |
| 10:00am | **Postiz Batch Scheduler** | Marketing | Silent if none |
| 12:00pm | **GHL Pipeline Watcher** | Pipeline | Silent if none |
| 12:30pm | **Cold Call Challenge Q** | Practice | Telegram |
| 1:00pm | **Procrastination Nudge** | Accountability | Silent if active |
| 2:00pm | **Mid-Day Pulse + GHL Pipeline** | Accountability | Telegram |
| 3:00pm | **Procrastination Nudge** | Accountability | Silent if active |
| 4:00pm | **GHL Pipeline Watcher** | Pipeline | Silent if none |
| 4:00pm | **Postiz Batch Scheduler** | Marketing | Silent if none |
| 6:00pm | **Demo Follow-Up Tracker** | Pipeline | Silent if clean |
| 8:00pm | **Evening Wrap** | Accountability | Telegram |
| 8:00pm | **Loom + Remotion Reminder** | Marketing | Telegram |
| 9:00pm | **Night-Before Commitment** | Accountability | Telegram |
| Sunday 6pm | **Weekly Progress Report** | Reporting | Telegram |

## New: Social Media Growth Engine

### Agents
- **Social Media Research & Script Generator** (6am) — scrapes trending AI/agency topics, generates 2-3 video scripts daily
- **Postiz Batch Scheduler** (10am + 4pm) — publishes ready content via Postiz Docker at localhost:5000
- **Loom + Remotion Reminder** (8pm) — prompts recording after gym

### Tools
- **Postiz:** Docker at localhost:5000, CLI installed (`postiz`), 28+ platform support
- **Remotion:** `npx skills add remotion-dev/skills` for Claude Code, programmatic video via React
- **Loom:** Screen recording for walkthroughs/demos

### Vault
- `04 Business/Manyhat-Automations/social-media/` — scripts, videos, research, calendar

### Postiz Setup Checklist
- [ ] Get API key from http://localhost:5000/settings/developers
- [ ] Configure CLI: `postiz config:set --api-url http://localhost:5000/api`
- [ ] Connect social accounts (X, LinkedIn, TikTok, Instagram)
- [ ] Install Remotion on Claude Code: `npx skills add remotion-dev/skills`

## Skills (6 Manyhat)
- manyhat-cold-call — scripts, openers, rebuttals
- manyhat-call-practice — practice analysis + scoring
- manyhat-client-onboarding — 3-phase: Discovery → Setup → Agent
- manyhat-ghl-deployment — GHL pipeline + automation
- manyhat-lead-generation — scraping + enrichment pipeline
- manyhat-social-media — Remotion + Postiz content engine

## Delivery
All agents deliver to Telegram chat 6396832173 via @hermesmanyhats_bot.
Silent agents only send when they have actionable intel.
