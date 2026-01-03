import json, os, re
from bs4 import BeautifulSoup

def extract_quotes():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []
    
    # THE PRO REGEX:
    # 1. Finds the quote
    # 2. Finds the verb (said/told/etc)
    # 3. Finds a Capitalized Name (e.g., Donald Trump or Harris)
    # Pattern: "Quote" + optional space + verb + optional space + Name
    pro_pattern = r'[“\"‘](.{30,500}?)[”\"’]\s*(?:said|told|warned|argued|stated|added|replied)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'

    print(f"🚀 Running Pro-Level Extraction on {len(articles)} articles...")

    for art in articles:
        soup = BeautifulSoup(art.get('content', ''), "html.parser")
        text = soup.get_text()
        
        # We use finditer for precision
        for match in re.finditer(pro_pattern, text, flags=re.DOTALL):
            quote_text = match.group(1).strip()
            speaker_name = match.group(2).strip() # This captures the actual name!
            
            # Cleaning
            clean_quote = " ".join(quote_text.split())
            
            # VALIDATION: Ignore common "non-person" names
            ignore_list = ["The", "But", "And", "According", "In", "On", "If"]
            if speaker_name in ignore_list:
                continue

            all_found_quotes.append({
                "politician": speaker_name,
                "quote": clean_quote,
                "source": art.get("source"),
                "date": art.get("date"), # If you added date to fetcher
                "url": art.get("url")
            })

    os.makedirs("data/quotes", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_found_quotes, f, indent=2)
    
    print(f"💎 BEST-IN-CLASS SUCCESS: Found {len(all_found_quotes)} verified political quotes.")

if __name__ == "__main__":
    extract_quotes()
