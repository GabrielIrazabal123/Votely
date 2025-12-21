import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_fifty():
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    all_articles = []
    
    # We loop 5 times to get 50 articles (10 per page)
    for page in range(5):
        print(f"Fetching page {page}...")
        params = {
            "q": "politics",
            "api-key": API_KEY,
            "sort": "newest",
            "page": page
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            all_articles.extend(docs)
        else:
            print(f"❌ Error on page {page}: {response.status_code}")
            break
            
        # IMPORTANT: NYT requires a 6-second pause between requests
        time.sleep(6)

    # Save the giant list of 50 articles
    with open("data/raw/nyt_articles.json", "w") as f:
        json.dump({"response": {"docs": all_articles}}, f, indent=2)
    
    print(f"✅ Success! Saved {len(all_articles)} articles to data/raw/nyt_articles.json")

if __name__ == "__main__":
    fetch_fifty()
