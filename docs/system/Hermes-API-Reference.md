---
title: Hermes API Reference — All Connected Services
tags: [hermes, apis, integrations, credentials]
updated: 2026-05-21
---

# Hermes API Reference

All APIs and services available to Hermes. Keys live in Hermes `.env` — reference this file for capabilities and endpoints.

---

## aidemo.app — AI Demo Generator

**What it does:** Creates personalized AI chat + voice demos for prospects by scraping their website.

**Endpoint:** `POST https://aidemo.app/api/v1/demos`

**Auth:** `Authorization: Bearer {AIDEMO_API_KEY}` (key in Hermes .env)

**Tenant ID:** `1b02ccef-12a0-4f91-bbc3-b88a391c976d`

**Payload:**
```json
{
  "company_name": "Acme Roofing",
  "company_type": "Roofing contractor",
  "website_url": "https://example.com",
  "demo_type": "both",
  "email": "owner@example.com",
  "first_name": "John",
  "source": "cold-call"
}
```

**demo_type options:** `"chat"`, `"voice"`, `"both"`

**Webhooks that fire back:**
- **Engagement** (prospect genuinely interacts): `https://services.leadconnectorhq.com/hooks/V7xvEWzegiFLI2NFz0h0/webhook-trigger/2007c84d-054b-433c-aca8-844e6640b9e7`
- Payload includes: demo_url, email, phone, engagement type, chat messages, call duration

**Hermes use cases:**
- When Paul says "generate a demo for [business]" → call this API
- When Paul cold calls and wants a ready demo → trigger before the call
- Telegram command: `/demo [business name]` (to be implemented)

**Generic demo (no API needed):** `https://manyhatautomations.aidemo.app`

---

## Retell AI — Voice Agent

**What it does:** Powers AI voice agents for inbound/outbound calls — qualification, booking, post-call analysis.

**API Base:** `https://api.retell.ai`

**Auth:** `Authorization: Bearer {RETELL_API_KEY}` (key in Hermes .env)

**Key IDs:**
- Demo agent: `agent_a15c1428332dd2d6e4f394d144`
- Demo call webhook: `https://operatorbase.supabase.co/functions/v1/demo-retell-webhook`

**Key endpoints:**
- `GET /v2/list-agents` — list all agents
- `GET /v2/get-agent/{agent_id}` — get agent details
- `POST /v2/create-phone-call` — trigger outbound call
- `GET /v2/list-calls` — recent call history
- `GET /v2/get-call/{call_id}` — get call transcript + analysis

**Hermes use cases:**
- Check call history and summaries
- Trigger outbound demo calls for interested leads
- Pull call transcripts after prospect calls

---

## GHL — GoHighLevel CRM

**What it does:** Full CRM — contacts, conversations, pipelines, automation workflows, calendars.

**API Base:** `https://services.leadconnectorhq.com`

**Auth:** 
```
Authorization: Bearer {GHL_API_KEY}
Version: 2021-07-28
```
(key in Hermes .env)

**Location ID:** `V7xvEWzegiFLI2NFz0h0`

**Key endpoints:**
- `GET /contacts/?locationId={loc}` — search contacts
- `POST /contacts/` — create new contact
- `PUT /contacts/{id}` — update contact
- `GET /workflows/?locationId={loc}` — list workflows
- `GET /opportunities/pipelines?locationId={loc}` — pipeline stages
- `GET /calendars/?locationId={loc}` — calendars

**Pipelines:**
- **Delta Division** (`tS6Xetmdll9xPENOS36y`) — main client acquisition pipeline
  - Stages: New Lead → AI Demo → Booked Appt → Onboarding → AI Follow Up Calendar

**Calendars:**
- AI Follow Up Reminder: `T1YAeim9IQJ24zxKtxgD`
- Success Session: `mhqvkO0NT9ieeQyVS5Cj`

**Key workflows (all published):** See [[GHL-Map]] for full list.

**Hermes use cases:**
- Look up contact status and pipeline stage
- Add new leads as contacts
- Check upcoming booked appointments
- Trigger workflow actions (apply tags)

---

## n8n — Workflow Automation

**Two separate instances:**

### Instance 1: Railway (Content + Response Engine)
- URL: `https://primary-production-424023.up.railway.app`
- Public API base: `https://primary-production-424023.up.railway.app/api/v1`
- Hermes env vars: `N8N_API_URL`, `N8N_API_KEY`, `RAILWAY_N8N_API_URL`, `RAILWAY_N8N_API_KEY`
- Connection status: **verified 2026-05-22** via `/api/v1/workflows`
- Key workflows:
  - AI Delta Response (messaging): workflow `eeosgS5oNMCffbbi`
  - Voice AI inbound: workflow `hreP25F46Y3xPk8A`
  - ManyHat Content Engine v2.0: workflow `0J8UnIfBdeRZcBUE` — active
  - Webhook processor: `https://webhook-processor-production-f687.up.railway.app/webhook/fe696ec2-ea68-446e-ab1a-3e0d2ce3eaab22dsds`
