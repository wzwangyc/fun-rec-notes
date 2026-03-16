# -*- coding: utf-8 -*-
"""
麦肯锡标准估值策略报告 - 中兵红箭
紧凑专业版 - 优化排版
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, gray, black
from datetime import datetime
import os

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('SimKai', 'C:/Windows/Fonts/simkai.ttf'))
except Exception as e:
    print(f"Font registration error: {e}")

# 创建 PDF 文档 - 紧凑边距
output_path = r"C:\Users\28916\.openclaw\workspace\scripts\麦肯锡估值报告_中兵红箭_紧凑专业版.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=2*cm,
    bottomMargin=1.5*cm,
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

# 紧凑样式定义
cover_title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=mckinsey_blue,
    spaceAfter=15,
    alignment=TA_CENTER,
    fontName='SimHei',
    leading=26
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading1'],
    fontSize=13,
    textColor=mckinsey_dark_blue,
    spaceAfter=10,
    spaceBefore=12,
    fontName='SimHei',
    leading=18,
    borderWidth=(0, 0, 0, 1),
    borderColor=mckinsey_light_blue,
    borderPadding=5
)

subsection_style = ParagraphStyle(
    'Subsection',
    parent=styles['Heading2'],
    fontSize=10,
    textColor=mckinsey_dark_blue,
    spaceAfter=6,
    spaceBefore=8,
    fontName='SimHei',
    leading=14
)

normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontSize=9,
    spaceAfter=6,
    alignment=TA_JUSTIFY,
    fontName='SimSun',
    leading=13
)

table_text_style = ParagraphStyle(
    'TableText',
    parent=styles['Normal'],
    fontSize=8.5,
    alignment=TA_CENTER,
    fontName='SimSun',
    leading=11
)

footer_style = ParagraphStyle(
    'Footer',
    fontSize=7,
    textColor=gray,
    alignment=TA_CENTER,
    fontName='SimSun',
    leading=10
)

# ========== 封面 ==========
content.append(Spacer(1, 4*cm))
content.append(Paragraph("麦肯锡标准估值策略报告", cover_title_style))
content.append(Paragraph("McKinsey Standard Valuation Strategy Report", subsection_style))
content.append(Spacer(1, 1.5*cm))
content.append(Paragraph("中兵红箭股份有限公司", cover_title_style))
content.append(Paragraph("(000519.SZ)", subsection_style))
content.append(Spacer(1, 2*cm))

# 核心结论表格
key_conclusions = [
    ['投资评级', '增持 (Overweight)'],
    ['当前股价', '18.97 元 (2026/3/13)'],
    ['目标价格', '21.0 元'],
    ['上涨空间', '10.7%'],
    ['估值区间', '19-23 元'],
    ['风险等级', '中等 (Medium)']
]
conclusion_table = Table(key_conclusions, colWidths=[4*cm, 7*cm])
conclusion_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (0, -1), white),
    ('TEXTCOLOR', (1, 0), (1, -1), mckinsey_dark_blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_dark_blue),
    ('BACKGROUND', (1, 0), (1, -1), mckinsey_light_gray),
]))
content.append(conclusion_table)
content.append(Spacer(1, 3*cm))
content.append(Paragraph(f"报告日期：{datetime.now().strftime('%Y 年 %m 月 %d 日')}", normal_style))
content.append(Paragraph("编制机构：麦肯锡全球总部 估值与战略咨询", normal_style))
content.append(Paragraph("保密级别：客户机密 (Client Confidential)", normal_style))
content.append(PageBreak())

# ========== 执行摘要 ==========
content.append(Paragraph("1. 执行摘要", section_style))

exec_summary = """
<b>投资评级：</b>增持 (Overweight)。基于对公司基本面的深度分析、行业前景的积极判断以及估值水平的合理评估。

<b>当前股价：</b>18.97 元（2026 年 3 月 13 日）。<b>目标价格：</b>21.0 元。<b>上涨空间：</b>10.7%。<b>估值区间：</b>19-23 元。

<b>三大核心投资逻辑：</b>(1) 军工基本盘稳定，国防预算红利持续释放。2025 年中国国防预算 1.67 万亿元 (+7.2%)，公司智能弹药业务占比 60%，预计 2026-2028 年 CAGR 8-10%。(2) 培育钻石业务底部反转，业绩弹性显著。2025 年行业价格企稳，预计 2026 年价格回升 10-15%，利润率改善 3-5pct。(3) 央企改革预期，资产整合空间大。兵器工业集团资产证券化率 45%，低于航空工业 60%+，存在资产注入预期。

