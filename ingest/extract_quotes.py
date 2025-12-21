import json
import os
import re

def extract_quotes():
    raw_path = "data/raw/nyt_articles.json"
    
    if not os.path.exists(raw_path):
        print("❌ No raw file found.")
        return

    with open(raw_path, "r") as f:
        data = json.load(f)

    articles = data.get("response", {}).get("docs") or []
    
    # We will store everything here
    all_extracted = []

    for art in articles:
        # Check BOTH the lead paragraph and the abstract for more data
        text = (art.get("lead_paragraph") or "") + " " + (art.get("abstract") or "")
        
        # This regex finds ANYTHING between double quotes
        # It looks for "Anything"
        matches = re.findall(r'\"([^\"]+)\"', text)
        
        for quote in matches:
            if len(quote) > 15:  # Ignore tiny fragments like "the" or "yes"
                all_extracted.append({
                    "quote": quote,
                    "source": art.get("source"),
                    "url": art.get("web_url")
                })

    if all_extracted:
        output_path = "data/quotes/extracted_dump.json"
        with open(output_path, "w") as f:
            json.dump(all_extracted, f, indent=2)
        print(f"✅ SUCCESS! Found {len(all_extracted)} quotes. Check data/quotes/extracted_dump.json")
    else:
        print("⚠️ Still nothing. This means the articles fetched literally don't have quote marks in the first paragraph.")

if __name__ == "__main__":
    extract_quotes()
