# Social Media Engine Optimization — Design Spec

**Date:** 2026-03-18
**Author:** Claude (brainstorming session with Paul)
**Status:** Approved

---

## Overview

Optimize and expand ManyHat Automations' social media publishing infrastructure across 4 systems to achieve fully hands-free, multi-platform content distribution with research-backed scheduling. The goal is to position ManyHat as the primary authority in AI automation while maximizing reach across all brand accounts.

### Systems in Scope

| System | ID / Location | Role |
|---|---|---|
| Content Engine v2.0 | Railway n8n `0J8UnIfBdeRZcBUE` | AI text/image content with brand voice |
| RSS Feed Scraper | Railway n8n `q7ZwLmDHkDnuoTvF` | News sourcing → Airtable |
| AI Mate | Prospect n8n `bN4Xp4RbwbqaKdZ2` | Avatar lip-sync video pipeline |
| Canva Reels | Make.com scenario `4412058` | Polished branded video exports |

---

## 1. Content Engine v2.0 — Fixes & Expansion

### 1.1 Trigger Changes

**Remove:** Airtable Trigger node (was causing issues — polling conflicts, OAuth token expiry)

**Fix Schedule Trigger:**
- Change from "every 3 days" to 2x/day, weekdays only (Mon-Fri)
- Run 1: 6:30 AM EST (`30 11 * * 1-5` UTC)
- Run 2: 12:00 PM EST (`0 17 * * 1-5` UTC)

**Keep Webhook Trigger:** RSS scraper will POST to it when new articles are ready, passing `sourceSummary`, `sourceURL`, `sourceHeadline` as the topic.

### 1.2 Image Domain Fix

Change image upload URL from `https://postiz.proisp.no/uploads` to `https://postiz.prospectai.app/api/public/v1/upload` to match the posting endpoint and resolve the domain mismatch.

### 1.3 Publishing Overhaul — Single Code Node + Single API Call

**Remove nodes:**
- `Prepare Posts (Image)`
- `Prepare Posts (No Image)`
- `Post to Postiz`
- `Post to Postiz1`

**Replace with:**

#### Node: `Build All Posts` (Code Node)

Inputs:
- Parsed captions from `Parse Captions` node (JSON with platform keys)
- `has_image` boolean from the IF node branch merge
- Optional image `id` and `path` from Postiz upload response

Logic:
```
IF has_image:
  Build posts[] for ALL 35 channels including Instagram
  Each post includes image[{id, path}]
ELSE:
  Build posts[] for 28 channels (exclude 7 Instagram accounts)
  No image array in posts
```

Platform-specific settings per post:
- **Instagram**: `{ "__type": "instagram", "post_type": "post", "is_trial_reel": false }` — caption wrapped in `<p>` tags
- **Facebook**: `{ "__type": "facebook" }` — caption wrapped in `<p>` tags
- **Threads**: `{ "__type": "threads" }`
- **X/Twitter**: `{ "__type": "x", "who_can_reply_post": "everyone" }` — note: video won't attach on Pay Per Use tier
- **LinkedIn Personal**: `{ "__type": "linkedin" }`
- **LinkedIn Page**: `{ "__type": "linkedin-page" }`

Scheduling offsets (staggered from execution time):
- LinkedIn: +5 min
- Facebook: +15 min
- X/Twitter: +30 min
- Threads: +45 min
- Instagram: +60 min (image path only)

#### Node: `Post to Postiz` (HTTP Request)

Single POST to `https://postiz.prospectai.app/api/public/v1/posts` with the full payload.
Auth: `Authorization: 9ea4d98f2f968afacedaaa3bdcde6eb548178d6b91841aae85747afd2d91df21`

### 1.4 Channel IDs (35 total for Content Engine)

#### Instagram (7) — only when image is generated
| Brand | Channel ID |
|---|---|
| PaulManyHats | `cmmv7cbmu0003qr77254218vw` |
| ManyHatsWire | `cmmv7e8ll0005qr77yk73uya4` |
| ManyHatsAI | `cmmv7emj70007qr77j1d0a6ri` |
| @paul_manyhats | `cmmlhrdil0007qq6vwu18e5i9` |
| ManyHatsHQ | `cmmv7f7jj0009qr775ufx5rsh` |
| ManyHatsLabs | `cmmv7fp1g000bqr777dh1znfz` |
| ManyHatsIO | `cmmv7g7sh000dqr77awyehngv` |

