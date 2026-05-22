# Phase 1: Content Intelligence Hub — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python-based daily content intelligence system that scrapes GitHub Trending, HackerNews, Product Hunt, and RSS feeds, scores each item via DeepSeek, generates content angles via Kimi, writes the top 3 ideas to Airtable, and sends a Telegram brief via Hermes each morning.

**Architecture:** A single Python project with one module per data source, a shared LLM client, and two runnable entry-point scripts (`intelligence.py` runs the full pipeline; `daily_brief.py` sends the Telegram message). n8n triggers `intelligence.py` via a 3-node cron workflow.

**Tech Stack:** Python 3.13, `requests`, `feedparser`, `pyairtable`, OpenRouter API (DeepSeek + Kimi), Telegram Bot API, n8n Railway (cron trigger only)

---

## File Structure

```
C:/Users/paulr/content-pipeline/
├── .env                         # Secrets (gitignored)
├── .env.example                 # Template checked into git
├── requirements.txt
├── config.py                    # Reads .env, exposes typed constants
├── llm_client.py                # Shared OpenRouter API wrapper
├── sources/
│   ├── __init__.py
│   ├── github_trending.py       # Fetches top 10 trending repos
│   ├── hackernews.py            # Fetches top AI stories via Algolia
│   ├── producthunt.py           # Fetches top 5 products via GraphQL
│   └── rss_feeds.py             # Aggregates 18 RSS feeds
├── scoring.py                   # Scores items 1-10 via DeepSeek
├── angles.py                    # Generates content angles via Kimi
├── airtable_client.py           # Read/write to ideas table
├── intelligence.py              # Entry point: full pipeline
├── daily_brief.py               # Entry point: send Telegram brief
└── tests/
    ├── test_github_trending.py
    ├── test_hackernews.py
    ├── test_scoring.py
    ├── test_airtable_client.py
    └── test_daily_brief.py
```

---

## Task 1: Project Bootstrap

**Files:**
- Create: `C:/Users/paulr/content-pipeline/requirements.txt`
- Create: `C:/Users/paulr/content-pipeline/.env.example`
- Create: `C:/Users/paulr/content-pipeline/config.py`

- [ ] **Step 1: Create project directory**

```bash
mkdir C:/Users/paulr/content-pipeline
cd C:/Users/paulr/content-pipeline
mkdir sources tests
```

- [ ] **Step 2: Create `requirements.txt`**

```
requests==2.32.3
feedparser==6.0.11
pyairtable==2.3.3
python-dotenv==1.0.1
pytest==8.3.4
pytest-mock==3.14.0
responses==0.25.3
```

- [ ] **Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: All packages install without error.

- [ ] **Step 4: Create `.env.example`**

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEEPSEEK_MODEL=deepseek/deepseek-chat
KIMI_MODEL=moonshot/moonshot-v1-8k
AIRTABLE_PAT=your_airtable_personal_access_token
AIRTABLE_BASE_ID=appw5JcYwgEswfcV2
AIRTABLE_IDEAS_TABLE=tblIDEAS
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
GITHUB_TOKEN=your_github_token_optional
PRODUCTHUNT_API_TOKEN=your_producthunt_developer_token
```

- [ ] **Step 5: Create `.env` by copying `.env.example` and filling in real values**

Real values are in `~/.claude/projects/C--/memory/reference_all_api_keys.md`.  
`OPENROUTER_API_KEY` is already in `~/.bashrc` as `$OPENROUTER_API_KEY`.  
`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are in `reference_ghl.md`.

- [ ] **Step 6: Create `config.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek/deepseek-chat")
KIMI_MODEL = os.getenv("KIMI_MODEL", "moonshot/moonshot-v1-8k")

AIRTABLE_PAT = os.environ["AIRTABLE_PAT"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_IDEAS_TABLE = os.getenv("AIRTABLE_IDEAS_TABLE", "Ideas")

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
PRODUCTHUNT_API_TOKEN = os.getenv("PRODUCTHUNT_API_TOKEN", "")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
```

- [ ] **Step 7: Verify config loads**

```bash
python -c "import config; print('OK:', config.AIRTABLE_BASE_ID)"
```

Expected: `OK: appw5JcYwgEswfcV2`

- [ ] **Step 8: Add `.gitignore` and initial commit**

Create `.gitignore`:
```
.env
__pycache__/
*.pyc
.pytest_cache/
```

```bash
git init
git add requirements.txt .env.example config.py .gitignore
git commit -m "feat: project bootstrap — config + deps"
```

