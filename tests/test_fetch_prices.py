import pytest
from stocker.scripts.fetch_prices import fetch_and_store_prices

class MockResponse:
    status_code = 200
    def json(self):
        return [{
            "date": "2024-01-01",
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 105,
            "volume": 1000000,
            "adjusted_close": 105
        }]

def test_fetch_and_store_prices(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url: MockResponse())
    # Should run without error for a fake ticker
    fetch_and_store_prices("FAKE") 