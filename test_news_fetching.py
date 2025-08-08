#!/usr/bin/env python3
"""
Test script to check news fetching functionality
"""

import os
import sys
from datetime import datetime

def test_newsapi():
    """Test NewsAPI functionality"""
    print("🔍 Testing NewsAPI...")
    
    try:
        from news_scraper import fetch_news_by_country
        
        # Check if API key is set
        from config import Config
        config = Config()
        api_key = config.NEWSAPI_KEY
        
        if not api_key or api_key == "":
            print("❌ NewsAPI key not configured")
            print("💡 Please set NEWSAPI_KEY environment variable")
            return False
        
        print(f"✅ NewsAPI key found: {api_key[:10]}...")
        
        # Test fetching news
        articles = fetch_news_by_country(country="us", page_size=5)
        print(f"✅ Successfully fetched {len(articles)} articles from NewsAPI")
        
        if articles:
            print("📰 Sample article:")
            article = articles[0]
            print(f"   Title: {article.get('title', 'N/A')[:50]}...")
            print(f"   Source: {article.get('source', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ NewsAPI error: {e}")
        return False

def test_rss_feeds():
    """Test RSS feed functionality"""
    print("\n🔍 Testing RSS feeds...")
    
    try:
        # Try original RSS scraper first
        try:
            from rss_scraper import fetch_news_by_country as rss_fetch
            print("✅ Original RSS scraper loaded")
            articles = rss_fetch(country="US", page_size=5)
            print(f"✅ Successfully fetched {len(articles)} articles from original RSS")
            return True
        except ImportError as e:
            print(f"⚠️  Original RSS scraper not available: {e}")
        
        # Try alternative RSS scraper
        try:
            from rss_scraper_alt import fetch_news_by_country as rss_fetch
            print("✅ Alternative RSS scraper loaded")
            articles = rss_fetch(country="US", page_size=5)
            print(f"✅ Successfully fetched {len(articles)} articles from alternative RSS")
            
            if articles:
                print("📰 Sample RSS article:")
                article = articles[0]
                print(f"   Title: {article.get('title', 'N/A')[:50]}...")
                print(f"   Source: {article.get('source', 'N/A')}")
                print(f"   URL: {article.get('url', 'N/A')[:50]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Alternative RSS scraper error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ RSS test error: {e}")
        return False

def test_app_integration():
    """Test app integration"""
    print("\n🔍 Testing app integration...")
    
    try:
        from app import app
        
        with app.app_context():
            from models import db, NewsItem
            
            # Check if we can access the database
            news_count = NewsItem.query.count()
            print(f"✅ Database accessible, {news_count} news items stored")
            
            # Test sentiment analysis
            from sentiment import analyze_text
            result = analyze_text("This is a positive financial news about market growth.")
            print(f"✅ Sentiment analysis working: {result}")
            
        return True
        
    except Exception as e:
        print(f"❌ App integration error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing news fetching functionality...\n")
    
    success = True
    success &= test_newsapi()
    success &= test_rss_feeds()
    success &= test_app_integration()
    
    print(f"\n{'='*50}")
    if success:
        print("🎉 All tests passed! News fetching should work.")
    else:
        print("❌ Some tests failed. Check the issues above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