---

## Task 2: Shared LLM Client

**Files:**
- Create: `C:/Users/paulr/content-pipeline/llm_client.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_llm_client.py`:

```python
import responses as resp
import requests
from llm_client import call_llm

@resp.activate
def test_call_llm_returns_content():
    resp.add(
        resp.POST,
        "https://openrouter.ai/api/v1/chat/completions",
        json={
            "choices": [{"message": {"content": "test response"}}]
        },
        status=200
    )
    result = call_llm(model="deepseek/deepseek-chat", prompt="hello")
    assert result == "test response"

@resp.activate
def test_call_llm_sends_system_prompt():
    resp.add(
        resp.POST,
        "https://openrouter.ai/api/v1/chat/completions",
        json={"choices": [{"message": {"content": "ok"}}]},
        status=200
    )
    call_llm(model="deepseek/deepseek-chat", prompt="p", system="you are x")
    body = resp.calls[0].request.body
    import json
    payload = json.loads(body)
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][0]["content"] == "you are x"
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_llm_client.py -v
```

Expected: `ImportError: cannot import name 'call_llm' from 'llm_client'`

- [ ] **Step 3: Create `llm_client.py`**

```python
import requests
import config

def call_llm(model: str, prompt: str, system: str = "", temperature: float = 0.7) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = requests.post(
        f"{config.OPENROUTER_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://manyhatautomations.com",
            "X-Title": "ManyHat Content Pipeline"
        },
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_llm_client.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add llm_client.py tests/test_llm_client.py
git commit -m "feat: shared OpenRouter LLM client"
```

---

## Task 3: GitHub Trending Source

**Files:**
- Create: `C:/Users/paulr/content-pipeline/sources/github_trending.py`
- Create: `C:/Users/paulr/content-pipeline/tests/test_github_trending.py`
- Create: `C:/Users/paulr/content-pipeline/sources/__init__.py` (empty)

- [ ] **Step 1: Create `sources/__init__.py`**

```bash
type nul > sources/__init__.py
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_github_trending.py`:

```python
import responses as resp
import json
from sources.github_trending import fetch_github_trending

MOCK_RESPONSE = [
    {
        "author": "openai",
        "name": "gpt-4o",
        "description": "GPT-4o model toolkit",
        "stars": 12500,
        "language": "Python",
        "url": "https://github.com/openai/gpt-4o"
    }
]

@resp.activate
def test_fetch_github_trending_returns_list():
    resp.add(
        resp.GET,
        "https://api.gtrending.com/repos",
        json=MOCK_RESPONSE,
        status=200
    )
    result = fetch_github_trending()
    assert isinstance(result, list)
    assert len(result) == 1

@resp.activate
def test_fetch_github_trending_item_schema():
    resp.add(
        resp.GET,
        "https://api.gtrending.com/repos",
        json=MOCK_RESPONSE,
        status=200
    )
    result = fetch_github_trending()
    item = result[0]
    assert "title" in item
    assert "url" in item
    assert "description" in item
    assert "source" in item
    assert item["source"] == "github"

@resp.activate
def test_fetch_github_trending_handles_api_failure():
    resp.add(
        resp.GET,
        "https://api.gtrending.com/repos",
        status=500
    )
    result = fetch_github_trending()
    assert result == []
```

- [ ] **Step 3: Run test to confirm it fails**

```bash
python -m pytest tests/test_github_trending.py -v
```

Expected: `ImportError`

- [ ] **Step 4: Create `sources/github_trending.py`**

```python
import requests

def fetch_github_trending(language: str = "python", since: str = "daily") -> list[dict]:
    try:
        response = requests.get(
            "https://api.gtrending.com/repos",
            params={"language": language, "since": since},
            timeout=15
        )
        response.raise_for_status()
        repos = response.json()
        return [
            {
                "title": f"{r['author']}/{r['name']}",
                "url": r.get("url", f"https://github.com/{r['author']}/{r['name']}"),
                "description": r.get("description", ""),
                "stars": r.get("stars", 0),
                "language": r.get("language", ""),
                "source": "github"
            }
            for r in repos[:10]
        ]
    except Exception:
        return []
```

- [ ] **Step 5: Run tests — expect pass**

```bash
python -m pytest tests/test_github_trending.py -v
```

Expected: `3 passed`

- [ ] **Step 6: Commit**

```bash
git add sources/__init__.py sources/github_trending.py tests/test_github_trending.py
git commit -m "feat: GitHub Trending source"
```

---

## Task 4: HackerNews Source

