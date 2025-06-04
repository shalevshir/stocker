"""
calculate_indicators.py
----------------------
Script to calculate moving averages and RSI for all tickers and store them in the technical_indicators table.
"""
import sys
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from stocker.models import Price, TechnicalIndicator, Base
from stocker.indicators import moving_average, rsi
import logging
import os
from dotenv import load_dotenv
import math

# --- CONFIG ---
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set.")

# --- LOGGER ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calculate_indicators")

# --- DB SETUP ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def to_float(val):
    if pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
        return None
    if hasattr(val, "item"):
        return float(val.item())
    return float(val)

def calculate_and_store_indicators():
    tickers = session.query(Price.ticker).distinct().all()
    tickers = [t[0] for t in tickers]
    logger.info(f"Found {len(tickers)} tickers.")

    for ticker in tickers:
        logger.info(f"Starting processing for {ticker}")
        prices = session.query(Price).filter(Price.ticker == ticker).order_by(Price.date).all()
        if not prices:
            logger.warning(f"No price data for {ticker}, skipping.")
            continue
        df = pd.DataFrame([
            {"date": p.date, "close": float(p.close) if p.close is not None else None}
            for p in prices
        ]).dropna()
        logger.info(f"{ticker}: {len(df)} price records after dropping nulls.")
        if df.empty:
            logger.warning(f"No valid price data for {ticker} after dropping nulls, skipping.")
            continue
        df.set_index("date", inplace=True)
        df["ma_5"] = moving_average(df["close"], 5)
        df["ma_20"] = moving_average(df["close"], 20)
        df["ma_50"] = moving_average(df["close"], 50)
        df["rsi_14"] = rsi(df["close"], 14)

        count = 0
        for date, row in df.iterrows():
            ti = session.query(TechnicalIndicator).filter_by(ticker=ticker, date=date).first()
            if not ti:
                ti = TechnicalIndicator(ticker=ticker, date=date)
            ti.ma_5 = to_float(row["ma_5"])
            ti.ma_20 = to_float(row["ma_20"])
            ti.ma_50 = to_float(row["ma_50"])
            ti.rsi_14 = to_float(row["rsi_14"])
            session.merge(ti)
            count += 1
        session.commit()
        logger.info(f"Finished processing {ticker}: {count} indicator records written.")
    logger.info("All indicators calculated and stored.")

if __name__ == "__main__":
    try:
        calculate_and_store_indicators()
    except Exception as e:
        logger.exception(f"Error calculating indicators: {e}")
        sys.exit(1) 