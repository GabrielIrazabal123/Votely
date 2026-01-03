import json, os, re
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []
    
    # 1. NEW REGEX: Look for the quote AND the word after it (the attribution)
    # This looks for: "Quote Text" followed by words like said, told, added...
    pattern = r'[“\"‘](.{30,500}?)[”\"’]\s*(said|told|added|warned|stated|argued)'

    print(f"🔎 Filtering {len(articles)} articles for high-quality quotes...")

    for art in articles:
        soup = BeautifulSoup(art.get('content', ''), "html.parser")
        text = soup.get_text()
        
        # We use re.IGNORECASE to catch "Said" and "said"
        for match in re.finditer(pattern, text, flags=re.DOTALL | re.IGNORECASE):
            quote_text = match.group(1).strip()
            verb_found = match.group(2) # e.g., "said"
            
            clean_quote = " ".join(quote_text.split())
            
            all_found_quotes.append({
                "quote": clean_quote,
                "attribution_verb": verb_found,
                "source": art.get("source"),
                "url": art.get("url"),
                "title": art.get("title")
            })

    os.makedirs("data/quotes", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_found_quotes, f, indent=2)
    
    print(f"🎯 SUCCESS: Filtered down to {len(all_found_quotes)} verified quotes.")

if __name__ == "__main__":
    extract_quotes()
