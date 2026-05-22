---
title: GHL Automation Map
tags: [ghl, automation, workflows, crm]
updated: 2026-05-21
---

# GHL Automation Map — ManyHat Automations

Location ID: `V7xvEWzegiFLI2NFz0h0`
API key: [see Claude memory: reference_ghl]

---

## Pipelines

### Delta Division (Main Client Pipeline)
ID: `tS6Xetmdll9xPENOS36y`

| Stage | Description |
|-------|-------------|
| New Lead | Contact enters system from any source |
| AI Demo | Demo sent or being engaged with |
| Booked Appt | Call booked after demo interest |
| Onboarding | Client signed, completing onboarding form |
| AI Follow Up Calendar | Post-onboarding follow-up sequence |

### AI Sales Funnel (Legacy)
ID: `Fu2n3sSQyAFHLaQETyOE` — stages: New Lead → Pur FE → Pur OTO → Call Booked

---

## Calendars

| Name | ID | Type | Use |
|------|----|------|-----|
| AI Follow Up Reminder | `T1YAeim9IQJ24zxKtxgD` | Round Robin | Follow-up call scheduling |
| Success Session | `mhqvkO0NT9ieeQyVS5Cj` | Round Robin | Client onboarding/success call |
| Paul's Personal Calendar | `vBSx2qFO2hoqCSAb0JP2` | Personal | One-on-one meetings |

---

## Workflows

### Core AI Demo Flows (Published)

| Workflow | ID | Purpose |
|----------|----|---------|
| AI Demo Bot - Base Triggers (Lead Reply) | `dc49d520-4cfd-4502-a535-5a474ad98d9d` | Handles when lead replies to any channel |
| AI Demo Bot - Base Triggers (AI Reply) | `ef9bd457-707f-4363-aa6a-05ef3bd00149` | AI generates automated reply back to lead |
| AI Demo Optin Tag > Start Demo | `ae1e6f32-43bc-4a7c-aba4-9760e84b4d95` | Triggers demo start when optin tag applied |

### AI Bot (Our Business Conversation Engine)

| Workflow | ID | Purpose |
|----------|----|---------|
| AI Bot - Base Triggers (Lead Reply) | `466feb9c-afe5-45b5-b0c3-6b13b13b3ddf` | Lead message in → process |
| AI Bot - Base Triggers (AI Reply) | `30140c4c-4aa7-4fdf-ab72-4f753fd1eeb2` | AI generates reply → send |
| AI Bot - Opt-in | `a230cbdf-15d8-45aa-a005-cb90094d369e` | Lead opts in → starts AI conversation |

### Voice AI Flows

| Workflow | ID | Status | Purpose |
|----------|----|--------|---------|
| [Voice AI] Post-call Data Extraction | `a494fa83-fe7b-4316-891a-0acc37085f59` | Published | Extracts data after Retell call, syncs to CRM |
| [Voice AI] Send feedback SMS | `4ee83b0b-9dd6-44fa-b7d5-7c4dba965f17` | Published | Sends SMS after voice call |
| [Voice AI] Outbound Agent Trigger | `fe8c9674-5f19-4ab6-be78-08b061c744c8` | Draft | Trigger outbound AI call |

### Follow-up & Conversion

| Workflow | ID | Status | Purpose |
|----------|----|--------|---------|
| AI Follow Up Calendar | `2b297c35-999f-4fdb-babd-158ef970afab` | Published | Calendar-based follow-up sequence |
| AI Follow-up Trigger | `16aa169c-1fef-4d4a-899a-985c1e09af4e` | Published | Triggers follow-up sequences |
| Success Call (DFY) - Reminders | `4a21e391-d9ec-47f6-9663-93a4a7585277` | Published | Reminders for booked success calls |

### Utility Flows

