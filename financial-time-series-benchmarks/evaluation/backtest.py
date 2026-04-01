# -*- coding: utf-8 -*-
"""
Backtest Framework
"""

import numpy as np
import pandas as pd

class Backtest:
    """
    Simple backtest framework for evaluating predictions
    
    Business Intent:
        Evaluate trading strategy performance with realistic transaction costs.
        Calculate standard financial metrics (Sharpe, MaxDD, etc.).
    
    Fail-Fast:
        - Invalid capital → ValueError
        - Mismatched lengths → ValueError
        - Empty data → ValueError
    """
    
    def __init__(self, initial_capital=1000000, commission=0.0003, slippage=0.0005):
        """
        Initialize backtest
        
        Business Intent:
            Configure backtest with realistic parameters.
        
        Args:
            initial_capital: Initial capital (must be positive)
            commission: Commission rate (0.03% = 0.0003)
            slippage: Slippage rate (0.05% = 0.0005)
        
        Fail-Fast:
            - Zero or negative capital → ValueError
        """
        # Fail-fast: Validate capital
        if not isinstance(initial_capital, (int, float)) or initial_capital <= 0:
            raise ValueError(f"Initial capital must be positive, got {initial_capital}")
        
        self.initial_capital = float(initial_capital)
        self.commission = commission
        self.slippage = slippage
    
    def run(self, prices, predictions, position_size=1.0):
        """
        Run backtest
        
        Business Intent:
            Execute backtest with given predictions.
            Calculate all performance metrics.
        
        Args:
            prices: Series of prices (must match predictions length)
            predictions: Series of predicted prices
            position_size: Position size (1.0 = 100% capital)
        
        Returns:
            Dictionary with backtest results
        
        Fail-Fast:
            - Mismatched lengths → ValueError
            - Empty data → ValueError
        """
        # Fail-fast: Validate inputs
        if len(prices) == 0 or len(predictions) == 0:
            raise ValueError("Prices and predictions cannot be empty")
        
        # Align prices and predictions
        common_idx = prices.index.intersection(predictions.index)
        
        if len(common_idx) == 0:
            raise ValueError("Prices and predictions have no common index")
        
        prices = prices.loc[common_idx]
        predictions = predictions.loc[common_idx]
        
        if len(prices) != len(predictions):
            raise ValueError(f"Prices and predictions length mismatch: {len(prices)} vs {len(predictions)}")
        
        # Generate signals
        # Long if prediction > current price, Short if prediction < current price
        signals = np.sign(predictions - prices)
        
        # Calculate returns
        returns = prices.pct_change()
        
        # Strategy returns (with lag to avoid lookahead bias)
        # Fill NaN with 0 for first period
        lagged_signals = signals.shift(1).fillna(0)
        strategy_returns = lagged_signals * returns.fillna(0)
        
        # Apply transaction costs
        trades = signals.diff().abs()
        strategy_returns -= trades * (self.commission + self.slippage)
        
        # Calculate cumulative returns
        # Fill NaN in first period with 0 (no return on day 1)
        strategy_returns_filled = strategy_returns.fillna(0)
        cumulative_returns = (1 + strategy_returns_filled).cumprod()
        
        # Calculate equity curve
        equity = self.initial_capital * cumulative_returns
        
        # Calculate metrics
        metrics = self._calculate_metrics(equity, strategy_returns)
        
        return {
            'equity': equity,
            'returns': strategy_returns,
            'cumulative_returns': cumulative_returns,
            'signals': signals,
            'metrics': metrics
        }
    
    def _calculate_metrics(self, equity, returns):
        """
        Calculate performance metrics
        
        Business Intent:
            Calculate standard financial metrics for strategy evaluation.
            All metrics must be finite and auditable.
        
        Args:
            equity: Equity curve (pandas Series)
            returns: Strategy returns (pandas Series)
        
        Returns:
            Dictionary with metrics (all finite values)
        """
        # Total return
        total_return = (equity.iloc[-1] / equity.iloc[0]) - 1
        
        # Annualized return (assuming 252 trading days)
        n_days = len(equity)
        annualized_return = (equity.iloc[-1] / equity.iloc[0]) ** (252 / n_days) - 1
        
        # Volatility
        volatility = returns.std() * np.sqrt(252)
        
        # Sharpe ratio (assuming risk-free rate = 0)
        # Handle zero volatility and NaN returns
        if volatility > 0 and np.isfinite(annualized_return):
            sharpe = annualized_return / volatility
        else:
            sharpe = 0.0
        
        # Maximum drawdown
        rolling_max = equity.expanding().max()
        drawdown = (equity - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Win rate
        valid_returns = returns.dropna()
        if len(valid_returns) > 0:
            win_rate = (valid_returns > 0).sum() / len(valid_returns)
        else:
            win_rate = 0.0
        
        # Profit factor
        gross_profit = valid_returns[valid_returns > 0].sum()
        gross_loss = abs(valid_returns[valid_returns < 0].sum())
        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
        elif gross_profit > 0:
            profit_factor = float('inf')
        else:
            profit_factor = 1.0
        
        return {
            'total_return': float(total_return),
            'annualized_return': float(annualized_return),
            'volatility': float(volatility),
            'sharpe': float(sharpe),
            'max_drawdown': float(max_drawdown),
            'win_rate': float(win_rate),
            'profit_factor': float(profit_factor)
        }

def compare_backtests(results_dict):
    """
    Compare multiple backtest results
    
    Args:
        results_dict: Dictionary of {model_name: backtest_result}
    
    Returns:
        DataFrame with comparison metrics
    """
    metrics_list = []
    
    for model_name, result in results_dict.items():
        metrics = result['metrics'].copy()
        metrics['model'] = model_name
        metrics_list.append(metrics)
    
    comparison_df = pd.DataFrame(metrics_list)
    comparison_df.set_index('model', inplace=True)
    
    return comparison_df
