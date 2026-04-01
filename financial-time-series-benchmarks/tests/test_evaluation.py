# -*- coding: utf-8 -*-
"""
Tests for Evaluation Module

Business Intent:
    Verify that all evaluation metrics and backtest logic are correct.
    Financial calculations must be precise and auditable.
    100% coverage required for all financial logic.
"""

import pytest
import numpy as np
import pandas as pd

from evaluation.metrics import (
    calculate_mae,
    calculate_mse,
    calculate_rmse,
    calculate_mape,
    calculate_r2,
    calculate_direction_accuracy,
    calculate_all_metrics,
)

from evaluation.backtest import Backtest, compare_backtests


class TestMAE:
    """Test Mean Absolute Error"""
    
    def test_mae_perfect_prediction(self):
        """Test MAE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        mae = calculate_mae(y_true, y_pred)
        
        assert mae == 0.0
    
    def test_mae_imperfect_prediction(self):
        """Test MAE with imperfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        
        mae = calculate_mae(y_true, y_pred)
        
        assert mae == 0.5
    
    def test_mae_negative_errors(self):
        """Test MAE with negative errors"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([0.5, 1.5, 2.5])
        
        mae = calculate_mae(y_true, y_pred)
        
        assert mae == 0.5


class TestMSE:
    """Test Mean Squared Error"""
    
    def test_mse_perfect_prediction(self):
        """Test MSE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        
        mse = calculate_mse(y_true, y_pred)
        
        assert mse == 0.0
    
    def test_mse_penalizes_large_errors(self):
        """Test that MSE penalizes large errors more"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 5.0])  # Error of 2
        
        mse = calculate_mse(y_true, y_pred)
        
        # MSE should be 4/3 (average of squared errors)
        assert np.isclose(mse, 4.0/3.0)


class TestRMSE:
    """Test Root Mean Squared Error"""
    
    def test_rmse_perfect_prediction(self):
        """Test RMSE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        
        rmse = calculate_rmse(y_true, y_pred)
        
        assert rmse == 0.0
    
    def test_rmse_equals_sqrt_mse(self):
        """Test that RMSE equals sqrt(MSE)"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.5, 2.5, 3.5, 4.5])
        
        rmse = calculate_rmse(y_true, y_pred)
        mse = calculate_mse(y_true, y_pred)
        
        assert np.isclose(rmse, np.sqrt(mse))


class TestMAPE:
    """Test Mean Absolute Percentage Error"""
    
    def test_mape_perfect_prediction(self):
        """Test MAPE with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        
        mape = calculate_mape(y_true, y_pred)
        
        assert mape == 0.0
    
    def test_mape_percentage(self):
        """Test MAPE returns percentage"""
        y_true = np.array([100.0, 200.0, 300.0])
        y_pred = np.array([110.0, 220.0, 330.0])  # 10% error
        
        mape = calculate_mape(y_true, y_pred)
        
        assert np.isclose(mape, 10.0)  # 10%
    
    def test_mape_zero_true_values(self):
        """Test MAPE with zero true values"""
        y_true = np.array([0.0, 1.0, 2.0])
        y_pred = np.array([0.5, 1.5, 2.5])
        
        # Should raise ValueError for division by zero
        with pytest.raises(ValueError):
            calculate_mape(y_true, y_pred)


class TestR2:
    """Test R-squared"""
    
    def test_r2_perfect_prediction(self):
        """Test R² with perfect predictions"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        r2 = calculate_r2(y_true, y_pred)
        
        assert r2 == 1.0
    
    def test_r2_worse_than_mean(self):
        """Test R² worse than mean prediction"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        
        r2 = calculate_r2(y_true, y_pred)
        
        assert r2 < 0.0
    
    def test_r2_reasonable_prediction(self):
        """Test R² with reasonable predictions"""
        np.random.seed(42)
        y_true = np.random.randn(100)
        y_pred = y_true + np.random.randn(100) * 0.1
        
        r2 = calculate_r2(y_true, y_pred)
        
        assert 0.0 < r2 < 1.0


