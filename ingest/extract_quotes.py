import json
import os
import re
import requests
import time
from bs4 import BeautifulSoup

def extract_full_text_quotes():
    raw_path = "data/raw/nyt_articles.json"
    output_path = "data/quotes/full_quotes_dump.json"
    
    if not os.path.exists(raw_path):
        print("❌ Run fetch_nyt.py first!")
        return

    with open(raw_path, "r") as f:
        articles = json.load(f).get("response", {}).get("docs", [])

    all_found = []
    print(f"Starting extraction for {len(articles)} articles...")

    for i, art in enumerate(articles):
        url = art.get("web_url")
        print(f"[{i+1}/{len(articles)}] Reading: {url}")
        
        try:
            # We pretend to be a browser so the NYT doesn't block the 'bot'
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # Grab all paragraph text
                text = " ".join([p.get_text() for p in soup.find_all('p')])
                
                # SMART REGEX: Matches "..." OR “...”
                quotes = re.findall(r'[“\"].{10,250}?[”\"]', text)
                
                for q in quotes:
                    all_found.append({
                        "quote": q.strip('“”\"'),
                        "title": art.get("headline", {}).get("main"),
                        "url": url
                    })
            time.sleep(1) # Small pause to be polite to the server
        except Exception as e:
            print(f"Skipping {i+1} due to error.")

    with open(output_path, "w") as f:
        json.dump(all_found, f, indent=2)
    
    print(f"✅ Done! Found {len(all_found)} quotes.")

if __name__ == "__main__":
    extract_full_text_quotes()
