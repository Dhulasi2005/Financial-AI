#!/usr/bin/env python3
"""
Test script to debug news fetching issues
"""
import os
from dotenv import load_dotenv
from news_scraper import fetch_news_by_country, get_supported_countries

# Load environment variables
load_dotenv()

def test_news_fetching():
    """Test news fetching for different countries"""
    
    # Check if API key is set
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        print("❌ NEWSAPI_KEY not found in environment variables")
        print("Please set NEWSAPI_KEY in your .env file")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test countries
    test_countries = ["us", "in", "gb", "cn", "jp"]
    
    for country in test_countries:
        print(f"\n🔍 Testing news fetch for country: {country}")
        try:
            articles = fetch_news_by_country(country=country, page_size=5)
            print(f"✅ Successfully fetched {len(articles)} articles for {country}")
            if articles:
                print(f"   First article: {articles[0]['title'][:50]}...")
        except Exception as e:
            print(f"❌ Error fetching news for {country}: {str(e)}")
    
    # Show supported countries
    print(f"\n📋 Supported countries: {len(get_supported_countries())}")
    for code, name in list(get_supported_countries().items())[:10]:
        print(f"   {code}: {name}")

if __name__ == "__main__":
    test_news_fetching()
