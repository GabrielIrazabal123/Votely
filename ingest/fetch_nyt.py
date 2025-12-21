import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch():
    # We are broadening the search to "Politics" as a general term
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": "politics", 
        "api-key": API_KEY,
        "sort": "newest"
    }
    
    print("Connecting to NYT...")
    r = requests.get(url, params=params)
    
    if r.status_code == 200:
        data = r.json()
        # Verify if 'docs' actually exists in the response
        if "response" in data and "docs" in data["response"]:
            with open("data/raw/nyt_articles.json", "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Success! Saved {len(data['response']['docs'])} articles.")
        else:
            print("❌ NYT returned an empty response. Check your API key or query.")
    else:
        print(f"❌ HTTP Error: {r.status_code}")

if __name__ == "__main__":
    fetch()
