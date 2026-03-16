#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行全天候策略并生成 PDF 报告（可配置版本）
"""

import sys
import os
from datetime import datetime

# 添加 scripts 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from engine import AllWeatherEngine, Config, ReportGenerator

# ========== 在这里修改你的配置 ==========

# 1. ETF 配置池（每行一个 ETF 代码）
MY_ETF_LIST = [
    "515450",  # 易方达沪深 300ETF
    "159545",  # 华夏中证 500ETF
    "159531",  # 易方达中证 2000ETF
    "513100",  # 国泰纳斯达克 100ETF
    "518880",  # 华安黄金 ETF
    "159985",  # 华夏饲料豆粕期货 ETF
    "511010",  # 国泰上证 5 年期国债 ETF
]

# 2. 配置总金额（元）
MY_TOTAL_AMOUNT = 10000.0  # 可以改成 50000, 100000 等

# 3. 回看天数（用于计算历史波动率）
MY_LOOKBACK_DAYS = 365  # 可以改成 180, 730 等

# 4. 是否自动发送邮件
AUTO_SEND_EMAIL = True  # True=自动发送，False=不发送

# =======================================

def main():
    """主函数"""
    print("=" * 60)
    print("全天候 ETF 资产配置系统（自定义配置）")
    print("=" * 60)
    
    # 应用配置
    Config.apply_settings()
    
    # 显示配置
    print(f"\n使用的 ETF 列表：")
    for etf in MY_ETF_LIST:
        print(f"  - {etf}")
    print(f"\n配置总金额：{MY_TOTAL_AMOUNT:,.2f} 元")
    print(f"回看天数：{MY_LOOKBACK_DAYS} 天")
    print(f"自动发送邮件：{'是' if AUTO_SEND_EMAIL else '否'}")
    
    # 进度回调
    def update_progress(progress, text):
        print(f"[{progress*100:.0f}%] {text}")
    
    # 运行引擎
    print("\n开始计算配置方案...")
    engine = AllWeatherEngine(MY_ETF_LIST)
    results = engine.run(
        total_amount=MY_TOTAL_AMOUNT,
        lookback_days=MY_LOOKBACK_DAYS,
        progress_callback=update_progress
    )
    
    if results:
        print("\n[OK] 计算成功！")
        print(f"\n预估年化收益：{results['metrics']['annualized_return']*100:.2f}%")
        print(f"年化风险 (波动率): {results['metrics']['annualized_risk']*100:.2f}%")
        
        # 生成 PDF 报告
        print("\n正在生成 PDF 报告...")
        
        # 创建输出目录
        output_dir = os.path.join(os.path.dirname(__file__), Config.OUTPUT_DIR)
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成 PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_path = os.path.join(output_dir, f"AllWeather_Report_{timestamp}.pdf")
        
        gen = ReportGenerator(Config.register_chinese_font(), MY_TOTAL_AMOUNT)
        gen.generate_pdf(
            result_df=results['result_df'],
            weights=results['weights'],
            etf_names=results['etf_names'],
            output_path=pdf_path
        )
        
        print(f"\n[PDF] PDF 报告已生成：{pdf_path}")
        print(f"\n配置方案详情：")
        print(results['result_df'].to_string(index=False))
        
        # 自动发送邮件
        if AUTO_SEND_EMAIL:
            print("\n[邮件] 正在发送邮件...")
            import subprocess
            try:
                subprocess.run([sys.executable, "send_report_email.py"], 
                             cwd=os.path.dirname(__file__), 
                             check=True, 
                             capture_output=True)
                print("[邮件] 发送成功！")
            except Exception as e:
                print(f"[邮件] 发送失败：{e}")
        
        return pdf_path, results
    else:
        print("\n[错误] 计算失败，请检查网络或 ETF 代码")
        return None, None

if __name__ == "__main__":
    pdf_path, results = main()
    
    if pdf_path:
        print("\n" + "=" * 60)
        print("运行完成！")
        print("=" * 60)
