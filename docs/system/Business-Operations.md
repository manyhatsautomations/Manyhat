---
date: 2026-05-21
type: business-operations
tags: [manyhat, operations, pipeline]
---

# ManyHat Automations — Business Operations

*AI automation agency | British Columbia, Canada*

---

```
Google Maps → Data Miner → CSV → leads-inbox/ → Lead Enrichment Agent
                                                                  │
                                    ┌─────────────────────────────┴─────────────────────────────┐
                                    │                                                           │
                              Cold Calling (brief)                                      Email via Reacher
                                    │                      "Want a free AI demo built on your website?"
                                    │                                                           │
                                    └─────────────────────────────┬─────────────────────────────┘
                                                                  │
                                                      ┌───────────┴───────────┐
                                          Send Generic Demo Link    OR    Generate Custom Demo (API)
                                                      │                         │
                                                      └───────────┬─────────────┘
                                                                  │
                                                    Prospect Engages (3+ min chat / call)
                                                                  │
                                                    Engagement Webhook → GHL → AI Delta Response (text/chat)
                                                                  │
                                                            Books Consultation Call
                                                                  │
                                                      Voice AI (Maya) handles inbound/outbound
                                                                  │
                                                              Close Sale
                                                                  │
                                                      14-Day Free Pilot Agreement
                                                                  │
                                                    Onboarding Questionnaire (OperatorBase)
                                                                  │
                                            Webhook → Hermes/Claude → GHL → PromptForge generates voice prompt
                                                                  │
                                                    Setup: GHL + Retell Agent + Custom Prompt
                                                                  │
                                                               Go Live
                                                                  │
                                                       Client pays: $1,000 + $500/mo
```

---

## 1. Prospect Journey (Numbered)

1. **Discovery**: Google Maps search → Data Miner Chrome extension scrapes → CSV
2. **Ingestion**: Drop CSV into `C:/Users/paulr/leads-inbox/`
3. **Enrichment**: Lead enrichment agent processes → enriches → outputs to [[Lead-Pipeline]] and `Lead-Generation/enriched/`
4. **Scoring**: Leads scored 1–10; Telegram notification fires with top leads; cold call brief generated
5. **Parallel Outreach**:
   - **Cold Calling**: Uses generated brief
   - **Email Outreach**: Reacher campaign → pitch: *"Want to see a free AI demo built on your website?"*
6. **Demo Delivery**:
   - Generic demo: `https://manyhatautomations.aidemo.app`
   - Custom demo: API POST if high-value or requested
7. **Engagement**: Prospect engages for 3+ min chat or completes voice call
8. **Webhook Fires**: Engagement data → GHL → AI Delta Response triggers text/chat follow-up
9. **Booking**: Prospect books consultation call
10. **Call Handling**: Voice AI Maya (Retell) handles inbound/outbound consultation call
11. **Close**: 14-day free pilot agreement signed
12. **Onboarding**: Client fills questionnaire → Hermes/Claude processes → GHL updates
13. **Prompt Generation**: PromptForge generates custom voice agent system prompt
14. **Setup**: Configure GHL for client + Retell agent + deploy custom prompt
15. **Go Live**: Client starts paying — $1,000 setup + $500/month

---

## 2. Pricing & Pilot (LOCKED)

| Item | Value |
|------|-------|
| **One-Time Setup** | $1,000 |
| **Monthly Retainer** | $500 |
| **Pilot Period** | 14 days |
| **Pilot Terms** | No payment until it books appointments |

> **Rule**: Never discount or alter without written approval.

---

## 3. Tech Stack Overview

### 3.1 Lead Generation

| Tool | Role | Details |
|------|------|---------|
| **Data Miner** | Google Maps scraping | Chrome extension → CSV (Business Name, Address, Rating, Reviews, Category, Phone, Email/Website) |
| **Lead Enrichment Agent** | Process + score leads | Watches `C:/Users/paulr/leads-inbox/` → enriches (finds email, audits website for no chat widget = opportunity) → scores 1–10 → generates cold call brief → Telegram notification with top leads |
| **Future** | Apollo / LinkedIn | Email finding expansion |

**Output**: `04 Business/Manyhat-Automations/Lead-Generation/enriched/` + Reacher CSV

---

### 3.2 Email Outreach — OperatorBase / Reacher

| Setting | Value |
|---------|-------|
| **Platform** | OperatorBase (membership) |
| **Sender** | Reacher (built-in) |
| **Infrastructure** | 9 emails across 3 subdomains |
| **Volume** | 20/day per email = **180/day** |
| **Monthly Quota** | **~3,000 emails/month** |

**Workflow**:
- Upload leads via CSV
- Create **Jobs** (niche buckets)
- Assign to **Campaigns**
- Campaign AI: Claude Sonnet 4.6, auto mode, timezone Eastern

**Stale Follow-Up**:
- Trigger: 7 days of silence
- Frequency: Every 3 days
- Max: 3 attempts
- Prompt: [[SOPs/stale followup prompt]]

**AI Demo Generation**:
- Enabled in Reacher
- Auto-generates personalized demos for interested leads

