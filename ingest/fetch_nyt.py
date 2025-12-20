import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NYT_API_KEY")
SEARCH_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

def fetch_politics_articles():
    params = {
        "q": "politics",
        "fq": 'section_name:"Politics"',
        "api-key": API_KEY,
        "sort": "newest"
    }
    
    response = requests.get(SEARCH_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Ensure the data/raw directory exists
        os.makedirs("data/raw", exist_ok=True)
        
        with open("data/raw/latest_articles.json", "w") as f:
            json.dump(data, f, indent=2)
        print("✅ Raw articles saved to data/raw/latest_articles.json")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    fetch_politics_articles()
