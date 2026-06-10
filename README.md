# 🇩🇪 Germany News WhatsApp Bot

**Daily German news headlines delivered to your WhatsApp at 8:30 AM Berlin time — bilingual English/German — completely FREE.**

## 🎯 Features

- ✅ **4 News Categories**: Politics 🏛️, Sports ⚽, Technology 💻, Business 📈
- ✅ **Bilingual Summaries**: Every article summarized in **English + German**
- ✅ **WhatsApp Delivery**: Sent directly to your WhatsApp every morning
- ✅ **AI-Powered**: Google Gemini Flash creates intelligent, concise summaries
- ✅ **Zero Cost**: All services used have generous free tiers — **₹0 / $0**
- ✅ **No Server Needed**: Runs on GitHub Actions (free)

## 🧠 How It Works

```
🌅 8:30 AM Berlin Time
    ↓
GitHub Actions (cron trigger)
    ↓
📡 World News API → Fetches top German news (4 categories)
    ↓
🤖 Google Gemini Flash → Summarizes each article in EN + DE
    ↓
📱 CallMeBot API → Sends formatted digest to your WhatsApp
```

## 📋 Prerequisites

Before you start, you'll need **3 free API keys** (takes 5 minutes total):

| Service | What For | Free Tier | Sign Up |
|---------|----------|-----------|---------|
| **World News API** | Fetch German news headlines | 50 requests/day, no credit card | [worldnewsapi.com](https://worldnewsapi.com) |
| **Google Gemini API** | Summarize articles with AI | ~1,500 requests/day | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **CallMeBot** | Send messages to your WhatsApp | Free for personal use | [callmebot.com](https://www.callmebot.com/blog/free-api-whatsapp-messages/) |

## 🚀 Quick Start

### 1. Get Your API Keys

**World News API:**
1. Go to [worldnewsapi.com](https://worldnewsapi.com) and sign up
2. Copy your free API key from the dashboard

**Google Gemini API:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" → Create API key
3. Copy your key

**CallMeBot (WhatsApp):**
1. Add **+34 644 03 87 31** to your WhatsApp contacts
2. Send the message: `I allow callmebot to send me messages`
3. You'll receive your API key via reply within 2 minutes

### 2. Fork & Clone This Repo

```bash
git clone https://github.com/YOUR_USERNAME/germany-news-whatsapp.git
cd germany-news-whatsapp
```

### 3. Test Locally (Optional)

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your keys
cp .env.example .env
# Edit .env with your actual API keys

# Run it!
python main.py
```

### 4. Deploy with GitHub Actions (Free)

1. Push this repo to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/germany-news-whatsapp.git
   git push -u origin main
   ```

2. Add your API keys as **GitHub Secrets**:
   - Go to your repo → **Settings** → **Secrets and variables** → **Actions**
   - Add these 4 secrets:
     - `WORLD_NEWS_API_KEY` — Your World News API key
     - `GEMINI_API_KEY` — Your Google Gemini API key
     - `WHATSAPP_PHONE` — Your phone number (e.g., `491701234567`, no `+`)
     - `CALLMEBOT_API_KEY` — Your CallMeBot API key

3. ✅ **Done!** The bot will automatically run at **8:30 AM Berlin time** every day.
   
   You can also manually trigger it from the Actions tab to test.

## 📱 What Your WhatsApp Will Look Like

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

## 🛠️ Project Structure

```
germany-news-whatsapp/
├── main.py                          # Entry point
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py              # World News API client
│   ├── summarizer.py                # Gemini Flash summarizer
│   └── whatsapp_sender.py           # CallMeBot WhatsApp sender
├── .github/workflows/
│   └── daily-news.yml               # GitHub Actions schedule
├── .env.example                     # Environment variables template
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔧 Customization

- **Change categories**: Edit `DEFAULT_CATEGORIES` in `main.py`
- **Change time**: Update the `cron` and `timezone` in `.github/workflows/daily-news.yml`
- **More articles per category**: Change `max_articles` in `news_fetcher.py`
- **Different LLM**: Swap the model name in `summarizer.py` (e.g., `gemini-2.5-flash`)

## 📝 License

MIT — Do whatever you want with it!

---

Made with ❤️ and 🤖 — No servers, no subscriptions, just free APIs.