| Workflow | ID | Status | Purpose |
|----------|----|--------|---------|
| DND | `7e888285-aec0-4f23-bb8a-f3e88dc9ed49` | Published | Do Not Disturb tag handling |
| DND GPT Tag | `9c76c057-b5ae-4273-a4b2-35c2610a0664` | Published | GPT-specific DND logic |
| Human Tag > Internal Notification | `31e6dff1-897d-4d6b-8ec1-f93b80acf510` | Published | Notifies when conversation needs human takeover |
| Send Magic Link v3 | `04854a23-9ac1-4f74-934c-68d515f47d22` | **Published (should be DRAFT)** | Old magic link sender — needs to be deactivated |

### Draft / Legacy

| Workflow | ID | Purpose |
|----------|----|---------|
| [WhatsApp] AI Demo Bot - Lead Reply | `db32684d-7986-41d5-9478-c7f08ca35c58` | WhatsApp demo bot (not active) |
| [WhatsApp] AI Demo Bot - AI Reply | `43882e2b-34c1-4076-8ac2-842d9ef3e179` | WhatsApp AI reply (not active) |
| Generate Magic Link | `05f61a52-7fe5-4873-9b2c-29a5e91e087d` | Old magic link flow |
| Database Reactivation Template | `2763b03e-c82f-4c06-9350-2357fe84daee` | Re-engagement campaign template |

---

## Custom Contact Fields (15)

| Field Name | Key | Use |
|------------|-----|-----|
| web_url | `contact.web_url` | Business website URL |
| Company Type | `contact.company_type` | Industry/type of business |
| demo context | `contact.demo_context` | Scraped website content used to build demo |
| Website Screenshot | `contact.website_screenshot` | Screenshot of their site |
| magic link | `contact.magic_link` | The demo link sent to prospect |
| AI Voice Call Summary | `contact.ai_voice_call_summary` | Post-call analysis from Retell |
| assistantchat last message | `contact.assistantchat_last_message` | Last message in AI chat |
| User Last Message | `contact.user_last_message` | Last message sent by lead |
| What would 10x your business? | `contact.what_would_10x_your_business` | Sales qualification |
| How fast do you need results? | `contact.how_fast_do_you_need_results` | Urgency qualifier |
| Monthly marketing spend? | `contact.monthly_marketing_spend` | Budget qualifier |
| Monthly revenue? | `contact.monthly_revenue` | Company size qualifier |
| Your #1 lead source today? | `contact.your_1_lead_source_today` | Current marketing insight |
| Your biggest bottleneck? | `contact.your_biggest_bottleneck` | Pain point |
| marketing team size | `contact.marketing_team_size` | Team size qualifier |

---

## Key Webhooks

| Trigger | URL | Fires When |
|---------|-----|------------|
| Demo Engagement | `https://services.leadconnectorhq.com/hooks/V7xvEWzegiFLI2NFz0h0/webhook-trigger/2007c84d-054b-433c-aca8-844e6640b9e7` | OperatorBase demo genuinely engaged |
| GHL AI Delta Response | Via Railway n8n workflow | All messaging in/out |

---

## How It All Connects

```
Lead engages with OperatorBase demo
           ↓
Engagement webhook fires to GHL
           ↓
"AI Demo Optin Tag > Start Demo" workflow triggers
           ↓
AI Demo Bot handles the conversation (Lead Reply + AI Reply workflows)
           ↓
Lead expresses interest → AI Follow-up Trigger fires
           ↓
AI Follow Up Calendar → Success Session booked
           ↓
[Voice AI] Post-call Data Extraction runs after call
           ↓
Lead moves to Onboarding stage in Delta Division pipeline
```

---

## Action Items

- [ ] Set "Send Magic Link v3" (`04854a23`) to DRAFT — it's published but should be inactive
- [ ] Wire onboarding webhook to Hermes when DNS resolves for `onboarding.manyhatautomations.com`
- [ ] Document what n8n Railway workflow `eeosgS5oNMCffbbi` does in full

---

*Auto-mapped via GHL API on 2026-05-21. API key rotated same date — update reference_ghl in Claude memory.*
*[[Claude-Integration]] | [[Business-Operations]] | [[Lead-Pipeline]]*
