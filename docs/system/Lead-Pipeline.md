---
date: 2026-05-21
type: lead-pipeline
tags: [leads, pipeline, reacher, outreach]
aliases: [outreach-pipeline, lead-flow]
---

# Lead Pipeline

> **Purpose:** A repeatable system for finding, enriching, and converting local BC service businesses into AI voice agent clients for ManyHat Automations.
>
> **Integration:** This pipeline feeds directly into [[Business-Operations]] for daily execution, campaign tracking, and revenue reporting. For SOPs referenced below, see [[SOPs/email system prompt]] and [[SOPs/stale followup prompt]].

---

## Pipeline Overview

| Stage | Tool | Output | Owner |
|-------|------|--------|-------|
| Scraping (Data Miner) | Data Miner Chrome Extension | Raw CSV to `leads-inbox/` | You |
| Drop Folder / Enrichment | Enrichment Agent | Enriched .md + Reacher CSV | Agent (auto) |
| Reacher Upload / Campaign | Reacher (OperatorBase) | Verified email campaigns | You |
| Cold Call / Follow-Up | Phone + Enriched Brief | Demos booked, leads converted | You |
| Integration / Handoff | GHL + Lead .md logs | Closed deals, nurture pipeline | System |

The full pipeline runs in two lanes: **automated outreach** (Reacher email) and **manual outreach** (cold calls). They work together. See the Integration section for how leads move between them.

---

## 1. Scraping (Data Miner)

> **Goal:** Build a list of local service businesses that have no live chat widget — a clear signal they could benefit from our AI voice agent.

### Prerequisites
- Chrome browser
- **Data Miner** extension installed (Chrome Web Store)

### Sources & Search Patterns
- **Primary source:** Google Maps
- **Search query pattern:** `[niche] near [city], BC`
  - Example: `dental near Vancouver, BC` | `HVAC near Victoria, BC` | `roofing near Kelowna, BC`

### Target Niches
HVAC, dental, med spa, roofing, law, auto repair, real estate, and other local service businesses.

### Data Miner Scrape Setup
1. Go to Google Maps and run one of the search queries above.
2. Open Data Miner → choose the Google Maps recipe (or build one with these columns).
3. **Required columns:** `Business Name`, `Address`, `Rating`, `# Reviews`, `Category`, `Phone`, `Email/Website`

### Pro Tips for Quality Scrapes

| Tip | Why It Matters |
|-----|---------------|
| Sort results by **rating 3.5–4.5** | Too high (4.8+) = often resistant to change; too low = tough sell |
| Filter for **50+ reviews** | Signals established business with budget to invest |
| Target businesses with **no live chat widget** on website | Our core angle — they are missing real-time lead capture |
| Verify website exists and loads | Dead sites = wasted effort |

### Output
- Export as CSV to: `C:/Users/paulr/leads-inbox/`
- Naming convention: `[niche]-[city]-[YYYY-MM-DD].csv`

---

## 2. Drop Folder / Enrichment Agent

> **Goal:** Turn raw CSVs into sales-ready intelligence — one file per business, scored and briefed.

### How It Works
1. Save or drop any CSV into: `C:/Users/paulr/leads-inbox/`
2. The **Enrichment Agent** detects the new file and processes it automatically.
3. For every business in the CSV, the agent:
   - Finds the best available **email**
   - Audits the **website** (checks for live chat widget)
   - **Scores the lead 1–10**
   - Generates a **cold call brief** (3–5 bullets)
4. Telegram notification fires with the **top leads scored 7+**

### Enrichment Outputs (Dual Path)

| Path | Location | Format | Purpose |
|------|----------|--------|---------|
| Vault | `04 Business/Manyhat-Automations/Lead-Generation/enriched/` | One `.md` file per lead | Human review, cold call prep, status tracking |
| Reacher | Same folder or linked | Reacher-formatted CSV | Direct upload to Reacher campaigns |

### How to Read an Enriched Lead .md File

Each file represents one business and follows this structure:

- **Business Name**
- **Contact Info** (phone, email, website)
- **Website Audit:** Live chat widget present? `Yes` or `No`
- **Pain Points Identified** (auto-generated from reviews + site audit)
- **Score:** `1–10`
- **Cold Call Brief:** 3–5 bullets covering business pain points, opportunity angle, and suggested opener

---

### Lead Scoring Guide (1–10)

