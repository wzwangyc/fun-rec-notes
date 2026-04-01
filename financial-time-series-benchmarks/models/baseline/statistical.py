# -*- coding: utf-8 -*-
"""
Statistical Models
"""

import numpy as np
import pandas as pd
from models.base import BaseModel
from statsmodels.tsa.arima.model import ARIMA
try:
    from arch import arch_model
    HAS_ARCH = True
except:
    HAS_ARCH = False
from statsmodels.tsa.holtwinters import ExponentialSmoothing
class ARIMAModel(BaseModel):
    """ARIMA(p,d,q) Model"""
    
    def __init__(self, p=1, d=1, q=1):
        super().__init__(f"ARIMA({p},{d},{q})")
        self.p = p
        self.d = d
        self.q = q
        self.model = None
        self.results = None
    
    def fit(self, df):
        if isinstance(df, pd.DataFrame):
            df = df['Close']
        self.model = ARIMA(df, order=(self.p, self.d, self.q))
        self.results = self.model.fit()
        self.is_fitted = True
    
    def predict(self, steps):
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        return self.results.forecast(steps)

class GARCHModel(BaseModel):
    """GARCH(p,q) Model for Volatility"""
    
    def __init__(self, p=1, q=1):
        super().__init__(f"GARCH({p},{q})")
        self.p = p
        self.q = q
        self.model = None
        self.results = None
    
    def fit(self, df):
        if isinstance(df, pd.DataFrame):
            df = df['Close'].pct_change().dropna() * 100  # Convert to percentage
        self.model = GARCH(df)
        self.results = self.model.fit()
        self.is_fitted = True
    
    def predict(self, steps):
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        return self.results.forecast(horizon=steps)

class ETSModel(BaseModel):
    """ETS (Error, Trend, Seasonal) Model"""
    
    def __init__(self, trend='add', seasonal='add', seasonal_periods=252):
        super().__init__("ETS")
        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None
        self.results = None
    
    def fit(self, df):
        if isinstance(df, pd.DataFrame):
            df = df['Close']
        self.model = ExponentialSmoothing(
            df,
            trend=self.trend,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods
        )
        self.results = self.model.fit()
        self.is_fitted = True
    
    def predict(self, steps):
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        return self.results.forecast(steps)

# ThetaModel temporarily disabled due to statsmodels version
