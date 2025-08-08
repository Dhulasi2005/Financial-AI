import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from models import db, User, NewsItem
from forms import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from news_scraper import fetch_news_by_country, fetch_international_financial_news, fetch_global_financial_news, get_supported_countries
from rss_scraper import fetch_news_by_country as rss_fetch_news_by_country, fetch_international_financial_news as rss_fetch_international_news, fetch_global_financial_news as rss_fetch_global_news, get_supported_countries as rss_get_supported_countries
from sentiment import analyze_text
from strategy import generate_strategy
from ai_advisor import FinancialAIAdvisor
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth
import secrets

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config())
    db.init_app(app)
    mail = Mail(app)
    
    # Initialize OAuth
    oauth = OAuth(app)
    
    # Google OAuth configuration
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET', ''),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
    )
    
    # Apple OAuth configuration (Note: Apple Sign-In requires special setup)
    oauth.register(
        name='apple',
        client_id=os.getenv('APPLE_CLIENT_ID', ''),
        client_secret=os.getenv('APPLE_CLIENT_SECRET', ''),
        access_token_url='https://appleid.apple.com/auth/token',
        access_token_params=None,
        authorize_url='https://appleid.apple.com/auth/authorize',
        authorize_params=None,
        api_base_url='https://appleid.apple.com/',
        client_kwargs={'scope': 'name email'},
    )
    
    # Initialize AI Advisor
    financial_advisor = FinancialAIAdvisor()
    
    def _merge_and_deduplicate_articles(newsapi_articles, rss_articles):
        """
        Merge articles from both sources and remove duplicates based on URL
        """
        all_articles = []
        seen_urls = set()
        
        # Add NewsAPI articles
        for article in newsapi_articles:
            if article.get("url") and article["url"] not in seen_urls:
                all_articles.append(article)
                seen_urls.add(article["url"])
        
        # Add RSS articles
        for article in rss_articles:
            if article.get("url") and article["url"] not in seen_urls:
                all_articles.append(article)
                seen_urls.add(article["url"])
        
        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get("publishedAt") or datetime.min, reverse=True)
        
        return all_articles

    # Login
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            existing = User.query.filter_by(email=form.email.data.lower()).first()
            if existing:
                flash("Email already registered. Please login.", "warning")
                return redirect(url_for("login"))
            hashed = generate_password_hash(form.password.data)
            user = User(email=form.email.data.lower(), name=form.name.data, password=hashed)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged in successfully.", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.", "danger")
        return render_template("login.html", form=form)

    @app.route("/login/google")
    def google_login():
        """Initiate Google OAuth login"""
        if not os.getenv('GOOGLE_CLIENT_ID') or not os.getenv('GOOGLE_CLIENT_SECRET'):
            flash("Google OAuth is not configured. Please set up GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your environment variables. See OAUTH_SETUP.md for instructions.", "warning")
            return redirect(url_for("login"))
        redirect_uri = url_for('google_authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

    @app.route("/login/google/authorize")
    def google_authorize():
        """Handle Google OAuth callback"""
        try:
            token = oauth.google.authorize_access_token()
            resp = oauth.google.get('userinfo')
            user_info = resp.json()
            
            # Check if user exists
            user = User.query.filter_by(email=user_info['email'].lower()).first()
            
            if not user:
                # Create new user
                user = User(
                    email=user_info['email'].lower(),
                    name=user_info.get('name', user_info['email']),
                    password=generate_password_hash(secrets.token_urlsafe(32)),  # Random password for OAuth users
                    oauth_provider='google',
                    oauth_id=user_info['id']
                )
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully with Google.", "success")
            else:
                flash("Logged in successfully with Google.", "success")
            
            login_user(user)
            return redirect(url_for("dashboard"))
            
        except Exception as e:
            flash(f"Google login failed: {str(e)}", "danger")
            return redirect(url_for("login"))

    @app.route("/login/apple")
    def apple_login():
        """Initiate Apple OAuth login"""
        if not os.getenv('APPLE_CLIENT_ID') or not os.getenv('APPLE_CLIENT_SECRET'):
            flash("Apple OAuth is not configured. Please set up APPLE_CLIENT_ID and APPLE_CLIENT_SECRET in your environment variables. See OAUTH_SETUP.md for instructions.", "warning")
            return redirect(url_for("login"))
        redirect_uri = url_for('apple_authorize', _external=True)
        return oauth.apple.authorize_redirect(redirect_uri)

    @app.route("/login/apple/authorize")
    def apple_authorize():
        """Handle Apple OAuth callback"""
        try:
            token = oauth.apple.authorize_access_token()
            # Apple provides user info in the token response
            user_info = token.get('user', {})
            
            # Extract email from Apple's response
            email = user_info.get('email', '')
            if not email:
                flash("Apple login failed: Email not provided", "danger")
                return redirect(url_for("login"))
            
            # Check if user exists
            user = User.query.filter_by(email=email.lower()).first()
            
            if not user:
                # Create new user
                user = User(
                    email=email.lower(),
                    name=user_info.get('name', {}).get('firstName', email),
                    password=generate_password_hash(secrets.token_urlsafe(32)),  # Random password for OAuth users
                    oauth_provider='apple',
                    oauth_id=user_info.get('sub', '')
                )
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully with Apple.", "success")
            else:
                flash("Logged in successfully with Apple.", "success")
            
            login_user(user)
            return redirect(url_for("dashboard"))
            
        except Exception as e:
            flash(f"Apple login failed: {str(e)}", "danger")
            return redirect(url_for("login"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out.", "info")
        return redirect(url_for("home"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        # Show recent stored news
        news = NewsItem.query.order_by(NewsItem.published_at.desc()).limit(50).all()
        # build simple aggregation metrics
        total = len(news)
        pos = sum(1 for n in news if n.sentiment == "positive")
        neg = sum(1 for n in news if n.sentiment == "negative")
        neu = sum(1 for n in news if n.sentiment == "neutral")
        return render_template("dashboard.html", news=news, total=total, pos=pos, neg=neg, neu=neu)

    @app.route("/fetch-news", methods=["POST"])
    @login_required
    def fetch_news():
        # Allow user to choose region in UI
        country = request.form.get("country") or "us"
        page_size = int(request.form.get("page_size") or 50)
        use_rss = request.form.get("use_rss", "false")
        
        print(f"Fetching news for country: {country}, page_size: {page_size}, use_rss: {use_rss}")
        
        all_articles = []
        newsapi_articles = []
        rss_articles = []
        
        # Fetch from NewsAPI if requested
        if use_rss in ["false", "both"]:
            try:
                newsapi_articles = fetch_news_by_country(country=country, page_size=page_size)
                print(f"Successfully fetched {len(newsapi_articles)} articles via NewsAPI for {country}")
            except Exception as e:
                print(f"NewsAPI error for {country}: {str(e)}")
                if use_rss == "false":  # Only NewsAPI requested
                    flash(f"NewsAPI error: {e}", "danger")
                    return redirect(url_for("dashboard"))
                else:  # Both requested, continue with RSS
                    flash(f"NewsAPI failed: {e}, continuing with RSS feeds.", "warning")
        
        # Fetch from RSS if requested
        if use_rss in ["true", "both"]:
            try:
                rss_articles = rss_fetch_news_by_country(country=country, page_size=page_size)
                print(f"Successfully fetched {len(rss_articles)} articles via RSS for {country}")
            except Exception as e:
                print(f"RSS error for {country}: {str(e)}")
                if use_rss == "true":  # Only RSS requested
                    flash(f"RSS feed error: {e}", "danger")
                    return redirect(url_for("dashboard"))
                else:  # Both requested, continue with NewsAPI
                    flash(f"RSS failed: {e}, continuing with NewsAPI.", "warning")
        
        # Combine articles and remove duplicates
        all_articles = _merge_and_deduplicate_articles(newsapi_articles, rss_articles)
        
        # Analyze and store
        stored = 0
        for a in all_articles:
            # avoid duplicates by url
            if a["url"] is None:
                continue
            if NewsItem.query.filter_by(url=a["url"]).first():
                continue
            title = a.get("title") or ""
            desc = a.get("description") or ""
            text = title + ". " + desc
            label, score = analyze_text(text)
            ni = NewsItem(
                title=title,
                description=desc,
                source=a.get("source"),
                url=a.get("url"),
                published_at=a.get("publishedAt"),
                sentiment=label,
                score=score,
                region=a.get("country", country.upper())
            )
            db.session.add(ni)
            stored += 1
        db.session.commit()
        
        # Generate success message
        if use_rss == "both":
            source_type = f"NewsAPI ({len(newsapi_articles)}) + RSS ({len(rss_articles)})"
        elif use_rss == "true":
            source_type = "RSS"
        else:
            source_type = "NewsAPI"
            
        flash(f"Fetched {len(all_articles)} articles via {source_type}. Stored {stored} new items.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/fetch-international", methods=["POST"])
    @login_required
    def fetch_international_news():
        """Fetch news from multiple international markets"""
        page_size = int(request.form.get("page_size") or 100)
        use_rss = request.form.get("use_rss", "false")
        
        print(f"Fetching international news, page_size: {page_size}, use_rss: {use_rss}")
        
        all_articles = []
        newsapi_articles = []
        rss_articles = []
        
        # Fetch from NewsAPI if requested
        if use_rss in ["false", "both"]:
            try:
                newsapi_articles = fetch_international_financial_news(page_size=page_size)
                print(f"Successfully fetched {len(newsapi_articles)} international articles via NewsAPI")
            except Exception as e:
                print(f"NewsAPI international error: {str(e)}")
                if use_rss == "false":  # Only NewsAPI requested
                    flash(f"NewsAPI international error: {e}", "danger")
                    return redirect(url_for("dashboard"))
                else:  # Both requested, continue with RSS
                    flash(f"NewsAPI failed: {e}, continuing with RSS feeds.", "warning")
        
        # Fetch from RSS if requested
        if use_rss in ["true", "both"]:
            try:
                rss_articles = rss_fetch_international_news(page_size=page_size)
                print(f"Successfully fetched {len(rss_articles)} international articles via RSS")
            except Exception as e:
                print(f"RSS international error: {str(e)}")
                if use_rss == "true":  # Only RSS requested
                    flash(f"RSS international feed error: {e}", "danger")
                    return redirect(url_for("dashboard"))
                else:  # Both requested, continue with NewsAPI
                    flash(f"RSS failed: {e}, continuing with NewsAPI.", "warning")
        
        # Combine articles and remove duplicates
        all_articles = _merge_and_deduplicate_articles(newsapi_articles, rss_articles)

        # Analyze and store
        stored = 0
        for a in all_articles:
            if a["url"] is None:
                continue
            if NewsItem.query.filter_by(url=a["url"]).first():
                continue
            title = a.get("title") or ""
            desc = a.get("description") or ""
            text = title + ". " + desc
            label, score = analyze_text(text)
            ni = NewsItem(
                title=title,
                description=desc,
                source=a.get("source"),
                url=a.get("url"),
                published_at=a.get("publishedAt"),
                sentiment=label,
                score=score,
                region=a.get("country", "INTERNATIONAL")
            )
            db.session.add(ni)
            stored += 1
        db.session.commit()
        
        # Generate success message
        if use_rss == "both":
            source_type = f"NewsAPI ({len(newsapi_articles)}) + RSS ({len(rss_articles)})"
        elif use_rss == "true":
            source_type = "RSS"
        else:
            source_type = "NewsAPI"
            
        flash(f"Fetched {len(all_articles)} international articles via {source_type}. Stored {stored} new items.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/fetch-global", methods=["POST"])
    @login_required
    def fetch_global_news():
        """Fetch global financial news using search"""
        query = request.form.get("query", "financial markets")
        page_size = int(request.form.get("page_size") or 50)
        use_rss = request.form.get("use_rss", "false")
        
        print(f"Fetching global news for query: {query}, page_size: {page_size}, use_rss: {use_rss}")
        
        all_articles = []
        newsapi_articles = []
        rss_articles = []
        
        # Fetch from NewsAPI if requested
        if use_rss in ["false", "both"]:
            try:
                newsapi_articles = fetch_global_financial_news(query=query, page_size=page_size)
                print(f"Successfully fetched {len(newsapi_articles)} global articles via NewsAPI")
            except Exception as e:
                print(f"NewsAPI global error: {str(e)}")
                if "rate limit" in str(e).lower():
                    if use_rss == "false":  # Only NewsAPI requested
                        flash("NewsAPI rate limit exceeded. Please try using RSS feeds instead, or wait and try again later.", "warning")
                        return redirect(url_for("dashboard"))
                    else:  # Both requested, continue with RSS
                        flash("NewsAPI rate limit exceeded, continuing with RSS feeds.", "warning")
                else:
                    if use_rss == "false":  # Only NewsAPI requested
                        flash(f"NewsAPI global error: {e}", "danger")
                        return redirect(url_for("dashboard"))
                    else:  # Both requested, continue with RSS
                        flash(f"NewsAPI failed: {e}, continuing with RSS feeds.", "warning")
        
        # Fetch from RSS if requested
        if use_rss in ["true", "both"]:
            try:
                rss_articles = rss_fetch_global_news(query=query, page_size=page_size)
                print(f"Successfully fetched {len(rss_articles)} global articles via RSS")
            except Exception as e:
                print(f"RSS global error: {str(e)}")
                if use_rss == "true":  # Only RSS requested
                    flash(f"RSS global feed error: {e}", "danger")
                    return redirect(url_for("dashboard"))
                else:  # Both requested, continue with NewsAPI
                    flash(f"RSS failed: {e}, continuing with NewsAPI.", "warning")
        
        # Combine articles and remove duplicates
        all_articles = _merge_and_deduplicate_articles(newsapi_articles, rss_articles)

        # Analyze and store
        stored = 0
        for a in all_articles:
            if a["url"] is None:
                continue
            if NewsItem.query.filter_by(url=a["url"]).first():
                continue
            title = a.get("title") or ""
            desc = a.get("description") or ""
            text = title + ". " + desc
            label, score = analyze_text(text)
            ni = NewsItem(
                title=title,
                description=desc,
                source=a.get("source"),
                url=a.get("url"),
                published_at=a.get("publishedAt"),
                sentiment=label,
                score=score,
                region="GLOBAL"
            )
            db.session.add(ni)
            stored += 1
        db.session.commit()
        
        # Generate success message
        if use_rss == "both":
            source_type = f"NewsAPI ({len(newsapi_articles)}) + RSS ({len(rss_articles)})"
        elif use_rss == "true":
            source_type = "RSS"
        else:
            source_type = "NewsAPI"
            
        flash(f"Fetched {len(all_articles)} global articles via {source_type}. Stored {stored} new items.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/news/<int:news_id>")
    @login_required
    def news_item(news_id):
        n = NewsItem.query.get_or_404(news_id)
        advice = generate_strategy(n.sentiment, region=n.region, user_type="investor")
        return render_template("news_item.html", n=n, advice=advice)

    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)

    @app.route("/ai-advisor")
    @login_required
    def ai_advisor():
        """AI Advisor dashboard with investment suggestions and stock recommendations"""
        # Get recent news for analysis
        recent_news = NewsItem.query.order_by(NewsItem.published_at.desc()).limit(100).all()
        
        # Convert to dict format for AI advisor
        news_data = []
        for item in recent_news:
            news_data.append({
                "sentiment": item.sentiment,
                "publishedAt": item.published_at,
                "country": item.region
            })
        
        # Get market sentiment analysis
        market_sentiment = financial_advisor.analyze_market_sentiment(news_data)
        
        # Generate investment suggestions
        risk_profile = request.args.get("risk_profile", "Moderate")
        investment_suggestions = financial_advisor.generate_investment_suggestions(market_sentiment, risk_profile)
        
        # Generate stock recommendations
        stock_recommendations = financial_advisor.generate_stock_recommendations(market_sentiment, risk_profile)
        
        # Generate market insights
        market_insights = financial_advisor.generate_market_insights(news_data)
        
        return render_template("ai_advisor.html", 
                             market_sentiment=market_sentiment,
                             suggestions=investment_suggestions,
                             stock_recommendations=stock_recommendations,
                             insights=market_insights,
                             risk_profiles=financial_advisor.risk_levels,
                             current_risk=risk_profile)

    @app.route("/financial-guidance", methods=["GET", "POST"])
    @login_required
    def financial_guidance():
        """AI-powered financial guidance"""
        if request.method == "POST":
            question = request.form.get("question", "")
            if question:
                guidance = financial_advisor.provide_financial_guidance(question)
                return render_template("financial_guidance.html", guidance=guidance, question=question)
        
        return render_template("financial_guidance.html")

    @app.route("/supported-countries")
    def supported_countries():
        """API endpoint to get supported countries"""
        return {"countries": get_supported_countries()}

    @app.route("/health")
    def health_check():
        """Health check endpoint for deployment platforms"""
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }

    return app

# Create the app instance for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))