import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stocker.models import Fundamental
from stocker.tickers import TICKERS
import datetime
from stocker.logger import get_logger

logger = get_logger(__name__)

DATABASE_URL = "postgresql+psycopg2://stocker:stockerpass@localhost:54320/stockerdb"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_report_date(info):
    # Try earningsDate first
    report_date = info.get("earningsDate")
    if isinstance(report_date, (list, tuple)):
        report_date = report_date[0]
    # If it's a pandas Timestamp or datetime, convert to string
    if hasattr(report_date, "strftime"):
        return report_date.strftime("%Y-%m-%d")
    # If it's a string, return as is
    if isinstance(report_date, str):
        return report_date[:10]
    # If it's a Unix timestamp (int/float), convert to date
    if isinstance(report_date, (int, float)):
        return datetime.datetime.utcfromtimestamp(report_date).strftime("%Y-%m-%d")
    # Try mostRecentQuarter or lastFiscalYearEnd as fallback
    for alt_key in ["mostRecentQuarter", "lastFiscalYearEnd"]:
        ts = info.get(alt_key)
        if isinstance(ts, (int, float)):
            return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    return None

def fetch_and_store_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe_ratio = info.get("trailingPE")
        eps_growth = info.get("earningsQuarterlyGrowth")
        market_cap = info.get("marketCap")
        dividend_yield = info.get("dividendYield")
        report_date = get_report_date(info)
        if report_date is None:
            logger.warning(f"Skipping {ticker}: No report_date found.")
            return
        fundamental = Fundamental(
            ticker=ticker,
            report_date=report_date,
            pe_ratio=pe_ratio,
            eps_growth=eps_growth,
            market_cap=market_cap,
            dividend_yield=dividend_yield
        )
        session.merge(fundamental)
        session.commit()
        logger.info(f"Inserted/updated fundamentals for {ticker} ({report_date})")
    except Exception as e:
        logger.error(f"Error processing {ticker}: {e}")

def main():
    for ticker in TICKERS:
        fetch_and_store_fundamentals(ticker)
    session.close()

if __name__ == "__main__":
    main() 