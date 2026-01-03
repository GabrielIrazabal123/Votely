import os, requests, json
from dotenv import load_dotenv

load_dotenv()
GUARDIAN_KEY = os.getenv("GUARDIAN_API_KEY")

def fetch_data():
    all_articles = []
    print("📡 Connecting to The Guardian...")
    
    # We use 'body' to get everything
    g_url = "https://content.guardianapis.com/search"
    g_params = {
        "section": "politics",
        "show-fields": "body,headline", 
        "page-size": 50,
        "api-key": GUARDIAN_KEY
    }
    
    try:
        res = requests.get(g_url, params=g_params).json()
        articles = res.get("response", {}).get("results", [])
        
        print(f"🔎 Found {len(articles)} articles online. Processing...")
        
        for i, art in enumerate(articles):
            content = art.get("fields", {}).get("body", "")
            if len(content) > 50:
                print(f"   [{i+1}] Grabbed: {art.get('webTitle')[:40]}...")
                all_articles.append({
                    "source": "The Guardian",
                    "content": content,
                    "title": art.get("fields", {}).get("headline"),
                    "url": art.get("webUrl")
                })
        
        os.makedirs("data/raw", exist_ok=True)
        with open("data/raw/all_articles.json", "w") as f:
            json.dump(all_articles, f, indent=2)
            
        print(f"✅ FINAL: Saved {len(all_articles)} articles to data/raw/all_articles.json")
        
    except Exception as e:
        print(f"❌ FETCH ERROR: {e}")

if __name__ == "__main__":
    fetch_data()
