import logging
import re
from collections import Counter

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple sentiment analysis using keyword matching
def analyze_text(text):
    """
    Returns (label, score) where label is 'positive'|'neutral'|'negative' and score is confidence.
    Uses simple keyword-based analysis instead of transformers to avoid deployment issues.
    """
    if not text:
        return "neutral", 0.5
    
    # Convert to lowercase for analysis
    text_lower = text.lower()
    
    # Define sentiment keywords
    positive_words = [
        'positive', 'good', 'great', 'excellent', 'strong', 'growth', 'profit', 'gain',
        'rise', 'increase', 'up', 'higher', 'better', 'success', 'win', 'bullish',
        'optimistic', 'recovery', 'surge', 'rally', 'boom', 'thrive', 'flourish'
    ]
    
    negative_words = [
        'negative', 'bad', 'poor', 'weak', 'loss', 'decline', 'fall', 'down', 'lower',
        'worse', 'fail', 'crash', 'bearish', 'pessimistic', 'recession', 'drop',
        'plunge', 'collapse', 'struggle', 'suffer', 'decline', 'downturn'
    ]
    
    # Count occurrences
    words = re.findall(r'\b\w+\b', text_lower)
    word_count = Counter(words)
    
    positive_count = sum(word_count[word] for word in positive_words)
    negative_count = sum(word_count[word] for word in negative_words)
    
    total_sentiment_words = positive_count + negative_count
    
    if total_sentiment_words == 0:
        return "neutral", 0.5
    
    # Calculate sentiment score
    if positive_count > negative_count:
        sentiment = "positive"
        score = positive_count / total_sentiment_words
    elif negative_count > positive_count:
        sentiment = "negative"
        score = negative_count / total_sentiment_words
    else:
        sentiment = "neutral"
        score = 0.5
    
    # Ensure score is between 0.1 and 0.9
    score = max(0.1, min(0.9, score))
    
    return sentiment, score