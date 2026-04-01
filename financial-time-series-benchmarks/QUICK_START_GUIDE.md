# Financial Time Series Benchmarks - Quick Start Guide

**金融时序预测基准模型库 - 快速入门指南**

---

## 🚀 5 分钟快速开始

### 1. 安装依赖

```bash
cd financial-time-series-benchmarks
pip install numpy pandas scikit-learn statsmodels matplotlib
```

### 2. 运行示例

```bash
cd examples
python 01_baseline_comparison.py
```

### 3. 查看结果

结果保存在 `results/` 目录：
- `charts/` - 对比图表
- `predictions/` - 预测值
- `metrics/` - 评估指标

---

## 📊 已实现模型

### Baseline 模型 (已完成)

✅ **朴素基准**:
- Random Walk (随机游走)
- Seasonal Random Walk (季节性随机游走)
- Drift Random Walk (带漂移随机游走)

✅ **统计模型**:
- ARIMA(p,d,q)
- ETS (指数平滑)

✅ **机器学习**:
- LightGBM
- XGBoost
- CatBoost

### SOTA 模型 (计划中)

⏳ **Transformer**:
- PatchTST
- Autoformer
- Informer

⏳ **基础模型**:
- TimesFM
- Time-MoE

⏳ **混合模型**:
- MIGA
- UMI

---

## 📝 使用示例

### 示例 1: 简单预测

```python
from models.baseline.naive import RandomWalk
import numpy as np

# 创建数据
prices = np.random.randn(100).cumsum() + 100

# 训练模型
model = RandomWalk()
model.fit(prices)

# 预测未来 10 天
predictions = model.predict(10)
print(predictions)
```

### 示例 2: 模型对比

```python
from models.baseline.naive import RandomWalk, DriftRandomWalk
from models.baseline.statistical import ARIMAModel
from evaluation.metrics import calculate_all_metrics

# 定义模型
models = {
    'Random Walk': RandomWalk(),
    'Drift RW': DriftRandomWalk(),
    'ARIMA': ARIMAModel(p=1, d=1, q=1)
}

# 训练和预测
for name, model in models.items():
    model.fit(train_data)
    pred = model.predict(steps=30)
    metrics = calculate_all_metrics(test_data, pred)
    print(f"{name}: RMSE={metrics['RMSE']:.4f}")
```

### 示例 3: 完整回测

```python
from evaluation.backtest import Backtest

backtest = Backtest(initial_capital=1000000)
results = backtest.run(prices, predictions)

print(f"Sharpe: {results['sharpe']:.2f}")
print(f"MaxDD: {results['maxdd']:.2%}")
print(f"Return: {results['return']:.2%}")
```

---

## 📁 项目结构

```
financial-time-series-benchmarks/
├── models/
│   ├── baseline/          # Baseline 模型
│   │   ├── naive.py      # 朴素基准
│   │   ├── statistical.py # 统计模型
│   │   └── machine_learning.py # 机器学习
│   └── sota/             # SOTA 模型 (开发中)
│
├── evaluation/
│   ├── metrics.py        # 评估指标
│   └── backtest.py       # 回测框架
│
├── examples/             # 示例脚本
│   ├── 01_baseline_comparison.py
│   └── ...
│
└── results/              # 结果输出
```

---

## 🎯 下一步计划

### Phase 1 (本周): Baseline 完成
- [x] 朴素基准 (3 个模型)
- [x] 统计模型 (2 个模型)
- [ ] 机器学习 (3 个模型)
- [ ] 完整评估框架

### Phase 2 (下周): SOTA 模型
- [ ] Transformer 模型 (4 个)
- [ ] 基础模型 (3 个)
- [ ] 混合模型 (3 个)

### Phase 3 (月底): 完整工具库
- [ ] GitHub 发布
- [ ] 文档完善
- [ ] 示例代码
- [ ] 性能对比

---

## 📞 联系与贡献

**GitHub**: https://github.com/your-username/financial-time-series-benchmarks

**Email**: your.email@example.com

欢迎提交 Issue 和 Pull Request！

---

**最后更新**: 2026-04-01  
**版本**: v0.1.0 (Beta)
