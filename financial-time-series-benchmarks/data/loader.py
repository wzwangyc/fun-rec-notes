# -*- coding: utf-8 -*-
"""
Data Loader Module

Business Intent:
    Load and validate financial time series data from various sources.
    Ensures data integrity and prevents dirty data from entering core logic.
    
Design Boundaries:
    - All external inputs must be validated
    - All timestamps must be timezone-aware (UTC)
    - Invalid data must be rejected, not silently fixed
    - Clear error messages for all failure scenarios

Applicable Scenarios:
    - Loading historical price data for backtesting
    - Loading real-time data for live trading
    - Generating synthetic data for testing
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Literal, Union, Optional
from datetime import datetime, timezone
import warnings

# Import domain types for type safety
from models.types import (
    PrecisionWarning,
    create_money,
    Currency,
)


def load_stock_data(
    symbol: str,
    start: Union[str, datetime] = '2020-01-01',
    end: Union[str, datetime] = '2024-12-31',
    source: Literal['akshare', 'yfinance', 'synthetic'] = 'akshare',
    timezone: str = 'UTC'
) -> pd.DataFrame:
    """
    Load stock price data with strict validation.
    
    Business Intent:
        Load validated price data for backtesting and live trading.
        All inputs are validated to prevent data corruption.
    
    Args:
        symbol: Stock symbol (e.g., '000001.SZ' for A-share, 'AAPL' for US)
        start: Start date (string or datetime)
        end: End date (string or datetime)
        source: Data source ('akshare' for A-shares, 'yfinance' for US, 'synthetic' for testing)
        timezone: Timezone for timestamps (default: 'UTC')
    
    Returns:
        DataFrame with OHLCV data, timezone-aware timestamps
    
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If data source fails
    
    Usage:
        >>> df = load_stock_data('AAPL', start='2023-01-01', end='2023-12-31')
        >>> df.index.tz
        <UTC>
    """
    # Fail-fast: Validate symbol
    _validate_symbol(symbol, source)
    
    # Fail-fast: Validate date range
    start_date, end_date = _validate_date_range(start, end)
    
    # Fail-fast: Validate source
    _validate_source(source)
    
    # Load data based on source
    try:
        if source == 'synthetic':
            df = _generate_synthetic_data(start_date, end_date)
        elif source == 'akshare':
            df = _load_akshare_data(symbol, start_date, end_date)
        elif source == 'yfinance':
            df = _load_yfinance_data(symbol, start_date, end_date)
        else:
            # Should never reach here due to validation
            raise RuntimeError(f"Unknown source: {source}")
        
        # Post-processing: Ensure timezone-aware
        df = _ensure_timezone(df, timezone)
        
        # Post-processing: Validate output
        _validate_output(df)
        
        return df
    
    except Exception as e:
        # Fail-fast: Re-raise with context
        raise RuntimeError(f"Failed to load data for {symbol}: {str(e)}") from e


def _validate_symbol(symbol: str, source: str) -> None:
    """
    Validate stock symbol format.
    
    Business Intent:
        Prevent invalid symbols from causing data corruption.
    """
    # Fail-fast: Symbol must be non-empty string
    if not symbol or not isinstance(symbol, str):
        raise ValueError(f"Symbol must be a non-empty string, got {repr(symbol)}")
    
    symbol = symbol.strip()
    
    if len(symbol) == 0:
        raise ValueError("Symbol cannot be empty after stripping")
    
    # Source-specific validation
    if source == 'akshare':
        # A-share format: 6 digits + .SZ or .SH
        if not (len(symbol) == 6 or (len(symbol) == 9 and '.' in symbol)):
            warnings.warn(
                f"A-share symbol '{symbol}' may be invalid. Expected format: 6 digits or XXXXXX.SZ/SH",
                DataWarning,
                stacklevel=3
            )
    
    elif source == 'yfinance':
        # US stock format: 1-5 characters
        if len(symbol) > 10:
            warnings.warn(
                f"US stock symbol '{symbol}' may be invalid. Expected 1-10 characters",
                DataWarning,
                stacklevel=3
            )


def _validate_date_range(
    start: Union[str, datetime],
    end: Union[str, datetime]
) -> tuple[datetime, datetime]:
    """
    Validate date range.
    
    Business Intent:
        Prevent invalid date ranges that could cause look-ahead bias or empty data.
    """
    # Convert to datetime if string
    if isinstance(start, str):
        try:
            start_date = pd.to_datetime(start)
        except Exception as e:
            raise ValueError(f"Invalid start date '{start}': {str(e)}") from e
    elif isinstance(start, datetime):
        start_date = start
    else:
        raise TypeError(f"Start must be str or datetime, got {type(start)}")
    
    if isinstance(end, str):
        try:
            end_date = pd.to_datetime(end)
        except Exception as e:
            raise ValueError(f"Invalid end date '{end}': {str(e)}") from e
    elif isinstance(end, datetime):
        end_date = end
    else:
        raise TypeError(f"End must be str or datetime, got {type(end)}")
    
    # Fail-fast: Start must be before end
    if start_date >= end_date:
        raise ValueError(
            f"Start date ({start_date}) must be before end date ({end_date})"
        )
    
    # Fail-fast: Reasonable date range (max 50 years)
    if (end_date - start_date).days > 50 * 365:
        raise ValueError(
            f"Date range too large: {(end_date - start_date).days} days. Maximum is 50 years."
        )
    
    return start_date, end_date


def _validate_source(source: str) -> None:
    """
    Validate data source.
    
    Business Intent:
        Prevent unknown data sources that could return invalid data.
    """
    valid_sources = ['akshare', 'yfinance', 'synthetic']
    
    if source not in valid_sources:
        raise ValueError(
            f"Unknown source '{source}'. Valid sources: {', '.join(valid_sources)}"
        )


def _ensure_timezone(df: pd.DataFrame, timezone: str = 'UTC') -> pd.DataFrame:
    """
    Ensure DataFrame has timezone-aware index.
    
    Business Intent:
        All timestamps must be timezone-aware to prevent timezone confusion.
        Default to UTC for consistency.
    """
    if df.index.tz is None:
        # Localize to UTC if naive
        df.index = df.index.tz_localize(timezone)
    else:
        # Convert to target timezone
        df.index = df.index.tz_convert(timezone)
    
    return df


def _validate_output(df: pd.DataFrame) -> None:
    """
    Validate loaded data.
    
    Business Intent:
        Ensure data quality before it enters core logic.
        Reject dirty data immediately.
    """
    # Fail-fast: Check for empty data
    if len(df) == 0:
        raise ValueError("Loaded data is empty")
    
    # Fail-fast: Check for required columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Fail-fast: Check for NaN values
    if df[required_columns].isnull().any().any():
        nan_columns = [col for col in required_columns if df[col].isnull().any()]
        raise ValueError(f"NaN values found in columns: {', '.join(nan_columns)}")
    
    # Fail-fast: Check for invalid prices
    if (df[['Open', 'High', 'Low', 'Close']] <= 0).any().any():
        raise ValueError("Non-positive prices found in data")
    
    # Fail-fast: Check for invalid volume
    if (df['Volume'] < 0).any():
        raise ValueError("Negative volume found in data")
    
    # Fail-fast: Check OHLC logic
    if (df['High'] < df['Low']).any():
        raise ValueError("High < Low found in data")
    
    if (df['High'] < df['Open']).any():
        raise ValueError("High < Open found in data")
    
    if (df['High'] < df['Close']).any():
        raise ValueError("High < Close found in data")
    
    if (df['Low'] > df['Open']).any():
        raise ValueError("Low > Open found in data")
    
    if (df['Low'] > df['Close']).any():
        raise ValueError("Low > Close found in data")


def _generate_synthetic_data(
    start: datetime,
    end: datetime,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic stock price data for testing.
    
    Business Intent:
        Generate realistic test data with known properties.
        Used for testing and development when real data is not available.
    
    Args:
        start: Start date
        end: End date
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with synthetic OHLCV data
    """
    import numpy as np
    
    # Set seed for determinism
    np.random.seed(seed)
    
    # Generate dates (business days only)
    dates = pd.date_range(start, end, freq='B')  # Business days
    n_days = len(dates)
    
    if n_days == 0:
        raise ValueError(f"No business days in range {start} to {end}")
    
    # Generate realistic returns with momentum and mean reversion
    mu = 0.0005  # Daily mean return
    sigma = 0.02  # Daily volatility
    
    # Generate returns with autocorrelation and volatility clustering
    returns = np.random.normal(mu, sigma, n_days)
    for i in range(1, n_days):
        returns[i] += 0.1 * returns[i-1]  # Autocorrelation
        returns[i] *= (1 + 0.5 * abs(returns[i-1]))  # Volatility clustering
    
    # Generate prices
    prices = 100 * np.cumprod(1 + returns)
    
    # Generate OHLCV from close prices
    df = pd.DataFrame(index=dates)
    df['Close'] = prices
    
    # Generate Open, High, Low from Close
    df['Open'] = df['Close'].shift(1).fillna(100)
    df['High'] = df['Close'] * (1 + np.abs(np.random.randn(n_days) * 0.01))
    df['Low'] = df['Close'] * (1 - np.abs(np.random.randn(n_days) * 0.01))
    df['Volume'] = np.random.randint(1e6, 1e8, n_days)
    
    # Ensure OHLC logic
    df['High'] = df[['Open', 'High', 'Low', 'Close']].max(axis=1)
    df['Low'] = df[['Open', 'High', 'Low', 'Close']].min(axis=1)
    
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]


