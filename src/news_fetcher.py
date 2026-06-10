"""
News Fetcher — World News API client for German news headlines.
Fetches top headlines by category (politics, sports, tech, business).
"""

import os
import requests

WORLD_NEWS_API_BASE = "https://api.worldnewsapi.com"
NEWSAPI_BASE = "https://newsapi.org/v2"


def _fetch_world_news_api(category: str, max_articles: int = 3) -> list[dict]:
    """
    Fetch German news for a given category using World News API.
    Returns a list of article dicts with title, description, url, source.
    """
    api_key = os.environ.get("WORLD_NEWS_API_KEY")
    if not api_key:
        raise ValueError("WORLD_NEWS_API_KEY environment variable is not set")

    params = {
        "source-countries": "DE",
        "language": "de",
        "categories": category,
        "number": max_articles,
        "api-key": api_key,
        "earliest-publish-date": "1 day ago",
        "sort": "publish-time",
    }

    resp = requests.get(
        f"{WORLD_NEWS_API_BASE}/search-news",
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    articles = data.get("news", data.get("articles", []))
    results = []
    for article in articles[:max_articles]:
        title = article.get("title") or article.get("text", "")[:100]
        description = (
            article.get("text") or article.get("description") or ""
        )
        # Truncate very long text
        if len(description) > 800:
            description = description[:800] + "..."

        results.append({
            "title": title,
            "description": description,
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "category": category,
        })

    return results


def fetch_german_news(categories: list[str] | None = None) -> list[dict]:
    """
    Fetch top German news for all requested categories.
    If categories is None, fetches all 4 default categories.

    Returns a flat list of article dicts.
    """
    if categories is None:
        categories = ["politics", "sports", "technology", "business"]

    all_articles: list[dict] = []
    results_log: list[str] = []

    for cat in categories:
        try:
            articles = _fetch_world_news_api(cat, max_articles=2)
            all_articles.extend(articles)
            results_log.append(f"   • {cat}: {len(articles)} articles")
            print(f"   ✅ {cat}: fetched {len(articles)} articles")
        except Exception as e:
            results_log.append(f"   • {cat}: ERROR — {e}")
            print(f"   ⚠️  Failed to fetch category '{cat}': {e}")
            # Try to continue with other categories
            continue

    print(f"   📊 Category summary: {', '.join(r.strip() for r in results_log)}")
    return all_articles