#### Facebook (7)
| Brand | Channel ID |
|---|---|
| PaulManyHats | `cmmv7i0b3000fqr77yocw2dfz` |
| ManyHatsWire | `cmmv7ii02000hqr77xncmvmso` |
| ManyHatsAI | `cmmv7iyk0000jqr770k3mhrae` |
| @paul_manyhats | `cmmlhoxlm0005qq6v2v0vo04b` |
| ManyHatsHQ | `cmmv7jips000lqr775mfsj9q6` |
| ManyHatsLabs | `cmmv7jxs8000nqr77rjhkp1f1` |
| ManyHatsIO | `cmmv7kgmd000pqr77resukq6l` |

#### Threads (7)
| Brand | Channel ID |
|---|---|
| ManyHatsIO | `cmmv8hd1p000rqr77e21xyv3j` |
| PaulManyHats | `cmmv8jv55000tqr77tmmi6026` |
| ManyHatsWire | `cmmv8kp6x000vqr77vwxcl6ba` |
| ManyHatsAI | `cmmv8lp0n000xqr77w2tffsjo` |
| ManyHatsHQ | `cmmv8mqrm000zqr77he7ebpqt` |
| ManyHatsLabs | `cmmv8nxfq0011qr77vnfht96x` |
| paul_manyhats | `cmmmcat4s0001o56fth358ut7` |

#### X/Twitter (7)
| Brand | Channel ID |
|---|---|
| ManyHatsIO | `cmmwjhkfs0002qg7bn8fdxve5` |
| PaulManyHats | `cmmwjmppk0004qg7bzsv3w39b` |
| ManyHatsWire | `cmmvm65rt0006qg7brrqwpyv2` |
| ManyHatsAI | `cmmvm58sl0004qg7bm8pmll36` |
| ManyHatsHQ | `cmmwjvwtf0006qg7boiwx1ubv` |
| ManyHatsLabs | `cmmwk89sk0008qg7b0dsrbk7l` |
| Paul Rammeloo | `cmmlqpzi00001nb6p0nosx4a0` |

#### LinkedIn (2)
| Brand | Channel ID |
|---|---|
| Paul Rammeloo (personal) | `cmmlhofia0001qq6vfcmn7e9p` |
| ManyHats Automations (page) | `cmmlhol5k0003qq6vlgw4pdky` |

### 1.5 Content Angle Selector

Add weighted randomness to the `Pick Content Angle` Code node:

| Angle | Weight | Behavior |
|---|---|---|
| Industry Authority | 40% | Reports on trend, ManyHat comments as expert |
| Our Solution | 25% | Ties topic to ManyHat's AI agent offerings |
| Educational | 20% | Teaches a concept — pure value, no pitch |
| Contrarian Take | 15% | Hot take on the trend — engagement driver |

The `user_prompt` passed to the AI Agent includes the selected angle, which instructs the agent how to frame the content. The AI Agent's system prompt is updated with ManyHat's positioning: AI automation agency, AI agents, lead generation, demo URL.

### 1.6 IF Node Merge

The existing IF node (`Should Generate Image`) branches into YES (image) and NO (no-image) paths. Both paths converge into the new `Build All Posts` Code node. The merge carries:
- `captions` — parsed JSON from AI Agent
- `has_image` — boolean
- `image_id` + `image_path` — only present on the image path

---

## 2. RSS Feed Scraper — Niche Overhaul

### 2.1 Feed Replacement

**Keep (3 crypto with AI overlap):**
1. CoinDesk — `https://www.coindesk.com/arc/outboundfeeds/rss/`
2. CoinTelegraph — `https://cointelegraph.com/rss`
3. Decrypt — `https://decrypt.co/feed`

**Add (15 AI/automation feeds):**