def _load_akshare_data(
    symbol: str,
    start: datetime,
    end: datetime
) -> pd.DataFrame:
    """
    Load A-share data from akshare.
    
    Business Intent:
        Load validated A-share data for backtesting.
    """
    try:
        import akshare as ak
        
        # Remove suffix if present (akshare expects 6 digits)
        symbol_clean = symbol.split('.')[0] if '.' in symbol else symbol
        
        df = ak.stock_zh_a_hist(
            symbol=symbol_clean,
            start_date=start.strftime('%Y%m%d'),
            end_date=end.strftime('%Y%m%d'),
            adjust='qfq'  # Forward adjusted
        )
        
        # Convert column names
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        df.rename(columns={
            '开盘': 'Open',
            '收盘': 'Close',
            '最高': 'High',
            '最低': 'Low',
            '成交量': 'Volume',
            '成交额': 'Turnover'
        }, inplace=True)
        
        return df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    except Exception as e:
        raise RuntimeError(f"Failed to load from akshare: {str(e)}") from e


def _load_yfinance_data(
    symbol: str,
    start: datetime,
    end: datetime
) -> pd.DataFrame:
    """
    Load US stock data from yfinance.
    
    Business Intent:
        Load validated US stock data for backtesting.
    """
    try:
        import yfinance as yf
        
        df = yf.download(symbol, start=start, end=end)
        
        return df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    except Exception as e:
        raise RuntimeError(f"Failed to load from yfinance: {str(e)}") from e


class DataWarning(Warning):
    """
    Warning for potential data quality issues.
    
    Business Intent:
        Alert users to potential data issues without blocking execution.
    """
    pass