- API key in Hermes .env (Railway n8n key)

### Instance 2: ProspectAI (AI Mate + face swap workflows)
- URL: `https://n8n.prospectai.app`
- Claude's MCP is connected here (`mcp__n8n-mcp__*`)
- API key in Hermes .env (ProspectAI key)

**Hermes use cases:**
- Trigger workflows for specific leads
- Check execution history
- Monitor automation health

---

## Telegram — Hermes's Own Channel

**Bot:** `@hermesmanyhats_bot`
**Bot ID:** `8911993061`
**Paul's Chat ID:** `6396832173`

**Bot API base:** `https://api.telegram.org/bot{TOKEN}`

**Auth:** `TELEGRAM_BOT_TOKEN` in Hermes .env

**Key endpoints:**
- `POST /sendMessage` — send text message
- `POST /sendDocument` — send a file
- `POST /getUpdates` — poll for messages

**Hermes use cases:**
- Morning briefing to Paul
- Lead enrichment completion notifications
- Demo engagement alerts
- Sales coaching prompts

---

## Anthropic — Claude API

**What it does:** Claude models for AI tasks.

**Auth:** `ANTHROPIC_TOKEN` in Hermes .env

**Models available:**
- `claude-opus-4-7` — most capable
- `claude-sonnet-4-6` — balanced (current Reacher email model)
- `claude-haiku-4-5-20251001` — fast/cheap

**Hermes use cases:**
- Generate cold call briefs for enriched leads
- Analyze call transcripts
- Draft personalized outreach
- Run PromptForge to generate client voice agent prompts

---

## ElevenLabs — Text-to-Speech

**What it does:** High-quality AI voice synthesis.

**Auth:** `ELEVENLABS_API_KEY` in Hermes .env

**Sarah voice ID:** (in Claude memory: reference_elevenlabs)

**Hermes use cases:**
- Voice responses from Hermes
- Generate audio versions of outreach messages
- Practice call audio generation

---

## NVIDIA API — Cheap AI Models

**What it does:** Access to DeepSeek, Qwen, Kimi, and other models via NVIDIA endpoints.

**Auth:** `NVIDIA_API_KEY` in Hermes .env

**Base URL:** `https://integrate.api.nvidia.com/v1`

**Models:**
- `deepseek-ai/deepseek-r1-distill-qwen-14b` — reasoning (cheap)
- `deepseek-ai/deepseek-v3` — general (cheap)
- `qwen/qwen3-235b-a22b` — heavy reasoning

**Hermes use cases:**
- Lead enrichment AI brief generation (cheap, fast)
- Email draft generation
- Content analysis without burning Anthropic quota

---

## OperatorBase / Reacher — Email Platform

**What it does:** AI-managed cold email campaigns. No API — web platform only.

**Web app:** operatorbase.app (login via Paul's account)

**Lead upload:** CSV format → "Jobs" tab → create job → assign to campaign

**CSV format expected by Reacher:**
```
first_name,last_name,email,company,website,phone
```

**Campaign settings:**
- Model: Claude Sonnet 4.6
- Mode: Auto (AI replies automatically)
- Stale follow-up: after 7 days, every 3 days, max 3x
- Email quota: ~3,000/month (9 emails × 20/day)

**Hermes use cases:**
- Notify Paul when Reacher-ready CSV is generated
- Report on which leads are ready for upload
- No direct API — all actions through Paul

---

## Onboarding System (Pending)

**URL (pending DNS):** `https://onboarding.manyhatautomations.com`
**DNS needed:** CNAME `onboarding` → `cname.vercel-dns.com` (Cloudflare DNS-only, no proxy)

**When ready — webhook payload fields:**
```
event: "onboarding.submitted"
submission.client_name, submission.client_email
submission.business_name, submission.website_url
submission.business_type, submission.answers
submission.scraped_content
```

**Flow when live:**
1. Client fills out onboarding form
2. Webhook fires to Hermes first
3. Hermes notifies Paul + forwards to GHL
4. Claude runs PromptForge to generate custom voice agent prompt

---

## Perplexity — Web Search

**Auth:** `PERPLEXITY_API_KEY` in Hermes .env

**Hermes use cases:**
- Research businesses before cold calls
- Find news about a prospect's industry
- Competitive research

---

## Quick Reference — What to Use When

| Task | Use |
|------|-----|
| Generate demo for a lead | aidemo.app API |
| Look up a contact in CRM | GHL API |
| Check recent call transcript | Retell API |
| Draft AI brief for cold call | NVIDIA (cheap) or Anthropic |
| Send Paul a notification | Telegram Bot |
| Generate client voice agent prompt | Anthropic (PromptForge) |
| Research a business | Perplexity |
| Trigger a GHL workflow | GHL API (apply tag) |
| Upload leads to email campaigns | Manual CSV → OperatorBase |

---

*All API keys are in Hermes `.env` — never stored in vault files.*
*[[GHL-Map]] | [[Business-Operations]] | [[Lead-Pipeline]] | [[Claude-Integration]]*
