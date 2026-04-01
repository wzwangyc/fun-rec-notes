# -*- coding: utf-8 -*-
"""
Base Model Class
"""

import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for all forecasting models"""
    
    def __init__(self, name="BaseModel"):
        self.name = name
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, df):
        """Fit the model to training data"""
        pass
    
    @abstractmethod
    def predict(self, steps):
        """Predict future values"""
        pass
    
    def fit_predict(self, df, steps):
        """Fit and predict in one step"""
        self.fit(df)
        return self.predict(steps)
    
    def evaluate(self, y_true, y_pred):
        """Evaluate model performance"""
        from evaluation.metrics import calculate_all_metrics
        return calculate_all_metrics(y_true, y_pred)
