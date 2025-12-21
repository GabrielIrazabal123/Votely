import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_50_articles():
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    all_articles = []
    
    # NYT gives 10 per page. We do 5 pages = 50 articles.
    for page in range(5):
        print(f"📡 Fetching page {page}...")
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
            
        # VERY IMPORTANT: NYT will block you if you go faster than 6 seconds per request
        time.sleep(6)

    output_path = "data/raw/nyt_articles.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump({"response": {"docs": all_articles}}, f, indent=2)
    
    print(f"✅ Saved {len(all_articles)} articles. Ready to extract.")

if __name__ == "__main__":
    fetch_50_articles()
