import uuid
from sqlalchemy import (
    Column, String, Date, Numeric, BigInteger, Integer, Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'
    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(BigInteger)
    adjusted_close = Column(Numeric)

class Fundamental(Base):
    __tablename__ = 'fundamentals'
    ticker = Column(String, primary_key=True)
    report_date = Column(Date, primary_key=True)
    pe_ratio = Column(Numeric)
    eps_growth = Column(Numeric)
    market_cap = Column(Numeric)
    dividend_yield = Column(Numeric)

class NewsSentiment(Base):
    __tablename__ = 'news_sentiment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String, nullable=False)
    headline = Column(Text)
    source = Column(Text)
    published_at = Column(TIMESTAMP)
    sentiment_score = Column(Numeric)

class Signal(Base):
    __tablename__ = 'signals'
    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    signal_strength = Column(Numeric)
    rank = Column(Integer)

class Feedback(Base):
    __tablename__ = 'feedback'
    signal_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    user_id = Column(String, primary_key=True)
    feedback_value = Column(Integer)  # 1 (👍), -1 (👎), or 0 (neutral)
    submitted_at = Column(TIMESTAMP)

class TechnicalIndicator(Base):
    __tablename__ = 'technical_indicators'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    ma_5 = Column(Numeric)
    ma_20 = Column(Numeric)
    ma_50 = Column(Numeric)
    rsi_14 = Column(Numeric)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # Optionally, add a UniqueConstraint for (ticker, date) if not handled by the DB
    # __table_args__ = (UniqueConstraint('ticker', 'date', name='uix_ticker_date'),) 