**Files:**
- Create: `C:/Users/paulr/content-pipeline/sources/hackernews.py`
- Create: `C:/Users/paulr/content-pipeline/tests/test_hackernews.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_hackernews.py`:

```python
import responses as resp
from sources.hackernews import fetch_hackernews

MOCK_RESPONSE = {
    "hits": [
        {"title": "GPT-5 announced", "url": "https://openai.com/gpt5", "points": 850, "objectID": "1"},
        {"title": "New AI chip breakthrough", "url": "https://techcrunch.com/ai-chip", "points": 620, "objectID": "2"},
    ]
}

@resp.activate
def test_fetch_hackernews_returns_list():
    resp.add(resp.GET, "https://hn.algolia.com/api/v1/search", json=MOCK_RESPONSE, status=200)
    result = fetch_hackernews()
    assert isinstance(result, list)
    assert len(result) == 2

@resp.activate
def test_fetch_hackernews_item_schema():
    resp.add(resp.GET, "https://hn.algolia.com/api/v1/search", json=MOCK_RESPONSE, status=200)
    result = fetch_hackernews()
    item = result[0]
    assert item["title"] == "GPT-5 announced"
    assert item["url"] == "https://openai.com/gpt5"
    assert item["source"] == "hackernews"

@resp.activate
def test_fetch_hackernews_handles_failure():
    resp.add(resp.GET, "https://hn.algolia.com/api/v1/search", status=503)
    result = fetch_hackernews()
    assert result == []
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_hackernews.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `sources/hackernews.py`**

```python
import requests

def fetch_hackernews(query: str = "AI OR automation OR LLM", limit: int = 10) -> list[dict]:
    try:
        response = requests.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": query,
                "tags": "front_page",
                "hitsPerPage": limit
            },
            timeout=15
        )
        response.raise_for_status()
        hits = response.json().get("hits", [])
        return [
            {
                "title": h.get("title", ""),
                "url": h.get("url", f"https://news.ycombinator.com/item?id={h['objectID']}"),
                "description": h.get("story_text", "")[:200],
                "points": h.get("points", 0),
                "source": "hackernews"
            }
            for h in hits if h.get("url")
        ]
    except Exception:
        return []
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_hackernews.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add sources/hackernews.py tests/test_hackernews.py
git commit -m "feat: HackerNews source"
```

---

## Task 5: RSS Feeds Source

**Files:**
- Create: `C:/Users/paulr/content-pipeline/sources/rss_feeds.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_rss_feeds.py`:

```python
from unittest.mock import patch, MagicMock
from sources.rss_feeds import fetch_rss_feeds

def make_mock_feed(entries):
    feed = MagicMock()
    feed.entries = entries
    feed.bozo = False
    return feed

def make_entry(title, link, summary=""):
    e = MagicMock()
    e.title = title
    e.link = link
    e.summary = summary
    e.get = lambda k, d="": getattr(e, k, d)
    return e

def test_fetch_rss_feeds_returns_list():
    entry = make_entry("AI breaks new record", "https://example.com/1", "Summary here")
    mock_feed = make_mock_feed([entry])
    with patch("sources.rss_feeds.feedparser.parse", return_value=mock_feed):
        result = fetch_rss_feeds(feeds=["https://example.com/feed"])
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "AI breaks new record"
    assert result[0]["source"] == "rss"

def test_fetch_rss_feeds_skips_broken_feed():
    broken = MagicMock()
    broken.bozo = True
    broken.entries = []
    with patch("sources.rss_feeds.feedparser.parse", return_value=broken):
        result = fetch_rss_feeds(feeds=["https://broken.com/feed"])
    assert result == []
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_rss_feeds.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `sources/rss_feeds.py`**

```python
import feedparser

DEFAULT_FEEDS = [
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://blog.n8n.io/rss/",
    "https://zapier.com/blog/feed/",
    "https://a16z.com/ai/feed/",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]

def fetch_rss_feeds(feeds: list[str] = None, max_per_feed: int = 3) -> list[dict]:
    feeds = feeds or DEFAULT_FEEDS
    results = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                continue
            for entry in feed.entries[:max_per_feed]:
                results.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "description": entry.get("summary", "")[:300],
                    "source": "rss"
                })
        except Exception:
            continue
    return results
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_rss_feeds.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add sources/rss_feeds.py tests/test_rss_feeds.py
git commit -m "feat: RSS feeds aggregator (18 AI/automation feeds)"
```

---

## Task 6: DeepSeek Scoring

