# AI & Bollywood News Bot

Automated news aggregator that fetches AI/tech and Bollywood news, scores for virality, generates digest posts using Gemini AI, routes through human review, and publishes to Telegram channels.

---

## What It Does

1. **Fetches** articles from 30+ RSS sources every 6 hours (or scrapes Drik Panchang for astrology)
2. **Filters** off-topic and unsafe content via guardrails
3. **Scores** articles by recency, source credibility, and cross-source overlap — with source weight multipliers (official AI blogs score higher than community aggregators)
4. **Selects** top 5 articles applying diversity caps: max 2 per source, max 2 per movie/topic, no duplicate titles
5. **Generates** a daily digest post using Gemini 2.5 Pro + a cover image, with clickable **Read more** links for each story
6. **Sends** the post to your private Telegram reviewer chat with ✅ Approve / ❌ Reject buttons
7. **Publishes** to the correct channel immediately after you tap Approve

---

## Bots

| Bot | Channel | Language | Posts/Day | Status |
|-----|---------|----------|-----------|--------|
| AI News Bot | `@ai26news` | English | 1 digest (top 5) | Active |
| Bollywood Buzz Bot | `@bollywood_daily_gossip` | Hindi/Hinglish | 2 digests (top 5 each) | Active |
| Daily Astrology Bot | `@astrochhayah` | Hindi/Hinglish | 1 panchang post | Built, inactive |

Each bot uses its **own Telegram token** for publishing and for the review flow — tapping Approve on a Bollywood post always routes to the Bollywood bot.

Each bot can also send review messages to a **different Telegram account** via per-bot reviewer chat IDs.

---

## Prerequisites