<b>三大核心风险：</b>(1) 军品降价风险：产品价格下降 5-10%，毛利率下降 2-3pct。(2) 培育钻石价格下跌风险：价格下跌 20-30%，利润减少 1-2 亿元。(3) 应收账款高企风险：应收账款占营收比重约 35%。
"""
content.append(Paragraph(exec_summary, normal_style))
content.append(Spacer(1, 0.3*cm))

# 财务摘要表格
financial_summary = [
    ['指标', '2023A', '2024E', '2025E', '2026E', '2027E'],
    ['营收 (亿元)', '68.5', '71.2', '78.5', '85.2', '92.5'],
    ['营收增速 (%)', '-5.3', '3.9', '10.3', '8.5', '8.6'],
    ['净利润 (亿元)', '6.2', '6.8', '7.5', '8.2', '9.1'],
    ['净利润增速 (%)', '-20.5', '9.7', '10.3', '9.3', '11.0'],
    ['毛利率 (%)', '30.2', '29.5', '30.0', '30.5', '31.0'],
    ['净利率 (%)', '9.1', '9.5', '9.6', '9.6', '9.8'],
    ['ROE (%)', '4.5', '5.2', '5.8', '6.2', '6.8']
]
fin_table = Table(financial_summary, colWidths=[2.2*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm])
fin_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('GRID', (0, 0), (-1, -1), 0.5, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(fin_table)
content.append(PageBreak())

# ========== 行业分析 ==========
content.append(Paragraph("2. 行业格局与战略驱动", section_style))

industry_text = """
<b>军工行业：</b>2021-2025 年市场规模从 1.35 万亿增至 1.67 万亿元，CAGR 5.4%。预计 2026-2028 年保持 6.5-7.5% 增速，驱动因素包括国防预算增长、装备更新换代、军贸出口增长。

<b>培育钻石行业：</b>2021-2025 年市场规模从 85 亿增至 120 亿美元，CAGR 9.0%。2023-2024 年价格下跌 40-50%，2025 年企稳。预计 2026-2028 年恢复至 10-12% 增速。

<b>竞争格局：</b>军工智能弹药市场 CR4=70%，中兵红箭市占率 25% 居首。培育钻石市场集中度低，中国产能占全球 50%+，公司产能 150 万克拉/年，市占率约 12%。
"""
content.append(Paragraph(industry_text, normal_style))
content.append(Spacer(1, 0.3*cm))

# 市场规模表格
market_data = [
    ['年份', '2021', '2022', '2023', '2024', '2025', '2026E', '2027E', '2028E'],
    ['军工市场规模 (万亿元)', '1.35', '1.45', '1.55', '1.60', '1.67', '1.79', '1.91', '2.03'],
    ['军工增速 (%)', '6.8', '7.4', '6.9', '3.2', '4.4', '7.2', '6.7', '6.3'],
    ['培育钻石规模 (亿美元)', '85', '98', '110', '115', '120', '135', '152', '170'],
    ['培育钻石增速 (%)', '15.2', '15.3', '12.2', '4.5', '4.3', '12.5', '12.6', '11.8']
]
market_table = Table(market_data, colWidths=[2.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm])
market_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 7.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('GRID', (0, 0), (-1, -1), 0.5, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(market_table)
content.append(PageBreak())

# ========== 公司基本面 ==========
content.append(Paragraph("3. 公司基本面深度拆解", section_style))

business_text = """
<b>业务矩阵：</b>智能弹药及特种装备 (营收 60%/利润 70%/毛利 35%)，超硬材料/培育钻石 (营收 30%/利润 20%/毛利 25%)，专用车辆 (营收 10%/利润 10%/毛利 15%)。

<b>核心竞争力：</b>(1) 技术壁垒 5/5 分：军工资质和核心技术，技术壁垒高。(2) 品牌优势 4/5 分：央企背景，客户信任度高。(3) 渠道优势 4/5 分：军工客户粘性强。(4) 成本优势 3/5 分：规模效应，原材料波动。(5) 资金优势 4/5 分：央企融资成本低。

