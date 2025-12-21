import os
import requests
import json
from dotenv import load_dotenv

# 1. Load the secret key from your .env file
load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")

def fetch_politics_data():
    # NYT Article Search API endpoint
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    
    # We are asking for the most recent articles in the Politics section
    params = {
        "fq": 'section_name:"Politics"',
        "api-key": API_KEY,
        "sort": "newest"
    }
    
    print("Checking New York Times for latest politics articles...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 2. Save the result into your data/raw/ folder
        # This matches your sidebar structure exactly
        file_path = os.path.join("data", "raw", "nyt_articles.json")
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Success! Raw data saved to: {file_path}")
    else:
        print(f"❌ Error: {response.status_code}")
        print("Check if your API Key in .env is correct.")

if __name__ == "__main__":
    fetch_politics_data()
