import requests
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import time
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class RSSFeedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # RSS Feed sources organized by category and region
        self.rss_feeds = {
            "global": {
                "reuters": "https://feeds.reuters.com/reuters/businessNews",
                "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
                "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
                "wsj": "https://feeds.wsj.com/public/rss/2_0/rss.xml",
                "ft": "https://www.ft.com/rss/home",
                "yahoo_finance": "https://feeds.finance.yahoo.com/rss/2.0/headline",
                "investing": "https://www.investing.com/rss/news_301.rss"
            },
            "us": {
                "cnn_business": "http://rss.cnn.com/rss/money_latest.rss",
                "fox_business": "https://feeds.foxnews.com/foxnews/business",
                "abc_business": "https://abcnews.go.com/abcnews/usheadlines",
                "nbc_business": "https://feeds.nbcnews.com/nbcnews/public/business"
            },
            "in": {
                "times_of_india": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
                "ndtv": "https://feeds.feedburner.com/ndtvnews-top-stories",
                "hindustan_times": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
                "economic_times": "https://economictimes.indiatimes.com/rss.cms",
                "business_standard": "https://www.business-standard.com/rss/india-news-6.rss",
                "moneycontrol": "https://www.moneycontrol.com/rss/business.xml"
            },
            "gb": {
                "bbc_business": "https://feeds.bbci.co.uk/news/business/rss.xml",
                "guardian_business": "https://www.theguardian.com/business/rss",
                "telegraph_business": "https://www.telegraph.co.uk/business/rss.xml",
                "sky_business": "https://feeds.skynews.com/feeds/rss/business.xml"
            },
            "au": {
                "abc_news": "https://www.abc.net.au/news/feed/45910/rss.xml",
                "sbs_news": "https://www.sbs.com.au/news/feed",
                "smh_business": "https://www.smh.com.au/rss/feed.xml"
            },
            "ca": {
                "cbc_business": "https://www.cbc.ca/cmlink/rss-business",
                "globe_mail": "https://www.theglobeandmail.com/feed/business/",
                "national_post": "https://nationalpost.com/feed/"
            },
            "sg": {
                "straits_times": "https://www.straitstimes.com/news/singapore/rss.xml",
                "channel_news_asia": "https://www.channelnewsasia.com/api/v1/rss-feeds",
                "today_online": "https://www.todayonline.com/feed"
            },
            "jp": {
                "nikkei": "https://www.nikkei.com/rss/english/nikkei_news.rdf",
                "reuters_japan": "https://feeds.reuters.com/reuters/businessNews",
                "japan_times": "https://www.japantimes.co.jp/feed/"
            }
        }

    def fetch_rss_feed(self, feed_url: str, max_articles: int = 20) -> List[Dict]:
        """
        Fetch and parse RSS feed from a given URL
        """
        try:
            # Parse the RSS feed
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                print(f"Warning: Feed parsing issues for {feed_url}")
            
            articles = []
            for entry in feed.entries[:max_articles]:
                # Extract publication date
                published_at = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_at = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_at = datetime(*entry.updated_parsed[:6])
                
                # Extract source name from URL
                source_name = self._extract_source_name(feed_url)
                
                article = {
                    "title": entry.get('title', ''),
                    "description": entry.get('summary', ''),
                    "url": entry.get('link', ''),
                    "source": source_name,
                    "publishedAt": published_at,
                    "country": self._determine_country_from_url(feed_url)
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error fetching RSS feed {feed_url}: {str(e)}")
            return []

    def fetch_news_by_country(self, country: str = "us", max_articles: int = 50) -> List[Dict]:
        """
        Fetch news from RSS feeds for a specific country
        """
        country = country.lower()
        
        # Get feeds for the country
        country_feeds = self.rss_feeds.get(country, {})
        global_feeds = self.rss_feeds.get("global", {})
        
        # Combine country-specific and global feeds
        all_feeds = {**global_feeds, **country_feeds}
        
        all_articles = []
        
        for source_name, feed_url in all_feeds.items():
            try:
                articles = self.fetch_rss_feed(feed_url, max_articles // len(all_feeds))
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} articles from {source_name}")
            except Exception as e:
                print(f"Error fetching from {source_name}: {str(e)}")
                continue
        
        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get("publishedAt") or datetime.min, reverse=True)
        
        return all_articles[:max_articles]

    def fetch_international_news(self, max_articles: int = 100) -> List[Dict]:
        """
        Fetch news from multiple international sources
        """
        all_articles = []
        
        for country, feeds in self.rss_feeds.items():
            if country == "global":
                continue
                
            for source_name, feed_url in feeds.items():
                try:
                    articles = self.fetch_rss_feed(feed_url, max_articles // (len(self.rss_feeds) - 1))
                    all_articles.extend(articles)
                    print(f"Fetched {len(articles)} articles from {source_name} ({country})")
                except Exception as e:
                    print(f"Error fetching from {source_name}: {str(e)}")
                    continue
        
        # Sort by publication date
        all_articles.sort(key=lambda x: x.get("publishedAt") or datetime.min, reverse=True)
        
        return all_articles[:max_articles]

    def fetch_global_financial_news(self, query: str = "financial markets", max_articles: int = 50) -> List[Dict]:
        """
        Fetch global financial news from major financial sources
        """
        financial_feeds = {
            "reuters": "https://feeds.reuters.com/reuters/businessNews",
            "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
            "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
            "wsj": "https://feeds.wsj.com/public/rss/2_0/rss.xml",
            "ft": "https://www.ft.com/rss/home",
            "yahoo_finance": "https://feeds.finance.yahoo.com/rss/2.0/headline",
            "investing": "https://www.investing.com/rss/news_301.rss"
        }
        
        all_articles = []
        
        for source_name, feed_url in financial_feeds.items():
            try:
                articles = self.fetch_rss_feed(feed_url, max_articles // len(financial_feeds))
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} financial articles from {source_name}")
            except Exception as e:
                print(f"Error fetching from {source_name}: {str(e)}")
                continue
        
        # Sort by publication date
        all_articles.sort(key=lambda x: x.get("publishedAt") or datetime.min, reverse=True)
        
        return all_articles[:max_articles]

    def _extract_source_name(self, url: str) -> str:
        """
        Extract source name from RSS feed URL
        """
        try:
            domain = urlparse(url).netloc
            if 'reuters.com' in domain:
                return 'Reuters'
            elif 'bloomberg.com' in domain:
                return 'Bloomberg'
            elif 'cnbc.com' in domain:
                return 'CNBC'
            elif 'marketwatch.com' in domain:
                return 'MarketWatch'
            elif 'wsj.com' in domain:
                return 'Wall Street Journal'
            elif 'ft.com' in domain:
                return 'Financial Times'
            elif 'yahoo.com' in domain:
                return 'Yahoo Finance'
            elif 'investing.com' in domain:
                return 'Investing.com'
            elif 'cnn.com' in domain:
                return 'CNN'
            elif 'foxnews.com' in domain:
                return 'Fox Business'
            elif 'abcnews.go.com' in domain:
                return 'ABC News'
            elif 'nbcnews.com' in domain:
                return 'NBC News'
            elif 'timesofindia.indiatimes.com' in domain:
                return 'Times of India'
            elif 'ndtv.com' in domain:
                return 'NDTV'
            elif 'hindustantimes.com' in domain:
                return 'Hindustan Times'
            elif 'economictimes.indiatimes.com' in domain:
                return 'Economic Times'
            elif 'business-standard.com' in domain:
                return 'Business Standard'
            elif 'moneycontrol.com' in domain:
                return 'Moneycontrol'
            elif 'bbc.co.uk' in domain:
                return 'BBC'
            elif 'theguardian.com' in domain:
                return 'The Guardian'
            elif 'telegraph.co.uk' in domain:
                return 'The Telegraph'
            elif 'sky.com' in domain:
                return 'Sky News'
            elif 'abc.net.au' in domain:
                return 'ABC News Australia'
            elif 'sbs.com.au' in domain:
                return 'SBS News'
            elif 'smh.com.au' in domain:
                return 'Sydney Morning Herald'
            elif 'cbc.ca' in domain:
                return 'CBC News'
            elif 'theglobeandmail.com' in domain:
                return 'The Globe and Mail'
            elif 'nationalpost.com' in domain:
                return 'National Post'
            elif 'straitstimes.com' in domain:
                return 'The Straits Times'
            elif 'channelnewsasia.com' in domain:
                return 'Channel News Asia'
            elif 'todayonline.com' in domain:
                return 'Today Online'
            elif 'nikkei.com' in domain:
                return 'Nikkei'
            elif 'japantimes.co.jp' in domain:
                return 'The Japan Times'
            else:
                return domain.replace('www.', '').replace('.com', '').title()
        except:
            return 'Unknown Source'

    def _determine_country_from_url(self, url: str) -> str:
        """
        Determine country from RSS feed URL
        """
        if 'indiatimes.com' in url or 'ndtv.com' in url or 'hindustantimes.com' in url:
            return 'IN'
        elif 'bbc.co.uk' in url or 'theguardian.com' in url or 'telegraph.co.uk' in url:
            return 'GB'
        elif 'abc.net.au' in url or 'sbs.com.au' in url or 'smh.com.au' in url:
            return 'AU'
        elif 'cbc.ca' in url or 'theglobeandmail.com' in url or 'nationalpost.com' in url:
            return 'CA'
        elif 'straitstimes.com' in url or 'channelnewsasia.com' in url or 'todayonline.com' in url:
            return 'SG'
        elif 'nikkei.com' in url or 'japantimes.co.jp' in url:
            return 'JP'
        else:
            return 'GLOBAL'

    def get_supported_countries(self) -> Dict[str, str]:
        """
        Return list of supported countries
        """
        return {
            "us": "United States",
            "gb": "United Kingdom",
            "in": "India",
            "ca": "Canada",
            "au": "Australia",
            "sg": "Singapore",
            "jp": "Japan"
        }

    def test_feeds(self):
        """
        Test RSS feeds to see which ones are working
        """
        print("Testing RSS feeds...")
        
        for country, feeds in self.rss_feeds.items():
            print(f"\n{country.upper()} feeds:")
            for source, url in feeds.items():
                try:
                    articles = self.fetch_rss_feed(url, 1)
                    if articles:
                        print(f"  ✅ {source}: {len(articles)} articles")
                    else:
                        print(f"  ❌ {source}: No articles")
                except Exception as e:
                    print(f"  ❌ {source}: Error - {str(e)}")

# Create a global instance
rss_scraper = RSSFeedScraper()

# Convenience functions for backward compatibility
def fetch_news_by_country(country="us", page_size=50):
    """Fetch news from RSS feeds for a specific country"""
    return rss_scraper.fetch_news_by_country(country, page_size)

def fetch_international_financial_news(page_size=100):
    """Fetch international news from RSS feeds"""
    return rss_scraper.fetch_international_news(page_size)

def fetch_global_financial_news(query="financial markets", page_size=50):
    """Fetch global financial news from RSS feeds"""
    return rss_scraper.fetch_global_financial_news(query, page_size)

def get_supported_countries():
    """Return list of supported countries"""
    return rss_scraper.get_supported_countries()

if __name__ == "__main__":
    # Test the RSS scraper
    rss_scraper.test_feeds()
