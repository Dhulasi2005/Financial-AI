# 🌍 Global Financial AI - Intelligent Market Analysis Platform

## 📊 Project Overview

**Global Financial AI** is a comprehensive web-based platform that combines real-time financial news aggregation, AI-powered sentiment analysis, and intelligent investment advisory services. The platform provides users with actionable insights for making informed financial decisions in global markets.

### 🎯 Key Features

#### 📰 **Multi-Source News Aggregation**
- **NewsAPI Integration**: Real-time financial news from 15+ countries
- **RSS Feed Support**: No API key required, works immediately
- **Dual Source System**: Combine both NewsAPI and RSS for comprehensive coverage
- **International Markets**: Coverage of US, UK, India, Canada, Australia, Singapore, Japan
- **Global Search**: Custom queries across global financial markets

#### 🤖 **AI-Powered Analysis**
- **FinBERT Sentiment Analysis**: Advanced NLP for financial text analysis
- **Market Sentiment Tracking**: Real-time sentiment scoring for news articles
- **Investment Suggestions**: AI-generated recommendations based on market conditions
- **Risk Profile Analysis**: Personalized advice based on user risk tolerance
- **Financial Guidance**: Q&A system for investment and financial questions

#### 🎨 **Modern User Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark Theme**: Professional financial dashboard aesthetic
- **Animated Elements**: Smooth animations and interactive effects
- **Real-time Updates**: Live sentiment analysis and news aggregation
- **Professional UX**: Intuitive navigation and user experience

#### 🔐 **User Management**
- **Secure Authentication**: Email-based registration and login
- **User Profiles**: Personalized dashboard and settings
- **Session Management**: Secure login/logout functionality
- **Data Persistence**: SQLite database for user data and news storage

## 🏗️ Architecture

### **Backend Technologies**
- **Flask**: Python web framework for API and routing
- **SQLAlchemy**: Database ORM for data management
- **Flask-Login**: User authentication and session management
- **WTForms**: Form handling and validation
- **Transformers**: FinBERT model for sentiment analysis
- **Requests**: HTTP client for API calls
- **Feedparser**: RSS feed parsing

### **Frontend Technologies**
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with animations and responsive design
- **JavaScript**: Interactive elements and dynamic content
- **Font Awesome**: Professional icons
- **Google Fonts**: Typography (Inter font family)

### **Data Sources**
- **NewsAPI**: Primary news source (requires API key)
- **RSS Feeds**: Alternative news source (no API key required)
- **Multiple Sources**: Reuters, Bloomberg, CNBC, MarketWatch, WSJ, FT, Yahoo Finance

## 📁 Project Structure

```
global-financial-ai/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models (User, NewsItem)
├── forms.py              # Form definitions
├── news_scraper.py       # NewsAPI integration
├── rss_scraper.py        # RSS feed integration
├── sentiment.py          # FinBERT sentiment analysis
├── strategy.py           # Investment strategy generation
├── ai_advisor.py         # AI financial advisor
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── ai_advisor.html   # AI advisor interface
│   ├── financial_guidance.html # Financial Q&A
│   ├── news_item.html    # Individual news view
│   └── profile.html      # User profile
└── instance/
    └── app.db           # SQLite database
```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd global-financial-ai
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Environment Configuration**
Create a `.env` file in the project root:
```bash
# Required for NewsAPI (optional for RSS-only usage)
NEWSAPI_KEY=your_newsapi_key_here

# Flask secret key (auto-generated if not provided)
SECRET_KEY=your-secret-key-here
```

### **Step 5: Initialize Database**
```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

### **Step 6: Run the Application**
```bash
python app.py
```

The application will be available at:
- **Local**: http://127.0.0.1:5001
- **Network**: http://your-ip:5001

## 🔧 Configuration

### **Environment Variables**
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEWSAPI_KEY` | NewsAPI authentication key | No (for RSS-only) | None |
| `SECRET_KEY` | Flask session secret | No | Auto-generated |
| `PORT` | Application port | No | 5001 |

