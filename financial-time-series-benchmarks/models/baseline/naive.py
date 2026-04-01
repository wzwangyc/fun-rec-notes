# -*- coding: utf-8 -*-
"""
Naive Baseline Models
"""

import numpy as np
import pandas as pd
from models.base import BaseModel

class RandomWalk(BaseModel):
    """
    Random Walk Model: y(t) = y(t-1)
    
    Business Intent:
        Simple baseline model assuming next value equals current value.
        Used as benchmark for more complex models.
    
    Fail-Fast:
        - Empty data → ValueError
        - Predict before fit → RuntimeError
        - Invalid steps → ValueError
    """
    
    def __init__(self):
        super().__init__("Random Walk")
        self.last_value = None
    
    def fit(self, df):
        # Fail-fast: Validate input
        if isinstance(df, pd.DataFrame):
            df = df['Close']
        
        if len(df) == 0:
            raise ValueError("Input data cannot be empty")
        
        self.last_value = df.iloc[-1]
        self.is_fitted = True
    
    def predict(self, steps):
        # Fail-fast: Check fitted
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
        
        # Fail-fast: Validate steps
        if not isinstance(steps, int) or steps <= 0:
            raise ValueError(f"Steps must be positive integer, got {steps}")
        
        return np.full(steps, self.last_value)

class SeasonalRandomWalk(BaseModel):
    """
    Seasonal Random Walk: y(t) = y(t-T)
    
    Business Intent:
        Model with seasonal pattern, using values from previous season.
        Useful for data with yearly/weekly seasonality.
    
    Fail-Fast:
        - Insufficient data for season → ValueError
        - Predict before fit → RuntimeError
    """
    
    def __init__(self, seasonal_period=252):
        super().__init__("Seasonal RW")
        self.seasonal_period = seasonal_period
        self.seasonal_values = None
    
    def fit(self, df):
        # Fail-fast: Validate input
        if isinstance(df, pd.DataFrame):
            df = df['Close']
        
        if len(df) == 0:
            raise ValueError("Input data cannot be empty")
        
        # Handle case where data is shorter than seasonal period
        if len(df) < self.seasonal_period:
            # Use all available data
            self.seasonal_values = df.values
        else:
            self.seasonal_values = df.iloc[-self.seasonal_period:].values
        
        self.is_fitted = True
    
    def predict(self, steps):
        # Fail-fast: Check fitted
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
        
        predictions = []
        for i in range(steps):
            idx = i % len(self.seasonal_values)
            predictions.append(self.seasonal_values[idx])
        return np.array(predictions)

class DriftRandomWalk(BaseModel):
    """
    Random Walk with Drift: y(t) = y(t-1) + mean(drift)
    
    Business Intent:
        Random walk with drift term based on historical average return.
        Captures long-term trend in data.
    
    Fail-Fast:
        - Empty data → ValueError
        - Predict before fit → RuntimeError
        - Invalid steps → ValueError
    """
    
    def __init__(self, drift_window=252):
        super().__init__("Drift RW")
        self.drift_window = drift_window
        self.last_value = None
        self.drift = None
    
    def fit(self, df):
        # Fail-fast: Validate input
        if isinstance(df, pd.DataFrame):
            df = df['Close']
        
        if len(df) == 0:
            raise ValueError("Input data cannot be empty")
        
        self.last_value = df.iloc[-1]
        returns = df.pct_change().dropna()
        
        if len(returns) == 0:
            raise ValueError("Cannot calculate drift: no valid returns")
        
        self.drift = returns.iloc[-self.drift_window:].mean()
        self.is_fitted = True
    
    def predict(self, steps):
        # Fail-fast: Check fitted
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
        
        # Fail-fast: Validate steps
        if not isinstance(steps, int) or steps <= 0:
            raise ValueError(f"Steps must be positive integer, got {steps}")
        
        predictions = []
        current = self.last_value
        for _ in range(steps):
            current = current * (1 + self.drift)
            predictions.append(current)
        return np.array(predictions)