| # | Source | Feed URL | Category |
|---|---|---|---|
| 1 | The Verge AI | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` | AI News |
| 2 | Ars Technica AI | `https://feeds.arstechnica.com/arstechnica/technology-lab` | AI News |
| 3 | VentureBeat AI | `https://venturebeat.com/category/ai/feed/` | AI News |
| 4 | MIT Technology Review AI | `https://www.technologyreview.com/topic/artificial-intelligence/feed` | AI Research |
| 5 | TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` | AI Startups |
| 6 | OpenAI Blog | `https://openai.com/blog/rss.xml` | LLMs / Agents |
| 7 | Anthropic Blog | `https://www.anthropic.com/rss.xml` | LLMs / Agents |
| 8 | Google AI Blog | `https://blog.google/technology/ai/rss/` | LLMs / Agents |
| 9 | Hugging Face Blog | `https://huggingface.co/blog/feed.xml` | Open Source AI |
| 10 | n8n Blog | `https://blog.n8n.io/rss/` | Automation |
| 11 | Zapier Blog | `https://zapier.com/blog/feed/` | Automation |
| 12 | Make.com Blog | `https://www.make.com/en/blog/rss.xml` | Automation |
| 13 | HubSpot Marketing Blog | `https://blog.hubspot.com/marketing/rss.xml` | Marketing AI |
| 14 | Search Engine Journal | `https://www.searchenginejournal.com/category/artificial-intelligence/feed/` | Marketing AI |
| 15 | a16z AI | `https://a16z.com/ai/feed/` | AI Strategy |

**Total: 18 feeds** (3 crypto + 15 AI/automation)

### 2.2 Airtable Output
Continues writing to Daily News table (`appw5JcYwgEswfcV2` / `tbljAtK678rkIMLBz`) with fields:
- `sourceHeadline`, `sourceSummary`, `sourceURL`
- `needsImage?` → `"No"`
- `Status` → `"Waiting for Content"`

### 2.3 Webhook Integration with Content Engine
Add a final node after Airtable write that POSTs to the Content Engine's webhook:
```
POST https://webhook-processor-production-f687.up.railway.app/webhook/data-processing
Body: { topic: sourceHeadline, summary: sourceSummary, url: sourceURL, source: "rss" }
```

This fires the Content Engine's webhook path, which formats the input and feeds it to the AI Agent.

### 2.4 Activation
Set workflow to **ACTIVE** with daily 8:00 AM EST schedule (existing config).

---

## 3. Make.com Canva Reels — Platform Expansion

### 3.1 Add Missing Platforms to Postiz HTTP Module

Add to the existing `posts[]` array in the Postiz posting step:

#### LinkedIn (2 new)
| Brand | Channel ID | Settings |
|---|---|---|
| Paul Rammeloo | `cmmlhofia0001qq6vfcmn7e9p` | `{ "__type": "linkedin" }` |
| ManyHats Automations | `cmmlhol5k0003qq6vlgw4pdky` | `{ "__type": "linkedin-page" }` |

#### Pinterest (7 new) — Board: "AI Content"
| Brand | Channel ID | Settings |
|---|---|---|
| Paul Rammeloo | `cmmtn67an0001nu7a5fllgj0i` | `{ "__type": "pinterest", "board": "AI Content" }` |
| ManyHatsIO | `cmmwkzvye000iqg7b1381uhqw` | `{ "__type": "pinterest", "board": "AI Content" }` |
| PaulManyHats | `cmmwl2fsp000kqg7bd3zz179z` | `{ "__type": "pinterest", "board": "AI Content" }` |
| ManyHatsWire | `cmmwki28e000aqg7bko7ybgu6` | `{ "__type": "pinterest", "board": "AI Content" }` |
| ManyHatsAI | `cmmwkpmzq000cqg7biksty816` | `{ "__type": "pinterest", "board": "AI Content" }` |
| ManyHatsHQ | `cmmwku2nv000eqg7bp0eus2tg` | `{ "__type": "pinterest", "board": "AI Content" }` |
| ManyHatsLabs | `cmmwkwmw1000gqg7be0p60fom` | `{ "__type": "pinterest", "board": "AI Content" }` |

#### YouTube (1 new)
| Brand | Channel ID | Settings |
|---|---|---|
| ManyHats Automations | `cmmtmvfru0003mo6tfr7szmgt` | `{ "__type": "youtube" }` |

#### X/Twitter (4 additional — 3 already exist)
| Brand | Channel ID |
|---|---|
| ManyHatsIO | `cmmwjhkfs0002qg7bn8fdxve5` |
| PaulManyHats | `cmmwjmppk0004qg7bzsv3w39b` |
| ManyHatsHQ | `cmmwjvwtf0006qg7boiwx1ubv` |
| ManyHatsLabs | `cmmwk89sk0008qg7b0dsrbk7l` |

**New total: 45 channels** (up from 31)

