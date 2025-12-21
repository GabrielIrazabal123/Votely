import json
import os
import re
import requests
import time
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/nyt_articles.json"
    output_path = "data/quotes/full_quotes_dump.json"
    
    if not os.path.exists(raw_path):
        print("❌ No articles found. Run fetch_nyt.py first!")
        return

    with open(raw_path, "r") as f:
        articles = json.load(f).get("response", {}).get("docs", [])

    all_found = []
    print(f"🔎 Scanning {len(articles)} articles for quotes...")

    for i, art in enumerate(articles):
        url = art.get("web_url")
        print(f"[{i+1}/{len(articles)}] Visiting: {url}")
        
        try:
            # Enhanced Headers to bypass simple bot detection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # We specifically look for tags that NYT uses for article body
                # 'section' and 'p' covers the majority of their layout
                paragraphs = soup.find_all('p')
                text = " ".join([p.get_text() for p in paragraphs])
                
                print(f"   ∟ Found {len(text)} characters.")

                # REGEX: Matches "..." OR “...” OR ‘...’
                # Catches quotes between 15 and 300 characters long
                quotes = re.findall(r'[“\"‘](.{15,300}?[”\"’])', text)
                
                for q in quotes:
                    all_found.append({
                        "quote": q[:-1].strip(), # Strip the closing quote mark
                        "title": art.get("headline", {}).get("main"),
                        "url": url
                    })
            else:
                print(f"   ∟ Blocked! (Status: {res.status_code})")
            
            time.sleep(1) # Be nice to the servers
            
        except Exception as e:
            print(f"   ∟ Error reading page: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_found, f, indent=2)
    
    print(f"\n✅ COMPLETE! Extracted {len(all_found)} total quotes.")

if __name__ == "__main__":
    extract_quotes()