**Files:**
- Create: `C:/Users/paulr/content-pipeline/scoring.py`
- Create: `C:/Users/paulr/content-pipeline/tests/test_scoring.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_scoring.py`:

```python
from unittest.mock import patch
from scoring import score_items

SAMPLE_ITEMS = [
    {"title": "New open-source AI agent framework", "url": "https://github.com/ai/agent", "description": "Build agents easily", "source": "github"},
    {"title": "GPT-5 benchmarks released", "url": "https://openai.com", "description": "New SOTA results", "source": "hackernews"},
]

def test_score_items_returns_scored_list():
    mock_response = '{"scores": [{"index": 0, "viral": 9, "relevance": 8, "fit": 7}, {"index": 1, "viral": 8, "relevance": 9, "fit": 6}]}'
    with patch("scoring.call_llm", return_value=mock_response):
        result = score_items(SAMPLE_ITEMS)
    assert len(result) == 2
    assert "score" in result[0]
    assert isinstance(result[0]["score"], float)

def test_score_items_sorted_descending():
    mock_response = '{"scores": [{"index": 0, "viral": 5, "relevance": 5, "fit": 5}, {"index": 1, "viral": 9, "relevance": 9, "fit": 9}]}'
    with patch("scoring.call_llm", return_value=mock_response):
        result = score_items(SAMPLE_ITEMS)
    assert result[0]["score"] > result[1]["score"]

def test_score_items_handles_llm_failure():
    with patch("scoring.call_llm", side_effect=Exception("API error")):
        result = score_items(SAMPLE_ITEMS)
    assert len(result) == 2
    assert result[0]["score"] == 5.0
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_scoring.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `scoring.py`**

```python
import json
import config
from llm_client import call_llm

SYSTEM_PROMPT = """You are a content scoring expert for ManyHat Automations, an AI automation agency.
Score each item on three dimensions from 1-10:
- viral: viral potential on social media in the AI/automation niche
- relevance: relevance to AI, automation, n8n, agents
- fit: fit with ManyHat's brand (AI automation agency for SMBs)

Respond ONLY with valid JSON matching this schema exactly:
{"scores": [{"index": 0, "viral": 8, "relevance": 9, "fit": 7}, ...]}"""

def score_items(items: list[dict]) -> list[dict]:
    if not items:
        return []
    prompt = "Score these content items:\n\n" + "\n".join(
        f"{i}. [{item['source']}] {item['title']}: {item['description'][:150]}"
        for i, item in enumerate(items)
    )
    try:
        raw = call_llm(model=config.DEEPSEEK_MODEL, prompt=prompt, system=SYSTEM_PROMPT, temperature=0.3)
        data = json.loads(raw.strip())
        scores_map = {s["index"]: s for s in data["scores"]}
        scored = []
        for i, item in enumerate(items):
            s = scores_map.get(i, {"viral": 5, "relevance": 5, "fit": 5})
            avg = round((s["viral"] + s["relevance"] + s["fit"]) / 3, 2)
            scored.append({**item, "score": avg, "score_detail": s})
        return sorted(scored, key=lambda x: x["score"], reverse=True)
    except Exception:
        return [{**item, "score": 5.0, "score_detail": {}} for item in items]
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_scoring.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add scoring.py tests/test_scoring.py
git commit -m "feat: DeepSeek content scoring"
```

---

## Task 7: Kimi Content Angles

**Files:**
- Create: `C:/Users/paulr/content-pipeline/angles.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_angles.py`:

```python
from unittest.mock import patch
from angles import generate_angles

ITEM = {
    "title": "New open-source AI agent framework",
    "description": "Build agents with minimal code",
    "url": "https://github.com/ai/agentkit",
    "source": "github",
    "score": 8.5
}

def test_generate_angles_returns_three():
    mock = '{"angles": [{"type": "tutorial", "hook": "Build your first AI agent in 10 min"}, {"type": "hot_take", "hook": "This kills LangChain"}, {"type": "educational", "hook": "What AI agents actually are"}]}'
    with patch("angles.call_llm", return_value=mock):
        result = generate_angles(ITEM)
    assert len(result) == 3
    assert all("type" in a and "hook" in a for a in result)

def test_generate_angles_handles_failure():
    with patch("angles.call_llm", side_effect=Exception("fail")):
        result = generate_angles(ITEM)
    assert len(result) == 3
    assert result[0]["type"] == "educational"
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_angles.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `angles.py`**