### 3.2 Schedule Change
From: Mon/Thu/Sat at 08:04
To: **Tue/Thu/Sat** at optimized times:
- Tuesday: 10:00 AM EST (15:00 UTC)
- Thursday: 4:00 PM EST (21:00 UTC)
- Saturday: 11:00 AM EST (16:00 UTC)

---

## 4. AI Mate — No Changes

Already optimized. 3x/day to all 50+ channels. Schedule stays:
- 7:01 AM EST
- 2:02 PM EST
- 9:03 PM EST

---

## 5. Master Posting Schedule

### Weekly Overview

| Time (EST) | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| 6:30 AM | CE | CE | CE | CE | CE | - | - |
| 7:01 AM | AM | AM | AM | AM | AM | AM | AM |
| 10:00 AM | - | **CR** | - | - | - | - | - |
| 11:00 AM | - | - | - | - | - | **CR** | - |
| 12:00 PM | CE | CE | CE | CE | CE | - | - |
| 2:02 PM | AM | AM | AM | AM | AM | AM | AM |
| 4:00 PM | - | - | - | **CR** | - | - | - |
| 9:03 PM | AM | AM | AM | AM | AM | AM | AM |

**Legend:** CE = Content Engine, AM = AI Mate, CR = Canva Reels

### Daily Content Volume Per Platform (Weekday with Canva Reels)

| Platform | AM posts | CE posts | CR posts | Total |
|---|---|---|---|---|
| X/Twitter | 3 (7 brands) | 2 (7 brands) | 1 (7 brands) | 6 per brand |
| LinkedIn | 3 (2 accounts) | 2 (2 accounts) | 1 (2 accounts) | 6 per account |
| Instagram | 3 (7 brands) | 0-2 (7 brands, image only) | 1 (7 brands) | 4-6 per brand |
| Facebook | 3 (7 brands) | 2 (7 brands) | 1 (7 brands) | 6 per brand |
| Threads | 3 (7 brands) | 2 (7 brands) | 1 (7 brands) | 6 per brand |
| TikTok | 3 (7 brands) | - | 1 (7 brands) | 4 per brand |
| Pinterest | 3 (7 brands) | - | 1 (7 brands) | 4 per brand |
| YouTube | 3 (1 channel) | - | 1 (1 channel) | 4 |

### Anti-Spam Safety Check

All frequencies stay within safe algorithmic limits:
- X: max 6/day per brand (safe limit: 5-8)
- LinkedIn: max 6/day per account (slightly aggressive — monitor; can reduce CE to 1x/day if needed)
- Instagram: max 6/day per brand (safe limit: 2 feed + unlimited Stories — Reels count separately)
- Facebook: max 6/day per brand (safe limit: 2 — this is aggressive across 3 workflows; monitor closely)
- Threads: max 6/day per brand (safe limit: 5+ — Threads is tolerant)
- TikTok: max 4/day per brand (safe limit: 3-4)
- Pinterest: max 4/day per brand (safe limit: 10/week — we're at ~28/week, fine)
- YouTube: max 4/day (safe limit: 1 — this needs attention; YouTube penalizes >1 Short/day)

### YouTube Concern
At 4 Shorts/day, YouTube may suppress reach. **Recommendation:** Only post to YouTube from AI Mate (1x/day instead of 3x) and Canva Reels (3x/week). Remove YouTube from 2 of the 3 AI Mate runs. This brings it to ~1/day average.

### Facebook Concern
At 6 posts/day per brand, Facebook organic reach will likely be suppressed. **Recommendation:** Monitor after 1 week. If engagement drops, reduce Content Engine Facebook posting to 1x/day instead of 2x.

---

## 6. Implementation Order

1. **RSS Feed Scraper** — Update feeds, add webhook call, activate
2. **Content Engine v2.0** — Fix triggers, fix image domain, replace publishing nodes, update AI prompts
3. **Make.com Canva Reels** — Add platforms, update schedule
4. **Verify & test** each system individually, then cross-system

---

## Success Criteria

- [ ] All 3 active workflows fire on their schedules without errors
- [ ] Content Engine posts to 35 channels (28 without image, 35 with image)
- [ ] RSS Scraper feeds AI/automation articles to Content Engine via webhook
- [ ] Make.com posts to 45 channels on Tue/Thu/Sat
- [ ] AI Mate continues unchanged at 3x/day to 50+ channels
- [ ] No platform rate-limit violations after 1 week of operation
- [ ] Content angles distribute roughly 40/25/20/15 across authority/solution/educational/contrarian
