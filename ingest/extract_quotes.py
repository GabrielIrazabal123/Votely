import json
import os
import spacy
import re
from fastcoref import FCoref
from bs4 import BeautifulSoup

# 1. Load the AI Models
print("🧠 Loading AI Models (this may take a minute)...")
# 'en_core_web_trf' is the high-accuracy Transformer model
nlp = spacy.load("en_core_web_trf")  
coref_model = FCoref()

def extract_quotes_ai():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: {raw_path} not found. Please run your scraper first.")
        return

    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []
    
    print(f"🚀 Processing {len(articles)} articles with AI...")

    for art in articles:
        # Step A: Clean HTML to get plain text
        raw_html = art.get('content', '')
        text = BeautifulSoup(raw_html, "html.parser").get_text()
        
        # Step B: AI Coreference Resolution (Fixes "He" -> "Politician Name")
        # In the newest fastcoref, use .text instead of .get_resolved_content()
        preds = coref_model.predict(texts=[text])
        resolved_text = preds[0].text
        
        # Step C: Use spaCy to "read" the resolved text
        doc = nlp(resolved_text)
        
        # Step D: Grammar-based Quote Extraction
        for sent in doc.sents:
            # Filter 1: Ignore fragments shorter than 5 words
            if len(sent.text.split()) < 5:
                continue
                
            for token in sent:
                # Look for verbs of 'speech' (lemmatized)
                if token.lemma_ in ["say", "tell", "warn", "add", "state", "claim", "argue"]:
                    
                    # Find the subject (the speaker) of that verb
                    speaker_tokens = [w for w in token.children if w.dep_ == "nsubj"]
                    if speaker_tokens:
                        speaker_name = speaker_tokens[0].text
                        
                        # Filter 2: Verify the speaker is a PERSON known to the AI
                        is_person = any(ent.text == speaker_name and ent.label_ == "PERSON" for ent in doc.ents)
                        
                        if is_person:
                            # Step E: Find the actual text inside quote marks
                            # This Regex looks for various types of curly and straight quotes
                            quote_match = re.search(r'[“\"‘](.{15,500}?)[”\"’]', sent.text)
                            
                            if quote_match:
                                found_quote = quote_match.group(1).strip()
                                
                                # Filter 3: Final check for "sentence-ending" logic
                                # Discards quotes that end in common conjunctions (sign of a bad cut)
                                if found_quote.lower().endswith((" and", " the", " with", " we", " of")):
                                    continue
                                
                                # Step F: Upgrade to Full Name if possible
                                # Changes "Starmer" to "Keir Starmer" if found elsewhere in doc
                                full_name = speaker_name
                                for ent in doc.ents:
                                    if ent.label_ == "PERSON" and speaker_name in ent.text and len(ent.text) > len(full_name):
                                        full_name = ent.text
                                
                                all_found_quotes.append({
                                    "politician": full_name,
                                    "quote": found_quote,
                                    "source": "The Guardian",
                                    "url": art.get("url")
                                })

    # Step G: Remove duplicates and save
    # We use the quote text as the unique key
    unique_quotes = {q['quote']: q for q in all_found_quotes}.values()
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(list(unique_quotes), f, indent=2)
    
    print("-" * 30)
    print(f"💎 SUCCESS: {len(unique_quotes)} clean quotes saved to {output_path}")

if __name__ == "__main__":
    extract_quotes_ai()