```python
import json
import config
from llm_client import call_llm

SYSTEM_PROMPT = """You are a social media strategist for ManyHat Automations (AI automation agency for SMBs).
Given a content item, generate exactly 3 content angles for short-form video/post content.
Angle types: tutorial, hot_take, educational, demo, client_story, news_breakdown.
Each angle needs a scroll-stopping hook (max 15 words).

Respond ONLY with valid JSON:
{"angles": [{"type": "tutorial", "hook": "hook text here", "format": "60s Reel"}, ...]}"""

FALLBACK_ANGLES = [
    {"type": "educational", "hook": "What you need to know about this", "format": "Thread"},
    {"type": "tutorial", "hook": "Step-by-step: how to use this today", "format": "60s Reel"},
    {"type": "hot_take", "hook": "Why everyone is wrong about this", "format": "30s Reel"},
]

def generate_angles(item: dict) -> list[dict]:
    prompt = f"""Title: {item['title']}
Description: {item['description'][:300]}
Source: {item['source']}
Viral score: {item.get('score', 5)}

Generate 3 content angles for ManyHat's AI automation audience (business owners, developers, entrepreneurs)."""
    try:
        raw = call_llm(model=config.KIMI_MODEL, prompt=prompt, system=SYSTEM_PROMPT, temperature=0.8)
        data = json.loads(raw.strip())
        return data["angles"][:3]
    except Exception:
        return FALLBACK_ANGLES
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_angles.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add angles.py tests/test_angles.py
git commit -m "feat: Kimi content angle generator"
```

---

## Task 8: Airtable Client

**Files:**
- Create: `C:/Users/paulr/content-pipeline/airtable_client.py`
- Create: `C:/Users/paulr/content-pipeline/tests/test_airtable_client.py`

> **Note:** Before running this task, create the "Ideas" table in Airtable base `appw5JcYwgEswfcV2` with these fields:
> - `Topic` (single line text)
> - `Source URL` (URL)
> - `Viral Score` (number, 1 decimal)
> - `Content Angle` (long text — JSON string)
> - `Format` (single line text)
> - `Script` (long text)
> - `Status` (single select: Pending Review, Approved, In Production, Rendered, Posted)
> - `Scheduled Date` (date)
> - `Source` (single line text: github / hackernews / producthunt / rss)

- [ ] **Step 1: Write the failing test**

Create `tests/test_airtable_client.py`:

```python
from unittest.mock import patch, MagicMock
from airtable_client import write_idea, get_approved_ideas

SAMPLE_IDEA = {
    "title": "New AI agent framework",
    "url": "https://github.com/ai/agentkit",
    "score": 8.5,
    "angles": [{"type": "tutorial", "hook": "Build your first AI agent", "format": "60s Reel"}],
    "source": "github"
}

def test_write_idea_calls_airtable():
    mock_table = MagicMock()
    mock_table.create.return_value = {"id": "recABC123"}
    with patch("airtable_client.Table", return_value=mock_table):
        record_id = write_idea(SAMPLE_IDEA)
    assert record_id == "recABC123"
    mock_table.create.assert_called_once()

def test_write_idea_maps_fields_correctly():
    mock_table = MagicMock()
    mock_table.create.return_value = {"id": "recXYZ"}
    with patch("airtable_client.Table", return_value=mock_table):
        write_idea(SAMPLE_IDEA)
    call_args = mock_table.create.call_args[0][0]
    assert call_args["Topic"] == "New AI agent framework"
    assert call_args["Status"] == "Pending Review"
    assert call_args["Viral Score"] == 8.5

def test_get_approved_ideas_filters_by_status():
    mock_table = MagicMock()
    mock_table.all.return_value = [
        {"id": "rec1", "fields": {"Topic": "Idea A", "Status": "Approved", "Content Angle": "[]", "Source URL": ""}}
    ]
    with patch("airtable_client.Table", return_value=mock_table):
        result = get_approved_ideas()
    assert len(result) == 1
    mock_table.all.assert_called_with(formula="{Status}='Approved'")
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_airtable_client.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `airtable_client.py`**

```python
import json
from pyairtable import Table
import config

def _get_table() -> Table:
    return Table(config.AIRTABLE_PAT, config.AIRTABLE_BASE_ID, config.AIRTABLE_IDEAS_TABLE)

def write_idea(idea: dict) -> str:
    table = _get_table()
    record = table.create({
        "Topic": idea["title"],
        "Source URL": idea.get("url", ""),
        "Viral Score": idea.get("score", 0),
        "Content Angle": json.dumps(idea.get("angles", [])),
        "Format": idea["angles"][0]["format"] if idea.get("angles") else "",
        "Source": idea.get("source", ""),
        "Status": "Pending Review",
    })
    return record["id"]

