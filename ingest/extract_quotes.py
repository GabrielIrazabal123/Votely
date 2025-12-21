import json
import os
import re

def extract_quotes():
    raw_file = "data/raw/nyt_articles.json"
    
    if not os.path.exists(raw_file):
        print("❌ Error: 'data/raw/nyt_articles.json' not found. Run fetch_nyt.py first!")
        return

    with open(raw_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Error: The raw data file is empty or corrupted.")
            return

    # SAFETY CHECK: Get articles, but default to an empty list [] instead of None
    articles = data.get("response", {}).get("docs", [])

    if not articles:
        print("⚠️ No articles found in the raw data. Try running the fetcher again.")
        return
    
    found_count = 0
    for art in articles:
        text = art.get("lead_paragraph", "") or ""
        matches = re.findall(r'\"(.+?)\"\s*(?:said|stated|told)\s+([A-Z][a-z]+\s[A-Z][a-z]+)', text)
        
        for quote, speaker in matches:
            speaker_slug = speaker.lower().replace(" ", "-")
            output_path = os.path.join("data", "quotes", f"{speaker_slug}.json")
            
            new_quote = {"text": quote, "source": "NYT", "url": art.get("web_url")}

            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    content = json.load(f)
            else:
                content = {"person": speaker, "quotes": []}

            content["quotes"].append(new_quote)
            with open(output_path, "w") as f:
                json.dump(content, f, indent=2)
            found_count += 1

    print(f"✅ Done! Extracted {found_count} quotes.")

if __name__ == "__main__":
    extract_quotes()
