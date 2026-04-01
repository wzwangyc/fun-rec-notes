# -*- coding: utf-8 -*-
"""
Evaluation Metrics
"""

import numpy as np

def calculate_mae(y_true, y_pred):
    """Mean Absolute Error"""
    return np.mean(np.abs(y_true - y_pred))

def calculate_mse(y_true, y_pred):
    """Mean Squared Error"""
    return np.mean((y_true - y_pred) ** 2)

def calculate_rmse(y_true, y_pred):
    """Root Mean Squared Error"""
    return np.sqrt(calculate_mse(y_true, y_pred))

def calculate_mape(y_true, y_pred):
    """
    Mean Absolute Percentage Error
    
    Business Intent:
        Calculate percentage error for interpretability.
        Useful for comparing accuracy across different scales.
    
    Fail-Fast:
        - Zero in y_true → ValueError (division by zero)
    """
    # Fail-fast: Check for zeros
    if np.any(y_true == 0):
        raise ValueError("MAPE undefined: y_true contains zeros (division by zero)")
    
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def calculate_r2(y_true, y_pred):
    """R-squared"""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

def calculate_direction_accuracy(y_true, y_pred):
    """Direction Accuracy"""
    if len(y_true) < 2:
        return 0.0
    true_direction = np.diff(y_true) > 0
    pred_direction = np.diff(y_pred) > 0
    return np.mean(true_direction == pred_direction)

def calculate_all_metrics(y_true, y_pred):
    """Calculate all metrics"""
    return {
        'MAE': calculate_mae(y_true, y_pred),
        'MSE': calculate_mse(y_true, y_pred),
        'RMSE': calculate_rmse(y_true, y_pred),
        'MAPE': calculate_mape(y_true, y_pred),
        'R2': calculate_r2(y_true, y_pred),
        'Direction_Accuracy': calculate_direction_accuracy(y_true, y_pred)
    }
