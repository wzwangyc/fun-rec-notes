# -*- coding: utf-8 -*-
"""
Visualization Module
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_predictions(y_true, y_pred, model_name="Model", save_path=None):
    """
    Plot actual vs predicted values
    
    Args:
        y_true: Actual values
        y_pred: Predicted values
        model_name: Model name for title
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Time series plot
    axes[0].plot(y_true, label='Actual', linewidth=2)
    axes[0].plot(y_pred, label='Predicted', linewidth=2, linestyle='--')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Price')
    axes[0].set_title(f'{model_name} - Actual vs Predicted')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Residual plot
    residuals = y_true - y_pred
    axes[1].plot(residuals, color='red', linewidth=1)
    axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Residual')
    axes[1].set_title('Residuals')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  [OK] Chart saved to {save_path}")
    
    plt.show()

def plot_backtest_results(backtest_result, model_name="Model", save_path=None):
    """
    Plot backtest results
    
    Args:
        backtest_result: Dictionary with backtest results
        model_name: Model name for title
        save_path: Path to save figure
    """
    equity = backtest_result['equity']
    metrics = backtest_result['metrics']
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # Equity curve
    axes[0].plot(equity, linewidth=2)
    axes[0].set_xlabel('Trading Days')
    axes[0].set_ylabel('Equity')
    axes[0].set_title(f'{model_name} - Equity Curve')
    axes[0].grid(True, alpha=0.3)
    
    # Add metrics text
    metrics_text = f"Sharpe: {metrics['sharpe']:.2f}\n"
    metrics_text += f"MaxDD: {metrics['max_drawdown']:.2%}\n"
    metrics_text += f"Return: {metrics['total_return']:.2%}"
    axes[0].text(0.02, 0.98, metrics_text, transform=axes[0].transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Returns histogram
    returns = backtest_result['returns']
    axes[1].hist(returns, bins=50, alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('Return')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Return Distribution')
    axes[1].grid(True, alpha=0.3)
    
    # Drawdown
    rolling_max = equity.expanding().max()
    drawdown = (equity - rolling_max) / rolling_max
    axes[2].plot(drawdown, color='red', linewidth=1)
    axes[2].fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
    axes[2].set_xlabel('Trading Days')
    axes[2].set_ylabel('Drawdown')
    axes[2].set_title('Drawdown')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  [OK] Chart saved to {save_path}")
    
    plt.show()

def plot_model_comparison(results_df, metric='RMSE', save_path=None):
    """
    Plot model comparison
    
    Args:
        results_df: DataFrame with model results
        metric: Metric to plot ('RMSE', 'MAPE', 'Sharpe', etc.)
        save_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Sort by metric
    sorted_df = results_df.sort_values(metric)
    
    # Bar chart
    bars = ax.barh(sorted_df.index, sorted_df[metric])
    ax.set_xlabel(metric)
    ax.set_title(f'Model Comparison - {metric}')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar, value in zip(bars, sorted_df[metric]):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2,
                f'{value:.4f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  [OK] Chart saved to {save_path}")
    
    plt.show()
