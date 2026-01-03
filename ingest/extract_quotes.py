import json, os, re
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    if not os.path.exists(raw_path):
        print("❌ Error: Run fetch_all.py first!")
        return

    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []
    
    # We use a non-capturing group (?:) for the quotes themselves 
    # to avoid the 'findall' group trap.
    pattern = r'[“\"‘](.{30,500}?)[”\"’]'

    print(f"🔎 Processing {len(articles)} articles...")

    for art in articles:
        # Step 1: Clean HTML
        soup = BeautifulSoup(art.get('content', ''), "html.parser")
        text = soup.get_text()
        
        # Step 2: Use finditer to ensure we catch EVERY match individually
        # flags=re.DOTALL allows matches to span across newlines
        for match in re.finditer(pattern, text, flags=re.DOTALL):
            quote_text = match.group(1).strip()
            
            # Clean up nested junk/newlines
            clean_quote = " ".join(quote_text.split())
            
            all_found_quotes.append({
                "quote": clean_quote,
                "source": art.get("source"),
                "url": art.get("url")
            })

    # Save ONLY after the loops are finished
    os.makedirs("data/quotes", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_found_quotes, f, indent=2)
    
    print(f"🎯 SUCCESS: Found {len(all_found_quotes)} total quotes.")

if __name__ == "__main__":
    extract_quotes()
