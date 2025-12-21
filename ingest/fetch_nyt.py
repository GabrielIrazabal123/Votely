import os, requests, json, time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_open_articles():
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    all_articles = []
    
    # Target 'AP' and 'Reuters' - they have softer paywalls
    search_query = 'politics "Associated Press" OR "Reuters"'
    
    for page in range(3): # Let's start with 30 articles
        print(f"📡 Fetching open-access page {page}...")
        params = {"q": search_query, "api-key": API_KEY, "page": page}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            all_articles.extend(response.json().get("response", {}).get("docs", []))
        
        # NYT requires 6 seconds, but let's do 10 to be safe
        time.sleep(10)

    with open("data/raw/nyt_articles.json", "w") as f:
        json.dump({"response": {"docs": all_articles}}, f, indent=2)
    print(f"✅ Saved {len(all_articles)} articles.")

if __name__ == "__main__":
    fetch_open_articles()
