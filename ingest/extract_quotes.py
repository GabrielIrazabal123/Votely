import json, os, re, requests, time, random
from bs4 import BeautifulSoup

def extract_with_stealth():
    raw_path = "data/raw/nyt_articles.json"
    output_path = "data/quotes/full_quotes_dump.json"
    
    with open(raw_path, "r") as f:
        articles = json.load(f).get("response", {}).get("docs", [])

    all_found = []
    # Disguise as Google's Crawler
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

    for i, art in enumerate(articles):
        url = art.get("web_url")
        print(f"[{i+1}/{len(articles)}] Attempting: {url[:50]}...")
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                # NYT often hides text in <section name="articleBody">
                paragraphs = soup.find_all('p')
                full_text = " ".join([p.get_text() for p in paragraphs])
                
                print(f"   ∟ Found {len(full_text)} characters.")

                # If we only find 100-200 chars, it's just the 'Subscribe' message
                if len(full_text) > 500:
                    quotes = re.findall(r'[“\"‘](.{15,400}?[”\"’])', text)
                    for q in quotes:
                        all_found.append({"quote": q[:-1], "url": url, "title": art.get("headline", {}).get("main")})
            
            # Random wait between 2-5 seconds to look human
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"   ∟ Connection error: {e}")

    with open(output_path, "w") as f:
        json.dump(all_found, f, indent=2)
    print(f"\n✅ Total quotes captured: {len(all_found)}")

if __name__ == "__main__":
    extract_with_stealth()
