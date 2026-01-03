import json, os, spacy
from fastcoref import FCoref
from bs4 import BeautifulSoup

# 1. Load the AI Models
print("🧠 Loading AI Models (this may take a minute)...")
nlp = spacy.load("en_core_web_trf")  # High-accuracy transformer
coref_model = FCoref()               # Coreference engine

def extract_quotes_ai():
    raw_path = "data/raw/all_articles.json"
    output_path = "data/quotes/final_database.json"
    
    with open(raw_path, "r") as f:
        articles = json.load(f)

    all_found_quotes = []

    for art in articles:
        # Step A: Clean HTML and prepare text
        text = BeautifulSoup(art.get('content', ''), "html.parser").get_text()
        
        # Step B: AI Coreference Resolution
        # This replaces "He" with "Trump" throughout the text
        preds = coref_model.predict(texts=[text])
        resolved_text = preds[0].text
        
        # Step C: Use spaCy to "read" the sentences
        doc = nlp(resolved_text)
        
        # Step D: Extract Speaker + Quote
        # We look for verbs of 'speech' (said, told, warned)
        for sent in doc.sents:
            for token in sent:
                if token.lemma_ in ["say", "tell", "warn", "add", "state"]:
                    # Look for the subject (the speaker) and the object (the quote)
                    speaker = [w for w in token.children if w.dep_ == "nsubj"]
                    if speaker:
                        speaker_name = speaker[0].text
                        
                        # Only keep if the speaker is a recognized PERSON entity
                        if any(ent.text == speaker_name and ent.label_ == "PERSON" for ent in doc.ents):
                            # Find text in quotes within this sentence
                            quote_match = re.search(r'[“\"‘](.{10,500}?)[”\"’]', sent.text)
                            if quote_match:
                                all_found_quotes.append({
                                    "politician": speaker_name,
                                    "quote": quote_match.group(1).strip(),
                                    "url": art.get("url")
                                })

    # Save unique results
    unique_quotes = {q['quote']: q for q in all_found_quotes}.values()
    with open(output_path, "w") as f:
        json.dump(list(unique_quotes), f, indent=2)
    
    print(f"💎 AI SUCCESS: Found {len(unique_quotes)} high-precision quotes.")

if __name__ == "__main__":
    extract_quotes_ai()
