# 🇩🇪 Germany News Digest Bot

**Daily German news headlines delivered via Telegram/WhatsApp — bilingual English/German — zero cost.**

---

## Features

- **4 News Categories**: Politics, Sports, Technology, Business
- **Bilingual Summaries**: Every article summarized in English + German
- **Dual Delivery**: Telegram (primary) or WhatsApp (fallback)
- **Automated Scheduling**: Runs daily at 8:30 AM Berlin time via GitHub Actions
- **Zero Cost**: All services have generous free tiers
- **No Server Required**: Runs entirely on GitHub Actions

---

## How It Works

```
8:30 AM Berlin Time
    ↓
GitHub Actions (cron trigger)
    ↓
World News API → Fetches top German news (4 categories)
    ↓
Gemini Flash → Summarizes each article in EN + DE
    ↓
Telegram / WhatsApp → Delivers formatted digest
```

---

## Prerequisites

You'll need **3 free API keys** (takes ~5 minutes):

| Service | Purpose | Free Tier | Sign Up |
|---------|---------|-----------|---------|
| **World News API** | Fetch German news headlines | 50 req/day, no card | [worldnewsapi.com](https://worldnewsapi.com) |
| **Google Gemini API** | Summarize articles | ~1,500 req/day | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **Telegram Bot** | Deliver digest to chat | Free | [@BotFather](https://t.me/BotFather) |

---

## Quick Start

### 1. Get Your API Keys

**World News API:**
1. Go to [worldnewsapi.com](https://worldnewsapi.com) and sign up
2. Copy your free API key from the dashboard

**Google Gemini API:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" → Create API key
3. Copy your key

**Telegram Bot:**
1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`, follow prompts, copy the bot token
3. Send a message to your bot to initialize the chat
4. Get your chat ID from `https://api.telegram.org/bot<TOKEN>/getUpdates`

### 2. Clone the Repo

```bash
git clone https://github.com/10xdev4u-alt/GermanyNews.git
cd GermanyNews
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 4. Test Locally (Optional)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 5. Deploy via GitHub Actions

1. Push this repo to GitHub
2. Add your API keys as **GitHub Secrets** (Settings → Secrets and variables → Actions):
   - `WORLD_NEWS_API_KEY` — Your World News API key
   - `GEMINI_API_KEY` — Your Google Gemini API key
   - `TELEGRAM_BOT_TOKEN` — Your Telegram bot token
   - `TELEGRAM_CHAT_ID` — Your Telegram chat ID
3. Done! The bot runs automatically at **8:30 AM Berlin time** every day.

Trigger manually from the Actions tab to test.

---

## Sample Output

```
🇩🇪 Guten Morgen! — Good Morning! ☀️
📅 Daily News Digest — 10.06.2026
🌍 Germany News — English / Deutsch

🏛️ POLITICS / POLITIK
------------------------------
1. [Headline]
EN: [English summary 2-3 sentences]
DE: [German summary 2-3 sentences]
🔗 https://example.com/article
📰 Source: Spiegel

⚽ SPORTS / SPORT
...
💻 TECHNOLOGY / TECHNIK
...
📈 BUSINESS / WIRTSCHAFT
...

⏰ Next update: Tomorrow at 8:30 AM CET/CEST
🇩🇪 Bis morgen! — See you tomorrow! 👋
```

---

## Project Structure

```
GermanyNews/
├── main.py                  # Entry point
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py      # World News API client
│   ├── summarizer.py        # Gemini summarizer
│   ├── telegram_sender.py   # Telegram delivery
│   └── whatsapp_sender.py   # WhatsApp delivery (fallback)
├── .github/workflows/
│   └── daily-news.yml       # GitHub Actions schedule
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Customization

- **Categories**: Edit `DEFAULT_CATEGORIES` in `main.py`
- **Schedule time**: Update the `cron` field in `.github/workflows/daily-news.yml`
- **Articles per category**: Change `max_articles` in `news_fetcher.py`
- **Delivery method**: Toggle `USE_TELEGRAM` in `.env` (Telegram recommended)

---

## License

MIT
