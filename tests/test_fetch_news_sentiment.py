import pytest
from stocker.scripts.fetch_news_sentiment import fetch_and_store_news_sentiment

class MockResponse:
    status_code = 200
    def json(self):
        return {"articles": [
            {
                "title": "Stock rises on good news",
                "source": {"name": "TestSource"},
                "publishedAt": "2024-01-01T12:00:00Z"
            }
        ]}

def test_fetch_and_store_news_sentiment(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: MockResponse())
    monkeypatch.setattr("stocker.scripts.fetch_news_sentiment.get_sentiment_score", lambda text: 0.5)
    # Should run without error for a fake ticker
    fetch_and_store_news_sentiment("FAKE") 