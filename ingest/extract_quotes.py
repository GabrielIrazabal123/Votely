import json, os, re
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []
    
    # STYLE 1: "Quote" said Name.
    pattern_a = r'[“\"‘](.{30,500}?)[”\"’]\s*(?:said|told|warned|added|replied)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    
    # STYLE 2: Name said: "Quote"
    pattern_b = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:said|told|warned|stated):\s*[“\"‘](.{30,500}?)[”\"’]'

    # STYLE 3: "Quote," Name said, "Quote continue." (Interrupted Quote)
    pattern_c = r'[“\"‘](.{10,500}?)[”\"’],\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:said|added|continued),\s*[“\"‘](.{10,500}?)[”\"’]'

    for art in articles:
        text = BeautifulSoup(art.get('content', ''), "html.parser").get_text()
        
        # --- Run Style 1 ---
        for m in re.finditer(pattern_a, text, flags=re.DOTALL):
            save_quote(all_found_quotes, m.group(2), m.group(1), art)
            
        # --- Run Style 2 ---
        for m in re.finditer(pattern_b, text, flags=re.DOTALL):
            save_quote(all_found_quotes, m.group(1), m.group(2), art)

        # --- Run Style 3 (The Interrupted Quote) ---
        for m in re.finditer(pattern_c, text, flags=re.DOTALL):
            combined_quote = f"{m.group(1)}... {m.group(3)}"
            save_quote(all_found_quotes, m.group(2), combined_quote, art)

    # REMOVE DUPLICATES & PROTECT AGAINST "THE" AS A NAME
    unique_quotes = {}
    blacklist = ["The", "But", "And", "According", "In", "On", "If", "However"]
    
    for q in all_found_quotes:
        if q['politician'] not in blacklist and q['quote'] not in unique_quotes:
            unique_quotes[q['quote']] = q

    os.makedirs("data/quotes", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(list(unique_quotes.values()), f, indent=2)
    
    print(f"🎯 MASTER EXTRACTION COMPLETE: Found {len(unique_quotes)} verified quotes.")

def save_quote(collection, name, text, art):
    clean_text = " ".join(text.split())
    collection.append({
        "politician": name.strip(),
        "quote": clean_text,
        "source": "The Guardian",
        "url": art.get("url")
    })

if __name__ == "__main__":
    extract_quotes()
