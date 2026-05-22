---
date: 2026-05-21
type: system-documentation
maintained-by: claude-code
---

# Claude Code — Integration Guide for Hermes

This document describes how Claude Code is configured, what it can do, and how Hermes should collaborate with it. Written so that Hermes has a complete picture of Claude's capabilities, constraints, and preferred communication patterns.

---

## Who Claude Code Is

Claude Code is Paul's primary AI development assistant. It lives at `~/.claude/` (`C:\Users\paulr\.claude\`) and is responsible for:
- All coding, debugging, and file-system work
- Delegating heavy analytical tasks to cheaper specialist models
- Maintaining project memory and session context
- Managing n8n workflows, Airtable bases, and the full automation stack

Claude Code does NOT:
- Run as a background daemon or schedule itself
- Send Telegram messages to Paul directly (that is Hermes's job)
- Store secrets or API keys in vault files

---

## MCP Servers (Claude's Active Connections)

Claude Code has the following MCP servers registered in `~/.mcp.json`. These are the external tools Claude can invoke directly.

### Workflow Automation
| Server | Prefix | Tools | Target |
|--------|--------|-------|--------|
| n8n-mcp (czlonkowski standalone) | `mcp__n8n-mcp__*` | 24 tools — full workflow CRUD | ProspectAI n8n (`https://n8n.prospectai.app`) |
| n8n-mcp-native (n8n built-in) | `mcp__n8n-mcp-native__*` | 3 tools — search/execute/get | Only workflows with `availableInMCP: true` |

Critical: `n8n-mcp` env var must be `N8N_API_URL` (not `N8N_URL`). Wrong name → only 7 doc tools load, no workflow management.

### Browser Automation
| Server | Prefix | Purpose |
|--------|--------|---------|
| puppeteer | `mcp__puppeteer__*` | Headless browser automation |
| playwright | `mcp__playwright__*` | Browser testing and scraping |

### Knowledge & Documentation
| Server | Prefix | Purpose |
|--------|--------|---------|
| context7 | `mcp__context7__*` | Live library documentation (any framework/SDK) |

### Agent Orchestration
| Server | Prefix | Purpose |
|--------|--------|---------|
| claude-flow / Ruflo v3.5 | `mcp__ruflo__*` | 259 tools — swarm orchestration, agent management, memory, coordination |

### Data & Productivity
| Server | Prefix | Purpose |
|--------|--------|---------|
| Airtable | `mcp__claude_ai_Airtable__*` | Read/write Airtable bases (scraper, DailyNews, ContentLog) |
| Gmail | `mcp__claude_ai_Gmail__*` | Google Workspace email |
| Google Calendar | `mcp__claude_ai_Google_Calendar__*` | Google Calendar events |

### Messaging
| Server | Prefix | Purpose |
|--------|--------|---------|
| Hermes | `mcp__hermes__*` | Messaging bridge — Telegram, Discord, Slack, WhatsApp, Signal, Matrix |

---

## Model Aliases (Claude's Delegation System)

Claude's rule: **respond, judge, merge results only**. All heavy work delegates to cheaper specialist models via bash aliases in `~/.model-functions.sh`.

### Primary Aliases
| Alias | Model | Best For |
|-------|-------|----------|
| `kimi "..."` | Kimi K2.6 — 262k context | Coding, debugging, file analysis (primary) |
| `kimi_think "..."` | Kimi K2.6 thinking mode | Deep multi-file reasoning |
| `deepseek "..."` | DeepSeek V4 Pro (NVIDIA) | General analysis, search, coding |
| `qwen "..."` | Qwen3.5 397B (NVIDIA) | Architecture, heavy reasoning |
| `glm "..."` | GLM-5.1 (NVIDIA) | Agentic tasks, orchestration |

### n8n-Specific Aliases (auto-inject full skills context)
| Alias | Purpose |
|-------|---------|
| `n8n_kimi "..."` | n8n code, debug, workflow building |
| `n8n_deepseek "..."` | n8n quick analysis and search |
| `n8n_qwen "..."` | n8n architecture and reasoning |
| `n8n_glm "..."` | n8n agentic chains and orchestration |
| `n8n_claude "..."` | n8n large-context work via Claude Code subscription |

### Subscription-Backed
| Alias | Purpose |
|-------|---------|
| `claude_agent "..."` | Claude Code subscription agent |
| `claude_sonnet "..."` | Claude Code subscription agent (same) |

All aliases auto-inject `~/.claude/system-context.md` as the system prompt. The `n8n_*` aliases additionally inject `~/.claude/n8n-skills-compiled.md` (7 expert skills, 4647 lines).

---

## Delegation Rules

Claude enforces these rules every session:

1. **Never reads+processes files itself** when a bash alias suffices — delegates to `kimi` or `deepseek`
2. **Never writes code or generates content directly** — delegates and merges
3. **Spawns Task agents** (`run_in_background: true`) for multi-tool tasks to keep main context clean
4. **Uses Edit tool only** for single trivial file changes
5. **Batches all independent operations** into one message (parallel first)
6. **Enters plan mode** for any 3+ step task; waits for approval before implementation
7. **Writes task plan** to `tasks/todo.md` before implementation

---

## How Hermes Should Communicate With Claude

### Direct Messaging
- Hermes sends messages via `mcp__hermes__messages_send`
- Claude monitors via `mcp__hermes__messages_read` and `mcp__hermes__events_wait`
- Channel list available via `mcp__hermes__channels_list`

### Vault-Based Handoff (Preferred for Daily Data)
Claude reads vault files directly via the filesystem (Read tool). Hermes should write structured data to these locations:

| Data Type | File Path |
|-----------|-----------|
| Today's accountability summary | `03 Memories/Daily/today.md` |
| Previous day's summary | `03 Memories/Daily/yesterday.md` |
| Cold call practice progress | `04 Business/Manyhat-Automations/cold-call-practice/progress-tracker.md` |
| Business memory | `03 Memories/memory.md` |
| Cron agent outputs | `03 Memories/Daily/today.md` (append each time a cron fires) |

All paths are relative to vault root: `C:\Users\paulr\Documents\Agentic OS Vault\`

### What Claude Will Never Do
- Modify `~/.claude/settings.json` on Hermes's behalf
- Send Telegram messages (that is Hermes's domain)
- Store raw API keys or tokens in vault markdown files
- Push to GitHub without an explicit user request

---

## Skills & Commands Claude Has

### Cold Calling & Sales (Manyhat Core)
| Skill | What It Does |
|-------|-------------|
| `/cold-calling-practice` | Guided cold call practice sessions with scoring and feedback |
| `email-expert` agent | Email copy for outreach sequences |
| `headline-expert` agent | Headlines and hooks for offers |
| `audience-expert` agent | ICP and audience research |
| `problem-level-expert` agent | Pain point identification and messaging |
| `unique-process-expert` agent | Positioning and differentiation |
| `offer-expert` agent | Offer construction and pricing |
| `positioning-expert` agent | Market positioning strategy |
| `sales-landing-page-agent` | Landing page copy and structure |
| `google-media-buyer-expert` | Google Ads strategy |

### n8n Workflow Skills
| Skill/Command | What It Does |
|---------------|-------------|
| `/n8n-mcp-tools-expert` | MCP tool selection and workflow management |
| `/n8n-expression-syntax` | `{{}}` patterns, webhook data, common mistakes |
| `/n8n-workflow-patterns` | AI agents, webhooks, HTTP, DB, scheduled tasks |
| `/n8n-validation-expert` | Validation errors, autofix patterns |
| `/n8n-node-configuration` | Node operations, dependencies, required fields |
| `/n8n-code-javascript` | Code node JS patterns |
| `/n8n-code-python` | Code node Python patterns |

### Project Management (GSD — 32 commands)
| Command Group | Examples |
|---------------|---------|
| Planning | `/gsd:new-project`, `/gsd:plan-phase`, `/gsd:new-milestone` |
| Execution | `/gsd:execute-phase`, `/gsd:do`, `/gsd:fast` |
| Review | `/gsd:validate-phase`, `/gsd:review`, `/gsd:verify-work` |
| Progress | `/gsd:progress`, `/gsd:stats`, `/gsd:health` |
| Debug | `/gsd:debug`, `/gsd:audit-milestone` |

### Memory & Research
| Skill | What It Does |
|-------|-------------|
| `/consolidate-memory` | Distill session knowledge to `~/.claude/memory/` persistent files |
| `/research-scout` | Hunt for new info that updates or challenges existing knowledge |
| `/media-memory` | Ingest and search all media assets across sessions |
| `/graphify` | Convert any input into a knowledge graph |

### Infrastructure Skills
| Skill | What It Does |
|-------|-------------|
| `/sparc:*` | SPARC methodology — architect, coder, debugger, tester, reviewer |
| `/gsd:*` | Full project lifecycle management |
| `/github:*` | PR management, code review, issue tracking |

---

## Active Projects Claude Tracks

| Project | Location | Status |
|---------|----------|--------|
| AI Mate Face Swap Pipeline v2 | Workflow `Kqx28E2S31VirHQn` at n8n.prospectai.app | Deployed, needs testing |
| ManyHat Content Engine v2.0 | Workflow `0J8UnIfBdeRZcBUE` at Railway | Deployed inactive, needs testing |
| Cold Call Training System | `04 Business/Manyhat-Automations/cold-call-practice/` | Active |

---

## Key File Locations

| File | Purpose |
|------|---------|
| `~/.claude/memory/recent-memory.md` | Rolling 48hr session context — auto-loaded |
| `~/.claude/memory/project-memory.md` | Active project state — auto-loaded |
| `~/.claude/memory/long-term-memory.md` | Distilled facts and patterns — reference on demand |
| `~/.claude/settings.json` | Permissions, hooks, MCPs — DO NOT MODIFY |
| `~/.mcp.json` | User-scope MCP server registrations |
| `~/.model-functions.sh` | All bash model aliases |
| `~/.claude/n8n-skills-compiled.md` | Compiled n8n skills (4647 lines) |
| `~/.claude/system-context.md` | Auto-injected system prompt for all model aliases |

---

## OperatorBase & Lead Pipeline Integration

| System | Role | Claude Touchpoint |
|--------|------|------------------|
| aidemo.app | AI demo generation | API call (`POST /api/v1/demos`) |
| Retell (Maya) | Voice agent | PromptForge → deploy system prompt |
| GHL | Messaging automation | Read context from Hermes vault files |
| Onboarding webhook | Form ingestion | Parse → PromptForge → generate prompt |

---

### 1. AI Demo Generation (`aidemo.app`)

When to use:
- Before a cold call callback
- High-scored leads (9–10)
- Prospect explicitly asks for a demo

How it works:
- `POST https://aidemo.app/api/v1/demos`
- Scrapes the business URL → builds personalized AI chat + voice demo
- Types returned: chat, voice, or both
- Credentials: [see Claude memory: reference_operatorbase]

| Step | Actor | Action |
|------|-------|--------|
| 1 | Hermes | Receives `/demo [business URL]` in Telegram |
| 2 | Claude | Calls `aidemo.app` API with URL |
| 3 | Claude | Receives demo link |
| 4 | Hermes | Forwards link to Paul |

Fallback if API fails: `https://manyhatautomations.aidemo.app`

> **Status:** Planned — requires Hermes webhook handler setup.

---

### 2. Retell Voice Agent (Maya)

| Property | Value |
|----------|-------|
| Agent name | Maya |
| Agent ID | [see Claude memory: reference_operatorbase] |
| System prompt vault location | [[SOPs/retell voice system prompt universal]] |

**Current use:** Demo calls for prospects via OperatorBase.

**Business use:**
- Inbound call handling
- Lead qualification
- Calendar booking
- Post-call analysis

**Claude role on onboarding completion:**
1. Run PromptForge to generate new system prompt (XML-structured, 9 required sections)
2. Deploy prompt to Retell via API

---

### 3. GHL AI Delta Response

GHL handles all messaging automation for ManyHat's own operations.

| Trigger | Flow |
|---------|------|
| Prospect engages demo 3+ min or completes a call | Engagement webhook fires → GHL |

- GHL AI Delta Response picks up text/chat follow-up **automatically**
- Claude **does not** interact with GHL directly
- Claude reads context from Hermes vault files

**Conversation summaries:** Hermes writes to `03 Memories/Daily/today.md` daily.

---

### 4. Onboarding Webhook

**URL (pending DNS):** `https://onboarding.manyhatautomations.com`

Once DNS resolves:
1. Form submission POSTs to webhook
2. Webhook routes to **Claude/Hermes first**
3. Then forwards to GHL

**Claude's job on webhook receipt:**
- Parse onboarding answers
- Pass to PromptForge (see [[SOPs/prompt forge]])
- Generate XML voice agent prompt
- Confirm completion to Hermes

**Notification:** Hermes alerts Paul via Telegram when onboarding is received and the prompt is ready.

---

### 5. Telegram Command Plan (`/demo`)

| Field | Value |
|-------|-------|
| Command | `/demo [business URL]` |
| Handler | Hermes receives → passes to Claude via Hermes MCP bridge |
| Claude action | Calls `aidemo.app` API → waits for link → returns to Hermes |
| Hermes action | Texts/messages link to Paul |
| Credentials | [see Claude memory: reference_operatorbase] |
| Fallback (API fails) | Generic demo URL: `https://manyhatautomations.aidemo.app` |

> **Status:** Planned — requires Hermes webhook handler setup.
