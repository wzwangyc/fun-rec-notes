# -*- coding: utf-8 -*-
import akshare as ak
import json

# 获取中兵红箭 (000519) 的财务数据
stock_code = "000519"
stock_name = "中兵红箭"

print(f"正在获取 {stock_name}({stock_code}) 的财务数据...\n")

# 1. 获取实时行情
try:
    stock_realtime = ak.stock_zh_a_spot_em()
    target_stock = stock_realtime[stock_realtime['代码'] == stock_code]
    print("=== 实时行情 ===")
    print(f"最新价：{target_stock['最新价'].values[0]}")
    print(f"涨跌幅：{target_stock['涨跌幅'].values[0]}%")
    print(f"成交量：{target_stock['成交量'].values[0]}")
    print(f"成交额：{target_stock['成交额'].values[0]}")
    print(f"总市值：{target_stock['总市值'].values[0]}")
    print()
except Exception as e:
    print(f"获取实时行情失败：{e}\n")

# 2. 获取财务指标
try:
    financial指标 = ak.stock_financial_analysis_indicator(symbol=stock_code, start_year="2024")
    print("=== 主要财务指标 (2024-2025) ===")
    print(financial指标[['报告期', '净资产收益率 (%)', '销售净利率 (%)', '资产负债率 (%)', '营业收入同比增长率 (%)']].tail(5).to_string())
    print()
except Exception as e:
    print(f"获取财务指标失败：{e}\n")

# 3. 获取利润表
try:
    income_statement = ak.stock_financial_report_sina(stock=stock_code, symbol="利润表")
    print("=== 利润表摘要 ===")
    print(income_statement.head(5).to_string())
    print()
except Exception as e:
    print(f"获取利润表失败：{e}\n")

# 4. 获取资产负债表
try:
    balance_sheet = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
    print("=== 资产负债表摘要 ===")
    print(balance_sheet.head(5).to_string())
    print()
except Exception as e:
    print(f"获取资产负债表失败：{e}\n")

# 5. 获取现金流量表
try:
    cash_flow = ak.stock_financial_report_sina(stock=stock_code, symbol="现金流量表")
    print("=== 现金流量表摘要 ===")
    print(cash_flow.head(5).to_string())
    print()
except Exception as e:
    print(f"获取现金流量表失败：{e}\n")

print("数据获取完成！")
