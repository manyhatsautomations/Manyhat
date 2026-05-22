# ManyHat Content Pipeline — Design Spec

**Date:** 2026-05-21  
**Status:** Approved  
**Goal:** Build a sustainable, agent-driven video content pipeline targeting 1M followers across all platforms.

---

## Design Constraints

- n8n workflows: max 5 nodes, single-purpose only — no loops, merges, wait-and-poll, or complex logic
- All heavy logic lives in Python scripts (testable, debuggable, version-controlled)
- Hermes agent handles publishing via Postiz — no n8n in the publishing path
- Multi-LLM: Kimi for code/scripts, DeepSeek for research/scoring, Qwen for strategy, GLM for agentic steps
- Cost-first: cheap models handle 95% of work; Claude orchestrates only

---

## System Overview

```
[B] Content Intelligence Hub (Python + DeepSeek/Kimi)
    GitHub Trending · HackerNews · Product Hunt · RSS · X Trending
              ↓  daily scored idea queue → Airtable
[Hermes/Telegram] → you approve (reply "1", "2", "3", or "all")
              ↓  approved topic
[C] Video Production Pipeline
    video-use OR Playwright → screen MP4
    + your batch talking head recording
    → HyperFrames HTML composition → FFmpeg render
    → 9:16 + 16:9 + 1:1 exports
              ↓  completed video + captions
[Hermes agent → Postiz] → 35+ channels scheduled
              ↓  posts live with CTAs
[A] Comment-to-DM Engine
    ManyChat (IG/FB/TikTok) + n8n webhook → GHL CRM → nurture
              ↓
[D] Hermes/Telegram Command Center
    Daily briefs · lead alerts · post performance
```

---

## Sub-System A: Comment-to-DM Engine

**Stack:** ManyChat → n8n (4-node webhook) → GHL

### Flow
```
User comments trigger word on post
→ ManyChat detects keyword
→ Sends DM: "Here's your [lead magnet] 👇 [link]"
→ ManyChat webhook → n8n (4 nodes: receive → parse → GHL create contact → done)
→ GHL nurture sequence:
    Day 1: SMS "Did you try the workflow?"
    Day 3: Email — case study
    Day 7: Demo offer
```

### Platform Coverage
| Platform | Tool | Status |
|----------|------|--------|
| Instagram | ManyChat (IG API) | Need ManyChat account |
| Facebook | ManyChat | Need ManyChat account |
| TikTok | ManyChat (TikTok Business API) | Need ManyChat account |
| X/Twitter | n8n + Twitter v2 API | Need v2 API access |
| LinkedIn | NOT SUPPORTED — API bans automated DMs | Skip |

### Lead Magnets (build before launch)
| Magnet | Format | Keyword | Storage |
|--------|--------|---------|---------|
| AI Agent Starter Workflow | n8n JSON template | AGENT | Google Drive |
| 10 AI Tools That Replaced Staff | PDF | TOOLS | Google Drive |
| AI Automation ROI Calculator | Google Sheet | ROI | Google Drive |
| Lead Gen Agent Walkthrough | Loom video | BUILD | Google Drive |

### n8n Workflow: Comment-to-DM
```
[ManyChat Webhook] → [Parse body: platform, user, keyword, post_url]
→ [HTTP POST to GHL: create contact] → done
```
4 nodes. No branching. No error handling beyond HTTP retry.

---

## Sub-System B: Content Intelligence Hub

**Stack:** Python script → multi-LLM scoring → Airtable

### Script: `intelligence.py` (runs daily 7 AM via n8n cron)

**Data sources:**
| Source | Endpoint | Pull |
|--------|----------|------|
| GitHub Trending | `https://api.gtrending.com/repos?language=python&since=daily` | Top 10 repos |
| HackerNews | `https://hn.algolia.com/api/v1/search?tags=front_page&query=AI` | Top AI stories |
| Product Hunt | `https://api.producthunt.com/v2/api/graphql` | Top 5 products |
| RSS (18 feeds) | Existing feed list | Latest AI/automation |
| X Trending | Twitter v2 API | AI-tagged trending |

**LLM processing per item:**
1. DeepSeek — scores 1–10: viral potential, niche relevance, ManyHat fit
2. Kimi — generates 3 content angles: educational, tutorial, hot take
3. Script filters: top 3 ideas written to Airtable with status `Pending Review`