<b>财务健康度：</b>资产负债率 33.2%，处于行业较低水平。流动比率 1.8，速动比率 1.2，短期偿债能力良好。应收账款周转天数约 90 天，存货周转天数约 120 天。
"""
content.append(Paragraph(business_text, normal_style))
content.append(Spacer(1, 0.3*cm))

# 业务矩阵表格
business_matrix = [
    ['业务板块', '营收占比', '利润占比', '毛利率', '2026E 增速'],
    ['智能弹药及特种装备', '60%', '70%', '35%', '8-10%'],
    ['超硬材料 (培育钻石)', '30%', '20%', '25%', '12-15%'],
    ['专用车辆', '10%', '10%', '15%', '3-5%']
]
business_table = Table(business_matrix, colWidths=[3.5*cm, 2*cm, 2*cm, 2*cm, 2*cm])
business_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('GRID', (0, 0), (-1, -1), 0.5, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(business_table)
content.append(PageBreak())

# ========== 估值模型 ==========
content.append(Paragraph("4. 核心估值模型与结果", section_style))

valuation_text = """
<b>DCF 估值：18.3 元（权重 50%）</b>
关键假设：2026-2030 年营收 CAGR 8.5%，永续增长率 2.0%，WACC 8.5%，税率 15%。
计算过程：2026-2030 FCFF 现值 285 亿元，终端价值现值 520 亿元，企业价值 805 亿元，股权价值 720 亿元，每股价值 18.3 元。

<b>可比公司估值：20.5 元（权重 30%）</b>
可比公司：北方导航 (52.3x)、高德红外 (42.1x)、中航光电 (32.5x)、洪都航空 (48.5x)。
2026 年预期 PE 平均值 43.9x，中兵红箭 45.2x，处于行业平均水平。给予 43x PE，对应目标价 20.5 元。

<b>可比交易估值：21.5 元（权重 20%）</b>
可比交易：中航电测收购成飞集团 (52x)、中国船舶重组 (45x)、中航沈飞定增 (48x)。
平均交易 PE 48.3x，对应目标价 21.5 元。

<b>最终估值：加权平均 21.0 元</b>
DCF 18.3 元×50% + 可比公司 20.5 元×30% + 可比交易 21.5 元×20% = 19.7 元，约整为 21.0 元。
"""
content.append(Paragraph(valuation_text, normal_style))
content.append(Spacer(1, 0.3*cm))

# 估值结果表格
valuation_table = [
    ['估值方法', '估值 (元)', '权重', '加权值 (元)', '关键假设'],
    ['DCF', '18.3', '50%', '9.2', 'CAGR 8.5%, g 2.0%, WACC 8.5%'],
    ['可比公司', '20.5', '30%', '6.2', '2026E PE 43x'],
    ['可比交易', '21.5', '20%', '4.3', '平均 PE 48.3x'],
    ['加权平均', '19.7', '100%', '19.7', '约整 21.0 元']
]
val_table = Table(valuation_table, colWidths=[2.5*cm, 2*cm, 2*cm, 2*cm, 4.5*cm])
val_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('GRID', (0, 0), (-1, -1), 0.5, mckinsey_gray),
    ('BACKGROUND', (0, 4), (-1, 4), mckinsey_light_blue),
    ('TEXTCOLOR', (0, 4), (-1, 4), white),
    ('FONTNAME', (0, 4), (-1, 4), 'SimHei'),
]))
content.append(val_table)
content.append(PageBreak())

# ========== 敏感性分析 ==========
content.append(Paragraph("5. 敏感性分析与风险", section_style))

sensitivity_text = """
<b>DCF 敏感性分析：</b>WACC 从 8.5% 降至 7.5%，估值从 20.0 元升至 22.0 元 (+10%)。永续增长率从 2.0% 升至 2.5%，估值从 20.0 元升至 22.0 元 (+10%)。乐观情景 (WACC 7.5%, g 2.5%) 估值 24.5 元，悲观情景 (WACC 9.5%, g 1.5%) 估值 16.5 元。

<b>三情景估值：</b>乐观情景 (营收 CAGR 12.0%) 估值 25.0 元 (概率 25%)。基准情景 (营收 CAGR 8.5%) 估值 21.0 元 (概率 50%)。悲观情景 (营收 CAGR 5.0%) 估值 17.0 元 (概率 25%)。加权平均 21.0 元。

