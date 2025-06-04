import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocker.models import NewsSentiment
from dotenv import load_dotenv
from datetime import datetime
from textblob import TextBlob
from stocker.tickers import TICKERS
from stocker.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set.")

# NewsAPI endpoint template
NEWS_URL = "https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}&language=en&pageSize=10"

# Set up DB session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_sentiment_score(text):
    # Simple sentiment polarity using TextBlob (-1 to 1)
    return TextBlob(text).sentiment.polarity

def fetch_and_store_news_sentiment(ticker):
    url = NEWS_URL.format(ticker=ticker, api_key=NEWS_API_KEY)
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to fetch news for {ticker}: {response.text}")
        return
    data = response.json()
    for article in data.get("articles", []):
        headline = article["title"]
        source = article["source"]["name"]
        published_at = article["publishedAt"]
        sentiment_score = get_sentiment_score(headline)
        news = NewsSentiment(
            ticker=ticker,
            headline=headline,
            source=source,
            published_at=datetime.fromisoformat(published_at.replace("Z", "+00:00")),
            sentiment_score=sentiment_score
        )
        session.add(news)
    session.commit()
    logger.info(f"Inserted news sentiment for {ticker}")

def main():
    for ticker in TICKERS:
        fetch_and_store_news_sentiment(ticker)
    session.close()

if __name__ == "__main__":
    main() 