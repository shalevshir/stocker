"""
fetch_eod_prices_30d.py
----------------------
Fetch historical price data from EODHistoricalData for the last 30 days and store in the prices table.
"""
import os
import requests
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocker.models import Price, Base
from dotenv import load_dotenv
from stocker.tickers import TICKERS

# --- ENV & CONFIG ---
load_dotenv()
EOD_API_KEY = os.getenv("EOD_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set.")
if not EOD_API_KEY:
    raise RuntimeError("EOD_API_KEY environment variable not set.")

# Calculate date range for last 30 days
end_date = datetime.today().date()
start_date = end_date - timedelta(days=60)

# EOD API endpoint template
EOD_URL = "https://eodhistoricaldata.com/api/eod/{ticker}.US?from={start}&to={end}&api_token={api_key}&period=d&fmt=json"

# --- LOGGER ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fetch_eod_prices_30d")

# --- DB SETUP ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# --- MAIN LOGIC ---
def fetch_and_store_prices(ticker):
    url = EOD_URL.format(
        ticker=ticker,
        start=start_date,
        end=end_date,
        api_key=EOD_API_KEY
    )
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to fetch {ticker}: {response.text}")
        return
    data = response.json()
    for row in data:
        price = Price(
            ticker=ticker,
            date=row["date"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
            adjusted_close=row.get("adjusted_close", row["close"])
        )
        session.merge(price)  # Upsert
    session.commit()
    logger.info(f"Inserted/updated prices for {ticker}")

def main():
    for ticker in TICKERS:
        fetch_and_store_prices(ticker)
    session.close()

if __name__ == "__main__":
    main() 