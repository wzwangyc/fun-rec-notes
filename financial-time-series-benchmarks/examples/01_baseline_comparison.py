#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 1: Baseline Model Comparison

Compare all baseline models on a stock price prediction task.
"""

import sys
sys.path.append('..')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.baseline.naive import RandomWalk, SeasonalRandomWalk, DriftRandomWalk
from models.baseline.statistical import ARIMAModel, ETSModel
from evaluation.metrics import calculate_all_metrics

print("=" * 70)
print("Baseline Model Comparison")
print("=" * 70)

# 1. Load sample data
print("\n[Step 1] Loading data...")

# Create synthetic data for demonstration
np.random.seed(42)
n_days = 500
returns = np.random.normal(0.0005, 0.02, n_days)
prices = 100 * np.cumprod(1 + returns)
dates = pd.date_range('2020-01-01', periods=n_days, freq='D')
df = pd.DataFrame({'Close': prices}, index=dates)

print(f"  Loaded {len(df)} days of data")
print(f"  Price range: {df['Close'].min():.2f} - {df['Close'].max():.2f}")

# 2. Split data
print("\n[Step 2] Splitting data...")

train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

print(f"  Train: {len(train)} days")
print(f"  Test: {len(test)} days")

# 3. Define models
print("\n[Step 3] Defining models...")

models = {
    'Random Walk': RandomWalk(),
    'Drift RW': DriftRandomWalk(),
    'ARIMA(1,1,1)': ARIMAModel(p=1, d=1, q=1)
}

print(f"  Models: {list(models.keys())}")

# 4. Train and predict
print("\n[Step 4] Training and predicting...")

results = {}
for name, model in models.items():
    print(f"\n  Training {name}...")
    try:
        model.fit(train)
        predictions = model.predict(steps=len(test))
        
        # Evaluate
        metrics = calculate_all_metrics(test['Close'].values, predictions)
        results[name] = metrics
        
        print(f"    RMSE: {metrics['RMSE']:.4f}")
        print(f"    MAPE: {metrics['MAPE']:.2f}%")
        print(f"    R²:   {metrics['R2']:.4f}")
        
    except Exception as e:
        print(f"    Error: {e}")
        results[name] = None

# 5. Compare results
print("\n" + "=" * 70)
print("Results Comparison")
print("=" * 70)

if results:
    results_df = pd.DataFrame(results).T
    results_df = results_df[['RMSE', 'MAPE', 'R2', 'Direction_Accuracy']]
    
    print("\n" + results_df.to_string())
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # RMSE
    axes[0, 0].bar(results_df.index, results_df['RMSE'])
    axes[0, 0].set_ylabel('RMSE')
    axes[0, 0].set_title('RMSE Comparison')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # MAPE
    axes[0, 1].bar(results_df.index, results_df['MAPE'])
    axes[0, 1].set_ylabel('MAPE (%)')
    axes[0, 1].set_title('MAPE Comparison')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # R²
    axes[1, 0].bar(results_df.index, results_df['R2'])
    axes[1, 0].set_ylabel('R²')
    axes[1, 0].set_title('R² Comparison')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Direction Accuracy
    axes[1, 1].bar(results_df.index, results_df['Direction_Accuracy'])
    axes[1, 1].set_ylabel('Direction Accuracy')
    axes[1, 1].set_title('Direction Accuracy Comparison')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('../results/charts/baseline_comparison.png', dpi=300)
    print("\n[OK] Chart saved to results/charts/baseline_comparison.png")
    plt.show()

print("\n" + "=" * 70)
print("Baseline Comparison Complete!")
print("=" * 70)
