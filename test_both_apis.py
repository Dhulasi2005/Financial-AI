#!/usr/bin/env python3
"""
Test script to verify both NewsAPI and RSS APIs work together
"""
import os
from dotenv import load_dotenv
from news_scraper import fetch_news_by_country as newsapi_fetch
from rss_scraper import fetch_news_by_country as rss_fetch

# Load environment variables
load_dotenv()

def test_both_apis():
    """Test both NewsAPI and RSS APIs"""
    
    # Check if API key is set
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        print("⚠️  NEWSAPI_KEY not found - NewsAPI will not work")
    else:
        print(f"✅ NewsAPI Key found: {api_key[:10]}...")
    
    print("✅ RSS feeds available (no API key needed)")
    
    # Test countries
    test_countries = ["us", "in", "gb", "au"]
    
    for country in test_countries:
        print(f"\n🔍 Testing {country.upper()}:")
        
        # Test NewsAPI
        if api_key:
            try:
                newsapi_articles = newsapi_fetch(country=country, page_size=5)
                print(f"  ✅ NewsAPI: {len(newsapi_articles)} articles")
                if newsapi_articles:
                    print(f"     First: {newsapi_articles[0]['title'][:50]}...")
            except Exception as e:
                print(f"  ❌ NewsAPI: {str(e)}")
        else:
            print("  ⚠️  NewsAPI: Skipped (no API key)")
        
        # Test RSS
        try:
            rss_articles = rss_fetch(country=country, page_size=5)
            print(f"  ✅ RSS: {len(rss_articles)} articles")
            if rss_articles:
                print(f"     First: {rss_articles[0]['title'][:50]}...")
        except Exception as e:
            print(f"  ❌ RSS: {str(e)}")
    
    print(f"\n📊 Summary:")
    print(f"  • NewsAPI: {'Available' if api_key else 'No API key'}")
    print(f"  • RSS Feeds: Available")
    print(f"  • Recommendation: Use 'Both NewsAPI + RSS' for best coverage")

if __name__ == "__main__":
    test_both_apis()
