import json, os, re, requests, time, random
from bs4 import BeautifulSoup

def extract_with_stealth():
    raw_path = "data/raw/nyt_articles.json"
    output_path = "data/quotes/full_quotes_dump.json"
    
    if not os.path.exists(raw_path):
        print("❌ No articles found. Run fetch_nyt.py first!")
        return

    with open(raw_path, "r") as f:
        articles = json.load(f).get("response", {}).get("docs", [])

    all_found = []
    # Disguise as Google's Crawler
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

    print(f"🔎 Scanning {len(articles)} articles for quotes...")

    for i, art in enumerate(articles):
        url = art.get("web_url")
        print(f"[{i+1}/{len(articles)}] Attempting: {url[:60]}...")
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                paragraphs = soup.find_all('p')
                
                # We use 'full_text' consistently now
                full_text = " ".join([p.get_text() for p in paragraphs])
                
                # If we only find very little text, it's likely a paywall block
                if len(full_text) < 500:
                    print(f"   ∟ ⚠️ Paywall detected (only {len(full_text)} chars).")
                    continue

                # REGEX FIX: Now matches the variable 'full_text'
                # Looking for anything between quotes that is 15-400 characters
                quotes = re.findall(r'[“\"‘](.{15,400}?[”\"’])', full_text)
                
                if quotes:
                    print(f"   ∟ ✅ Success! Found {len(quotes)} quotes.")
                    for q in quotes:
                        all_found.append({
                            "quote": q[:-1].strip(), 
                            "url": url, 
                            "title": art.get("headline", {}).get("main")
                        })
                else:
                    print(f"   ∟ ℹ️ No quotes found in the {len(full_text)} characters scanned.")
            
            # Random wait to stay under the radar
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"   ∟ ❌ Error: {e}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_found, f, indent=2)
    
    print(f"\n🎉 ALL DONE! Total quotes captured: {len(all_found)}")

if __name__ == "__main__":
    extract_with_stealth()
