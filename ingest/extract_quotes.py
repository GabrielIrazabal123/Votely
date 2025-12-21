import json
import os
import re

def extract_quotes():
    # 1. Look for the file we created in Step 3
    raw_file = "data/raw/nyt_articles.json"
    
    if not os.path.exists(raw_file):
        print("❌ Error: I can't find the raw articles. Run fetch_nyt.py first!")
        return

    with open(raw_file, "r") as f:
        data = json.load(f)

    # 2. Get the list of articles
    articles = data.get("response", {}).get("docs", [])
    
    for art in articles:
        text = art.get("lead_paragraph", "")
        # Regex: Find "Quote" said Name
        matches = re.findall(r'\"(.+?)\"\s*(?:said|stated|told)\s+([A-Z][a-z]+\s[A-Z][a-z]+)', text)
        
        for quote, speaker in matches:
            # Create a filename like 'joe-biden.json'
            speaker_slug = speaker.lower().replace(" ", "-")
            output_path = os.path.join("data", "quotes", f"{speaker_slug}.json")
            
            # Prepare the data
            new_quote = {
                "text": quote,
                "source": "New York Times",
                "url": art.get("web_url")
            }

            # If the politician's file already exists, add to it
            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    content = json.load(f)
            else:
                content = {"person": speaker, "quotes": []}

            content["quotes"].append(new_quote)
            
            with open(output_path, "w") as f:
                json.dump(content, f, indent=2)

    print("✅ Done! Check your 'data/quotes' folder for new files.")

if __name__ == "__main__":
    extract_quotes()