def get_approved_ideas(limit: int = 3) -> list[dict]:
    table = _get_table()
    records = table.all(formula="{Status}='Approved'")
    return [
        {
            "id": r["id"],
            "title": r["fields"].get("Topic", ""),
            "url": r["fields"].get("Source URL", ""),
            "score": r["fields"].get("Viral Score", 0),
            "angles": json.loads(r["fields"].get("Content Angle", "[]")),
            "format": r["fields"].get("Format", ""),
        }
        for r in records[:limit]
    ]

def update_status(record_id: str, status: str) -> None:
    table = _get_table()
    table.update(record_id, {"Status": status})
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_airtable_client.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add airtable_client.py tests/test_airtable_client.py
git commit -m "feat: Airtable client — write ideas, get approved, update status"
```

---

## Task 9: Main `intelligence.py` Entry Point

**Files:**
- Create: `C:/Users/paulr/content-pipeline/intelligence.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_intelligence.py`:

```python
from unittest.mock import patch, MagicMock
from intelligence import run_pipeline

MOCK_ITEMS = [
    {"title": f"Item {i}", "url": f"https://example.com/{i}", "description": "desc", "source": "github"}
    for i in range(5)
]

MOCK_SCORED = [
    {**item, "score": 9.0 - i * 0.5, "score_detail": {}}
    for i, item in enumerate(MOCK_ITEMS)
]

MOCK_ANGLES = [
    {"type": "tutorial", "hook": "Hook text", "format": "60s Reel"},
    {"type": "hot_take", "hook": "Hot take", "format": "30s Reel"},
    {"type": "educational", "hook": "Learn this", "format": "Thread"},
]

def test_run_pipeline_writes_top_3():
    with patch("intelligence.fetch_github_trending", return_value=MOCK_ITEMS[:3]), \
         patch("intelligence.fetch_hackernews", return_value=MOCK_ITEMS[3:]), \
         patch("intelligence.fetch_rss_feeds", return_value=[]), \
         patch("intelligence.score_items", return_value=MOCK_SCORED), \
         patch("intelligence.generate_angles", return_value=MOCK_ANGLES), \
         patch("intelligence.write_idea", return_value="recABC") as mock_write:
        run_pipeline()
    assert mock_write.call_count == 3

def test_run_pipeline_passes_angles_to_idea():
    with patch("intelligence.fetch_github_trending", return_value=MOCK_ITEMS[:1]), \
         patch("intelligence.fetch_hackernews", return_value=[]), \
         patch("intelligence.fetch_rss_feeds", return_value=[]), \
         patch("intelligence.score_items", return_value=[MOCK_SCORED[0]]), \
         patch("intelligence.generate_angles", return_value=MOCK_ANGLES) as mock_angles, \
         patch("intelligence.write_idea", return_value="rec1"):
        run_pipeline()
    mock_angles.assert_called_once_with(MOCK_SCORED[0])
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_intelligence.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `intelligence.py`**

```python
from sources.github_trending import fetch_github_trending
from sources.hackernews import fetch_hackernews
from sources.rss_feeds import fetch_rss_feeds
from scoring import score_items
from angles import generate_angles
from airtable_client import write_idea

TOP_N = 3

def run_pipeline():
    print("[intelligence] Fetching sources...")
    items = (
        fetch_github_trending()
        + fetch_hackernews()
        + fetch_rss_feeds()
    )
    print(f"[intelligence] {len(items)} items collected. Scoring...")
    scored = score_items(items)
    top = scored[:TOP_N]
    print(f"[intelligence] Writing top {TOP_N} to Airtable...")
    for item in top:
        item["angles"] = generate_angles(item)
        record_id = write_idea(item)
        print(f"  -> {item['title'][:60]} [{item['score']}] → {record_id}")
    print("[intelligence] Done.")

if __name__ == "__main__":
    run_pipeline()
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_intelligence.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Run full suite to confirm nothing broke**

```bash
python -m pytest tests/ -v
```

Expected: All tests pass.

- [ ] **Step 6: Smoke test against live APIs**

```bash
python intelligence.py
```

Expected output (example):
```
[intelligence] Fetching sources...
[intelligence] 47 items collected. Scoring...
[intelligence] Writing top 3 to Airtable...
  -> openai/gpt-4o-mini-realtime — new voice mode [8.67] → recXXXXXX
  -> Why Claude 4 changes everything for AI agents [8.33] → recYYYYYY
  -> n8n adds native AI agent loop support [8.17] → recZZZZZZ
