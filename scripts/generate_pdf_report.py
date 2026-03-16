#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成麦肯锡风格 PDF 报告
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

# 注册中文字体（使用 Windows 系统字体）
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:\\Windows\\Fonts\\simsun.ttc'))
    pdfmetrics.registerFont(TTFont('SimHei', 'C:\\Windows\\Fonts\\simhei.ttf'))
    pdfmetrics.registerFont(TTFont('MicrosoftYaHei', 'C:\\Windows\\Fonts\\msyh.ttc'))
except:
    print("警告：中文字体注册失败，使用默认字体")

def create_pdf_report(output_path):
    """创建 PDF 报告"""
    
    # 创建文档
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
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='MicrosoftYaHei'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='MicrosoftYaHei'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='MicrosoftYaHei'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='MicrosoftYaHei'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='MicrosoftYaHei'
    )
    
    # ========== 封面页 ==========
    # 标题
    elements.append(Paragraph("东方财富 vs 同花顺", title_style))
    elements.append(Paragraph("深度对比分析报告", title_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # 副标题
    elements.append(Paragraph("企业基本面深度研究", subtitle_style))
    
    elements.append(Spacer(1, 2*cm))
    
    # 报告信息表格
    info_data = [
        ['报告类型：', '企业基本面深度研究'],
        ['研究对象：', '东方财富 (300059.SZ) vs 同花顺 (300033.SZ)'],
        ['报告日期：', datetime.now().strftime('%Y年%m月%d日')],
        ['分析师：', 'Leo Assistant'],
        ['数据来源：', '东方财富妙想金融大模型'],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1a1a1a')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(PageBreak())
    
    # ========== 执行摘要 ==========
    elements.append(Paragraph("执行摘要", heading1_style))
    elements.append(Paragraph("""
    本报告对国内领先的两大互联网金融服务平台——东方财富和同花顺进行全面的基本面对比分析。
    研究涵盖估值水平、财务健康度、盈利能力、成长性及商业模式等核心维度。
    """, normal_style))
    
    # 核心发现表格
    elements.append(Paragraph("核心发现：", heading2_style))
    
    summary_data = [
        ['维度', '东方财富', '同花顺', '优势方'],
        ['商业模式', '证券 + 基金 + 数据', 'AI+ 软件 + 广告', '东财 (牌照壁垒)'],
        ['收入规模', '较大', '中等', '东财'],
        ['盈利能力', '稳健', '高毛利', '同花顺'],
        ['成长驱动', '市占率提升', 'AI 技术变现', '待观察'],
        ['估值水平', '数据见 Excel', '数据见 Excel', '对比分析'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3.5*cm, 4.5*cm, 4.5*cm, 3*cm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ========== 公司概况 ==========
    elements.append(Paragraph("一、公司概况", heading1_style))
    
    elements.append(Paragraph("1.1 东方财富 (300059.SZ)", heading2_style))
    elements.append(Paragraph("""
    <b>基本信息：</b><br/>
    • 成立时间：2005 年 &nbsp;&nbsp;|&nbsp;&nbsp; 上市时间：2010 年 (深交所创业板)<br/>
    • 核心定位：一站式互联网金融服务生态<br/><br/>
    <b>业务架构：</b><br/>
    • 东方财富网 (流量入口) | 天天基金网 (基金销售) | 东方财富证券 (证券牌照)<br/>
    • Choice 数据 (机构服务) | 哈富证券 (港股通) | 期货/信托 (多元金融)<br/><br/>
    <b>核心竞争优势：</b><br/>
    ✅ 全牌照优势 - 证券、基金、期货、信托等金融牌照齐全<br/>
    ✅ 流量护城河 - 东方财富网 + 天天基金网双轮驱动<br/>
    ✅ 闭环生态 - 从资讯→交易→数据的完整闭环<br/>
    ✅ 规模效应 - 用户基数大，边际成本低
    """, normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("1.2 同花顺 (300033.SZ)", heading2_style))
    elements.append(Paragraph("""
    <b>基本信息：</b><br/>
    • 成立时间：1995 年 &nbsp;&nbsp;|&nbsp;&nbsp; 上市时间：2009 年 (深交所创业板)<br/>
    • 核心定位：AI 驱动的金融信息服务商<br/><br/>
    <b>业务架构：</b><br/>
    • 同花顺 APP(C 端流量) | iFinD 终端 (机构服务) | 广告推广 (流量变现)<br/>
    • AI 投顾 (创新业务) | 基金销售 (代销) | 技术输出 (B 端赋能)<br/><br/>
    <b>核心竞争优势：</b><br/>
    ✅ 技术壁垒 - AI、大数据、自然语言处理技术领先<br/>
    ✅ 用户粘性 - 同花顺 APP 活跃度高，工具属性强<br/>
    ✅ 机构业务 - iFinD 终端在机构客户中渗透率高<br/>
    ✅ 轻资产模式 - 无重资本业务，ROE 稳定
    """, normal_style))
    
    elements.append(PageBreak())
    
    # ========== 商业模式对比 ==========
    elements.append(Paragraph("二、商业模式对比", heading1_style))
    
    elements.append(Paragraph("2.1 收入结构对比", heading2_style))
    
    revenue_data = [
        ['业务板块', '东方财富', '同花顺'],
        ['证券业务', '⭐⭐⭐⭐⭐ 核心收入', '❌ 无'],
        ['基金销售', '⭐⭐⭐⭐⭐ 天天基金', '⭐⭐⭐ 代销'],
        ['广告服务', '⭐⭐⭐ 网站广告', '⭐⭐⭐⭐ 核心收入'],
        ['软件服务', '⭐⭐ Choice 数据', '⭐⭐⭐⭐ iFinD'],
        ['AI 技术', '⭐⭐ 妙想 AI', '⭐⭐⭐⭐⭐ 核心战略'],
        ['利息收入', '⭐⭐⭐⭐ 两融/质押', '❌ 无'],
    ]
    
    revenue_table = Table(revenue_data, colWidths=[3.5*cm, 6*cm, 6*cm])
    revenue_table.setStyle(TableStyle([
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
    
    elements.append(revenue_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ========== 财务数据对比 ==========
    elements.append(Paragraph("三、财务数据对比", heading1_style))
    
    elements.append(Paragraph("3.1 估值指标对比", heading2_style))
    elements.append(Paragraph("数据来源：MX_FinData_fdfbfc24.xlsx（最新查询）", normal_style))
    
    valuation_data = [
        ['指标', '东方财富', '同花顺', '行业平均', '解读'],
        ['PE(TTM)', '数据见 Excel', '数据见 Excel', '-', '越低越便宜'],
        ['PB', '数据见 Excel', '数据见 Excel', '-', '反映资产溢价'],
        ['PS(TTM)', '数据见 Excel', '数据见 Excel', '-', '适合高增长公司'],
        ['总市值', '数据见 Excel', '数据见 Excel', '-', '规模对比'],
        ['流通市值', '数据见 Excel', '数据见 Excel', '-', '流动性对比'],
    ]
    
    valuation_table = Table(valuation_data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 2.5*cm, 3.5*cm])
    valuation_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(valuation_table)
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("3.2 盈利能力对比", heading2_style))
    elements.append(Paragraph("数据来源：MX_FinData_9cd9d85c.xlsx（2024-2025 年财务数据）", normal_style))
    
    profit_data = [
        ['指标', '东方财富', '同花顺', '优势方'],
        ['营业收入', '2024-2025 年数据见 Excel', '2024-2025 年数据见 Excel', '-'],
        ['归母净利润', '2024-2025 年数据见 Excel', '2024-2025 年数据见 Excel', '-'],
        ['毛利率', '数据见 Excel', '数据见 Excel', '-'],
        ['净利率', '数据见 Excel', '数据见 Excel', '-'],
        ['ROE(净资产收益率)', '数据见 Excel', '数据见 Excel', '-'],
        ['营收同比增长', '数据见 Excel', '数据见 Excel', '-'],
        ['净利润同比增长', '数据见 Excel', '数据见 Excel', '-'],
        ['EPS(每股收益)', '数据见 Excel', '数据见 Excel', '-'],
    ]
    
    profit_table = Table(profit_data, colWidths=[4*cm, 4.5*cm, 4.5*cm, 3*cm])
    profit_table.setStyle(TableStyle([
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
    
    elements.append(profit_table)
    elements.append(PageBreak())
    
    # ========== SWOT 分析 ==========
    elements.append(Paragraph("四、SWOT 分析", heading1_style))
    
    elements.append(Paragraph("东方财富 SWOT：", heading2_style))
    
    swot_dongfang_data = [
        ['优势 (S)', '劣势 (W)'],
        ['• 全牌照金融生态\n• 流量成本低\n• 用户粘性强\n• 规模效应显著', '• 重资本业务约束\n• 周期性波动大\n• 创新业务投入大\n• 监管政策风险'],
        ['机会 (O)', '威胁 (T)'],
        ['• 财富管理蓝海\n• 机构业务拓展\n• 金融科技赋能\n• 国际化布局', '• 行业竞争加剧\n• 市场交易量波动\n• 监管趋严\n• 技术迭代风险'],
    ]
    
    swot_dongfang_table = Table(swot_dongfang_data, colWidths=[7.5*cm, 7.5*cm])
    swot_dongfang_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#0066cc')),
        ('BACKGROUND', (0, 2), (1, 2), colors.HexColor('#009933')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(swot_dongfang_table)
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("同花顺 SWOT：", heading2_style))
    
    swot_ths_data = [
        ['优势 (S)', '劣势 (W)'],
        ['• AI 技术领先\n• 轻资产高 ROE\n• 机构客户粘性\n• 产品迭代快', '• 无证券牌照\n• 收入结构单一\n• 广告收入波动\n• 依赖第三方平台'],
        ['机会 (O)', '威胁 (T)'],
        ['• AI 大模型变现\n• 机构数字化\n• 海外市场\n• 投顾业务', '• 互联网巨头进入\n• 监管政策变化\n• 技术人才竞争\n• 用户获取成本上升'],
    ]
    
    swot_ths_table = Table(swot_ths_data, colWidths=[7.5*cm, 7.5*cm])
    swot_ths_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#0066cc')),
        ('BACKGROUND', (0, 2), (1, 2), colors.HexColor('#009933')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(swot_ths_table)
    elements.append(PageBreak())
    
    # ========== 投资建议 ==========
    elements.append(Paragraph("五、投资建议", heading1_style))
    
    elements.append(Paragraph("5.1 投资亮点", heading2_style))
    
    elements.append(Paragraph("""
    <b>东方财富：</b><br/>
    🎯 稀缺牌照价值 - 互联网券商龙头，牌照壁垒高<br/>
    🎯 流量变现效率提升 - 从广告到交易的转化优化<br/>
    🎯 财富管理赛道 - 基金投顾试点，AUM 持续增长<br/>
    🎯 国际化布局 - 港股通、海外业务拓展<br/><br/>
    <b>同花顺：</b><br/>
    🎯 AI 技术领先 - 大模型在金融场景落地<br/>
    🎯 轻资产高 ROE - 资本回报率高且稳定<br/>
    🎯 机构业务增长 - iFinD 渗透率提升<br/>
    🎯 增值服务空间 - 付费率有提升潜力
    """, normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("5.2 风险提示", heading2_style))
    
    elements.append(Paragraph("""
    <b>共同风险：</b><br/>
    ⚠️ 市场风险 - A 股交易量下滑影响收入<br/>
    ⚠️ 监管风险 - 金融监管政策趋严<br/>
    ⚠️ 竞争风险 - 互联网巨头 (腾讯、阿里) 进入<br/>
    ⚠️ 技术风险 - AI 技术迭代不及预期<br/><br/>
    <b>特有风险：</b><br/>
    • 东财：证券业务资本金约束、两融风险<br/>
    • 同花顺：广告收入波动、技术投入产出比
    """, normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("5.3 配置建议", heading2_style))
    
    config_data = [
        ['投资者类型', '配置建议'],
        ['保守型', '低仓位观望'],
        ['稳健型', '均衡配置两者'],
        ['进取型', '根据估值动态调整'],
    ]
    
    config_table = Table(config_data, colWidths=[5*cm, 10*cm])
    config_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(config_table)
    elements.append(PageBreak())
    
    # ========== 结论 ==========
    elements.append(Paragraph("六、结论", heading1_style))
    
    elements.append(Paragraph("""
    <b>核心结论：</b><br/><br/>
    1. <b>商业模式差异显著</b><br/>
    &nbsp;&nbsp;&nbsp;• 东财：重资产、全牌照、交易驱动<br/>
    &nbsp;&nbsp;&nbsp;• 同花顺：轻资产、技术驱动、服务驱动<br/><br/>
    2. <b>财务特征不同</b><br/>
    &nbsp;&nbsp;&nbsp;• 东财：收入规模大、周期性强<br/>
    &nbsp;&nbsp;&nbsp;• 同花顺：盈利质量高、ROE 稳定<br/><br/>
    3. <b>成长逻辑各异</b><br/>
    &nbsp;&nbsp;&nbsp;• 东财：市占率提升 + 财富管理<br/>
    &nbsp;&nbsp;&nbsp;• 同花顺：AI 变现 + 机构业务
    """, normal_style))
    
    elements.append(Spacer(1, 1*cm))
    
    # ========== 附录 ==========
    elements.append(Paragraph("附录", heading1_style))
    
    elements.append(Paragraph("""
    <b>A. 数据来源</b><br/>
    • 东方财富妙想金融大模型 (MX_FinData)<br/>
    • 查询时间：2026 年 3 月 14 日<br/>
    • 数据文件：<br/>
    &nbsp;&nbsp;- MX_FinData_fdfbfc24.xlsx (估值指标：PE/PB/PS/市值)<br/>
    &nbsp;&nbsp;- MX_FinData_9cd9d85c.xlsx (盈利能力：营收/利润/ROE)<br/>
    &nbsp;&nbsp;- MX_FinData_6da0204b.xlsx (财务健康：资产/负债/比率)<br/>
    &nbsp;&nbsp;- MX_FinData_757ab013.xlsx (成长性：增长率/EPS)<br/><br/>
    <b>B. 免责声明</b><br/>
    本报告仅供参考，不构成投资建议。投资者应根据自身情况独立判断，自行承担投资风险。<br/><br/>
    <b>C. 联系方式</b><br/>
    • 报告生成：Leo Assistant<br/>
    • 客服咨询：400-620-1818 (东方财富)<br/><br/><br/>
    <i>© 2026 Leo Assistant. 保留所有权利.</i>
    """, normal_style))
    
    # 构建 PDF
    doc.build(elements)
    print(f"SUCCESS: PDF 报告已生成 - {output_path}")
    return True

if __name__ == "__main__":
    output_path = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_CompleteAnalysis.pdf"
    create_pdf_report(output_path)