- Python 3.10+
- A Telegram bot token for each active bot (from [@BotFather](https://t.me/BotFather))
- An Euri API key — free at [euron.one](https://euron.one), 200K tokens/day

---

## Setup

### 1. Clone and install dependencies

```bash
cd "AI News"
pip install -r requirements.txt
```

### 2. Create your `.env` file

```bash
cp .env.example .env
```

Fill in `.env`:

```env
# Euri AI (text + image generation via Gemini)
EURI_API_KEY=your_euri_api_key_here

# Telegram — AI News Bot
TELEGRAM_AI_BOT_TOKEN=your_ai_bot_token_here
TELEGRAM_AI_CHANNEL_ID=@your_ai_channel

# Telegram — Bollywood Buzz Bot
TELEGRAM_BOLLYWOOD_BOT_TOKEN=your_bollywood_bot_token_here
TELEGRAM_BOLLYWOOD_CHANNEL_ID=@your_bollywood_channel

# Telegram — Daily Astrology Bot
TELEGRAM_ASTROLOGY_BOT_TOKEN=your_astrology_bot_token_here
TELEGRAM_ASTROLOGY_CHANNEL_ID=@your_astrology_channel

# Telegram — Reviewer (default: used by AI News + Bollywood)
TELEGRAM_REVIEWER_CHAT_ID=123456789   # numeric ID only, not @username

# Telegram — Reviewer override for Astrology (optional — different account)
TELEGRAM_ASTROLOGY_REVIEWER_CHAT_ID=987654321
```

> **How to get your reviewer chat ID:** Search for `@userinfobot` on Telegram and send it any message — it replies with your numeric chat ID.

> **Per-bot reviewer:** If you want astrology posts reviewed from a different Telegram account, set `TELEGRAM_ASTROLOGY_REVIEWER_CHAT_ID`. Leave it blank to use the same account as AI News and Bollywood.

### 3. Add bots as channel admins

Each bot must be an admin of its Telegram channel before it can post:
1. Open your channel settings → Administrators
2. Add the bot by its username
3. Grant **Post Messages** permission

### 4. Verify connection

```bash
python test_euri_connection.py
```

---

## Running the Bot

### Option A — Full automated scheduler (production)

Runs all pipeline jobs on a schedule (fetch at 6 AM IST, review at 7 AM, publish at 8 AM):

```bash
python main.py
```

### Option B — Manual test run (development)

Generates a fresh post for a specific bot, sends it to your reviewer chat, and waits for your Approve/Reject:

```bash
python publisher/test_review_interface.py ai_news
python publisher/test_review_interface.py bollywood
python publisher/test_review_interface.py astrology
```

To run both news bots simultaneously (stagger by 8+ seconds to avoid Telegram conflicts):

```bash
python publisher/test_review_interface.py ai_news > logs/test_ai_news.log 2>&1 &
sleep 8
python publisher/test_review_interface.py bollywood > logs/test_bollywood.log 2>&1 &
```

---

## Individual Pipeline Scripts

| Script | What it does |
|--------|-------------|
| `python aggregator/test_fetch.py ai_news` | Fetch + save articles for AI News |
| `python aggregator/test_fetch.py bollywood` | Fetch + save articles for Bollywood |
| `python generator/test_generator.py` | Generate a post from the top scored article |
| `python publisher/test_review_interface.py ai_news` | Full flow for AI News: generate → review → publish |
| `python publisher/test_review_interface.py bollywood` | Full flow for Bollywood |
| `python publisher/test_review_interface.py astrology` | Full flow for Astrology: fetch panchang → generate → review → publish |

---

## Review Commands

Once the review bot is running, send these commands in your Telegram reviewer chat:

| Command | Action |
|---------|--------|
| `/generate` | Generate a new post for the current bot on demand |
| `/generate bollywood` | Generate for a specific bot (ai_news / bollywood / astrology) |
| `/pending` | List all posts waiting for review |
| `/preview 5` | Show full content of post #5 |
| `/sources 5` | Show the source article used for post #5 |
| `/skip 5` | Skip post #5 (no publish) |
| `/help` | Show all commands |

You can also tap the **✅ Approve** / **❌ Reject** inline buttons sent with each post.

**On Approve** → post is published to the bot's channel immediately.  
**On Reject** → bot asks you to type a reason, then marks it rejected.

---

## Digest Post Format

### AI News (English)
```
📰 AI News Daily — April 04, 2026

1️⃣  Headline for story one
    What happened + why it matters (2-3 sentences)
    📌 TechCrunch  |  🔗 Read more

2️⃣ ... (5 stories total)

🔍 Trend Insight
   What today's stories have in common / where AI is heading

#AINews #TechUpdate #ArtificialIntelligence
```

### Bollywood (Hindi/Hinglish)
```
🎬 Bollywood Buzz Daily — April 04, 2026
Aaj ki sabse hot Bollywood khabrein 🌟

1️⃣  Catchy Hinglish headline 🎬
    Kya hua + kyun interesting hai (2-3 sentences)
    📌 Pinkvilla  |  🔗 Read more

2️⃣ ... (5 stories total)

🔥 Top Trending Gossip
   Today's most viral story in 2-3 lines

#Bollywood #BollywoodNews #Entertainment
```

### Daily Astrology (Hindi/Hinglish)
```
🌙 Aaj ka Tithi: Dwitiya | Shukla Paksha
  Rohini Nakshatra • Saubhagya Yoga

🔮 Meaning:
[3-4 lines on spiritual significance, deity, cosmic energy, nakshatra]

💡 Daily Insight:
[3-4 lines on career, relationships, health, finance]

🪔 Remedy:
[3-4 lines — what to do, why it works, exact steps]

✨ Tip of the Day:
[2-3 lines — actionable, connected to tithi energy]

#DailyPanchang #AajKaTithi #HinduCalendar #Astrology
```
Data scraped from Drik Panchang daily. Falls back to date string if scraping fails — Gemini calculates the tithi from the date.

---

## Project Structure

```
AI News/
├── aggregator/
│   ├── rss_fetcher.py          # Fetches articles from RSS feeds
│   ├── panchang_fetcher.py     # Scrapes Drik Panchang for daily tithi/nakshatra
│   └── dedup.py                # Hash-based deduplication
├── scoring/
│   ├── virality.py             # Scoring engine + source weights + diversity caps
│   └── fallback.py             # Best-available selection when threshold not met
├── guardrails/
│   ├── content_filter.py       # Pre/post generation safety checks
│   ├── keyword_blocklist.py    # Blocked keyword categories
│   └── source_whitelist.py     # Trusted source registry
├── generator/
│   ├── claude_client.py        # Euri/Gemini API wrapper + Read more URL injection
│   ├── prompts_ai_news.py      # Digest templates for AI News Bot
│   ├── prompts_bollywood.py    # Digest templates for Bollywood Bot
│   └── prompts_astrology.py    # Templates for Astrology Bot (Hinglish panchang post)
├── publisher/
│   ├── telegram_bot.py         # Publishes posts + Markdown→HTML converter
│   ├── review_interface.py     # Review bot (Approve/Reject + /generate command)
│   └── test_review_interface.py
├── scheduler/
│   └── jobs.py                 # APScheduler jobs, IST timezone
├── db/
│   ├── database.py             # SQLite session management
│   └── models.py               # Article, Post, PublishLog models
├── config/
│   ├── bots.json               # Master bot registry
│   ├── sources_ai.json         # AI/tech sources (with category + weight)
│   ├── sources_bollywood.json  # Bollywood sources (17 sources, 4 groups)
│   ├── sources_astrology.json  # Astrology reference sources (6 sources)
│   ├── keywords.json           # Trending + blocked keywords
│   └── settings.py             # Global config
├── logs/
│   ├── app.log
│   ├── guardrail_violations.log
│   └── publish_history.log
├── .claude/
│   ├── rules/                  # Detailed rules (content, scoring, guardrails, etc.)
│   └── skills/                 # Reusable patterns and lessons learned
├── .env.example
├── requirements.txt
├── CLAUDE.md                   # Project index and architecture
└── main.py
```

---

## Adding a New Bot

1. Add an entry to `config/bots.json` (follow the existing schema, add `"digest_count": 5`)
2. Create `config/sources_<id>.json` with trusted RSS sources
3. Create `generator/prompts_<id>.py` with `SYSTEM_PROMPT`, `build_digest_prompt()`, `build_digest_image_prompt()`
4. Add `TELEGRAM_<ID_UPPERCASE>_BOT_TOKEN` and `TELEGRAM_<ID_UPPERCASE>_CHANNEL_ID` to `.env`
5. Optionally add `TELEGRAM_<ID_UPPERCASE>_REVIEWER_CHAT_ID` if reviews should go to a different Telegram account
6. Add the token to `_get_bot_token()` in `publisher/review_interface.py` and `BOT_CONFIG_MAP` in `publisher/telegram_bot.py`
7. If using a custom reviewer chat ID, add it to `_get_reviewer_chat_id()` in `publisher/review_interface.py`
8. Set `"active": true` in `bots.json` and restart

No changes to the core pipeline needed.

---

## Schedule (IST)

| Time | Action |
|------|--------|
| 6:00 AM | Fetch panchang (Astrology) + score articles (AI News + Bollywood) |
| 6:00 AM | Astrology panchang post generated + sent to reviewer |
| 7:00 AM | Generate digest + send to reviewer (AI News + Bollywood) |
| 8:00 AM | Publish if approved; hold until 12 PM if no response |
| 12:00 PM | Midday fetch (Bollywood only) |
| 6:00 PM | Second Bollywood digest sent for review |
| 7:00 PM | Publish if approved |

---

## Troubleshooting

**409 Conflict — bot already running**
Another instance is polling the same token. Kill all Python processes and restart:
```bash
ps aux | grep python | grep -v grep | awk '{print $1}' | xargs kill -9
```
Note: `taskkill /F /IM python.exe` does not work in Git Bash — use the command above.

**Approve/Reject button not responding**
Telegram callback queries expire after ~30 seconds. Tap the button again while the bot process is running — it is safe to tap multiple times.

**"Chat not found" when sending review**
`TELEGRAM_REVIEWER_CHAT_ID` must be a numeric ID (e.g. `543925804`), not `@username`.

**Review message shows no image / text only**
Normal — generated image URLs from Euri expire quickly. The bot automatically falls back to text-only if the image URL has expired.

**No articles selected / all from one source**
Run a manual fetch first, then retry:
```bash
python aggregator/test_fetch.py bollywood
python publisher/test_review_interface.py bollywood
```

**Post blocked by guardrails**
Check `logs/guardrail_violations.log` to see which category triggered and why.

**Post generation fails**
Check your `EURI_API_KEY` is set in `.env`:
```bash
python test_euri_connection.py
```

**Gemini 429 rate limit — generation fails**
The free Euri tier allows 200K tokens/day. Running many tests in one day exhausts the quota. Wait until the next day — the limit resets daily.

**"Chat not found" for a new bot (e.g. astrology)**
Telegram bots can only message users who have started a conversation with them. Open Telegram, find your new bot, and send it `/start` from the reviewer account before running the test. Confirm the correct account by checking `getUpdates` — the chat ID in the response must match your `TELEGRAM_<BOT>_REVIEWER_CHAT_ID`.
