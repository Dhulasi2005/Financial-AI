import requests
from datetime import datetime
from config import Config

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/top-headlines"
NEWSAPI_SEARCH_ENDPOINT = "https://newsapi.org/v2/everything"

# Comprehensive list of supported countries with their codes
SUPPORTED_COUNTRIES = {
    "us": "United States",
    "gb": "United Kingdom", 
    "in": "India",
    "ca": "Canada",
    "au": "Australia",
    "de": "Germany",
    "fr": "France",
    "jp": "Japan",
    "cn": "China",
    "sg": "Singapore",
    "hk": "Hong Kong",
    "kr": "South Korea",
    "br": "Brazil",
    "mx": "Mexico",
    "ar": "Argentina",
    "za": "South Africa",
    "ru": "Russia",
    "it": "Italy",
    "es": "Spain",
    "nl": "Netherlands",
    "se": "Sweden",
    "no": "Norway",
    "ch": "Switzerland",
    "at": "Austria",
    "be": "Belgium",
    "dk": "Denmark",
    "fi": "Finland",
    "ie": "Ireland",
    "nz": "New Zealand",
    "ae": "United Arab Emirates",
    "sa": "Saudi Arabia",
    "tr": "Turkey",
    "pl": "Poland",
    "cz": "Czech Republic",
    "hu": "Hungary",
    "ro": "Romania",
    "bg": "Bulgaria",
    "hr": "Croatia",
    "si": "Slovenia",
    "sk": "Slovakia",
    "lt": "Lithuania",
    "lv": "Latvia",
    "ee": "Estonia",
    "mt": "Malta",
    "cy": "Cyprus",
    "gr": "Greece",
    "pt": "Portugal",
    "lu": "Luxembourg"
}

