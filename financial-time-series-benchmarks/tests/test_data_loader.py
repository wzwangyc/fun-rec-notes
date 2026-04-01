# -*- coding: utf-8 -*-
"""
Tests for Data Loader Input Validation

Business Intent:
    Verify that all external inputs are validated at boundaries.
    Ensure dirty data is rejected before entering core logic.
    100% coverage required for all validation logic.
"""

import pytest
from datetime import datetime, timezone
import pandas as pd

from data.loader import (
    load_stock_data,
    _validate_symbol,
    _validate_date_range,
    _validate_source,
    _validate_output,
    DataWarning,
)


class TestSymbolValidation:
    """Test symbol validation"""
    
    def test_valid_symbol(self):
        """Test valid symbol passes"""
        # Should not raise
        _validate_symbol('AAPL', 'yfinance')
        _validate_symbol('000001.SZ', 'akshare')
    
    def test_empty_symbol(self):
        """Test that empty symbol is rejected"""
        with pytest.raises(ValueError):
            _validate_symbol('', 'akshare')
    
    def test_none_symbol(self):
        """Test that None symbol is rejected"""
        with pytest.raises(ValueError):
            _validate_symbol(None, 'akshare')
    
    def test_non_string_symbol(self):
        """Test that non-string symbol is rejected"""
        with pytest.raises(ValueError):
            _validate_symbol(123, 'akshare')
    
    def test_whitespace_symbol(self):
        """Test that whitespace symbol is rejected"""
        with pytest.raises(ValueError):
            _validate_symbol('   ', 'akshare')
    
    def test_invalid_akshare_symbol_warns(self):
        """Test that invalid A-share symbol format warns"""
        with pytest.warns(DataWarning):
            _validate_symbol('INVALID', 'akshare')


class TestDateRangeValidation:
    """Test date range validation"""
    
    def test_valid_date_range_strings(self):
        """Test valid date range with strings"""
        start, end = _validate_date_range('2023-01-01', '2023-12-31')
        assert start < end
    
    def test_valid_date_range_datetime(self):
        """Test valid date range with datetime"""
        start = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end = datetime(2023, 12, 31, tzinfo=timezone.utc)
        result_start, result_end = _validate_date_range(start, end)
        assert result_start < result_end
    
    def test_start_after_end(self):
        """Test that start after end is rejected"""
        with pytest.raises(ValueError):
            _validate_date_range('2023-12-31', '2023-01-01')
    
    def test_start_equals_end(self):
        """Test that start equals end is rejected"""
        with pytest.raises(ValueError):
            _validate_date_range('2023-01-01', '2023-01-01')
    
    def test_range_too_large(self):
        """Test that range > 50 years is rejected"""
        with pytest.raises(ValueError):
            _validate_date_range('1900-01-01', '2100-01-01')
    
    def test_invalid_start_date(self):
        """Test that invalid start date is rejected"""
        with pytest.raises(ValueError):
            _validate_date_range('not-a-date', '2023-12-31')
    
    def test_invalid_end_date(self):
        """Test that invalid end date is rejected"""
        with pytest.raises(ValueError):
            _validate_date_range('2023-01-01', 'not-a-date')
    
    def test_invalid_start_type(self):
        """Test that invalid start type is rejected"""
        with pytest.raises(TypeError):
            _validate_date_range(123, '2023-12-31')
    
    def test_invalid_end_type(self):
        """Test that invalid end type is rejected"""
        with pytest.raises(TypeError):
            _validate_date_range('2023-01-01', 123)


class TestSourceValidation:
    """Test source validation"""
    
    def test_valid_sources(self):
        """Test valid sources"""
        _validate_source('akshare')
        _validate_source('yfinance')
        _validate_source('synthetic')
    
    def test_invalid_source(self):
        """Test that invalid source is rejected"""
        with pytest.raises(ValueError):
            _validate_source('invalid_source')
    
    def test_case_sensitive_source(self):
        """Test that source is case-sensitive"""
        with pytest.raises(ValueError):
            _validate_source('Akshare')  # Wrong case


class TestOutputValidation:
    """Test output validation"""
    
    def test_valid_dataframe(self):
        """Test valid DataFrame passes validation"""
        df = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        # Should not raise
        _validate_output(df)
    
    def test_empty_dataframe(self):
        """Test that empty DataFrame is rejected"""
        df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_missing_columns(self):
        """Test that missing columns are rejected"""
        df = pd.DataFrame({
            'Open': [100.0],
            'Close': [101.0]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_nan_values(self):
        """Test that NaN values are rejected"""
        df = pd.DataFrame({
            'Open': [100.0, np.nan],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_non_positive_prices(self):
        """Test that non-positive prices are rejected"""
        df = pd.DataFrame({
            'Open': [100.0, -1.0],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_negative_volume(self):
        """Test that negative volume is rejected"""
        df = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, -1]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_high_less_than_low(self):
        """Test that High < Low is rejected"""
        df = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 99.0],  # Invalid: High < Low
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_high_less_than_open(self):
        """Test that High < Open is rejected"""
        df = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [99.0, 103.0],  # Invalid: High < Open
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)
    
    def test_low_greater_than_open(self):
        """Test that Low > Open is rejected"""
        df = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [101.0, 100.0],  # Invalid: Low > Open
            'Close': [101.0, 102.0],
            'Volume': [1000000, 2000000]
        })
        
        with pytest.raises(ValueError):
            _validate_output(df)


class TestLoadStockData:
    """Test load_stock_data function"""
    
    def test_load_synthetic_data(self):
        """Test loading synthetic data"""
        df = load_stock_data(
            symbol='TEST',
            start='2023-01-01',
            end='2023-01-31',
            source='synthetic'
        )
        
        # Validate output
        assert len(df) > 0
        assert all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
        assert df.index.tz is not None  # Timezone-aware
    
    def test_load_invalid_symbol(self):
        """Test that invalid symbol raises error"""
        with pytest.raises(ValueError):
            load_stock_data(
                symbol='',
                start='2023-01-01',
                end='2023-01-31',
                source='synthetic'
            )
    
    def test_load_invalid_date_range(self):
        """Test that invalid date range raises error"""
        with pytest.raises(ValueError):
            load_stock_data(
                symbol='TEST',
                start='2023-12-31',
                end='2023-01-01',
                source='synthetic'
            )
    
    def test_load_invalid_source(self):
        """Test that invalid source raises error"""
        with pytest.raises(ValueError):
            load_stock_data(
                symbol='TEST',
                start='2023-01-01',
                end='2023-01-31',
                source='invalid'
            )


# Import numpy for NaN tests
import numpy as np
