import json
import os
import re
import requests
import time
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/nyt_articles.json"
    output_dir = "data/quotes"
    
    if not os.path.exists(raw_path):
        print("❌ No raw data found. Run fetch_nyt.py first!")
        return

    # 1. Load the article list
    with open(raw_path, "r") as f:
        data = json.load(f)
    articles = data.get("response", {}).get("docs") or []

    all_quotes = []
    print(f"🧐 Found {len(articles)} articles. Starting full-text extraction...")

    # 2. Loop through each article URL
    for i, art in enumerate(articles):
        url = art.get("web_url")
        print(f"[{i+1}/{len(articles)}] Visiting: {url}")

        try:
            # 3. Visit the website and get the HTML
            # We add a 'User-Agent' so the website thinks we are a real browser
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 4. Find all paragraphs (<p> tags) to get the full story
                paragraphs = soup.find_all('p')
                full_text = " ".join([p.get_text() for p in paragraphs])

                # 5. Find all quotes in the full text
                found = re.findall(r'\"([^\"]{10,250})\"', full_text)
                
                for q in found:
                    all_quotes.append({
                        "quote": q.strip(),
                        "url": url,
                        "title": art.get("headline", {}).get("main", "Unknown Title")
                    })
            
            # 6. Wait 1 second between articles so NYT doesn't block us
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Could not read article {i+1}: {e}")

    # 7. Save everything to one big file
    if all_quotes:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(f"{output_dir}/full_quotes_dump.json", "w") as f:
            json.dump(all_quotes, f, indent=2)
        print(f"✅ SUCCESS! Extracted {len(all_quotes)} quotes to data/quotes/full_quotes_dump.json")
    else:
        print("❌ No quotes found in any of the articles.")

if __name__ == "__main__":
    extract_quotes()
