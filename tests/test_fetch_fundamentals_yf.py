import pytest
from stocker.scripts.fetch_fundamentals_yf import fetch_and_store_fundamentals

class MockTicker:
    def __init__(self, ticker):
        self.info = {
            "trailingPE": 20.0,
            "earningsQuarterlyGrowth": 0.1,
            "marketCap": 1000000000,
            "dividendYield": 0.02,
            "earningsDate": "2024-01-01"
        }

def test_fetch_and_store_fundamentals(monkeypatch):
    monkeypatch.setattr("yfinance.Ticker", lambda ticker: MockTicker(ticker))
    # Should run without error for a fake ticker
    fetch_and_store_fundamentals("FAKE") 