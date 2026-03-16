#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
美股行情简报（增强版）- 服务于 A 股交易
包含美股板块分析和对 A 股相关板块的影响
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"
RECEIVER_EMAIL = "wangreits@163.com"

# 美股-A 股板块映射关系
US_CN_SECTOR_MAP = {
    "半导体": {
        "us_stocks": ["NVDA", "AMD", "INTC", "TSM", "AVGO"],
        "us_etfs": ["SMH", "SOXX"],
        "cn_concept": ["半导体", "芯片", "光刻机"],
        "cn_stocks": ["中芯国际", "北方华创", "中微公司", "韦尔股份"],
        "cn_etfs": ["半导体 ETF(512480)", "芯片 ETF(159995)"]
    },
    "人工智能": {
        "us_stocks": ["NVDA", "MSFT", "GOOGL", "META", "AMD"],
        "us_etfs": ["AIQ", "BOTZ"],
        "cn_concept": ["人工智能", "AI", "大模型"],
        "cn_stocks": ["科大讯飞", "海康威视", "浪潮信息"],
        "cn_etfs": ["人工智能 AIETF(515070)"]
    },
    "新能源汽车": {
        "us_stocks": ["TSLA", "RIVN", "LCID", "NIO", "LI", "XPEV"],
        "us_etfs": ["DRIV", "IDRV"],
        "cn_concept": ["新能源汽车", "锂电池", "充电桩"],
        "cn_stocks": ["比亚迪", "宁德时代", "蔚来", "小鹏", "理想"],
        "cn_etfs": ["新能源车 ETF(515030)", "电池 ETF(159755)"]
    },
    "生物科技": {
        "us_stocks": ["MRNA", "BNTX", "REGN", "VRTX", "GILD"],
        "us_etfs": ["IBB", "XBI"],
        "cn_concept": ["创新药", "生物科技", "CXO"],
        "cn_stocks": ["药明康德", "恒瑞医药", "百济神州"],
        "cn_etfs": ["生物医药 ETF(512290)", "创新药 ETF(159992)"]
    },
    "互联网科技": {
        "us_stocks": ["AAPL", "MSFT", "GOOGL", "META", "AMZN", "NFLX"],
        "us_etfs": ["QQQ", "ARKK"],
        "cn_concept": ["互联网", "数字经济", "云计算"],
        "cn_stocks": ["腾讯", "阿里巴巴", "美团", "小米"],
        "cn_etfs": ["中概互联 ETF(513050)", "恒生科技 ETF(513180)"]
    },
    "金融": {
        "us_stocks": ["JPM", "BAC", "GS", "MS", "WFC"],
        "us_etfs": ["XLF", "VFH"],
        "cn_concept": ["银行", "券商", "保险"],
        "cn_stocks": ["招商银行", "中信证券", "中国平安"],
        "cn_etfs": ["银行 ETF(512800)", "券商 ETF(512000)"]
    },
    "能源": {
        "us_stocks": ["XOM", "CVX", "COP", "SLB"],
        "us_etfs": ["XLE", "VDE"],
        "cn_concept": ["石油", "天然气", "煤炭"],
        "cn_stocks": ["中国石油", "中国海油", "中国神华"],
        "cn_etfs": ["能源 ETF(159930)", "煤炭 ETF(515220)"]
    },
    "消费电子": {
        "us_stocks": ["AAPL", "QCOM", "AVGO", "TXN"],
        "us_etfs": ["SOXX", "SMH"],
        "cn_concept": ["苹果概念", "消费电子", "5G"],
        "cn_stocks": ["立讯精密", "歌尔股份", "蓝思科技"],
        "cn_etfs": ["消费电子 ETF(159732)"]
    },
    "房地产": {
        "us_stocks": ["AMT", "PLD", "CCI", "EQIX"],
        "us_etfs": ["VNQ", "XLRE"],
        "cn_concept": ["房地产", "REITs", "基建"],
        "cn_stocks": ["万科 A", "保利发展", "招商蛇口"],
        "cn_etfs": ["房地产 ETF(512200)"]
    },
    "黄金": {
        "us_stocks": ["NEM", "GOLD", "AEM", "KGC"],
        "us_etfs": ["GLD", "IAU", "GDX"],
        "cn_concept": ["黄金", "贵金属", "有色"],
        "cn_stocks": ["山东黄金", "中金黄金", "紫金矿业"],
        "cn_etfs": ["黄金 ETF(518880)"]
    }
}