**Airtable schema (ideas table):**
```
Topic | Source URL | Viral Score | Content Angle | Format | Script | Status | Date
```

**Status lifecycle:**
`Pending Review` → `Approved` → `In Production` → `Rendered` → `Posted`

**Hermes daily brief (7:30 AM Telegram):**
```
python daily_brief.py
→ reads top 3 from Airtable
→ sends via Hermes to Telegram:
  "Today's ideas:
   1. [topic] — score 9.2 — Tutorial format
   2. [topic] — score 8.7 — Hot take format
   3. [topic] — score 8.1 — Demo format
   Reply 1/2/3/all to approve"
```

You reply → Hermes updates Airtable status → triggers render pipeline.

### n8n Workflow: Content Discovery
```
[Cron: 7:00 AM daily] → [Execute: python intelligence.py] → done
```
3 nodes.

---

## Sub-System C: Video Production Pipeline

**Stack:** video-use / Playwright → HyperFrames → FFmpeg → Hermes → Postiz

### Script: `render_pipeline.py --topic-id <airtable_id>`

**Step-by-step:**

**Step 1 — Screen recording:**
- If topic = GitHub repo or web tool: `video-use` runs a browser-use agent to navigate and demo it
- If topic = news/hot take: no screen recording needed (talking head only)
- Playwright `video: 'on'` as fallback for any browser session

```python
# video-use pattern
from video_use import VideoRecorder
agent = Agent(task=f"Navigate to {url}, scroll through key sections, show main features")
recorder = VideoRecorder(agent)
recorder.start()
await agent.run()
recorder.stop()
recorder.save(f"recordings/{topic_id}_screen.mp4")
```

**Step 2 — Script generation:**
- Kimi generates 90-second script from topic + angle
- Script written to `scripts/{topic_id}.txt`
- Script paired with next available talking head clip from `recordings/talking_heads/`

**Step 3 — HyperFrames composition:**
- Kimi generates HTML composition file from template
- Template type selected from: `ai-tool-demo`, `github-spotlight`, `news-hottake`, `tutorial-walk`, `client-result`
- HyperFrames CLI renders locally:

```bash
npx hyperframes render compositions/{topic_id}.html --output renders/{topic_id}_draft.mp4
```

**Step 4 — Multi-format FFmpeg export:**
```bash
# 9:16 for Reels/TikTok
ffmpeg -i renders/{topic_id}_draft.mp4 -vf "scale=1080:1920,setsar=1" renders/{topic_id}_916.mp4

# 16:9 for YouTube
ffmpeg -i renders/{topic_id}_draft.mp4 -vf "scale=1920:1080,setsar=1" renders/{topic_id}_169.mp4

# 1:1 for LinkedIn/X feed
ffmpeg -i renders/{topic_id}_draft.mp4 -vf "scale=1080:1080,setsar=1" renders/{topic_id}_11.mp4
```

**Step 5 — Hermes → Postiz publish:**
- Hermes agent picks up render completion
- Posts all 3 formats to Postiz with platform-specific captions (Kimi-generated)
- Postiz schedules staggered across 35+ channels
- Hermes confirms to Telegram: "Posted ✅ — [topic] live on 35 channels"

### Five HyperFrames Templates (Kimi generates HTML)

| Template | Layers | Screen record needed |
|----------|--------|---------------------|
| `ai-tool-demo.html` | Screen BG + talking head PIP + tool name lower third | Yes — Playwright/video-use |
| `github-spotlight.html` | README scroll + PIP + repo stats card | Yes — video-use agent |
| `news-hottake.html` | Animated headline card + full talking head | No |
| `tutorial-walk.html` | Step counter + screen + PIP | Yes — Playwright |
| `client-result.html` | Before/after split + numbers animation | No |

### Your Manual Contribution (one session/week, 30 minutes)
- Record 5–10 talking head clips, 60–90 seconds each
- Read the Kimi-generated script
- Save to `recordings/talking_heads/`
- System pairs them with screen recordings automatically

---

## Sub-System D: Hermes Command Center

**Stack:** Hermes MCP → Telegram private channel

