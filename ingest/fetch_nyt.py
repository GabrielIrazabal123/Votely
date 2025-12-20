import os
import requests
import json
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_nyt_politics():
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    
    # We are searching for articles in the 'Politics' section
    params = {
        "fq": 'section_name:"Politics"',
        "api-key": API_KEY,
        "sort": "newest"
    }
    
    print("Fetching data from NYT...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Save to your existing data/raw folder
        file_path = os.path.join("data", "raw", "nyt_articles.json")
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Success! Raw data saved to {file_path}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_nyt_politics()
