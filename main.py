"""
Main entry point for the Germany News Digest Bot.

Fetches German news headlines → summarizes with Gemini →
sends bilingual digest via Telegram (primary) or WhatsApp (fallback).
"""

import os
import sys

# Add project root to path so 'from src...' imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.news_fetcher import fetch_german_news
from src.summarizer import compose_digest
from src.telegram_sender import send_telegram_message
from src.whatsapp_sender import send_whatsapp_message

DEFAULT_CATEGORIES = ["politics", "sports", "technology", "business"]


def main():
    print("=" * 50)
    print("🇩🇪  GERMANY NEWS DIGEST BOT")
    print("=" * 50)

    # Step 1: Fetch news
    print("\n📡 Step 1: Fetching German news...")
    categories = DEFAULT_CATEGORIES
    articles = fetch_german_news(categories)
    print(f"   ✅ Fetched {len(articles)} articles across {len(categories)} categories")

    if not articles:
        print("   ⚠️  No articles found. Sending fallback message.")

    # Step 2: Summarize & compose digest
    print("\n🤖 Step 2: Summarizing with Gemini Flash...")
    digest = compose_digest(articles)
    print(f"   ✅ Digest composed ({len(digest)} characters)")

    # Preview first 200 chars
    preview = digest[:200].replace("\n", " ").strip()
    print(f"   📝 Preview: {preview}...")

    # Step 3: Send — try Telegram first, fallback to WhatsApp
    print("\n📱 Step 3: Sending digest...")
    sent = False

    # Try Telegram (reliable, official, free)
    if os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"):
        print("   📬 Attempting Telegram delivery...")
        sent = send_telegram_message(digest)
        if sent:
            platform = "Telegram"
    else:
        print("   ⏭️  Telegram not configured, skipping")

    # Fallback to WhatsApp if Telegram not sent
    if not sent:
        print("   📬 Attempting WhatsApp delivery (CallMeBot)...")
        sent = send_whatsapp_message(digest)
        if sent:
            platform = "WhatsApp"

    if sent:
        print("\n" + "=" * 50)
        print(f"✅  MISSION COMPLETE!")
        print(f"   Your German news digest has been delivered via {platform}! 🎉")
        print("=" * 50)
    else:
        print("\n❌ Failed to send via any channel.")
        print("   Set TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID for Telegram delivery,")
        print("   or CALLMEBOT_API_KEY + WHATSAPP_PHONE for WhatsApp.")
        print("\n📝 Digest was still composed (printed below):")
        print(digest)
        sys.exit(1)


if __name__ == "__main__":
    main()