| Score | Label | Criteria | Action |
|:-----:|-------|----------|--------|
| **10** | Priority Demo | No chat widget, strong reviews (4.0+), 100+ reviews, email found, clear automation opportunity | Call first. Prepare custom demo. |
| **9** | Strong Opportunity | No chat widget, good reviews, email found, active online presence | Call + email immediately. |
| **8** | Good Lead | No chat widget, decent reviews, email found or phone confirmed | Call + email in first outreach wave. |
| **7** | Warm Lead | No chat widget, needs minor verification, contact found | Add to outreach; verify contact before call. |
| **6** | Marginal | Has basic website, contact uncertain, may have some automation | Email only; proceed with caution. |
| **5** | Borderline | Marginal opportunity, contact uncertain | Low priority; batch with email-only. |
| **4 or below** | Skip | Has live chat already, poor reviews, no contact info, or out of scope | Do NOT contact. Archive or delete. |

---

## 3. Uploading to Reacher

> **Goal:** Launch high-volume, personalized email campaigns using enriched and scored leads.

### Step-by-Step

1. Open **OperatorBase → Reacher → Jobs**
2. Create a new **Job** per niche bucket:
   - Example: `HVAC Vancouver`, `Dental Victoria`, `Roofing Kelowna`
3. Upload the **Reacher CSV** output from the enrichment agent
   - **Important:** Do NOT upload the raw Data Miner CSV. Use the enriched Reacher-formatted CSV only.
4. Assign the Job to a **Campaign**

### Campaign Setup

| Field | Guidance |
|-------|----------|
| **Campaign name** | `[Niche] - [City] - [Month YYYY]` |
| **From address** | Rotate across 9 sender emails across 3 subdomains |
| **Daily limit per email** | 20 |
| **Total daily capacity** | 180 emails |
| **Monthly quota** | ~3,000 — protect this; only confirmed emails, scored 6+ |
| **Email prompt** | [[SOPs/email system prompt]] |
| **Model** | Claude Sonnet 4.6 |
| **Mode** | Auto |
| **Timezone** | Eastern |
| **AI demo generation** | ON |
| **Stale follow-up** | [[SOPs/stale followup prompt]] — triggers after 7 days silence, every 3 days, max 3 times |
| **Subject lines** | A/B test 2–3 variations per campaign |
| **Personalization tokens** | `{{business_name}}`, `{{first_name}}`, `{{city}}` |

---

## 4. Cold Calling

> **Goal:** Book demos by calling the highest-scored leads using the enriched intelligence.

### Pre-Call Routine
Before dialing, open the lead's enriched `.md` file and read the **Cold Call Brief** section (3–5 bullets). This tells you what they care about.

### Opener Formula

> *"Hi [name], I was looking at [business name]'s website and noticed you don't have a live chat — is that something you've thought about?"*

### The Offer

> *"I can show you a free AI demo built specifically for your website — takes 2 minutes to see."*

- **First call:** Generic demo link is fine.
- **Callback / warm lead:** Generate custom demo — use Hermes Telegram command: `/demo [business URL]`
- Demo link to share: `https://manyhatautomations.aidemo.app`

### Objection Handling & Scripts
- [[SOPs/objection handling]]
- [[SOPs/sales call script]]

---

## 5. Integration & Handoff

> **Goal:** Track every touch in the lead's file, move hot leads fast, hand off engaged prospects to automation.

### Post-Touch Logging
After any cold call, update the lead's `.md` file with the result:
- `interested`
- `not interested`
- `callback` (note date/time)

### If Interested + Email Provided
- Add to Reacher immediately. Do not wait for the next batch upload.

### If Callback Scheduled
- Log in **GHL (GoHighLevel)**
- Set reminder for follow-up

### If Engaged with Demo
- Handoff: GHL AI Delta Response takes over — see [[Business-Operations]]
- Stop all manual outreach. The automation handles nurture from here.

---

## Quick Reference

| If you need to... | Go to... |
|-------------------|----------|
| Launch a new niche campaign | Section 3: Uploading to Reacher |
| Prepare for a cold call | Open the lead's `.md` in `enriched/` |
| Check what to say | [[SOPs/sales call script]] |
| Handle an objection | [[SOPs/objection handling]] |
| Review overall pipeline health | [[Business-Operations]] |
| Check email copy | [[SOPs/email system prompt]] |
| Set up stale follow-ups | [[SOPs/stale followup prompt]] |

---

*Last updated: 2026-05-21*
