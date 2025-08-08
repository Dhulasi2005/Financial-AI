def generate_strategy(sentiment, region=None, user_type="investor"):
    """
    sentiment: 'positive'|'neutral'|'negative'
    region: optional e.g. 'US', 'IN'
    user_type: 'investor','student','business'
    """
    # Basic mapping - extend with more rules or ML later
    if sentiment == "negative":
        if user_type == "investor":
            return "Caution: Reduce exposure to high-volatility assets. Consider short-term bonds or gold ETFs."
        if user_type == "student":
            return "Caution: Keep emergency funds; avoid risky trading."
        if user_type == "business":
            return "Caution: Hedge currency risk and delay major non-essential expenditures."
    elif sentiment == "positive":
        if user_type == "investor":
            return "Opportunity: Consider selective equity exposure; prioritize dividend or value stocks."
        if user_type == "student":
            return "Opportunity: Consider long-term investment with small SIPs."
        if user_type == "business":
            return "Opportunity: Consider gradual expansion; lock supplier contracts."
    return "Neutral: Maintain diversification and monitor daily updates."