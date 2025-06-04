import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocker.models import Price
from dotenv import load_dotenv
from stocker.tickers import TICKERS
from stocker.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()
EOD_API_KEY = os.getenv("EOD_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set.")    
# EOD API endpoint template
EOD_URL = "https://eodhistoricaldata.com/api/eod/{ticker}.US?from=2019-01-01&to=2024-01-01&api_token={api_key}&period=d&fmt=json"
print(EOD_API_KEY)
# Set up DB session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_store_prices(ticker):
    url = EOD_URL.format(ticker=ticker, api_key=EOD_API_KEY)
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