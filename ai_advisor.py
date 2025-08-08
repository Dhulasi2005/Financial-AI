import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class FinancialAIAdvisor:
    """
    AI-powered financial advisor that provides investment suggestions and financial guidance
    """
    
    def __init__(self):
        self.risk_levels = ["Conservative", "Moderate", "Aggressive"]
        self.investment_types = {
            "stocks": ["Large Cap", "Mid Cap", "Small Cap", "Growth", "Value", "Dividend"],
            "bonds": ["Government", "Corporate", "Municipal", "High Yield"],
            "etfs": ["S&P 500", "NASDAQ", "International", "Emerging Markets", "Commodities"],
            "crypto": ["Bitcoin", "Ethereum", "Stablecoins", "DeFi"],
            "commodities": ["Gold", "Silver", "Oil", "Natural Gas"],
            "real_estate": ["REITs", "Residential", "Commercial", "International"]
        }
        
        self.market_sectors = [
            "Technology", "Healthcare", "Financial Services", "Energy", 
            "Consumer Discretionary", "Consumer Staples", "Industrials",
            "Materials", "Real Estate", "Utilities", "Communication Services"
        ]
        
        # Stock recommendations database
        self.stock_recommendations = {
            "Technology": {
                "AAPL": {"name": "Apple Inc.", "sector": "Technology", "risk": "Moderate", "description": "Leading consumer electronics and software company"},
                "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "risk": "Moderate", "description": "Software and cloud services leader"},
                "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "risk": "Moderate", "description": "Internet services and advertising giant"},
                "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "risk": "Aggressive", "description": "Semiconductor and AI technology leader"},
                "TSLA": {"name": "Tesla Inc.", "sector": "Technology", "risk": "Aggressive", "description": "Electric vehicles and clean energy"},
                "AMZN": {"name": "Amazon.com Inc.", "sector": "Technology", "risk": "Moderate", "description": "E-commerce and cloud computing leader"}
            },
            "Healthcare": {
                "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "risk": "Conservative", "description": "Pharmaceutical and medical devices"},
                "PFE": {"name": "Pfizer Inc.", "sector": "Healthcare", "risk": "Conservative", "description": "Pharmaceutical company"},
                "UNH": {"name": "UnitedHealth Group", "sector": "Healthcare", "risk": "Moderate", "description": "Healthcare insurance and services"},
                "ABBV": {"name": "AbbVie Inc.", "sector": "Healthcare", "risk": "Moderate", "description": "Biopharmaceutical company"},
                "TMO": {"name": "Thermo Fisher Scientific", "sector": "Healthcare", "risk": "Moderate", "description": "Life sciences and laboratory equipment"}
            },
            "Financial Services": {
                "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial Services", "risk": "Moderate", "description": "Leading banking and financial services"},
                "BAC": {"name": "Bank of America Corp.", "sector": "Financial Services", "risk": "Moderate", "description": "Major banking institution"},
                "WFC": {"name": "Wells Fargo & Co.", "sector": "Financial Services", "risk": "Moderate", "description": "Diversified financial services"},
                "GS": {"name": "Goldman Sachs Group", "sector": "Financial Services", "risk": "Aggressive", "description": "Investment banking and securities"},
                "V": {"name": "Visa Inc.", "sector": "Financial Services", "risk": "Moderate", "description": "Digital payments technology"}
            },
            "Consumer Discretionary": {
                "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Discretionary", "risk": "Aggressive", "description": "Electric vehicles and clean energy"},
                "NKE": {"name": "Nike Inc.", "sector": "Consumer Discretionary", "risk": "Moderate", "description": "Athletic footwear and apparel"},
                "SBUX": {"name": "Starbucks Corporation", "sector": "Consumer Discretionary", "risk": "Moderate", "description": "Coffee retail and beverages"},
                "HD": {"name": "Home Depot Inc.", "sector": "Consumer Discretionary", "risk": "Moderate", "description": "Home improvement retail"},
                "MCD": {"name": "McDonald's Corporation", "sector": "Consumer Discretionary", "risk": "Conservative", "description": "Fast food restaurant chain"}
            },
            "Energy": {
                "XOM": {"name": "Exxon Mobil Corporation", "sector": "Energy", "risk": "Moderate", "description": "Oil and gas exploration and production"},
                "CVX": {"name": "Chevron Corporation", "sector": "Energy", "risk": "Moderate", "description": "Integrated oil and gas company"},
                "COP": {"name": "ConocoPhillips", "sector": "Energy", "risk": "Aggressive", "description": "Oil and gas exploration and production"},
                "EOG": {"name": "EOG Resources Inc.", "sector": "Energy", "risk": "Aggressive", "description": "Oil and gas exploration and production"}
            },
            "Consumer Staples": {
                "PG": {"name": "Procter & Gamble Co.", "sector": "Consumer Staples", "risk": "Conservative", "description": "Consumer goods and household products"},
                "KO": {"name": "Coca-Cola Company", "sector": "Consumer Staples", "risk": "Conservative", "description": "Beverage company"},
                "WMT": {"name": "Walmart Inc.", "sector": "Consumer Staples", "risk": "Conservative", "description": "Retail and e-commerce"},
                "COST": {"name": "Costco Wholesale Corp.", "sector": "Consumer Staples", "risk": "Moderate", "description": "Membership-based retail"},
                "PEP": {"name": "PepsiCo Inc.", "sector": "Consumer Staples", "risk": "Conservative", "description": "Beverages and snacks"}
            }
        }
    
    def analyze_market_sentiment(self, news_items: List[Dict]) -> Dict:
        """
        Analyze overall market sentiment from news items
        """
        if not news_items:
            return {"sentiment": "neutral", "confidence": 0.5, "trend": "stable"}
        
        positive_count = sum(1 for item in news_items if item.get("sentiment") == "positive")
        negative_count = sum(1 for item in news_items if item.get("sentiment") == "negative")
        neutral_count = sum(1 for item in news_items if item.get("sentiment") == "neutral")
        
        total = len(news_items)
        
        # Calculate sentiment scores
        positive_score = positive_count / total if total > 0 else 0
        negative_score = negative_count / total if total > 0 else 0
        neutral_score = neutral_count / total if total > 0 else 0
        
        # Determine overall sentiment
        if positive_score > 0.6:
            sentiment = "bullish"
            trend = "upward"
        elif negative_score > 0.6:
            sentiment = "bearish"
            trend = "downward"
        else:
            sentiment = "neutral"
            trend = "stable"
        
        confidence = max(positive_score, negative_score, neutral_score)
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "trend": trend,
            "positive_score": positive_score,
            "negative_score": negative_score,
            "neutral_score": neutral_score
        }
    
    def generate_investment_suggestions(self, market_sentiment: Dict, user_risk_profile: str = "Moderate") -> Dict:
        """
        Generate investment suggestions based on market sentiment and risk profile
        """
        sentiment = market_sentiment.get("sentiment", "neutral")
        confidence = market_sentiment.get("confidence", 0.5)
        
        suggestions = {
            "overall_recommendation": "",
            "suggested_actions": [],
            "sectors_to_watch": [],
            "risk_warnings": [],
            "opportunities": []
        }
        
        # Generate overall recommendation
        if sentiment == "bullish":
            if confidence > 0.7:
                suggestions["overall_recommendation"] = "Strong buy signals detected. Consider increasing equity exposure."
            else:
                suggestions["overall_recommendation"] = "Moderate positive sentiment. Maintain balanced portfolio with slight equity tilt."
        elif sentiment == "bearish":
            if confidence > 0.7:
                suggestions["overall_recommendation"] = "Strong sell signals detected. Consider defensive positioning and increased cash allocation."
            else:
                suggestions["overall_recommendation"] = "Moderate negative sentiment. Reduce risk exposure and focus on quality assets."
        else:
            suggestions["overall_recommendation"] = "Market sentiment is neutral. Maintain current allocation and focus on long-term strategy."
        
        # Generate specific actions based on sentiment and risk profile
        if sentiment == "bullish":
            suggestions["suggested_actions"].extend([
                "Consider increasing exposure to growth stocks",
                "Look for opportunities in emerging markets",
                "Review and potentially increase equity allocation",
                "Consider sector rotation into technology and consumer discretionary"
            ])
        elif sentiment == "bearish":
            suggestions["suggested_actions"].extend([
                "Increase cash position for future opportunities",
                "Focus on defensive sectors (utilities, consumer staples)",
                "Consider adding bonds for stability",
                "Review and potentially reduce equity exposure"
            ])
        else:
            suggestions["suggested_actions"].extend([
                "Maintain current asset allocation",
                "Focus on dollar-cost averaging",
                "Review portfolio for rebalancing opportunities",
                "Consider dividend-paying stocks for income"
            ])
        
        # Add risk profile specific suggestions
        if user_risk_profile == "Conservative":
            suggestions["suggested_actions"].extend([
                "Focus on blue-chip dividend stocks",
                "Consider government bonds for stability",
                "Maintain higher cash allocation",
                "Avoid speculative investments"
            ])
        elif user_risk_profile == "Aggressive":
            suggestions["suggested_actions"].extend([
                "Consider growth stocks and small caps",
                "Look for emerging market opportunities",
                "Consider sector-specific ETFs",
                "Review alternative investments"
            ])
        
        # Generate sector recommendations
        if sentiment == "bullish":
            suggestions["sectors_to_watch"] = ["Technology", "Consumer Discretionary", "Financial Services", "Industrials"]
        elif sentiment == "bearish":
            suggestions["sectors_to_watch"] = ["Utilities", "Consumer Staples", "Healthcare", "Real Estate"]
        else:
            suggestions["sectors_to_watch"] = ["Technology", "Healthcare", "Financial Services", "Consumer Staples"]
        
        # Add risk warnings
        suggestions["risk_warnings"] = [
            "Past performance does not guarantee future results",
            "Diversify across different asset classes and sectors",
            "Consider your investment timeline and goals",
            "Monitor market conditions regularly",
            "Consult with a financial advisor for personalized advice"
        ]
        
        # Generate opportunities
        if sentiment == "bullish":
            suggestions["opportunities"] = [
                "Market momentum favors growth investments",
                "Consider increasing international exposure",
                "Look for undervalued growth stocks",
                "Review sector rotation opportunities"
            ]
        elif sentiment == "bearish":
            suggestions["opportunities"] = [
                "Defensive positioning for capital preservation",
                "Look for quality stocks at discounted prices",
                "Consider bond laddering strategies",
                "Focus on dividend-paying stocks for income"
            ]
        else:
            suggestions["opportunities"] = [
                "Steady accumulation of quality assets",
                "Focus on long-term investment themes",
                "Consider dollar-cost averaging strategies",
                "Review and rebalance portfolio"
            ]
        
        return suggestions
    
    def provide_financial_guidance(self, question: str, context: Dict = None) -> Dict:
        """
        Provide AI-powered financial guidance for common questions
        """
        question_lower = question.lower()
        
        guidance = {
            "answer": "",
            "key_points": [],
            "recommendations": [],
            "resources": []
        }
        
        # Investment strategy guidance
        if any(word in question_lower for word in ["start", "begin", "invest", "first time"]):
            guidance["answer"] = "For beginners, start with a diversified approach using index funds or ETFs. Consider your risk tolerance and investment timeline."
            guidance["key_points"] = [
                "Start with index funds for broad market exposure",
                "Diversify across different asset classes",
                "Consider your risk tolerance and time horizon",
                "Use dollar-cost averaging to reduce timing risk"
            ]
            guidance["recommendations"] = [
                "Open a retirement account (401k, IRA)",
                "Start with S&P 500 index fund",
                "Set up automatic monthly contributions",
                "Educate yourself about basic investment concepts"
            ]
        
        # Risk management guidance
        elif any(word in question_lower for word in ["risk", "safe", "protect", "secure"]):
            guidance["answer"] = "Risk management is crucial for long-term investment success. Diversification and proper asset allocation are key."
            guidance["key_points"] = [
                "Diversify across different asset classes",
                "Don't put all eggs in one basket",
                "Consider your investment timeline",
                "Regularly rebalance your portfolio"
            ]
            guidance["recommendations"] = [
                "Maintain emergency fund (3-6 months expenses)",
                "Use asset allocation based on age and risk tolerance",
                "Consider bonds for stability",
                "Review portfolio quarterly"
            ]
        
        # Market timing guidance
        elif any(word in question_lower for word in ["timing", "when", "best time", "market"]):
            guidance["answer"] = "Market timing is extremely difficult. Focus on time in the market rather than timing the market."
            guidance["key_points"] = [
                "Time in the market beats timing the market",
                "Dollar-cost averaging reduces timing risk",
                "Focus on long-term investment goals",
                "Don't try to predict short-term market movements"
            ]
            guidance["recommendations"] = [
                "Use dollar-cost averaging strategy",
                "Set up automatic monthly investments",
                "Focus on long-term goals (5+ years)",
                "Ignore short-term market noise"
            ]
        
        # Retirement planning guidance
        elif any(word in question_lower for word in ["retirement", "401k", "ira", "pension"]):
            guidance["answer"] = "Start early and maximize tax-advantaged accounts. Compound interest is your friend for retirement planning."
            guidance["key_points"] = [
                "Start saving for retirement as early as possible",
                "Maximize employer matching contributions",
                "Use tax-advantaged accounts (401k, IRA)",
                "Consider your retirement timeline and goals"
            ]
            guidance["recommendations"] = [
                "Contribute to employer 401k up to match",
                "Open and fund IRA accounts",
                "Increase contributions annually",
                "Consider Roth vs Traditional IRA based on tax situation"
            ]
        
        # Stock vs ETF guidance
        elif any(word in question_lower for word in ["stock", "etf", "fund", "individual"]):
            guidance["answer"] = "ETFs offer instant diversification and are great for most investors. Individual stocks require more research and carry higher risk."
            guidance["key_points"] = [
                "ETFs provide instant diversification",
                "Individual stocks require more research",
                "ETFs typically have lower fees",
                "Consider your time and expertise"
            ]
            guidance["recommendations"] = [
                "Start with broad market ETFs",
                "Use ETFs for sector exposure",
                "Consider individual stocks for 5-10% of portfolio",
                "Research companies thoroughly before investing"
            ]
        
        # General financial advice
        else:
            guidance["answer"] = "Focus on building a solid financial foundation: emergency fund, debt management, and long-term investing."
            guidance["key_points"] = [
                "Build emergency fund first",
                "Pay off high-interest debt",
                "Start investing early and regularly",
                "Diversify your investments"
            ]
            guidance["recommendations"] = [
                "Create and follow a budget",
                "Build 3-6 months emergency fund",
                "Pay off credit card debt",
                "Start investing in index funds"
            ]
        
        guidance["resources"] = [
            "Financial education websites",
            "Investment books and courses",
            "Financial advisor consultation",
            "Online investment platforms"
        ]
        
        return guidance
    
    def generate_market_insights(self, news_items: List[Dict]) -> Dict:
        """
        Generate market insights from news analysis
        """
        if not news_items:
            return {"insights": [], "trends": [], "summary": "No news data available for analysis."}
        
        # Analyze recent news patterns
        recent_news = [item for item in news_items if item.get("publishedAt") and 
                      (datetime.now() - item["publishedAt"]).days <= 7]
        
        insights = []
        trends = []
        
        # Analyze sentiment trends
        positive_news = [item for item in recent_news if item.get("sentiment") == "positive"]
        negative_news = [item for item in recent_news if item.get("sentiment") == "negative"]
        
        if len(positive_news) > len(negative_news) * 2:
            insights.append("Strong positive sentiment in recent news suggests bullish market conditions.")
        elif len(negative_news) > len(positive_news) * 2:
            insights.append("Strong negative sentiment in recent news suggests cautious market approach.")
        else:
            insights.append("Mixed market sentiment indicates balanced approach to investing.")
        
        # Analyze geographic trends
        countries = {}
        for item in recent_news:
            country = item.get("country", "Unknown")
            countries[country] = countries.get(country, 0) + 1
        
        if countries:
            top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:3]
            trends.append(f"Major news focus: {', '.join([f'{country} ({count})' for country, count in top_countries])}")
        
        # Generate summary
        summary = f"Analysis of {len(recent_news)} recent news items shows "
        if len(positive_news) > len(negative_news):
            summary += "generally positive market sentiment with opportunities for growth investments."
        elif len(negative_news) > len(positive_news):
            summary += "cautious market sentiment suggesting defensive positioning."
        else:
            summary += "balanced market sentiment requiring careful analysis of individual opportunities."
        
        return {
            "insights": insights,
            "trends": trends,
            "summary": summary,
            "recent_news_count": len(recent_news),
            "positive_ratio": len(positive_news) / len(recent_news) if recent_news else 0
        }
    
    def generate_stock_recommendations(self, market_sentiment: Dict, user_risk_profile: str = "Moderate", max_recommendations: int = 6) -> Dict:
        """
        Generate specific stock recommendations based on market sentiment and risk profile
        """
        sentiment = market_sentiment.get("sentiment", "neutral")
        confidence = market_sentiment.get("confidence", 0.5)
        
        recommendations = {
            "top_picks": [],
            "sector_recommendations": {},
            "risk_adjusted_picks": [],
            "chart_data": {},
            "analysis": {}
        }
        
        # Select sectors based on sentiment
        if sentiment == "bullish":
            primary_sectors = ["Technology", "Consumer Discretionary", "Financial Services"]
            secondary_sectors = ["Healthcare", "Industrials"]
        elif sentiment == "bearish":
            primary_sectors = ["Consumer Staples", "Healthcare", "Utilities"]
            secondary_sectors = ["Financial Services", "Energy"]
        else:
            primary_sectors = ["Technology", "Healthcare", "Financial Services"]
            secondary_sectors = ["Consumer Staples", "Energy"]
        
        # Generate stock picks
        all_picks = []
        
        # Add stocks from primary sectors
        for sector in primary_sectors:
            if sector in self.stock_recommendations:
                sector_stocks = self.stock_recommendations[sector]
                for symbol, stock_info in sector_stocks.items():
                    # Filter by risk profile
                    if user_risk_profile == "Conservative" and stock_info["risk"] == "Conservative":
                        all_picks.append((symbol, stock_info, "primary"))
                    elif user_risk_profile == "Aggressive" and stock_info["risk"] in ["Moderate", "Aggressive"]:
                        all_picks.append((symbol, stock_info, "primary"))
                    elif user_risk_profile == "Moderate":
                        all_picks.append((symbol, stock_info, "primary"))
        
        # Add stocks from secondary sectors
        for sector in secondary_sectors:
            if sector in self.stock_recommendations:
                sector_stocks = self.stock_recommendations[sector]
                for symbol, stock_info in sector_stocks.items():
                    if user_risk_profile == "Conservative" and stock_info["risk"] == "Conservative":
                        all_picks.append((symbol, stock_info, "secondary"))
                    elif user_risk_profile == "Aggressive" and stock_info["risk"] in ["Moderate", "Aggressive"]:
                        all_picks.append((symbol, stock_info, "secondary"))
                    elif user_risk_profile == "Moderate":
                        all_picks.append((symbol, stock_info, "secondary"))
        
        # Select top picks (limit to max_recommendations)
        selected_picks = all_picks[:max_recommendations]
        
        # Format recommendations
        for symbol, stock_info, priority in selected_picks:
            recommendation = {
                "symbol": symbol,
                "name": stock_info["name"],
                "sector": stock_info["sector"],
                "risk_level": stock_info["risk"],
                "description": stock_info["description"],
                "priority": priority,
                "chart_url": f"https://www.tradingview.com/symbols/NASDAQ-{symbol}/",
                "analysis_url": f"https://finance.yahoo.com/quote/{symbol}",
                "reasoning": self._generate_stock_reasoning(symbol, stock_info, sentiment, user_risk_profile)
            }
            recommendations["top_picks"].append(recommendation)
        
        # Generate sector recommendations
        for sector in primary_sectors + secondary_sectors:
            if sector in self.stock_recommendations:
                sector_stocks = [stock for stock in recommendations["top_picks"] if stock["sector"] == sector]
                if sector_stocks:
                    recommendations["sector_recommendations"][sector] = {
                        "stocks": sector_stocks,
                        "sentiment": "positive" if sentiment == "bullish" else "neutral" if sentiment == "neutral" else "negative",
                        "reasoning": f"{sector} sector shows {sentiment} sentiment based on market analysis"
                    }
        
        # Generate risk-adjusted picks
        conservative_picks = [stock for stock in recommendations["top_picks"] if stock["risk_level"] == "Conservative"]
        moderate_picks = [stock for stock in recommendations["top_picks"] if stock["risk_level"] == "Moderate"]
        aggressive_picks = [stock for stock in recommendations["top_picks"] if stock["risk_level"] == "Aggressive"]
        
        recommendations["risk_adjusted_picks"] = {
            "conservative": conservative_picks[:2],
            "moderate": moderate_picks[:3],
            "aggressive": aggressive_picks[:2]
        }
        
        # Generate chart data URLs
        for stock in recommendations["top_picks"]:
            symbol = stock["symbol"]
            recommendations["chart_data"][symbol] = {
                "tradingview": f"https://www.tradingview.com/symbols/NASDAQ-{symbol}/",
                "yahoo_finance": f"https://finance.yahoo.com/quote/{symbol}",
                "marketwatch": f"https://www.marketwatch.com/investing/stock/{symbol}",
                "google_finance": f"https://www.google.com/finance/quote/{symbol}:NASDAQ"
            }
        
        # Generate analysis summary
        recommendations["analysis"] = {
            "market_sentiment": sentiment,
            "confidence": confidence,
            "risk_profile": user_risk_profile,
            "recommendation_summary": f"Based on {sentiment} market sentiment and {user_risk_profile} risk profile, we recommend {len(recommendations['top_picks'])} stocks across {len(recommendations['sector_recommendations'])} sectors.",
            "diversification_note": "These recommendations provide sector diversification and risk-appropriate exposure based on current market conditions."
        }
        
        return recommendations
    
    def _generate_stock_reasoning(self, symbol: str, stock_info: Dict, sentiment: str, risk_profile: str) -> str:
        """
        Generate reasoning for stock recommendation
        """
        sector = stock_info["sector"]
        risk_level = stock_info["risk"]
        
        reasoning_templates = {
            "bullish": {
                "Technology": f"{symbol} is well-positioned in the technology sector with strong growth potential in current market conditions.",
                "Healthcare": f"{symbol} offers stability in healthcare with defensive characteristics and growth opportunities.",
                "Financial Services": f"{symbol} benefits from economic expansion and rising interest rates in the financial sector.",
                "Consumer Discretionary": f"{symbol} is positioned to benefit from consumer spending growth in discretionary sectors.",
                "Energy": f"{symbol} is positioned to benefit from energy demand growth and commodity price strength.",
                "Consumer Staples": f"{symbol} provides defensive positioning with stable earnings in consumer staples."
            },
            "bearish": {
                "Technology": f"{symbol} offers defensive growth characteristics in technology with strong balance sheet.",
                "Healthcare": f"{symbol} provides defensive positioning in healthcare with stable earnings and growth potential.",
                "Financial Services": f"{symbol} offers value in financial services with strong fundamentals.",
                "Consumer Discretionary": f"{symbol} provides defensive positioning in consumer discretionary with strong brand value.",
                "Energy": f"{symbol} offers value in energy sector with strong fundamentals and dividend yield.",
                "Consumer Staples": f"{symbol} provides defensive positioning in consumer staples with stable earnings."
            },
            "neutral": {
                "Technology": f"{symbol} offers balanced growth and value characteristics in technology sector.",
                "Healthcare": f"{symbol} provides stable growth in healthcare with defensive characteristics.",
                "Financial Services": f"{symbol} offers balanced exposure to financial services with strong fundamentals.",
                "Consumer Discretionary": f"{symbol} provides balanced exposure to consumer discretionary with growth potential.",
                "Energy": f"{symbol} offers balanced exposure to energy sector with value characteristics.",
                "Consumer Staples": f"{symbol} provides defensive positioning in consumer staples with stable earnings."
            }
        }
        
        base_reasoning = reasoning_templates.get(sentiment, reasoning_templates["neutral"]).get(sector, f"{symbol} offers balanced characteristics in {sector} sector.")
        
        risk_note = ""
        if risk_profile == "Conservative" and risk_level == "Conservative":
            risk_note = " Suitable for conservative investors seeking stability."
        elif risk_profile == "Aggressive" and risk_level == "Aggressive":
            risk_note = " Suitable for aggressive investors seeking growth."
        elif risk_profile == "Moderate":
            risk_note = " Suitable for moderate investors seeking balanced exposure."
        
        return base_reasoning + risk_note
