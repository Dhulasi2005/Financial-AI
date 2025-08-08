#!/usr/bin/env python3
"""
Fallback news source for when external APIs fail
"""

from datetime import datetime, timedelta
from typing import List, Dict
import random

# Sample financial news articles
SAMPLE_NEWS = [
    {
        "title": "Global Markets Show Resilience Amid Economic Uncertainty",
        "description": "Major indices demonstrate stability as investors assess inflation data and central bank policies.",
        "source": "Financial Times",
        "url": "https://example.com/news/global-markets-resilience",
        "publishedAt": datetime.utcnow() - timedelta(hours=2),
        "country": "US"
    },
    {
        "title": "Tech Sector Leads Market Recovery",
        "description": "Technology stocks outperform as earnings season begins with strong quarterly results.",
        "source": "Reuters",
        "url": "https://example.com/news/tech-sector-recovery",
        "publishedAt": datetime.utcnow() - timedelta(hours=4),
        "country": "US"
    },
    {
        "title": "European Markets Respond to ECB Policy Changes",
        "description": "European indices gain ground following European Central Bank's latest monetary policy announcement.",
        "source": "Bloomberg",
        "url": "https://example.com/news/european-markets-ecb",
        "publishedAt": datetime.utcnow() - timedelta(hours=6),
        "country": "GB"
    },
    {
        "title": "Asian Markets Show Mixed Performance",
        "description": "Regional markets display varied performance as traders react to local economic indicators.",
        "source": "Nikkei",
        "url": "https://example.com/news/asian-markets-mixed",
        "publishedAt": datetime.utcnow() - timedelta(hours=8),
        "country": "JP"
    },
    {
        "title": "Commodity Prices Stabilize After Recent Volatility",
        "description": "Oil and precious metals find equilibrium as supply concerns ease and demand patterns normalize.",
        "source": "MarketWatch",
        "url": "https://example.com/news/commodity-prices-stabilize",
        "publishedAt": datetime.utcnow() - timedelta(hours=10),
        "country": "US"
    },
    {
        "title": "Cryptocurrency Markets Experience Renewed Interest",
        "description": "Digital assets gain traction as institutional adoption increases and regulatory clarity improves.",
        "source": "CoinDesk",
        "url": "https://example.com/news/crypto-renewed-interest",
        "publishedAt": datetime.utcnow() - timedelta(hours=12),
        "country": "US"
    },
    {
        "title": "Real Estate Sector Shows Signs of Recovery",
        "description": "Property markets demonstrate resilience as interest rates stabilize and demand remains strong.",
        "source": "Wall Street Journal",
        "url": "https://example.com/news/real-estate-recovery",
        "publishedAt": datetime.utcnow() - timedelta(hours=14),
        "country": "US"
    },
    {
        "title": "Green Energy Investments Surge",
        "description": "Renewable energy sector attracts significant capital as sustainability becomes a priority.",
        "source": "Financial Times",
        "url": "https://example.com/news/green-energy-investments",
        "publishedAt": datetime.utcnow() - timedelta(hours=16),
        "country": "GB"
    },
    {
        "title": "Banking Sector Reports Strong Quarterly Results",
        "description": "Major financial institutions exceed earnings expectations as loan demand increases.",
        "source": "Reuters",
        "url": "https://example.com/news/banking-strong-results",
        "publishedAt": datetime.utcnow() - timedelta(hours=18),
        "country": "US"
    },
    {
        "title": "Emerging Markets Attract Investor Attention",
        "description": "Developing economies show promise as growth prospects improve and valuations remain attractive.",
        "source": "Bloomberg",
        "url": "https://example.com/news/emerging-markets-attention",
        "publishedAt": datetime.utcnow() - timedelta(hours=20),
        "country": "IN"
    }
]

def get_fallback_news(country="us", limit=20) -> List[Dict]:
    """
    Get fallback news when external APIs fail
    """
    print("⚠️  Using fallback news source due to API limitations")
    
    # Filter by country if specified
    if country and country.lower() != "global":
        filtered_news = [article for article in SAMPLE_NEWS if article.get("country", "").lower() == country.lower()]
        if not filtered_news:
            # If no country-specific news, return random articles
            filtered_news = SAMPLE_NEWS
    else:
        filtered_news = SAMPLE_NEWS
    
    # Shuffle and limit
    random.shuffle(filtered_news)
    return filtered_news[:limit]

def get_fallback_international_news(limit=20) -> List[Dict]:
    """
    Get fallback international news
    """
    print("⚠️  Using fallback international news source")
    
    # Select articles from different countries
    international_news = [
        article for article in SAMPLE_NEWS 
        if article.get("country") in ["US", "GB", "JP", "IN"]
    ]
    
    random.shuffle(international_news)
    return international_news[:limit]

def get_fallback_global_news(limit=20) -> List[Dict]:
    """
    Get fallback global news
    """
    print("⚠️  Using fallback global news source")
    
    # Return all available news
    global_news = SAMPLE_NEWS.copy()
    random.shuffle(global_news)
    return global_news[:limit]