> **QUOTA IS PRECIOUS** — Only send to **scored leads with confirmed emails**. No spray-and-pray.

---

### 3.3 AI Demo Generator (OperatorBase / aidemo.app)

| Aspect | Details |
|--------|---------|
| **Generic Demo** | `https://manyhatautomations.aidemo.app` |
| **Custom Demo API** | `POST https://aidemo.app/api/v1/demos` |
| **Credentials** | [see Claude memory: reference_operatorbase] |
| **Process** | Scrapes business website → builds personalized AI chat + voice demo |
| **Types** | Chat, Voice, or Both |
| **Engagement Webhook** | Fires when prospect genuinely engages (3+ min chat / completed call) |
| **Webhook Target** | GHL for follow-up automation |

**Strategy**:

| Scenario | Action |
|----------|--------|
| Low-touch / high volume | Send generic demo link |
| High-value lead or explicit request | Generate custom demo via API |
| Engagement detected | Webhook → GHL → AI Delta Response |

---

### 3.4 Voice AI — Retell

| Setting | Value |
|---------|-------|
| **Agent Name** | Maya |
| **Demo Agent ID** | [see Claude memory: reference_operatorbase] |
| **Current Use** | Demo calls for prospects (via OperatorBase) |
| **Business Use** | Inbound calls, qualification, calendar booking, post-call analysis |
| **Integration** | Retell built-in webhook system |

**Voice Workflow (Our Business)**:
1. Inbound call received
2. Maya qualifies prospect
3. Calendar booking attempted
4. Post-call analysis generated

System prompt: [[SOPs/retell voice system prompt universal]]

---

### 3.5 GHL (GoHighLevel) — Our Business

| System | Purpose |
|--------|---------|
| **AI Delta Response** | All messaging automation for ManyHat operations |
| **Voice AI Workflow** | Inbound call handling with calendar booking |
| **Social** | Facebook + LinkedIn wired natively to GHL Conversations |

**Integration Points**:
- Engagement webhook (from demo) → GHL
- Onboarding data → GHL
- AI Delta Response handles all text/chat follow-up

---

### 3.6 Onboarding (OperatorBase)

| Aspect | Details |
|--------|---------|
| **URL** | `https://onboarding.manyhatautomations.com` (pending DNS) |
| **DNS** | CNAME `onboarding` → `cname.vercel-dns.com` (Cloudflare DNS-only, NOT proxied) |
| **Webhook** | Onboarding submission → Hermes/Claude first → then GHL |
| **Alternative** | Can send onboarding via email/text directly |

**Onboarding Flow**:

```
Client Fills Questionnaire (OperatorBase form / email / text)
                 │
                 ▼
Webhook Fires → Hermes/Claude processes
                 │
                 ▼
GHL Updated with client data
                 │
                 ▼
PromptForge generates custom voice agent system prompt (XML-structured, 9 sections)
                 │
                 ▼
Setup: GHL for client + Retell agent + deploy custom prompt
                 │
                 ▼
Go Live → Client pays $1,000 + $500/mo
```

---

## 4. Email Quota Management

**Monthly Budget: ~3,000 emails**

| Rule | Enforcement |
|------|-------------|
| Score first, send second | Only email leads with score ≥ 6 |
| Verify email existence | No bounces — protect sender reputation |
| Job-based targeting | Niche buckets only; no generic blasts |
| Track daily send rate | Max 180/day |
| Stale follow-up counts toward quota | Include in planning |

**Weekly Check**: Review send volume vs. quota remaining in OperatorBase dashboard.

---

## 5. SOP References

All SOPs stored at: `04 Business/Manyhat-Automations/SOPs/`

| SOP | Wikilink |
|-----|----------|
| Generic demo prompt | [[SOPs/generic demo prompt]] |
| Email system prompt | [[SOPs/email system prompt]] |
| Stale follow-up prompt | [[SOPs/stale followup prompt]] |
| Retell voice system prompt (universal) | [[SOPs/retell voice system prompt universal]] |
| PromptForge instructions | [[SOPs/prompt forge]] |
| Sales call script | [[SOPs/sales call script]] |
| Objection handling | [[SOPs/objection handling]] |

---

## 6. Key Credentials & References

| System | Reference |
|--------|-----------|
| OperatorBase credentials | [see Claude memory: reference_operatorbase] |
| Retell (Maya demo agent ID) | [see Claude memory: reference_operatorbase] |
| aidemo.app API | [see Claude memory: reference_operatorbase] |

---

## 7. Quick Reference

| Task | Location / Action |
|------|-------------------|
| Check lead pipeline | [[Lead-Pipeline]] |
| View enriched leads | `04 Business/Manyhat-Automations/Lead-Generation/enriched/` |
| Review email performance | OperatorBase dashboard |
| Trigger demo manually | API: `POST https://aidemo.app/api/v1/demos` |
| Update voice agent prompt | PromptForge → XML output → Retell |
| Handle inbound lead | GHL Conversations or Voice AI (Maya) |

---

*Last updated: 2026-05-21*
*For Hermes: This is the canonical operations reference. Use wikilinks to navigate related vault pages.*
