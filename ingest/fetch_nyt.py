import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch():
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "fq": 'section_name:"Politics"',
        "api-key": API_KEY,
        "sort": "newest"
    }
    print("Fetching newest political articles from NYT...")
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        with open("data/raw/nyt_articles.json", "w") as f:
            json.dump(data, f, indent=2)
        print("✅ Success! Raw articles saved.")
    else:
        print(f"❌ Error: {r.status_code}")

if __name__ == "__main__":
    fetch()
