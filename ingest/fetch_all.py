import os, requests, json, time
from dotenv import load_dotenv

load_dotenv()
NEWS_KEY = os.getenv("NEWS_API_KEY")
GUARDIAN_KEY = os.getenv("GUARDIAN_API_KEY")

def fetch_politics():
    all_articles = []

    # 1. Fetch from The Guardian (Best quality, full body text included)
    print("📡 Fetching from The Guardian...")
    g_url = "https://content.guardianapis.com/search"
    g_params = {
        "section": "politics",
        "show-fields": "bodyText,headline",
        "page-size": 20,
        "api-key": GUARDIAN_KEY
    }
    res = requests.get(g_url, params=g_params).json()
    for art in res.get("response", {}).get("results", []):
        all_articles.append({
            "source": "The Guardian",
            "url": art.get("webUrl"),
            "title": art.get("fields", {}).get("headline"),
            "content": art.get("fields", {}).get("bodyText") # FULL TEXT!
        })

    # 2. Fetch from NewsAPI (Broad discovery)
    print("📡 Fetching from NewsAPI...")
    n_url = "https://newsapi.org/v2/everything"
    n_params = {
        "q": "politics",
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 20,
        "apiKey": NEWS_KEY
    }
    res = requests.get(n_url, params=n_params).json()
    for art in res.get("articles", []):
        all_articles.append({
            "source": art.get("source", {}).get("name"),
            "url": art.get("url"),
            "title": art.get("title"),
            "content": art.get("content") # Note: NewsAPI content is usually truncated
        })

    with open("data/raw/all_articles.json", "w") as f:
        json.dump(all_articles, f, indent=2)
    print(f"✅ Saved {len(all_articles)} articles.")

if __name__ == "__main__":
    fetch_politics()
