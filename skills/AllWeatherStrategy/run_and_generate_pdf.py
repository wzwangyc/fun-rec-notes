#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行全天候策略并生成 PDF 报告
"""

import sys
import os
from datetime import datetime

# 添加 scripts 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from engine import AllWeatherEngine, Config, ReportGenerator

def main():
    """主函数"""
    print("=" * 60)
    print("全天候 ETF 资产配置系统")
    print("=" * 60)
    
    # 应用配置
    Config.apply_settings()
    
    # 使用默认 ETF 列表
    etf_list = Config.DEFAULT_ETF_LIST
    print(f"\n使用的 ETF 列表：{etf_list}")
    print(f"配置总金额：{Config.DEFAULT_AMOUNT} 元")
    print(f"回看天数：{Config.DEFAULT_LOOKBACK} 天")
    
    # 进度回调
    def update_progress(progress, text):
        print(f"[{progress*100:.0f}%] {text}")
    
    # 运行引擎
    print("\n开始计算配置方案...")
    engine = AllWeatherEngine(etf_list)
    results = engine.run(
        total_amount=Config.DEFAULT_AMOUNT,
        lookback_days=Config.DEFAULT_LOOKBACK,
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
        
        gen = ReportGenerator(Config.register_chinese_font(), Config.DEFAULT_AMOUNT)
        gen.generate_pdf(
            result_df=results['result_df'],
            weights=results['weights'],
            etf_names=results['etf_names'],
            output_path=pdf_path
        )
        
        print(f"\n[PDF] PDF 报告已生成：{pdf_path}")
        print(f"\n配置方案详情：")
        print(results['result_df'].to_string(index=False))
        
        return pdf_path, results
    else:
        print("\n❌ 计算失败，请检查网络或 ETF 代码")
        return None, None

if __name__ == "__main__":
    pdf_path, results = main()
    
    if pdf_path:
        print("\n" + "=" * 60)
        print("运行完成！")
        print("=" * 60)
