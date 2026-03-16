# -*- coding: utf-8 -*-
"""
中兵红箭 (000519) 投资价值分析报告
按照麦肯锡分析框架
"""

import akshare as ak
import pandas as pd
from datetime import datetime

# ==================== 数据获取 ====================

stock_code = "000519"
stock_name = "中兵红箭"

print("=" * 60)
print(f"{stock_name}({stock_code}) 投资价值分析报告")
print("=" * 60)
print(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. 公司概况
print("=" * 60)
print("一、公司概况")
print("=" * 60)
try:
    company_info = ak.stock_individual_info_em(symbol=stock_code)
    print(company_info.to_string())
    print()
except Exception as e:
    print(f"获取公司信息失败：{e}\n")

# 2. 实时行情
print("=" * 60)
print("二、市场表现")
print("=" * 60)
try:
    realtime = ak.stock_zh_a_spot_em()
    target = realtime[realtime['代码'] == stock_code]
    if not target.empty:
        print(f"最新价：{target['最新价'].values[0]} 元")
        print(f"涨跌幅：{target['涨跌幅'].values[0]}%")
        print(f"成交量：{target['成交量'].values[0]}")
        print(f"成交额：{target['成交额'].values[0]} 元")
        print(f"总市值：{target['总市值'].values[0]} 元")
        print(f"市盈率 (TTM): {target['市盈率 - 动态'].values[0]}")
        print(f"市净率：{target['市净率'].values[0]}")
    print()
except Exception as e:
    print(f"获取行情数据失败：{e}\n")

# 3. 财务指标
print("=" * 60)
print("三、财务指标分析")
print("=" * 60)
try:
    financial = ak.stock_financial_analysis_indicator(symbol=stock_code, start_year="2023")
    # 选择关键指标
    key_metrics = financial[['报告期', '净资产收益率 (%)', '销售净利率 (%)', 
                             '资产负债率 (%)', '营业收入同比增长率 (%)', 
                             '净利润同比增长率 (%)']].tail(8)
    print(key_metrics.to_string())
    print()
except Exception as e:
    print(f"获取财务指标失败：{e}\n")

# 4. 利润表
print("=" * 60)
print("四、盈利能力分析")
print("=" * 60)
try:
    income = ak.stock_financial_report_sina(stock=stock_code, symbol="利润表")
    print(income.head(5).to_string())
    print()
except Exception as e:
    print(f"获取利润表失败：{e}\n")

# 5. 资产负债表
print("=" * 60)
print("五、偿债能力分析")
print("=" * 60)
try:
    balance = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
    print(balance.head(5).to_string())
    print()
except Exception as e:
    print(f"获取资产负债表失败：{e}\n")

# 6. 现金流量表
print("=" * 60)
print("六、现金流分析")
print("=" * 60)
try:
    cashflow = ak.stock_financial_report_sina(stock=stock_code, symbol="现金流量表")
    print(cashflow.head(5).to_string())
    print()
except Exception as e:
    print(f"获取现金流量表失败：{e}\n")

# 7. 机构评级
print("=" * 60)
print("七、机构评级")
print("=" * 60)
try:
    rating = ak.stock_rank_forecast_cninfo(symbol=stock_code)
    print(rating.head(10).to_string())
    print()
except Exception as e:
    print(f"获取机构评级失败：{e}\n")

print("=" * 60)
print("数据获取完成！")
print("=" * 60)
