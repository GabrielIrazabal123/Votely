import json, os, re

def extract_specific_quotes():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    if not os.path.exists(raw_path):
        return

    with open(raw_path, "r") as f:
        articles = json.load(f)

    results = []
    # This regex looks for: "Quote" said/told/added [Name]
    # It requires the quote to be at least 40 chars to avoid vague soundbites
    quote_pattern = r'[“\"‘](.{40,500}?[”\"’])\s*(?:said|told|added|stated|argued)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'

    for art in articles:
        text = art.get("content")
        if not text: continue
        
        found = re.findall(quote_pattern, text)
        for quote_text, speaker in found:
            results.append({
                "politician": speaker,
                "quote": quote_text.strip(),
                "source": art.get("source"),
                "url": art.get("url")
            })

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"🎯 Captured {len(results)} high-quality political quotes.")

if __name__ == "__main__":
    extract_specific_quotes()
