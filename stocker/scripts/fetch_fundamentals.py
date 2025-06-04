import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocker.models import Fundamental
from dotenv import load_dotenv
from stocker.tickers import TICKERS

# Load environment variables
load_dotenv()
EOD_API_KEY = os.getenv("EOD_API_KEY")
DATABASE_URL = "postgresql+psycopg2://stocker:stockerpass@localhost:54320/stockerdb"

# EOD Fundamentals endpoint template
EOD_URL = "https://eodhistoricaldata.com/api/fundamentals/{ticker}.US?api_token={api_key}"

# Set up DB session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_store_fundamentals(ticker):
    url = EOD_URL.format(ticker=ticker, api_key=EOD_API_KEY)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch fundamentals for {ticker}: {response.text}")
        return
    data = response.json()
    # Example: get latest annual report
    try:
        annual_reports = data["Financials"]["Income_Statement"]["annual"]
        latest_report_date = sorted(annual_reports.keys())[-1]
        pe_ratio = data["Highlights"].get("PERatio")
        eps_growth = data["Highlights"].get("EPSGrowth")
        market_cap = data["Highlights"].get("MarketCapitalization")
        dividend_yield = data["Highlights"].get("DividendYield")
        fundamental = Fundamental(
            ticker=ticker,
            report_date=latest_report_date,
            pe_ratio=pe_ratio,
            eps_growth=eps_growth,
            market_cap=market_cap,
            dividend_yield=dividend_yield
        )
        session.merge(fundamental)
        session.commit()
        print(f"Inserted/updated fundamentals for {ticker} ({latest_report_date})")
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

def main():
    for ticker in TICKERS:
        fetch_and_store_fundamentals(ticker)
    session.close()

if __name__ == "__main__":
    main() 