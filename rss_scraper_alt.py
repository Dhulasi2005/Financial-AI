import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def parse_rss_feed(url: str) -> List[Dict]:
    """
    Parse RSS feed using xml.etree instead of feedparser
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        articles = []
        
        # Handle different RSS formats
        for item in root.findall('.//item'):
            article = {}
            
            # Extract title
            title_elem = item.find('title')
            if title_elem is not None:
                article['title'] = title_elem.text.strip() if title_elem.text else ''
            
            # Extract description
            desc_elem = item.find('description')
            if desc_elem is not None:
                article['description'] = desc_elem.text.strip() if desc_elem.text else ''
            
            # Extract link
            link_elem = item.find('link')
            if link_elem is not None:
                article['url'] = link_elem.text.strip() if link_elem.text else ''
            
            # Extract publication date
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # Parse common date formats
                    date_str = pub_date_elem.text.strip()
                    # Try different date formats
                    for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z']:
                        try:
                            article['publishedAt'] = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        article['publishedAt'] = datetime.utcnow()
                except Exception as e:
                    logger.warning(f"Could not parse date: {e}")
                    article['publishedAt'] = datetime.utcnow()
            else:
                article['publishedAt'] = datetime.utcnow()
            
            # Extract source
            source_elem = item.find('source')
            if source_elem is not None:
                article['source'] = source_elem.text.strip() if source_elem.text else 'RSS Feed'
            else:
                article['source'] = 'RSS Feed'
            
            if article.get('title') and article.get('url'):
                articles.append(article)
        
        return articles
        
    except Exception as e:
        logger.error(f"Error parsing RSS feed {url}: {e}")
        return []

def fetch_news_by_country(country_code: str, limit: int = 20) -> List[Dict]:
    """
    Fetch RSS news for a specific country
    """
    # Define RSS feeds for different countries - using more reliable sources
    rss_feeds = {
        'US': [
            'https://feeds.reuters.com/reuters/businessNews',
            'https://feeds.reuters.com/reuters/technologyNews',
            'https://rss.cnn.com/rss/money_latest.rss',
            'https://feeds.npr.org/1007/rss.xml'  # Business news
        ],
        'IN': [
            'https://feeds.financialexpress.com/latest-news',
            'https://www.moneycontrol.com/rss/business.xml',
            'https://economictimes.indiatimes.com/rss.cms'
        ],
        'GB': [
            'https://feeds.bbci.co.uk/news/business/rss.xml',
            'https://www.ft.com/rss/home',
            'https://feeds.skynews.com/feeds/rss/business.xml'
        ],
        'CA': [
            'https://feeds.globalnews.ca/GlobalNewsBusiness.xml',
            'https://www.cbc.ca/cmlink/rss-business',
            'https://feeds.financialpost.com/financialpost/business'
        ],
        'AU': [
            'https://feeds.abc.net.au/abcnews/business.xml',
            'https://www.afr.com/rss/feed.xml',
            'https://feeds.smh.com.au/rss/business.xml'
        ]
    }
    
    feeds = rss_feeds.get(country_code.upper(), [])
    all_articles = []
    
    for feed_url in feeds:
        try:
            articles = parse_rss_feed(feed_url)
            all_articles.extend(articles)
            print(f"✅ Fetched {len(articles)} articles from {feed_url}")
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_url}: {e}")
            print(f"❌ Failed to fetch from {feed_url}: {e}")
    
    # Sort by publication date (newest first)
    all_articles.sort(key=lambda x: x.get('publishedAt', datetime.min), reverse=True)
    
    return all_articles[:limit]

def fetch_international_financial_news(limit: int = 20) -> List[Dict]:
    """
    Fetch international financial news from RSS feeds
    """
    international_feeds = [
        'https://feeds.reuters.com/reuters/businessNews',
        'https://feeds.bbci.co.uk/news/business/rss.xml',
        'https://www.ft.com/rss/home',
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.reuters.com/Reuters/businessNews',
        'https://feeds.npr.org/1007/rss.xml'
    ]
    
    all_articles = []
    
    for feed_url in international_feeds:
        try:
            articles = parse_rss_feed(feed_url)
            all_articles.extend(articles)
            print(f"✅ Fetched {len(articles)} articles from {feed_url}")
        except Exception as e:
            logger.error(f"Error fetching international RSS feed {feed_url}: {e}")
            print(f"❌ Failed to fetch from {feed_url}: {e}")
    
    # Sort by publication date (newest first)
    all_articles.sort(key=lambda x: x.get('publishedAt', datetime.min), reverse=True)
    
    return all_articles[:limit]

def fetch_global_financial_news(limit: int = 20) -> List[Dict]:
    """
    Fetch global financial news from multiple RSS sources
    """
    global_feeds = [
        'https://feeds.reuters.com/reuters/businessNews',
        'https://feeds.bbci.co.uk/news/business/rss.xml',
        'https://www.ft.com/rss/home',
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.reuters.com/Reuters/businessNews',
        'https://feeds.financialexpress.com/latest-news',
        'https://rss.cnn.com/rss/money_latest.rss',
        'https://feeds.npr.org/1007/rss.xml'
    ]
    
    all_articles = []
    
    for feed_url in global_feeds:
        try:
            articles = parse_rss_feed(feed_url)
            all_articles.extend(articles)
            print(f"✅ Fetched {len(articles)} articles from {feed_url}")
        except Exception as e:
            logger.error(f"Error fetching global RSS feed {feed_url}: {e}")
            print(f"❌ Failed to fetch from {feed_url}: {e}")
    
    # Sort by publication date (newest first)
    all_articles.sort(key=lambda x: x.get('publishedAt', datetime.min), reverse=True)
    
    return all_articles[:limit]

def get_supported_countries() -> List[str]:
    """
    Get list of supported countries for RSS feeds
    """
    return ['US', 'IN', 'GB', 'CA', 'AU']