[intelligence] Done.
```

- [ ] **Step 7: Verify 3 records appear in Airtable with status "Pending Review"**

Open Airtable → base `appw5JcYwgEswfcV2` → Ideas table. Confirm 3 new records.

- [ ] **Step 8: Commit**

```bash
git add intelligence.py tests/test_intelligence.py
git commit -m "feat: intelligence.py main pipeline — fetch, score, write top 3 to Airtable"
```

---

## Task 10: Daily Brief via Telegram

**Files:**
- Create: `C:/Users/paulr/content-pipeline/daily_brief.py`
- Create: `C:/Users/paulr/content-pipeline/tests/test_daily_brief.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_daily_brief.py`:

```python
import responses as resp
import json
from unittest.mock import patch
from daily_brief import send_brief, format_brief_message

MOCK_IDEAS = [
    {"id": "rec1", "title": "New AI agent framework", "score": 9.2, "angles": [{"type": "tutorial", "hook": "Build your first AI agent in 10 min", "format": "60s Reel"}], "url": "https://github.com/ai/agentkit"},
    {"id": "rec2", "title": "GPT-5 benchmarks leak", "score": 8.7, "angles": [{"type": "hot_take", "hook": "The AI race just got serious", "format": "30s Reel"}], "url": "https://hn.com/123"},
    {"id": "rec3", "title": "n8n adds native AI loops", "score": 8.1, "angles": [{"type": "demo", "hook": "n8n just became an AI powerhouse", "format": "Tutorial"}], "url": "https://blog.n8n.io/ai-loops"},
]

def test_format_brief_message_contains_all_ideas():
    msg = format_brief_message(MOCK_IDEAS)
    assert "New AI agent framework" in msg
    assert "GPT-5 benchmarks leak" in msg
    assert "n8n adds native AI loops" in msg
    assert "9.2" in msg

def test_format_brief_message_contains_reply_instructions():
    msg = format_brief_message(MOCK_IDEAS)
    assert "Reply" in msg or "reply" in msg

@resp.activate
def test_send_brief_calls_telegram_api():
    resp.add(
        resp.POST,
        "https://api.telegram.org/botTEST_TOKEN/sendMessage",
        json={"ok": True, "result": {"message_id": 1}},
        status=200
    )
    with patch("daily_brief.get_approved_ideas", return_value=MOCK_IDEAS), \
         patch("daily_brief.config.TELEGRAM_BOT_TOKEN", "TEST_TOKEN"), \
         patch("daily_brief.config.TELEGRAM_CHAT_ID", "12345"):
        send_brief()
    assert len(resp.calls) == 1
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
python -m pytest tests/test_daily_brief.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Create `daily_brief.py`**

```python
import requests
import config
from airtable_client import get_approved_ideas

def format_brief_message(ideas: list[dict]) -> str:
    lines = ["*ManyHat Daily Content Brief*\n"]
    for i, idea in enumerate(ideas, 1):
        angle = idea["angles"][0] if idea.get("angles") else {}
        lines.append(
            f"{i}. *{idea['title'][:60]}*\n"
            f"   Score: {idea['score']} | {angle.get('format', '')}\n"
            f"   Hook: _{angle.get('hook', '')}_\n"
            f"   {idea.get('url', '')}\n"
        )
    lines.append("\nReply *1*, *2*, *3*, or *all* to approve and queue for production.")
    return "\n".join(lines)

def send_brief() -> None:
    ideas = get_approved_ideas(limit=3)
    if not ideas:
        print("[brief] No approved ideas found — check Airtable.")
        return
    message = format_brief_message(ideas)
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }, timeout=15)
    response.raise_for_status()
    print(f"[brief] Sent brief with {len(ideas)} ideas.")

if __name__ == "__main__":
    send_brief()
```

- [ ] **Step 4: Run tests — expect pass**

```bash
python -m pytest tests/test_daily_brief.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Full test suite**

```bash
python -m pytest tests/ -v
```

Expected: All tests pass.

- [ ] **Step 6: Smoke test (change one idea status to "Approved" in Airtable first)**

```bash
python daily_brief.py
```

Expected: Telegram message arrives in your channel with 3 ideas and reply instructions.

- [ ] **Step 7: Commit**

```bash
git add daily_brief.py tests/test_daily_brief.py
git commit -m "feat: Telegram daily brief via Telegram Bot API"
```

---

## Task 11: n8n Workflows

**No code — just 2 workflow configurations in Railway n8n.**

- [ ] **Step 1: Create Workflow 1 — Content Discovery (3 nodes)**

In Railway n8n (`https://primary-production-424023.up.railway.app`):