### **NewsAPI Setup (Optional)**
1. Visit [NewsAPI.org](https://newsapi.org/)
2. Register for a free account
3. Get your API key
4. Add to `.env` file: `NEWSAPI_KEY=your_key_here`

## 📊 Features in Detail

### **1. News Aggregation System**

#### **Multi-Source Integration**
- **NewsAPI**: Structured data with metadata
- **RSS Feeds**: Real-time updates from major financial sources
- **Dual Mode**: Combine both sources for maximum coverage

#### **Supported Countries**
- **US**: United States financial markets
- **GB**: United Kingdom markets
- **IN**: Indian financial markets
- **CA**: Canadian markets
- **AU**: Australian markets
- **SG**: Singapore markets
- **JP**: Japanese markets

#### **News Processing Pipeline**
1. **Fetch**: Retrieve news from selected sources
2. **Deduplicate**: Remove duplicate articles by URL
3. **Analyze**: Apply FinBERT sentiment analysis
4. **Store**: Save to database with metadata
5. **Display**: Present in user-friendly dashboard

### **2. AI-Powered Analysis**

#### **Sentiment Analysis**
- **FinBERT Model**: Specialized for financial text
- **Three Categories**: Positive, Negative, Neutral
- **Confidence Scores**: 0-1 scale for sentiment strength
- **Real-time Processing**: Immediate analysis of new articles

#### **Market Sentiment Tracking**
- **Aggregate Analysis**: Overall market sentiment
- **Trend Detection**: Sentiment changes over time
- **Regional Analysis**: Country-specific sentiment
- **Sector Analysis**: Industry-specific insights

### **3. AI Financial Advisor**

#### **Investment Suggestions**
- **Risk-Based Recommendations**: Conservative, Moderate, Aggressive
- **Asset Class Suggestions**: Stocks, Bonds, ETFs, Crypto, Commodities
- **Sector Analysis**: Technology, Healthcare, Financial Services, etc.
- **Market Timing**: Entry/exit recommendations

#### **Financial Guidance**
- **Q&A System**: Ask financial questions
- **Personalized Advice**: Based on user context
- **Educational Content**: Investment education
- **Risk Assessment**: Portfolio risk analysis

### **4. User Experience**

#### **Dashboard Features**
- **Real-time Metrics**: News count, sentiment distribution
- **Interactive Charts**: Visual sentiment analysis
- **News Feed**: Latest articles with sentiment indicators
- **Quick Actions**: One-click news fetching

#### **Responsive Design**
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Gesture support for mobile devices
- **Fast Loading**: Optimized assets and caching
- **Accessibility**: Screen reader support

## 🔒 Security Features

### **Authentication**
- **Email-based Registration**: Secure user accounts
- **Password Hashing**: bcrypt encryption
- **Session Management**: Secure login/logout
- **CSRF Protection**: Form security

### **Data Protection**
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Input sanitization
- **Secure Headers**: HTTP security headers
- **Environment Variables**: Sensitive data protection

## 📈 Performance Optimizations

### **Database**
- **SQLite**: Lightweight, file-based database
- **Indexed Queries**: Fast news retrieval
- **Connection Pooling**: Efficient database connections

### **Caching**
- **Static Assets**: CSS/JS caching
- **News Caching**: Reduce API calls
- **Session Storage**: User data caching

### **Frontend**
- **Minified Assets**: Reduced file sizes
- **Lazy Loading**: On-demand content loading
- **CDN Integration**: Fast asset delivery

## 🧪 Testing

### **Manual Testing**
```bash
# Test RSS functionality
python -c "from rss_scraper import RSSFeedScraper; scraper = RSSFeedScraper(); print('RSS Test:', len(scraper.fetch_news_by_country('us', 5)))"

# Test sentiment analysis
python -c "from sentiment import analyze_text; print('Sentiment Test:', analyze_text('Stock market shows strong growth today'))"
```

### **API Testing**
```bash
# Test application endpoints
curl http://127.0.0.1:5001/
curl http://127.0.0.1:5001/dashboard
```

## 🚀 Deployment

### **Development**
```bash
python app.py
```

### **Production (Gunicorn)**
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:create_app()
```

### **Docker (Optional)**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Code Style**
- Follow PEP 8 Python guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NewsAPI**: For providing financial news data
- **Hugging Face**: For the FinBERT model
- **Font Awesome**: For the icon library
- **Google Fonts**: For the Inter font family

## 📞 Support

For questions, issues, or contributions:
- **Issues**: Use GitHub Issues
- **Discussions**: Use GitHub Discussions
- **Email**: Contact the maintainers

---

**Built with ❤️ for the global financial community**