def fetch_news_by_country(country="us", category="business", page_size=50):
    """
    Fetch news from a specific country
    country: 'us', 'gb', 'in', etc.
    """
    key = Config().NEWSAPI_KEY
    
    # Check if API key is set
    if not key or key == "":
        raise Exception("NewsAPI key not configured. Please set NEWSAPI_KEY environment variable or add it to .env file")
    
    # First try with country-specific endpoint
    params = {
        "apiKey": key,
        "pageSize": page_size,
        "category": category,
    }
    if country:
        params["country"] = country
    
    try:
        resp = requests.get(NEWSAPI_ENDPOINT, params=params, timeout=20)
        
        # Handle rate limiting
        if resp.status_code == 429:
            print("⚠️  NewsAPI rate limit reached. Using fallback method...")
            return fetch_news_by_country_search(country, page_size)
        
        resp.raise_for_status()
        data = resp.json()
        
        # Check for API errors
        if data.get("status") == "error":
            error_msg = data.get('message', 'Unknown error')
            if "rateLimited" in error_msg or "429" in error_msg:
                print("⚠️  NewsAPI rate limit reached. Using fallback method...")
                return fetch_news_by_country_search(country, page_size)
            else:
                raise Exception(f"NewsAPI error: {error_msg}")
            
        articles = data.get("articles", [])
        
        # If no articles found, try search endpoint with country-specific terms
        if not articles:
            print(f"No articles found for country {country}, trying search endpoint...")
            return fetch_news_by_country_search(country, page_size)
        
        results = []
        for a in articles:
            published_at = None
            if a.get("publishedAt"):
                try:
                    published_at = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00"))
                except Exception:
                    published_at = None
            results.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "source": a.get("source", {}).get("name"),
                "publishedAt": published_at,
                "country": country.upper()
            })
        return results
    except requests.exceptions.RequestException as e:
        raise Exception(f"NewsAPI request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"NewsAPI error: {str(e)}")

def fetch_news_by_country_search(country="us", page_size=50):
    """
    Fallback method to fetch news using search endpoint for countries that don't have direct support
    """
    key = Config().NEWSAPI_KEY
    
    # Country-specific search terms
    country_terms = {
        "in": "India business finance economy",
        "cn": "China business finance economy",
        "jp": "Japan business finance economy",
        "kr": "South Korea business finance economy",
        "sg": "Singapore business finance economy",
        "hk": "Hong Kong business finance economy",
        "br": "Brazil business finance economy",
        "mx": "Mexico business finance economy",
        "ar": "Argentina business finance economy",
        "za": "South Africa business finance economy",
        "ru": "Russia business finance economy",
        "tr": "Turkey business finance economy",
        "ae": "UAE business finance economy",
        "sa": "Saudi Arabia business finance economy"
    }
    
    # Get search term for the country
    search_term = country_terms.get(country.lower(), f"{country} business finance")
    
    params = {
        "apiKey": key,
        "q": search_term,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "domains": "reuters.com,bloomberg.com,cnbc.com,marketwatch.com,wsj.com,ft.com,cnn.com,bbc.com,timesofindia.indiatimes.com,ndtv.com,hindustantimes.com"
    }
    
    try:
        resp = requests.get(NEWSAPI_SEARCH_ENDPOINT, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("status") == "error":
            raise Exception(f"NewsAPI search error: {data.get('message', 'Unknown error')}")
            
        articles = data.get("articles", [])
        results = []
        for a in articles:
            published_at = None
            if a.get("publishedAt"):
                try:
                    published_at = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00"))
                except Exception:
                    published_at = None
            results.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "source": a.get("source", {}).get("name"),
                "publishedAt": published_at,
                "country": country.upper()
            })
        return results
    except requests.exceptions.RequestException as e:
        raise Exception(f"NewsAPI search request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"NewsAPI search error: {str(e)}")

def fetch_international_financial_news(page_size=100):
    """
    Fetch international financial news from multiple major markets
    """
    key = Config().NEWSAPI_KEY
    
    if not key or key == "":
        raise Exception("NewsAPI key not configured. Please set NEWSAPI_KEY environment variable or add it to .env file")
    
    # Major financial markets to fetch from
    major_markets = ["us", "gb", "in", "ca", "au", "de", "jp", "cn", "sg", "hk", "kr", "br", "mx", "za", "ru"]
    
    all_articles = []
    
    for country in major_markets:
        try:
            articles = fetch_news_by_country(country, "business", min(page_size // len(major_markets), 20))
            all_articles.extend(articles)
        except Exception as e:
            print(f"Warning: Could not fetch news for {country}: {str(e)}")
            continue
    
    # Sort by publication date (newest first)
    all_articles.sort(key=lambda x: x.get("publishedAt") or datetime.min, reverse=True)
    
    return all_articles[:page_size]

def fetch_global_financial_news(query="financial markets", page_size=50):
    """
    Fetch global financial news using search endpoint
    """
    key = Config().NEWSAPI_KEY
    
    if not key or key == "":
        raise Exception("NewsAPI key not configured. Please set NEWSAPI_KEY environment variable or add it to .env file")
    
    params = {
        "apiKey": key,
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "domains": "reuters.com,bloomberg.com,cnbc.com,marketwatch.com,wsj.com,ft.com,cnn.com,bbc.com"
    }
    
    try:
        resp = requests.get(NEWSAPI_SEARCH_ENDPOINT, params=params, timeout=20)
        
        # Handle rate limiting specifically
        if resp.status_code == 429:
            raise Exception("NewsAPI rate limit exceeded. Please try again later or use RSS feeds instead.")
        
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("status") == "error":
            error_msg = data.get('message', 'Unknown error')
            if "rate" in error_msg.lower() or "limit" in error_msg.lower():
                raise Exception("NewsAPI rate limit exceeded. Please try again later or use RSS feeds instead.")
            raise Exception(f"NewsAPI error: {error_msg}")
            
        articles = data.get("articles", [])
        results = []
        for a in articles:
            published_at = None
            if a.get("publishedAt"):
                try:
                    published_at = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00"))
                except Exception:
                    published_at = None
            results.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "source": a.get("source", {}).get("name"),
                "publishedAt": published_at,
                "country": "GLOBAL"
            })
        return results
    except requests.exceptions.RequestException as e:
        if "429" in str(e) or "Too Many Requests" in str(e):
            raise Exception("NewsAPI rate limit exceeded. Please try again later or use RSS feeds instead.")
        raise Exception(f"NewsAPI request failed: {str(e)}")
    except Exception as e:
        if "rate limit" in str(e).lower():
            raise Exception("NewsAPI rate limit exceeded. Please try again later or use RSS feeds instead.")
        raise Exception(f"NewsAPI error: {str(e)}")

def get_supported_countries():
    """
    Return list of supported countries
    """
    return SUPPORTED_COUNTRIES