"""
indicators.py
-------------
Utility functions for calculating technical indicators (Moving Averages, RSI).
"""

import pandas as pd
import numpy as np

def moving_average(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate the simple moving average (SMA) for a given window.
    Args:
        series (pd.Series): Series of prices (e.g., closing prices).
        window (int): Number of periods for the moving average.
    Returns:
        pd.Series: SMA values (NaN for periods with insufficient data).
    """
    return series.rolling(window=window, min_periods=window).mean()

def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) using the standard EMA method.
    Args:
        series (pd.Series): Series of prices (e.g., closing prices).
        window (int): Number of periods for RSI calculation (default: 14).
    Returns:
        pd.Series: RSI values (NaN for periods with insufficient data).
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi 