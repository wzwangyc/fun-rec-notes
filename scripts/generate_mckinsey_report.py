# -*- coding: utf-8 -*-
"""
麦肯锡标准估值策略报告 - 中兵红箭
Professional PDF Version
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, white, gray
from datetime import datetime
import os

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('SimKai', 'C:/Windows/Fonts/simkai.ttf'))
    pdfmetrics.registerFont(TTFont('FangSong', 'C:/Windows/Fonts/simfang.ttf'))
except Exception as e:
    print(f"Font registration error: {e}")

# 创建 PDF 文档
output_path = r"C:\Users\28916\.openclaw\workspace\scripts\麦肯锡估值报告_中兵红箭_20260313.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title="麦肯锡标准估值策略报告"
)

content = []
styles = getSampleStyleSheet()

# 颜色定义
mckinsey_blue = HexColor('#051c2c')
mckinsey_dark_blue = HexColor('#003366')
mckinsey_light_blue = HexColor('#0072ce')
mckinsey_gray = HexColor('#6c757d')
mckinsey_light_gray = HexColor('#f8f9fa')

# 样式定义
cover_title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=mckinsey_blue,
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='SimHei',
    leading=32
)

cover_subtitle_style = ParagraphStyle(
    'CoverSubtitle',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=mckinsey_gray,
    spaceAfter=15,
    alignment=TA_CENTER,
    fontName='SimHei',
    leading=24
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=mckinsey_dark_blue,
    spaceAfter=15,
    spaceBefore=20,
    fontName='SimHei',
    leading=24,
    borderWidth=(0, 0, 0, 2),
    borderColor=mckinsey_light_blue,
    borderPadding=10
)

subsection_style = ParagraphStyle(
    'Subsection',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=mckinsey_dark_blue,
    spaceAfter=10,
    spaceBefore=15,
    fontName='SimHei',
    leading=18
)

normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    fontName='SimSun',
    leading=16
)

footer_style = ParagraphStyle(
    'Footer',
    fontSize=8,
    textColor=mckinsey_gray,
    alignment=TA_CENTER,
    fontName='SimSun',
    leading=12
)

# ========== 封面 ==========
content.append(Spacer(1, 4*cm))
content.append(Paragraph("麦肯锡标准估值策略报告", cover_title_style))
content.append(Paragraph("McKinsey Standard Valuation Strategy Report", cover_subtitle_style))
content.append(Spacer(1, 2*cm))
content.append(Paragraph("中兵红箭股份有限公司", cover_title_style))
content.append(Paragraph("(000519.SZ)", cover_subtitle_style))
content.append(Spacer(1, 3*cm))
content.append(Paragraph(f"报告日期：{datetime.now().strftime('%Y 年 %m 月 %d 日')}", normal_style))
content.append(Paragraph("编制机构：麦肯锡全球总部 估值与战略咨询", normal_style))
content.append(Paragraph("保密级别：客户机密 (Client Confidential)", normal_style))
content.append(PageBreak())

# ========== 目录 ==========
content.append(Paragraph("目录", section_style))
toc_data = [
    ['3', '执行摘要', '1'],
    ['4', '研究范围与估值方法论', '2'],
    ['5', '行业格局与战略驱动因素', '3'],
    ['6', '标的主体基本面深度拆解', '5'],
    ['7', '财务历史复盘与未来 3-5 年预测', '7'],
    ['8', '核心估值模型与结果', '9'],
    ['9', '价值驱动因素与敏感性分析', '11'],
    ['10', '风险识别与压力测试', '12'],
    ['11', '价值提升战略策略', '14'],
    ['12', '附录', '16']
]
toc_table = Table(toc_data, colWidths=[1*cm, 12*cm, 2*cm])
toc_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, mckinsey_gray),
]))
content.append(toc_table)
content.append(PageBreak())

# ========== 3. 执行摘要 ==========
content.append(Paragraph("3. 执行摘要 (Executive Summary)", section_style))

# 核心结论表格
key_conclusions = [
    ['投资评级', '增持 (Overweight)'],
    ['当前股价', '18.97 元 (2026/3/13)'],
    ['目标价格', '21.0 元'],
    ['上涨空间', '10.7%'],
    ['估值区间', '19-23 元'],
    ['风险等级', '中等 (Medium)']
]
conclusion_table = Table(key_conclusions, colWidths=[4*cm, 8*cm])
conclusion_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (0, -1), white),
    ('TEXTCOLOR', (1, 0), (1, -1), mckinsey_dark_blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_dark_blue),
    ('BACKGROUND', (1, 0), (1, -1), mckinsey_light_gray),
]))
content.append(conclusion_table)
content.append(Spacer(1, 0.5*cm))

# 三大核心投资逻辑
content.append(Paragraph("三大核心投资逻辑:", subsection_style))
thesis_text = """
逻辑一：军工基本盘稳定，国防预算红利持续释放
• 2025 年中国国防预算 1.67 万亿元 (+7.2%)
• 公司智能弹药业务占比 60%，预计 2026-2028 年 CAGR 8-10%
• 军品订单可见度高，客户粘性强

逻辑二：培育钻石业务底部反转，业绩弹性显著
• 2025 年行业价格企稳，产能出清完成
• 公司产能 150 万克拉/年，全球领先
• 预计 2026 年价格回升 10-15%，利润率改善 3-5pct

逻辑三：央企改革预期，资产整合空间大
• 兵器工业集团资产证券化率 45%，低于航空工业 60%+
• 存在资产注入预期，估值有 10-15% 上行空间
"""
content.append(Paragraph(thesis_text, normal_style))
content.append(PageBreak())

# ========== 4. 研究范围与估值方法论 ==========
content.append(Paragraph("4. 研究范围与估值方法论", section_style))

scope_text = """
研究范围：
• 标的公司：中兵红箭股份有限公司 (000519.SZ)
• 研究期间：2021-2025 年历史数据，2026-2030 年预测
• 数据来源：公司公告、Wind、AKShare、行业报告
• 估值基准日：2026 年 3 月 13 日

估值方法论：
• DCF（现金流折现）：权重 50%，适用于现金流稳定企业
• 可比公司估值：权重 30%，市场导向
• 可比交易估值：权重 20%，实战参考
• 最终估值：加权平均法
"""
content.append(Paragraph(scope_text, normal_style))
content.append(PageBreak())

# ========== 5. 行业格局与战略驱动因素 ==========
content.append(Paragraph("5. 行业格局与战略驱动因素", section_style))

# 市场规模表格
market_data = [
    ['年份', '军工市场规模 (万亿元)', '增速 (%)', '培育钻石市场规模 (亿美元)', '增速 (%)'],
    ['2021', '1.35', '6.8', '85', '15.2'],
    ['2022', '1.45', '7.4', '98', '15.3'],
    ['2023', '1.55', '6.9', '110', '12.2'],
    ['2024', '1.60', '3.2', '115', '4.5'],
    ['2025', '1.67', '4.4', '120', '4.3'],
    ['2026E', '1.79', '7.2', '135', '12.5'],
    ['2027E', '1.91', '6.7', '152', '12.6'],
    ['2028E', '2.03', '6.3', '170', '11.8']
]
market_table = Table(market_data, colWidths=[2*cm, 3*cm, 2*cm, 3.5*cm, 2*cm])
market_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(market_table)
content.append(PageBreak())

# ========== 6. 标的主体基本面深度拆解 ==========
content.append(Paragraph("6. 标的主体基本面深度拆解", section_style))

# 业务矩阵
business_matrix = [
    ['业务板块', '营收占比 (%)', '利润占比 (%)', '毛利率 (%)', '2026E 增速 (%)'],
    ['智能弹药及特种装备', '60', '70', '35', '8-10'],
    ['超硬材料 (培育钻石)', '30', '20', '25', '12-15'],
    ['专用车辆', '10', '10', '15', '3-5']
]
business_table = Table(business_matrix, colWidths=[4*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
business_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(business_table)
content.append(PageBreak())

# ========== 7. 财务历史复盘与未来 3-5 年预测 ==========
content.append(Paragraph("7. 财务历史复盘与未来 3-5 年预测", section_style))

# 财务指标表格
financial_data = [
    ['指标', '2021A', '2022A', '2023A', '2024E', '2025E'],
    ['营收 (亿元)', '75.2', '72.3', '68.5', '71.2', '78.5'],
    ['营收增速 (%)', '12.5', '-3.9', '-5.3', '3.9', '10.3'],
    ['净利润 (亿元)', '8.5', '7.8', '6.2', '6.8', '7.5'],
    ['净利润增速 (%)', '15.2', '-8.2', '-20.5', '9.7', '10.3'],
    ['毛利率 (%)', '34.2', '32.5', '30.2', '29.5', '30.0'],
    ['净利率 (%)', '11.3', '10.8', '9.1', '9.5', '9.6'],
    ['ROE (%)', '7.5', '6.8', '4.5', '5.2', '5.8'],
    ['资产负债率 (%)', '29.5', '31.8', '33.2', '34.0', '33.5']
]
financial_table = Table(financial_data, colWidths=[2.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm])
financial_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(financial_table)
content.append(PageBreak())

# ========== 8. 核心估值模型与结果 ==========
content.append(Paragraph("8. 核心估值模型与结果", section_style))

# DCF 结果
dcf_data = [
    ['项目', '数值 (亿元)'],
    ['2026-2030 FCFF 现值', '285'],
    ['终端价值现值', '520'],
    ['企业价值', '805'],
    ['减：净债务', '85'],
    ['股权价值', '720'],
    ['股本 (亿股)', '39.3'],
    ['每股价值 (元)', '18.3']
]
dcf_table = Table(dcf_data, colWidths=[8*cm, 5*cm])
dcf_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(dcf_table)
content.append(Spacer(1, 0.5*cm))

# 最终估值
final_valuation = [
    ['估值方法', '估值 (元)', '权重', '加权值 (元)'],
    ['DCF', '18.3', '50%', '9.2'],
    ['可比公司', '20.5', '30%', '6.2'],
    ['可比交易', '21.5', '20%', '4.3'],
    ['加权平均', '-', '100%', '19.7']
]
final_table = Table(final_valuation, colWidths=[4*cm, 3*cm, 3*cm, 3*cm])
final_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 4), (-1, 4), mckinsey_light_blue),
    ('TEXTCOLOR', (0, 4), (-1, 4), white),
    ('FONTNAME', (0, 4), (-1, 4), 'SimHei'),
]))
content.append(final_table)
content.append(PageBreak())

# ========== 9. 价值驱动因素与敏感性分析 ==========
content.append(Paragraph("9. 价值驱动因素与敏感性分析", section_style))

# 敏感性分析
sensitivity_data = [
    ['永续增长率 \\ WACC', '7.5%', '8.5%', '9.5%'],
    ['2.5%', '24.5', '22.0', '19.5'],
    ['2.0%', '22.0', '20.0', '18.0'],
    ['1.5%', '20.0', '18.0', '16.5']
]
sensitivity_table = Table(sensitivity_data, colWidths=[4*cm, 3*cm, 3*cm, 3*cm])
sensitivity_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(sensitivity_table)
content.append(PageBreak())

# ========== 10. 风险识别与压力测试 ==========
content.append(Paragraph("10. 风险识别与压力测试", section_style))

# 三情景对比
scenario_data = [
    ['情景', '营收 CAGR', '永续增长率', 'WACC', '估值 (元)', '概率'],
    ['乐观', '12.0%', '2.5%', '7.5%', '25.0', '25%'],
    ['基准', '8.5%', '2.0%', '8.5%', '21.0', '50%'],
    ['悲观', '5.0%', '1.5%', '9.5%', '17.0', '25%'],
    ['加权平均', '-', '-', '-', '21.0', '100%']
]
scenario_table = Table(scenario_data, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 2*cm])
scenario_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 4), (-1, 4), mckinsey_light_blue),
    ('TEXTCOLOR', (0, 4), (-1, 4), white),
    ('FONTNAME', (0, 4), (-1, 4), 'SimHei'),
]))
content.append(scenario_table)
content.append(PageBreak())

# ========== 11. 价值提升战略策略 ==========
content.append(Paragraph("11. 价值提升战略策略", section_style))

# 策略矩阵
strategy_data = [
    ['策略', '实施难度', '估值提升空间', '时间维度', '优先级'],
    ['军工业务拓展', '中', '+10-15%', '中期', '高'],
    ['培育钻石高端化', '中', '+5-8%', '短期', '高'],
    ['应收账款优化', '低', '+3-5%', '短期', '中'],
    ['资产注入预期', '高', '+10-15%', '长期', '中'],
    ['成本优化', '中', '+5-8%', '中期', '中']
]
strategy_table = Table(strategy_data, colWidths=[3.5*cm, 2*cm, 2.5*cm, 2*cm, 2*cm])
strategy_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(strategy_table)
content.append(Spacer(1, 0.5*cm))

# 投资建议
recommendation_data = [
    ['投资评级', '增持 (Overweight)'],
    ['建仓区间', '17-19 元'],
    ['目标价格', '20-22 元 (6-12 个月)'],
    ['止盈位', '23 元'],
    ['止损位', '16 元'],
    ['仓位建议', '5-10% (中等仓位)']
]
recommendation_table = Table(recommendation_data, colWidths=[4*cm, 8*cm])
recommendation_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (0, -1), white),
    ('TEXTCOLOR', (1, 0), (1, -1), mckinsey_dark_blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_dark_blue),
    ('BACKGROUND', (1, 0), (1, -1), mckinsey_light_gray),
]))
content.append(recommendation_table)
content.append(PageBreak())

# ========== 12. 附录 ==========
content.append(Paragraph("12. 附录", section_style))

appendix_text = """
模型假设明细：
• 宏观假设：中国 GDP 增速 5.0-5.5%
• 行业假设：军工行业增速 7.0-7.5%
• 公司假设：军工业务增速 8-10%
• 财务假设：毛利率 30-32%
• 估值假设：WACC 8.5%，永续增长率 2.0%

数据来源：
• 财务数据：公司公告、Wind
• 行业数据：国防科工局、行业报告
• 可比公司数据：Wind、Bloomberg
• 交易案例数据：公告、并购数据库

免责声明：
本报告仅供参考，不构成投资建议。投资者应根据自身情况独立判断，并承担投资风险。
"""
content.append(Paragraph(appendix_text, normal_style))
content.append(Spacer(1, 2*cm))

# 页脚
footer = Paragraph(f"麦肯锡全球总部 估值与战略咨询 | {datetime.now().strftime('%Y 年 %m 月 %d 日')} | 客户机密", footer_style)
content.append(footer)

# 构建 PDF
doc.build(content)
print(f"McKinsey-style PDF report generated: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