### Agent responsibilities:
| Trigger | Action |
|---------|--------|
| 7:30 AM daily | Send top 3 ideas brief to Telegram |
| You reply "approve" / number | Update Airtable → trigger render_pipeline.py |
| Render complete | Receive video files → post to Postiz |
| Post confirmed | Send confirmation to Telegram |
| New GHL lead from DM | Send lead alert to Telegram |
| Post hits >500 engagements in 2h | Flag to Telegram for manual boost/reply |

### Hermes ↔ Postiz integration:
- Hermes agent configured with Postiz API credentials
- Accepts: `{video_916: path, video_169: path, video_11: path, captions: {ig, tiktok, x, linkedin, facebook, threads}, schedule_offset_minutes: 30}`
- Posts to Postiz `/api/public/v1/posts` endpoint
- Handles staggered scheduling per platform

---

## Multi-LLM Delegation Matrix

| Task | Model | Rationale |
|------|-------|-----------|
| HyperFrames HTML generation | Kimi | HTML/CSS/GSAP native |
| Script writing (90s videos) | Kimi | Best quality/cost for structured output |
| Caption writing (per platform) | Kimi | Platform format rules well-defined |
| Topic scoring + research | DeepSeek | Search-capable, fast, cheap |
| Daily brief composition | DeepSeek | Analysis + summarization |
| Content angle strategy | Qwen | Strategic reasoning |
| Multi-step agent tasks | GLM | Agentic orchestration |
| n8n code nodes (if any) | Kimi | Code generation |
| Lead magnet PDF creation | Kimi + MiniMax | Cheap for doc generation |

---

## Content Calendar (sustainable path to 1M)

| Day | Video (auto pipeline) | Text/CTA post | You do |
|-----|-----------------------|---------------|--------|
| Mon | GitHub Spotlight → all platforms | — | — |
| Tue | AI Tool Demo → all platforms | "Comment AGENT" CTA post | Record week's talking heads (30 min) |
| Wed | — | Hot take / controversy | — |
| Thu | Tutorial walkthrough → all platforms | — | — |
| Fri | — | "Comment TOOLS" CTA post | Approve next week's idea queue (2 min in Airtable) |
| Sat | News Hot Take → all platforms | — | — |
| Sun | — | Thread repurpose (best of week) | — |

**Weekly output:** 4 videos + 3 high-CTA text posts across 35+ channels  
**Comment-to-DM cadence:** 2 trigger posts/week minimum

---

## n8n Workflows (complete list — nothing more)

### Workflow 1: Content Discovery Trigger
```
[Cron: 7:00 AM daily, Mon-Sat]
→ [Execute Command: python /scripts/intelligence.py]
→ done
```

### Workflow 2: Comment-to-DM
```
[Webhook: ManyChat callback URL]
→ [Set: extract platform, username, keyword, post_url from body]
→ [HTTP POST: GHL /contacts {firstName, phone/email if available, source: "comment-to-dm", keyword}]
→ done
```

**That's the entire n8n surface.** Two workflows, seven nodes total.

---

## Installation Requirements

| Tool | Runtime | Install command |
|------|---------|----------------|
| HyperFrames | Node.js 22+ | `npm install -g @heygen/hyperframes` |
| video-use | Python 3.11+ | `pip install video-use browser-use` |
| FFmpeg | System | `winget install ffmpeg` (Windows) |
| Playwright | Python | `pip install playwright && playwright install chromium` |
| browser-use | Python | included with video-use |

---

## Build Phases

| Phase | Week | Deliverables |
|-------|------|-------------|
| **1 — Comment-to-DM** | 1 | ManyChat setup + 3 lead magnets + n8n webhook + GHL nurture |
| **2 — Intelligence Hub** | 2–3 | intelligence.py + Airtable schema + Hermes daily brief |
| **3 — Video Pipeline** | 3–5 | HyperFrames templates (5) + render_pipeline.py + Hermes→Postiz agent |
| **4 — Integration** | 5–6 | Full pipeline test, approval loop, Telegram command center |

---

## Success Criteria

- [ ] Comment-to-DM live on Instagram, Facebook, TikTok within Week 1
- [ ] Daily idea queue populates Airtable automatically each morning
- [ ] Talking head + screen recording composited and posted within 2h of approval
- [ ] Hermes confirms every publish to Telegram
- [ ] 4 videos/week + 3 CTA posts published consistently for 30 days
- [ ] No n8n workflow exceeds 5 nodes
- [ ] 0 manual steps required to publish once content is approved