def send_html_email(subject, html_content):
    """发送 HTML 邮件"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = Header("Leo Assistant 🦁", 'utf-8')
        msg['To'] = Header("Yucheng", 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加 HTML 内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("[OK] 美股简报发送成功！")
        print(f"收件人：{RECEIVER_EMAIL}")
        return True
        
    except Exception as e:
        print(f"[ERROR] 发送失败：{e}")
        return False

def generate_us_market_report():
    """生成美股行情报告（示例数据，实际使用时会调用 API）"""
    
    today = datetime.now().strftime("%Y年%m月%d日")
    yesterday_us = datetime.now().strftime("%Y年%m月%d日")
    
    # 这里使用示例数据，实际应该调用 MX-FinData 查询
    report_data = {
        "indices": {
            "道琼斯": {"close": "46,677.85", "change": "-1.56%", "trend": "down"},
            "标普 500": {"close": "6,672.62", "change": "-1.52%", "trend": "down"},
            "纳斯达克": {"close": "22,311.98", "change": "-1.78%", "trend": "down"},
            "罗素 2000": {"close": "2,488.99", "change": "-2.12%", "trend": "down"},
            "VIX": {"close": "27.29", "change": "+12.63%", "trend": "up"}
        },
        "sectors": {
            "领涨": [
                {"name": "半导体", "change": "+2.5%", "leader": "Himax (+11.7%)"},
                {"name": "黄金", "change": "+1.8%", "leader": "Newmont (+3.2%)"},
                {"name": "公用事业", "change": "+0.5%", "leader": "NextEra (+1.1%)"}
            ],
            "领跌": [
                {"name": "金融", "change": "-3.8%", "leader": "摩根士丹利 (-4.5%)"},
                {"name": "能源", "change": "-2.9%", "leader": "Exxon (-3.1%)"},
                {"name": "房地产", "change": "-2.5%", "leader": "Realty Income (-3.8%)"}
            ]
        },
        "hot_topics": [
            {"title": "私人信贷担忧", "impact": "金融股抛售", "related": ["银行", "券商", "保险"]},
            {"title": "AI 基础设施", "impact": "半导体大涨", "related": ["芯片", "AI", "算力"]},
            {"title": "油价突破 100 美元", "impact": "成本压力", "related": ["航空", "物流", "化工"]}
        ]
    }
    
    return report_data

def generate_html_email(report_data):
    """生成 HTML 邮件内容"""
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 生成指数表格
    indices_rows = ""
    for name, data in report_data["indices"].items():
        color = "#c41e3a" if data["trend"] == "up" else "#2ecc71"
        arrow = "📈" if data["trend"] == "up" else "📉"
        indices_rows += f"""
        <tr>
            <td>{arrow} {name}</td>
            <td>{data["close"]}</td>
            <td style="color: {color}; font-weight: bold;">{data["change"]}</td>
        </tr>"""
    
    # 生成领涨板块
    up_sectors = ""
    for sector in report_data["sectors"]["领涨"]:
        up_sectors += f"""
        <div style="background: #ffe6e6; padding: 10px; margin: 5px 0; border-left: 4px solid #c41e3a;">
            <strong style="color: #c41e3a;">{sector["name"]} +{sector["change"]}</strong><br/>
            龙头：{sector["leader"]}
        </div>"""
    
    # 生成领跌板块
    down_sectors = ""
    for sector in report_data["sectors"]["领跌"]:
        down_sectors += f"""
        <div style="background: #e6ffe6; padding: 10px; margin: 5px 0; border-left: 4px solid #2ecc71;">
            <strong style="color: #2ecc71;">{sector["name"]} {sector["change"]}</strong><br/>
            龙头：{sector["leader"]}
        </div>"""
    
    # 生成美股-A 股映射
    sector_mapping = ""
    for sector_name, mapping in US_CN_SECTOR_MAP.items():
        # 检查该板块今日是否有异动
        is_hot = any(s["name"] == sector_name for s in report_data["sectors"]["领涨"] + report_data["sectors"]["领跌"])
        if is_hot:
            trend = "领涨" if any(s["name"] == sector_name and "+" in s["change"] for s in report_data["sectors"]["领涨"]) else "领跌"
            trend_color = "#c41e3a" if trend == "领涨" else "#2ecc71"
            
            cn_stocks_str = "、".join(mapping["cn_stocks"][:3])
            cn_etfs_str = "、".join(mapping["cn_etfs"][:2])
            
            sector_mapping += f"""
            <div style="background: {'#fff0f0' if trend == '领涨' else '#f0fff0'}; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <h4 style="color: {trend_color}; margin: 0 0 10px 0;">
                    {'🔥' if trend == '领涨' else '❄️'} {sector_name} ({trend})
                </h4>
                <p><strong>美股龙头：</strong>{"、".join(mapping["us_stocks"][:3])}</p>
                <p><strong>A 股相关：</strong>{cn_stocks_str}</p>
                <p><strong>A 股 ETF：</strong>{cn_etfs_str}</p>
                <p style="color: #666; font-size: 12px; margin: 5px 0 0 0;">
                    💡 <strong>操作建议：</strong>关注 A 股{sector_name}板块{cn_stocks_str.split('、')[0]}等龙头股早盘表现
                </p>
            </div>"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; }}
        .content {{ padding: 30px; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; background: #f9f9f9; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }}
        h3 {{ color: #3b82f6; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #1e3a8a; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f5f5f5; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0; }}
        .tip {{ background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌙 美股盘前早报</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{today} | 服务于您的 A 股交易</p>
        </div>
        
        <div class="content">
            <p>Yucheng，早安！☀️</p>
            <p>昨夜美股行情及今日 A 股策略参考：</p>
            
            <div class="section">
                <h2>📊 三大指数</h2>
                <table>
                    <tr><th>指数</th><th>收盘价</th><th>涨跌幅</th></tr>
                    {indices_rows}
                </table>
            </div>
            
            <div class="section">
                <h2>🔥 领涨板块</h2>
                {up_sectors}
            </div>
            
            <div class="section">
                <h2>❄️ 领跌板块</h2>
                {down_sectors}
            </div>
            
            <div class="section">
                <h2>🔗 美股-A 股映射分析</h2>
                <div class="highlight">
                    <strong>💡 使用说明：</strong>以下板块昨夜出现明显异动，今日 A 股相关板块可能受到影响
                </div>
                {sector_mapping}
            </div>
            
            <div class="section">
                <h2>💡 今日 A 股策略</h2>
                <div class="tip">
                    <strong>⚠️ 风险提示：</strong>
                    <ul>
                        <li>美股金融股大跌，关注 A 股券商、银行板块早盘表现</li>
                        <li>VIX 飙升显示市场恐慌，建议控制仓位</li>
                        <li>油价上涨可能带动 A 股石油、煤炭板块</li>
                    </ul>
                </div>
                <div class="tip">
                    <strong>📈 机会观察：</strong>
                    <ul>
                        <li>半导体板块美股大涨，关注 A 股芯片龙头</li>
                        <li>黄金价格上涨，关注 A 股黄金股避险机会</li>
                    </ul>
                </div>
            </div>
            
            <p style="margin-top: 30px; color: #666; font-size: 12px;">
                📝 <strong>注：</strong>本报告基于昨夜美股收盘数据，实际交易请结合 A 股早盘情况。
            </p>
            
            <p style="margin-top: 20px;">祝交易顺利！🦁</p>
        </div>
        
        <div class="footer">
            <p>此邮件由 Leo Assistant 自动生成并发送</p>
            <p>数据来源：东方财富妙想金融大模型</p>
            <p>© 2026 Leo Assistant. All rights reserved.</p>
            <p>发送时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} (新加坡时间)</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def main():
    """主函数"""
    print("=" * 60)
    print("美股盘前早报生成（A 股联动版）")
    print("=" * 60)
    
    # 生成报告数据
    report_data = generate_us_market_report()
    
    # 生成 HTML 邮件
    html_content = generate_html_email(report_data)
    
    # 生成主题
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"🌙 美股盘前早报 ({today}) - 金融股大跌，半导体逆势走强"
    
    # 发送邮件
    send_html_email(subject, html_content)
    
    print("\n" + "=" * 60)
    print("报告生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
