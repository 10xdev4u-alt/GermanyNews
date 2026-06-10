"""
Summarizer — Uses Google Gemini API (free tier Flash model) to summarize
news articles in both English and German (bilingual output).

Articles are BATCHED into a single Gemini call for performance.
"""

import os
import re
from datetime import datetime

from google import genai


def _get_client() -> genai.Client:
    """Get a configured Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)


def _summarize_all_batch(articles: list[dict]) -> list[dict]:
    """
    Send ALL articles in a single Gemini prompt for efficient batch summarization.
    Returns the articles list with 'summary_en' and 'summary_de' keys attached.
    """
    if not articles:
        return articles

    # Build a single prompt with all articles
    prompt_parts = [
        "You are a news summarizer. Below are German news articles to summarize.",
        "For EACH article, provide a 2-3 sentence summary in English AND in German.",
        "",
        "Respond with EXACTLY this format for each article:",
        "ARTICLE_1:",
        "EN: [English summary]",
        "DE: [German summary]",
        "ARTICLE_2:",
        "EN: ...",
        "DE: ...",
        "",
        "--- BEGIN ARTICLES ---",
    ]

    for idx, article in enumerate(articles, 1):
        title = article.get("title", "Untitled")
        text = (article.get("description") or "")[:1200]
        cat = article.get("category", "general")
        prompt_parts.append(f"\nARTICLE_{idx}:")
        prompt_parts.append(f"Title: {title}")
        prompt_parts.append(f"Category: {cat}")
        prompt_parts.append(f"Text: {text}")

    prompt_parts.append("\n--- END ARTICLES ---")
    prompt = "\n".join(prompt_parts)

    client = _get_client()
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        raw = response.text.strip()

        # Use block-based regex parsing to handle multi-line summaries correctly.
        # Split the response by ARTICLE_N: markers, then extract EN:/DE: from each block.
        blocks = re.split(r'\n(?=ARTICLE_\d+:)', raw)

        for block in blocks:
            # Extract the article index
            idx_match = re.match(r'ARTICLE_(\d+):', block.strip())
            if not idx_match:
                continue
            idx = int(idx_match.group(1)) - 1
            if idx < 0 or idx >= len(articles):
                continue

            # Extract EN: content (everything between EN: and DE: or end of block)
            en_match = re.search(r'EN:(.*?)(?=\nDE:|\Z)', block, re.DOTALL)
            if en_match:
                articles[idx]["summary_en"] = en_match.group(1).strip()

            # Extract DE: content (everything after DE: until next ARTICLE or end)
            de_match = re.search(r'DE:(.*?)(?=\nARTICLE_|\Z)', block, re.DOTALL)
            if de_match:
                articles[idx]["summary_de"] = de_match.group(1).strip()

        # Fill any missing summaries with fallback
        for article in articles:
            if "summary_en" not in article or not article.get("summary_en"):
                article["summary_en"] = "(Summary unavailable)"
            if "summary_de" not in article or not article.get("summary_de"):
                article["summary_de"] = "(Zusammenfassung nicht verfügbar)"

    except Exception as e:
        print(f"⚠️  Batch Gemini summarization failed: {e}")
        # Fallback: use truncated original text
        for article in articles:
            text = (article.get("description") or "")[:300]
            article["summary_en"] = text + "..."
            article["summary_de"] = "(Zusammenfassung nicht verfügbar)"

    return articles


def compose_digest(articles: list[dict]) -> str:
    """
    Take a list of article dicts, batch-summarize via Gemini, and compose
    a full WhatsApp-ready digest message with bilingual (EN+DE) summaries.
    """
    if not articles:
        return "🇩🇪 *Guten Morgen!* 🌅\n\nNo news articles were available today. Check back tomorrow!"

    # Batch-summarize all articles in ONE Gemini call
    articles = _summarize_all_batch(articles)

    # Group articles by category for a clean layout
    categories_order = ["politics", "sports", "technology", "business"]
    emoji_map = {
        "politics": "🏛️",
        "sports": "⚽",
        "technology": "💻",
        "business": "📈",
    }
    label_map = {
        "politics": "POLITICS / POLITIK",
        "sports": "SPORTS / SPORT",
        "technology": "TECHNOLOGY / TECHNIK",
        "business": "BUSINESS / WIRTSCHAFT",
    }

    grouped: dict[str, list[dict]] = {cat: [] for cat in categories_order}
    for article in articles:
        cat = article.get("category", "other")
        if cat in grouped:
            grouped[cat].append(article)

    lines = ["🇩🇪 *Guten Morgen! — Good Morning!* ☀️"]
    lines.append(f"📅 *Daily News Digest — {datetime.now().strftime('%d.%m.%Y')}*")
    lines.append("🌍 *Germany News — English / Deutsch*\n")

    for cat in categories_order:
        cat_articles = grouped.get(cat, [])
        if not cat_articles:
            continue

        emoji = emoji_map.get(cat, "📰")
        label = label_map.get(cat, cat.upper())
        lines.append(f"{emoji} *{label}*\n{'-' * 30}")

        for i, article in enumerate(cat_articles, 1):
            title = article.get("title", "Untitled")
            summary_en = article.get("summary_en", "")
            summary_de = article.get("summary_de", "")
            source = article.get("source", "Unknown")
            url = article.get("url", "")

            lines.append(f"\n*{i}. {title}*")
            if summary_en:
                lines.append(f"EN: {summary_en}")
            if summary_de:
                lines.append(f"DE: {summary_de}")
            if url:
                lines.append(f"🔗 {url}")
            lines.append(f"📰 Source: {source}")
            lines.append("")

    lines.append("\n" + "=" * 30)
    lines.append("🤖 *Powered by:*")
    lines.append("• World News API — News source")
    lines.append("• Google Gemini — AI Summaries")
    lines.append("• CallMeBot — WhatsApp Delivery")
    lines.append("• GitHub Actions — Daily Schedule")
    lines.append("\n⏰ *Next update: Tomorrow at 8:30 AM CET/CEST*")
    lines.append("🇩🇪 *Bis morgen! — See you tomorrow!* 👋")

    full_message = "\n".join(lines)

    # Warn if message is very long (CallMeBot may truncate)
    if len(full_message) > 5000:
        print(f"⚠️  Digest is {len(full_message)} chars (may exceed CallMeBot limits)")

    return full_message
