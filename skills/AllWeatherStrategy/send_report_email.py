#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
发送全天候策略 PDF 报告到邮箱
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header as EmailHeader
from datetime import datetime
import os

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"
RECEIVER_EMAIL = "wangreits@163.com"

def send_all_weather_report(pdf_path):
    """发送全天候策略报告邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EmailHeader("Leo Assistant", 'utf-8')
        msg['To'] = EmailHeader("Yucheng", 'utf-8')
        msg['Subject'] = EmailHeader(f"【全天候策略报告】ETF 资产配置方案 ({datetime.now().strftime('%Y-%m-%d')})", 'utf-8')
        
        # 邮件正文
        email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .highlight {{ background: #dbeafe; padding: 15px; border-left: 4px solid #3b82f6; margin: 20px 0; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #1e3a8a; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f5f5f5; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #dbeafe; border-radius: 8px; min-width: 200px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #1e3a8a; }}
        .metric-label {{ font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ 全天候 ETF 资产配置报告</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">基于 Risk Parity (风险平配) 策略</p>
    </div>
    
    <div class="content">
        <p>Yucheng，你好！👋</p>
        
        <p>你的全天候 ETF 资产配置方案已生成，请查收附件中的 PDF 报告。</p>
        
        <div class="highlight">
            <strong>📊 核心指标：</strong>
            <div class="metric">
                <div class="metric-value">20.51%</div>
                <div class="metric-label">预估年化收益</div>
            </div>
            <div class="metric">
                <div class="metric-value">11.83%</div>
                <div class="metric-label">年化风险 (波动率)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 配置方案概览</h2>
            <table>
                <tr><th>ETF 代码</th><th>ETF 名称</th><th>权重</th><th>配置金额</th><th>参考价格</th><th>申购份额</th></tr>
                <tr><td>515450</td><td>易方达沪深 300ETF</td><td>34.03%</td><td>3,402.99 元</td><td>1.457 元</td><td>2300 份</td></tr>
                <tr><td>159545</td><td>华夏中证 500ETF</td><td>16.57%</td><td>1,656.98 元</td><td>1.476 元</td><td>1100 份</td></tr>
                <tr><td>159531</td><td>易方达中证 2000ETF</td><td>12.46%</td><td>1,245.76 元</td><td>1.515 元</td><td>800 份</td></tr>
                <tr><td>159201</td><td>招商中证全指证券公司 ETF</td><td>10.58%</td><td>1,057.95 元</td><td>1.393 元</td><td>700 份</td></tr>
                <tr><td>513100</td><td>国泰纳斯达克 100ETF</td><td>10.37%</td><td>1,037.28 元</td><td>1.767 元</td><td>500 份</td></tr>
                <tr><td>588290</td><td>华夏上证科创板芯片 ETF</td><td>8.18%</td><td>818.38 元</td><td>2.425 元</td><td>300 份</td></tr>
                <tr><td>518880</td><td>华安黄金 ETF</td><td>7.81%</td><td>780.66 元</td><td>10.802 元</td><td>0 份</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📄 报告内容</h2>
            <p>PDF 报告包含以下内容：</p>
            <ul>
                <li><strong>配置方案详情：</strong> 各大类资产 ETF 的最优配置权重</li>
                <li><strong>权重分布可视化：</strong> 饼图展示各 ETF 配置比例</li>
                <li><strong>风险收益分析：</strong> 基于历史数据的年化收益和风险预测</li>
                <li><strong>操作建议：</strong> 各 ETF 的参考价格、申购份额和实际投入金额</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💡 策略说明</h2>
            <p><strong>全天候策略 (All Weather Strategy)</strong> 基于 Risk Parity (风险平配) 原理，通过均衡配置各大类资产的风险贡献，实现穿越牛熊的稳健收益。</p>
            <p><strong>适用场景：</strong> 长期资产配置、养老金投资、家庭财富保值增值</p>
            <p><strong>风险提示：</strong> 历史业绩不代表未来表现，投资需谨慎</p>
        </div>
        
        <p style="margin-top: 30px;">如有任何问题或需要调整配置方案，随时告诉我！🦁</p>
        
        <p style="margin-top: 20px;">Best regards,<br><strong>Leo Assistant</strong> 🦁</p>
    </div>
    
    <div class="footer">
        <p>此邮件由 Leo Assistant 自动生成并发送</p>
        <p>© 2026 wzwangyc. All Rights Reserved.</p>
        <p>技能来源：ClawHub - All Weather Strategy Skill by @wzwangyc</p>
    </div>
</body>
</html>
"""
        
        # 添加 PDF 附件
        with open(pdf_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(pdf_path)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=EmailHeader(filename, 'utf-8').encode()
            )
            msg.attach(part)
        
        # 连接 SMTP 服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("SUCCESS: Email sent!")
        print(f"To: {RECEIVER_EMAIL}")
        print(f"Subject: All Weather Strategy Report")
        print(f"Attachment: {filename}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    # PDF 报告路径
    import os
    output_dir = r"C:\Users\28916\.openclaw\workspace\skills\AllWeatherStrategy\全天候配置报告"
    
    # 获取最新的 PDF 文件
    pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
    if pdf_files:
        latest_pdf = max(pdf_files)
        pdf_path = os.path.join(output_dir, latest_pdf)
        
        print(f"Sending PDF report: {pdf_path}")
        send_all_weather_report(pdf_path)
    else:
        print("ERROR: No PDF files found in output directory")