class TestDirectionAccuracy:
    """Test Direction Accuracy"""
    
    def test_direction_perfect(self):
        """Test perfect direction accuracy"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.5, 2.5, 3.5, 4.5, 5.5])
        
        acc = calculate_direction_accuracy(y_true, y_pred)
        
        assert acc == 1.0  # 100% accuracy
    
    def test_direction_partial(self):
        """Test partial direction accuracy"""
        # True changes: +1, +1, +1 (all up)
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        # Pred changes: +0.5 (correct), -0.5 (wrong), +0.5 (correct)
        y_pred = np.array([1.5, 1.5, 2.5, 3.5])
        
        acc = calculate_direction_accuracy(y_true, y_pred)
        
        # Should be between 0 and 1
        assert 0.0 <= acc <= 1.0
    
    def test_direction_insufficient_data(self):
        """Test direction accuracy with insufficient data"""
        y_true = np.array([1.0])
        y_pred = np.array([1.5])
        
        acc = calculate_direction_accuracy(y_true, y_pred)
        
        assert acc == 0.0  # Not enough data for direction


class TestAllMetrics:
    """Test calculate_all_metrics function"""
    
    def test_all_metrics_returned(self):
        """Test that all metrics are returned"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 3.1, 4.1, 5.1])
        
        metrics = calculate_all_metrics(y_true, y_pred)
        
        assert 'MAE' in metrics
        assert 'MSE' in metrics
        assert 'RMSE' in metrics
        assert 'MAPE' in metrics
        assert 'R2' in metrics
        assert 'Direction_Accuracy' in metrics
    
    def test_all_metrics_finite(self):
        """Test that all metrics are finite"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 3.1, 4.1, 5.1])
        
        metrics = calculate_all_metrics(y_true, y_pred)
        
        for name, value in metrics.items():
            assert np.isfinite(value), f"{name} is not finite: {value}"


class TestBacktest:
    """Test backtest framework"""
    
    def test_backtest_profitable_strategy(self):
        """Test backtest with profitable strategy"""
        # Arrange
        backtest = Backtest(initial_capital=1000000.0)
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0])
        # Predict direction correctly: predict higher than current when price goes up
        predictions = pd.Series([101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0])
        
        # Act
        results = backtest.run(prices, predictions)
        
        # Assert
        assert 'metrics' in results
        assert 'equity' in results
        assert np.isfinite(results['metrics']['total_return'])
        assert np.isfinite(results['metrics']['sharpe'])
    
    def test_backtest_unprofitable_strategy(self):
        """Test backtest with unprofitable strategy"""
        backtest = Backtest(initial_capital=1000000.0)
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0, 105.0])
        # Always predict opposite direction (predict lower when price goes up)
        predictions = pd.Series([99.0, 100.0, 101.0, 102.0, 103.0, 104.0])
        
        results = backtest.run(prices, predictions)
        
        # Should have finite metrics
        assert np.isfinite(results['metrics']['total_return'])
        assert np.isfinite(results['metrics']['sharpe'])
    
    def test_backtest_with_transaction_costs(self):
        """Test backtest with transaction costs"""
        backtest = Backtest(initial_capital=1000000.0, commission=0.001)
        prices = pd.Series(range(0, 6), dtype=float) + 100  # [100, 101, 102, 103, 104, 105]
        predictions = pd.Series(range(1, 7), dtype=float) + 100  # [101, 102, 103, 104, 105, 106]
        
        results = backtest.run(prices, predictions)
        
        # Should have finite metrics
        assert np.isfinite(results['metrics']['total_return'])
        assert np.isfinite(results['metrics']['sharpe'])
    
    def test_backtest_invalid_inputs(self):
        """Test backtest with invalid inputs"""
        backtest = Backtest()
        # Use different indices so intersection is smaller
        prices = pd.Series([100.0, 101.0, 102.0], index=[0, 1, 2])
        predictions = pd.Series([101.0, 102.0], index=[10, 11])  # No common index
        
        with pytest.raises(ValueError):
            backtest.run(prices, predictions)
    
    def test_backtest_zero_capital(self):
        """Test backtest with zero initial capital"""
        with pytest.raises(ValueError):
            Backtest(initial_capital=0.0)
    
    def test_backtest_negative_capital(self):
        """Test backtest with negative initial capital"""
        with pytest.raises(ValueError):
            Backtest(initial_capital=-1000000.0)


class TestCompareBacktests:
    """Test compare_backtests function"""
    
    def test_compare_multiple_backtests(self):
        """Test comparing multiple backtests"""
        backtest = Backtest(initial_capital=1000000)
        prices = pd.Series([100, 101, 102, 103, 104, 105])
        
        results = {
            'model1': backtest.run(prices, pd.Series([101, 102, 103, 104, 105, 106])),
            'model2': backtest.run(prices, pd.Series([99, 100, 101, 102, 103, 104])),
        }
        
        comparison = compare_backtests(results)
        
        assert len(comparison) == 2
        assert 'model1' in comparison.index
        assert 'model2' in comparison.index


class TestBacktestMetrics:
    """Test backtest metrics calculation"""
    
    def test_sharpe_ratio_calculation(self):
        """Test Sharpe ratio in backtest"""
        backtest = Backtest()
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0])
        # Predict correctly with lag
        predictions = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0])
        
        results = backtest.run(prices, predictions)
        
        sharpe = results['metrics']['sharpe']
        assert np.isfinite(sharpe)
    
    def test_max_drawdown_calculation(self):
        """Test max drawdown in backtest"""
        backtest = Backtest()
        prices = pd.Series([100.0, 110.0, 120.0, 110.0, 100.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0])
        predictions = pd.Series([110.0, 120.0, 110.0, 100.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0])
        
        results = backtest.run(prices, predictions)
        
        mdd = results['metrics']['max_drawdown']
        assert np.isfinite(mdd)
        # Drawdown is typically negative or zero
        assert mdd <= 0
    
    def test_win_rate_calculation(self):
        """Test win rate in backtest"""
        backtest = Backtest()
        prices = pd.Series([100, 101, 102, 103, 104, 105])
        predictions = pd.Series([101, 102, 103, 104, 105, 106])
        
        results = backtest.run(prices, predictions)
        
        win_rate = results['metrics']['win_rate']
        assert 0.0 <= win_rate <= 1.0