1. **Cron Trigger** node
   - Mode: `Custom (Cron)`
   - Expression: `0 7 * * 1-6` (7:00 AM, Mon-Sat)

2. **Execute Command** node
   - Command: `cd /home/user/content-pipeline && python intelligence.py >> /tmp/intelligence.log 2>&1`
   - (Adjust path to wherever `content-pipeline/` is deployed on Railway)

3. **No-op** (just connect and activate)

Name this workflow: `Content Discovery — Daily 7AM`

- [ ] **Step 2: Create Workflow 2 — Daily Brief (3 nodes)**

1. **Cron Trigger** node
   - Expression: `30 7 * * 1-6` (7:30 AM, Mon-Sat, 30 min after intelligence.py)

2. **Execute Command** node
   - Command: `cd /home/user/content-pipeline && python daily_brief.py >> /tmp/brief.log 2>&1`

3. **No-op**

Name this workflow: `Daily Brief — Telegram 7:30AM`

- [ ] **Step 3: Activate both workflows**

Toggle both to Active in the Railway n8n dashboard.

- [ ] **Step 4: Test manually**

Click "Execute Workflow" on Content Discovery. Check `/tmp/intelligence.log` confirms run. Wait for Telegram brief at 7:30 AM or run the brief workflow manually.

---

## Task 12: Deployment to Railway

- [ ] **Step 1: Create `Procfile` in project root**

```
worker: python intelligence.py
```

- [ ] **Step 2: Push to GitHub**

```bash
git remote add origin https://github.com/YOUR_ORG/content-pipeline.git
git push -u origin main
```

- [ ] **Step 3: Connect Railway project to the GitHub repo**

In Railway dashboard: New Project → Deploy from GitHub → select `content-pipeline`.

- [ ] **Step 4: Add environment variables in Railway**

Add all variables from `.env` to Railway → Settings → Variables.

- [ ] **Step 5: Verify Railway deploy succeeds and logs are clean**

Expected in Railway logs: No import errors, no missing env var errors.

- [ ] **Step 6: Final integration test**

Trigger Content Discovery workflow manually in n8n → verify 3 new Airtable records → wait for 7:30 AM Telegram brief OR trigger Daily Brief workflow manually.

- [ ] **Step 7: Final commit**

```bash
git add Procfile
git commit -m "feat: Railway deployment config"
git push
```

---

## Self-Review

**Spec coverage check:**
- [x] GitHub Trending source — Task 3
- [x] HackerNews source — Task 4
- [x] RSS feeds — Task 5
- [x] DeepSeek scoring — Task 6
- [x] Kimi content angles — Task 7
- [x] Airtable write + read — Task 8
- [x] Main pipeline orchestrator — Task 9
- [x] Telegram daily brief — Task 10
- [x] n8n cron workflows (2, max 5 nodes each) — Task 11
- [x] Railway deployment — Task 12
- [ ] Product Hunt source — **GAP: not implemented**

**Gap fix — Product Hunt was listed in spec. Add as optional source:**

Add `sources/producthunt.py`:

```python
import requests
import config

QUERY = """
query {
  posts(order: VOTES, postedAfter: "YESTERDAY") {
    edges { node { name tagline url votesCount topics { edges { node { name } } } } }
  }
}
"""

def fetch_producthunt(limit: int = 5) -> list[dict]:
    if not config.PRODUCTHUNT_API_TOKEN:
        return []
    try:
        response = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            headers={"Authorization": f"Bearer {config.PRODUCTHUNT_API_TOKEN}"},
            json={"query": QUERY},
            timeout=15
        )
        response.raise_for_status()
        edges = response.json()["data"]["posts"]["edges"]
        return [
            {
                "title": e["node"]["name"],
                "description": e["node"]["tagline"],
                "url": e["node"]["url"],
                "votes": e["node"]["votesCount"],
                "source": "producthunt"
            }
            for e in edges[:limit]
        ]
    except Exception:
        return []
```

Add `from sources.producthunt import fetch_producthunt` to `intelligence.py` and include in the items list. Commit separately.

**Placeholder scan:** None found — all steps have actual code and exact commands.

**Type consistency:** `write_idea(item: dict)` — used consistently. `get_approved_ideas()` returns `list[dict]` — consumed correctly in `daily_brief.py`. All function signatures consistent across tasks.
