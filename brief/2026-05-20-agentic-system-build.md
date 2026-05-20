---
date: 2026-05-20
status: In Progress
session_id: TBD
---

# Brief: Agentic System Build

## Summary
Researched 7 leading agentic systems (Claude Code, Hermes, Cursor, CrewAI, AutoGen, OpenClaw), synthesized best practices, and built a 5-layer agentic system for Manyhat Automations: Identity → Memory → Skills → Planning → Output. All grounded in the Obsidian vault with GitHub sync.

## Key Decisions
- **5-layer architecture** based on user's agentic.txt blueprint + research
- **Identity**: Separate user.md, business.md, personality.md (OpenClaw/Hermes pattern)
- **Memory**: memory.md (durable) + Daily/ (short-term) + Dreamer cron (consolidation)
- **Skills**: Existing Hermes 3-level system + business context injection
- **Planning**: Formal planning skill with mandatory clarifying questions
- **Output**: brief/ folder with timestamped, searchable briefs

## Files Created/Modified
- `identity/user.md` — Paul's profile, preferences, pet peeves
- `identity/business.md` — Manyhat context, ICP, pricing, 9 clients
- `identity/personality.md` — Hermes agency persona
- `identity/15-questions.md` — Identity interview (0/15 answered)
- `03 Memories/memory.md` — Durable memory store
- `03 Memories/Daily/today.md` — Today's log
- `03 Memories/Daily/yesterday.md` + `2026-05-19.md`
- `brief/README.md` — Output index
- `brief/2026-05-19-github-vault-setup.md`
- `brief/2026-05-20-agentic-system-build.md`
- `plans/2026-05-20-agentic-system-blueprint.md`

## Next Steps
- Create dreamer cron job for nightly memory consolidation
- Add business context references to skills
- Create agency-specific skills (cold-call, onboarding, lead-gen, ghl-deploy)
- Push all to GitHub
- Answer 15 identity questions

#brief