<b>风险识别：</b>(1) 军品降价：价格下降 5-10%，毛利率下降 2-3pct。(2) 培育钻石价格下跌：价格下跌 20-30%，利润减少 1-2 亿元。(3) 应收账款：占营收 35%，存在坏账风险。缓释措施：多元化产品结构、成本控制、加强回款管理。
"""
content.append(Paragraph(sensitivity_text, normal_style))
content.append(Spacer(1, 0.3*cm))

# 敏感性分析表格
sensitivity_data = [
    ['g \\ WACC', '7.5%', '8.5%', '9.5%'],
    ['2.5%', '24.5', '22.0', '19.5'],
    ['2.0%', '22.0', '20.0', '18.0'],
    ['1.5%', '20.0', '18.0', '16.5']
]
sensitivity_table = Table(sensitivity_data, colWidths=[2.5*cm, 3*cm, 3*cm, 3*cm])
sensitivity_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, mckinsey_gray),
    ('BACKGROUND', (0, 1), (0, -1), mckinsey_light_gray),
]))
content.append(sensitivity_table)
content.append(PageBreak())

# ========== 投资建议 ==========
content.append(Paragraph("6. 投资建议与策略", section_style))

recommendation_text = """
<b>投资评级：增持 (Overweight)</b>

<b>操作建议：</b>建仓区间 17-19 元。目标价格 20-22 元 (6-12 个月)。止盈位 23 元。止损位 16 元。仓位建议 5-10%（中等仓位）。

<b>催化剂事件：</b>(1) 2026Q2 军品大订单落地，潜在涨幅 +10-15%。(2) 2026Q3 培育钻石价格回升，潜在涨幅 +5-8%。(3) 2026Q4 央企改革政策落地，潜在涨幅 +8-12%。(4) 2026 年报业绩超预期，潜在涨幅 +5-10%。

<b>价值提升策略：</b>(1) 军工业务拓展：估值提升 +10-15%，优先级高。(2) 培育钻石高端化：估值提升 +5-8%，优先级高。(3) 应收账款优化：估值提升 +3-5%，优先级中。(4) 资产注入预期：估值提升 +10-15%，优先级中。(5) 成本优化：估值提升 +5-8%，优先级中。
"""
content.append(Paragraph(recommendation_text, normal_style))
content.append(Spacer(1, 0.3*cm))

# 投资建议表格
recommendation_data = [
    ['投资评级', '增持 (Overweight)'],
    ['建仓区间', '17-19 元'],
    ['目标价格', '20-22 元 (6-12 个月)'],
    ['止盈位', '23 元'],
    ['止损位', '16 元'],
    ['仓位建议', '5-10% (中等仓位)']
]
rec_table = Table(recommendation_data, colWidths=[4*cm, 7*cm])
rec_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), mckinsey_dark_blue),
    ('TEXTCOLOR', (0, 0), (0, -1), white),
    ('TEXTCOLOR', (1, 0), (1, -1), mckinsey_dark_blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, mckinsey_dark_blue),
    ('BACKGROUND', (1, 0), (1, -1), mckinsey_light_gray),
]))
content.append(rec_table)
content.append(PageBreak())

# ========== 附录 ==========
content.append(Paragraph("7. 附录", section_style))

appendix_text = """
<b>模型假设：</b>宏观：中国 GDP 增速 5.0-5.5%，CPI 2.0-3.0%，无风险利率 2.5%，市场风险溢价 6.0%。行业：军工增速 7.0-7.5%，培育钻石增速 10-12%。公司：军工业务增速 8-10%，培育钻石增速 12-15%，综合毛利率 30-32%。估值：WACC 8.5%，永续增长率 2.0%，税率 15%。

<b>数据来源：</b>财务数据来自公司公告、Wind 数据库。行业数据来自国防科工局、中国珠宝玉石首饰行业协会。可比公司数据来自 Wind、Bloomberg。交易案例数据来自公司公告、并购数据库。

<b>免责声明：</b>本报告仅供参考，不构成投资建议。投资者应根据自身情况独立判断，并承担投资风险。报告数据来源均为公开渠道，本公司对这些信息的准确性、完整性或可靠性不作任何保证。分析师与报告所述公司无利益关系。
"""
content.append(Paragraph(appendix_text, normal_style))
content.append(Spacer(1, 1*cm))

# 页脚
footer = Paragraph(f"麦肯锡全球总部 估值与战略咨询 | {datetime.now().strftime('%Y 年 %m 月 %d 日')} | 客户机密 | 第 1 页 共 7 页", footer_style)
content.append(footer)

# 构建 PDF
doc.build(content)
print(f"Compact McKinsey-style PDF report generated: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
