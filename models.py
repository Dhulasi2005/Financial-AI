from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)  # hashed password
    name = db.Column(db.String(120), nullable=True)
    oauth_provider = db.Column(db.String(50), nullable=True)  # 'google', 'apple', etc.
    oauth_id = db.Column(db.String(200), nullable=True)  # OAuth provider's user ID
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"

class NewsItem(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.String(2000))
    source = db.Column(db.String(200))
    url = db.Column(db.String(1000))
    published_at = db.Column(db.DateTime)
    sentiment = db.Column(db.String(50))  # positive/neutral/negative
    score = db.Column(db.Float)  # confidence score
    region = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<News {self.title[:40]}>"