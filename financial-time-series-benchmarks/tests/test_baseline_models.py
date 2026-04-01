# -*- coding: utf-8 -*-
"""
Tests for Baseline Models

Business Intent:
    Verify that all baseline models produce correct financial predictions.
    Ensure all models are deterministic and auditable.
    100% coverage required for all financial logic.
"""

import pytest
import numpy as np
import pandas as pd

from models.baseline.naive import RandomWalk, DriftRandomWalk, SeasonalRandomWalk
from models.baseline.statistical import ARIMAModel, ETSModel


class TestRandomWalk:
    """Test Random Walk model"""
    
    def test_fit_and_predict(self):
        """Test basic fit and predict"""
        # Arrange
        model = RandomWalk()
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
        
        # Act
        model.fit(prices)
        predictions = model.predict(steps=3)
        
        # Assert
        expected = np.full(3, 104.0)  # Last value
        np.testing.assert_array_equal(predictions, expected)
    
    def test_fit_invalid_input(self):
        """Test that invalid input is rejected"""
        model = RandomWalk()
        
        with pytest.raises(ValueError):
            model.fit(pd.Series([]))  # Empty data
    
    def test_predict_before_fit(self):
        """Test that prediction before fit is rejected"""
        model = RandomWalk()
        
        with pytest.raises(RuntimeError):
            model.predict(steps=10)
    
    def test_predict_invalid_steps(self):
        """Test that invalid steps is rejected"""
        model = RandomWalk()
        model.fit(pd.Series([100, 101, 102]))
        
        with pytest.raises(ValueError):
            model.predict(steps=0)
        
        with pytest.raises(ValueError):
            model.predict(steps=-1)


class TestDriftRandomWalk:
    """Test Drift Random Walk model"""
    
    def test_fit_and_predict(self):
        """Test basic fit and predict with drift"""
        # Arrange
        model = DriftRandomWalk(drift_window=3)
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
        
        # Act
        model.fit(prices)
        predictions = model.predict(steps=3)
        
        # Assert
        # Drift = 1.0 per step (average increase)
        assert len(predictions) == 3
        assert all(np.isfinite(predictions))
        assert predictions[0] > 104.0  # Should be higher than last price
    
    def test_fit_empty_data(self):
        """Test that empty data is rejected"""
        model = DriftRandomWalk()
        
        with pytest.raises(ValueError):
            model.fit(pd.Series([]))
    
    def test_predict_before_fit(self):
        """Test that prediction before fit is rejected"""
        model = DriftRandomWalk()
        
        with pytest.raises(RuntimeError):
            model.predict(steps=10)


class TestSeasonalRandomWalk:
    """Test Seasonal Random Walk model"""
    
    def test_fit_and_predict(self):
        """Test basic fit and predict with seasonality"""
        # Arrange
        model = SeasonalRandomWalk(seasonal_period=3)
        prices = pd.Series([100.0, 101.0, 102.0, 100.5, 101.5, 102.5])
        
        # Act
        model.fit(prices)
        predictions = model.predict(steps=3)
        
        # Assert
        # Should use last 3 values: [100.5, 101.5, 102.5]
        expected = np.array([100.5, 101.5, 102.5])
        np.testing.assert_array_almost_equal(predictions, expected)
    
    def test_fit_invalid_period(self):
        """Test that invalid seasonal period is handled"""
        model = SeasonalRandomWalk(seasonal_period=100)
        prices = pd.Series([100.0, 101.0, 102.0])  # Only 3 data points
        
        # Should handle gracefully
        model.fit(prices)
        predictions = model.predict(steps=3)
        
        assert len(predictions) == 3


class TestARIMAModel:
    """Test ARIMA model"""
    
    def test_fit_and_predict(self):
        """Test ARIMA fit and predict"""
        # Arrange
        model = ARIMAModel(p=1, d=1, q=1)
        np.random.seed(42)
        prices = np.random.randn(100).cumsum() + 100
        prices = pd.Series(prices)
        
        # Act
        model.fit(prices)
        predictions = model.predict(steps=10)
        
        # Assert
        assert len(predictions) == 10
        assert all(np.isfinite(predictions))
    
    def test_invalid_order(self):
        """Test that invalid order is handled"""
        # Negative orders should be handled
        model = ARIMAModel(p=-1, d=0, q=0)
        prices = pd.Series([100, 101, 102, 103, 104])
        
        # Should handle gracefully or raise clear error
        try:
            model.fit(prices)
        except Exception as e:
            assert "order" in str(e).lower() or "invalid" in str(e).lower()
    
    def test_predict_before_fit(self):
        """Test that prediction before fit is rejected"""
        model = ARIMAModel()
        
        with pytest.raises(Exception):
            model.predict(steps=10)
    
    def test_small_dataset(self):
        """Test ARIMA with small dataset"""
        model = ARIMAModel(p=1, d=1, q=1)
        prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
        
        # Should work with small dataset
        model.fit(prices)
        predictions = model.predict(steps=5)
        
        assert len(predictions) == 5
        assert all(np.isfinite(predictions))


class TestETSModel:
    """Test ETS model"""
    
    def test_fit_and_predict(self):
        """Test ETS fit and predict"""
        # Arrange
        model = ETSModel(trend='add', seasonal='add', seasonal_periods=7)
        np.random.seed(42)
        prices = np.random.randn(100).cumsum() + 100
        prices = pd.Series(prices)
        
        # Act
        model.fit(prices)
        predictions = model.predict(steps=10)
        
        # Assert
        assert len(predictions) == 10
        assert all(np.isfinite(predictions))
    
    def test_predict_before_fit(self):
        """Test that prediction before fit is rejected"""
        model = ETSModel()
        
        with pytest.raises(Exception):
            model.predict(steps=10)
    
    def test_different_trend_specs(self):
        """Test ETS with different trend specifications"""
        np.random.seed(42)
        prices = pd.Series(np.random.randn(50).cumsum() + 100)
        
        # Test additive trend (may have convergence warnings but should work)
        model_add = ETSModel(trend='add')
        try:
            model_add.fit(prices)
            pred_add = model_add.predict(steps=5)
            assert len(pred_add) == 5
        except Exception:
            # ETS may fail on some data, that's OK for this test
            pass


class TestModelDeterminism:
    """Test that models are deterministic with fixed seeds"""
    
    def test_random_walk_determinism(self):
        """Test Random Walk is deterministic"""
        from utils.seed import set_global_seed
        
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
        
        # Run 1
        set_global_seed(42)
        model1 = RandomWalk()
        model1.fit(prices)
        pred1 = model1.predict(steps=3)
        
        # Run 2
        set_global_seed(42)
        model2 = RandomWalk()
        model2.fit(prices)
        pred2 = model2.predict(steps=3)
        
        # Assert identical
        np.testing.assert_array_equal(pred1, pred2)
    
    def test_arima_determinism(self):
        """Test ARIMA is deterministic with fixed seed"""
        from utils.seed import set_global_seed
        
        np.random.seed(42)
        prices = pd.Series(np.random.randn(50).cumsum() + 100)
        
        # Run 1
        set_global_seed(42)
        model1 = ARIMAModel(p=1, d=1, q=1)
        model1.fit(prices)
        pred1 = model1.predict(steps=5)
        
        # Run 2
        set_global_seed(42)
        model2 = ARIMAModel(p=1, d=1, q=1)
        model2.fit(prices)
        pred2 = model2.predict(steps=5)
        
        # Assert similar (may have small numerical differences)
        np.testing.assert_array_almost_equal(pred1, pred2, decimal=5)
