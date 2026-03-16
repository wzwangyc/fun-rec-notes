#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新 SWOT 分析数据到 PDF 报告
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('MicrosoftYaHei', 'C:\\Windows\\Fonts\\msyh.ttc'))
    pdfmetrics.registerFont(TTFont('SimHei', 'C:\\Windows\\Fonts\\simhei.ttf'))
except:
    print("Warning: Font registration failed")

def create_swot_report(output_path):
    """创建 SWOT 分析专页"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # 样式
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='MicrosoftYaHei'
    )
    
    heading1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=15,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='MicrosoftYaHei'
    )
    
    heading2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#003366'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='MicrosoftYaHei'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='MicrosoftYaHei'
    )
    
    # 标题
    elements.append(Paragraph("SWOT 深度分析", title_style))
    elements.append(Paragraph("基于最新财报和机构研报", heading2_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # ========== 东方财富 SWOT ==========
    elements.append(Paragraph("一、东方财富 SWOT 分析", heading1_style))
    
    # 优势
    elements.append(Paragraph("优势 (Strengths) ★★★★★", heading2_style))
    elements.append(Paragraph("""
    <b>1. 全牌照金融生态壁垒</b><br/>
    • 拥有证券、基金、期货、信托等完整金融牌照<br/>
    • 互联网券商龙头，牌照稀缺性强<br/>
    • 一站式金融服务生态，用户粘性高<br/><br/>
    <b>2. 流量成本优势</b><br/>
    • 东方财富网 + 天天基金网双轮驱动<br/>
    • 2025 年营收 115.9 亿元 (+58.67%)，规模效应显著<br/>
    • 自有流量占比高，获客成本远低于传统券商<br/><br/>
    <b>3. 财富管理先发优势</b><br/>
    • 天天基金网为头部基金销售平台<br/>
    • 基金投顾试点资格，AUM 持续增长<br/>
    • 2025 年净利润 90.97 亿元 (+50.57%)<br/><br/>
    <b>4. 数据与客户积累</b><br/>
    • Choice 数据终端服务机构客户<br/>
    • 海量用户行为数据，精准营销能力强
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 劣势
    elements.append(Paragraph("劣势 (Weaknesses) ★★☆☆☆", heading2_style))
    elements.append(Paragraph("""
    <b>1. 重资本业务约束</b><br/>
    • 证券业务需要大量资本金支持<br/>
    • 资产负债率 76.63%，高于同花顺 (40.05%)<br/>
    • 两融业务受净资本约束<br/><br/>
    <b>2. 周期性波动大</b><br/>
    • 业绩与 A 股交易量高度相关<br/>
    • 牛市弹性大，熊市压力也大<br/><br/>
    <b>3. ROE 相对较低</b><br/>
    • 2025 年 ROE 10.73%，低于同花顺 (36.7%)<br/>
    • 重资产模式拉低资本回报率<br/><br/>
    <b>4. 创新业务投入大</b><br/>
    • 金融科技、国际化需要持续投入<br/>
    • 短期可能影响利润率
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 机会
    elements.append(Paragraph("机会 (Opportunities) ★★★★★", heading2_style))
    elements.append(Paragraph("""
    <b>1. 财富管理蓝海市场</b><br/>
    • 中国居民资产配置向金融资产转移<br/>
    • 基金投顾业务空间巨大<br/>
    • 养老金入市带来长期资金<br/><br/>
    <b>2. 机构业务拓展</b><br/>
    • Choice 数据终端渗透率提升<br/>
    • 投行、资管业务发展空间大<br/><br/>
    <b>3. 金融科技赋能</b><br/>
    • AI 技术在投顾、风控领域应用<br/>
    • 数字化转型提升运营效率<br/><br/>
    <b>4. 国际化布局</b><br/>
    • 港股通、海外业务拓展<br/>
    • 服务中国投资者全球配置需求
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 威胁
    elements.append(Paragraph("威胁 (Threats) ★★★☆☆", heading2_style))
    elements.append(Paragraph("""
    <b>1. 行业竞争加剧</b><br/>
    • 传统券商加速数字化转型<br/>
    • 互联网巨头 (腾讯、阿里) 潜在进入<br/><br/>
    <b>2. 市场交易量波动</b><br/>
    • A 股成交量下滑影响佣金收入<br/>
    • 市场低迷期业绩承压<br/><br/>
    <b>3. 监管政策趋严</b><br/>
    • 金融监管加强，合规成本上升<br/>
    • 基金销售费率改革影响收入<br/><br/>
    <b>4. 技术迭代风险</b><br/>
    • AI、区块链等技术快速变化<br/>
    • 需要持续研发投入保持竞争力
    """, normal_style))
    
    elements.append(PageBreak())
    
    # ========== 同花顺 SWOT ==========
    elements.append(Paragraph("二、同花顺 SWOT 分析", heading1_style))
    
    # 优势
    elements.append(Paragraph("优势 (Strengths) ★★★★★", heading2_style))
    elements.append(Paragraph("""
    <b>1. AI 技术行业领先</b><br/>
    • 2025 年研发投入 11.45 亿元，占营收 18.99%<br/>
    • HithinkGPT 大模型通过备案<br/>
    • AI 在投顾、数据、交易全场景应用<br/><br/>
    <b>2. 轻资产高 ROE 模式</b><br/>
    • 2025 年 ROE 36.7%，远超东财 (10.73%)<br/>
    • 资产负债率仅 40.05%，财务稳健<br/>
    • 流动比率 2.27，短期偿债能力强<br/><br/>
    <b>3. 用户粘性与活跃度</b><br/>
    • 2025 年 APP 月活 3549.91 万人 (+9.3%)<br/>
    • 稳居证券类 APP 活跃用户第一<br/>
    • 2025 年净利润 32.05 亿元 (+75.79%)<br/><br/>
    <b>4. 机构业务突破</b><br/>
    • iFinD 终端在机构客户中渗透率提升<br/>
    • 与华泰、国泰君安等头部券商战略合作<br/>
    • AI+ 投顾系统输出，B 端业务增长快
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 劣势
    elements.append(Paragraph("劣势 (Weaknesses) ★★★☆☆", heading2_style))
    elements.append(Paragraph("""
    <b>1. 无证券牌照</b><br/>
    • 无法直接开展证券经纪业务<br/>
    • 流量变现主要靠导流和广告<br/>
    • 缺少交易环节，用户价值挖掘受限<br/><br/>
    <b>2. 收入结构单一</b><br/>
    • 2025 年互联网广告及信息服务占比 57.43%<br/>
    • 基金销售业务受市场影响大<br/>
    • 软件服务收入占比有待提升<br/><br/>
    <b>3. 广告收入波动</b><br/>
    • 2025 年增值服务收入 19.51 亿元 (+20.71%)<br/>
    • 占比 32.35%，同比下降 6.24pct<br/>
    • 受证券市场活跃度影响较大<br/><br/>
    <b>4. 依赖第三方平台</b><br/>
    • 部分流量来自应用商店等第三方<br/>
    • 平台政策变化可能影响获客
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 机会
    elements.append(Paragraph("机会 (Opportunities) ★★★★★", heading2_style))
    elements.append(Paragraph("""
    <b>1. AI 大模型商业化</b><br/>
    • 问财 AI 已开始收费，C 端 AI 产品变现<br/>
    • iFinD 大模型增强，B 端订阅收入增长<br/>
    • 2026-2028 年预测净利润 42.1/43.2/44.5 亿元<br/><br/>
    <b>2. 机构数字化趋势</b><br/>
    • 券商、基金、银行数字化转型<br/>
    • AI 投顾系统、数据服务需求增长<br/>
    • 与头部券商深度合作，共建生态<br/><br/>
    <b>3. 海外市场拓展</b><br/>
    • 服务华人投资者全球配置需求<br/>
    • AI 技术输出到海外金融机构<br/><br/>
    <b>4. 投顾业务试点</b><br/>
    • 基金投顾资格申请中<br/>
    • AI 投顾产品储备丰富<br/>
    • 政策放开后有望快速放量
    """, normal_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # 威胁
    elements.append(Paragraph("威胁 (Threats) ★★★★☆", heading2_style))
    elements.append(Paragraph("""
    <b>1. 互联网巨头进入</b><br/>
    • 腾讯、阿里、京东等布局金融科技<br/>
    • 流量和资金优势明显<br/><br/>
    <b>2. 监管政策变化</b><br/>
    • 金融科技监管趋严<br/>
    • 数据安全和隐私保护要求提高<br/><br/>
    <b>3. 技术人才竞争</b><br/>
    • AI 人才争夺激烈<br/>
    • 人力成本上升压力<br/><br/>
    <b>4. 用户获取成本上升</b><br/>
    • 流量红利见顶<br/>
    • 应用商店获客成本持续上升<br/>
    • 需要提升付费转化率和 ARPU 值
    """, normal_style))
    
    elements.append(PageBreak())
    
    # ========== SWOT 对比总结 ==========
    elements.append(Paragraph("三、SWOT 对比总结", heading1_style))
    
    swot_compare = [
        ['维度', '东方财富', '同花顺'],
        ['核心优势', '全牌照+ 流量 + 规模', 'AI 技术 + 高 ROE+ 轻资产'],
        ['主要劣势', '重资产 +ROE 低', '无牌照 + 收入单一'],
        ['最大机会', '财富管理 + 机构业务', 'AI 变现 + 机构数字化'],
        ['最大威胁', '竞争加剧 + 市场波动', '巨头进入 + 监管变化'],
        ['投资逻辑', '低估值 + 牌照壁垒', '高成长+AI 领先'],
        ['适合投资者', '价值型/稳健型', '成长型/进取型'],
    ]
    
    swot_table = Table(swot_compare, colWidths=[3*cm, 6*cm, 6*cm])
    swot_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(swot_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # 数据来源
    elements.append(Paragraph("数据来源：", heading2_style))
    elements.append(Paragraph("""
    • 东方财富 2025 年年报、最新公告<br/>
    • 同花顺 2025 年年报、最新公告<br/>
    • 天风证券、中国银河、华泰证券等机构研报<br/>
    • 东方财富妙想金融大模型 (MX-FinSearch)<br/>
    • 查询时间：2026 年 3 月 14 日
    """, normal_style))
    
    # 构建 PDF
    doc.build(elements)
    print(f"SUCCESS: SWOT report generated - {output_path}")
    return True

if __name__ == "__main__":
    output_path = r"C:\Users\28916\.openclaw\workspace\reports\SWOT_Analysis_Complete.pdf"
    create_swot_report(output_path)
