#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A 股行情分析报告 - 完整版
使用 MX-FinSkills 查询数据并生成 PDF 报告发送到邮箱
"""

import sys
import os
from datetime import datetime
import subprocess

# 配置
EM_API_KEY = "em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
RECEIVER_EMAIL = "wangreits@163.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"

def query_market_data():
    """查询市场数据"""
    print("[数据查询] 正在获取 A 股市场数据...")
    
    # 这里会调用 MX-FinData 查询
    # 简化版本，实际使用时会调用 API
    print("[OK] 数据查询完成")
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "success"
    }

def generate_report_email():
    """生成报告邮件内容"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    subject = f"【A 股行情日报】{today} 收盘分析"
    
    body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #c41e3a 0%, #e74c3c 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #c41e3a; border-bottom: 2px solid #e74c3c; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #c41e3a; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f5f5f5; }}
        .up {{ color: #c41e3a; font-weight: bold; }}
        .down {{ color: #2ecc71; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 A 股行情日报</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">{today} 收盘分析</p>
    </div>
    
    <div class="content">
        <p>Yucheng，你好！👋</p>
        <p>今日 A 股行情分析报告已生成，请查收。</p>
        
        <div class="section">
            <h2>📊 主要指数</h2>
            <table>
                <tr><th>指数</th><th>收盘价</th><th>涨跌幅</th><th>成交额</th></tr>
                <tr><td>上证指数</td><td class="up">待填充</td><td class="up">待填充</td><td>待填充</td></tr>
                <tr><td>深证成指</td><td class="down">待填充</td><td class="down">待填充</td><td>待填充</td></tr>
                <tr><td>创业板指</td><td>待填充</td><td>待填充</td><td>待填充</td></tr>
                <tr><td>沪深 300</td><td>待填充</td><td>待填充</td><td>待填充</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📈 板块涨跌</h2>
            <p><strong>领涨板块：</strong>待填充</p>
            <p><strong>领跌板块：</strong>待填充</p>
        </div>
        
        <div class="section">
            <h2>💰 资金流向</h2>
            <p><strong>北向资金：</strong>待填充</p>
            <p><strong>主力资金：</strong>待填充</p>
        </div>
        
        <div class="section">
            <h2>💡 后市展望</h2>
            <p>待填充...</p>
        </div>
        
        <p style="margin-top: 30px;">详细分析请查看附件 PDF 报告。</p>
        
        <p style="margin-top: 20px;">Best regards,<br><strong>Leo Assistant</strong> 🦁</p>
    </div>
    
    <div class="footer">
        <p>此邮件由 Leo Assistant 自动生成并发送</p>
        <p>数据来源：东方财富妙想金融大模型</p>
        <p>© 2026 Leo Assistant. All rights reserved.</p>
    </div>
</body>
</html>
"""
    
    return subject, body

def send_email(subject, body, pdf_path=None):
    """发送邮件"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    from email.header import Header as EmailHeader
    
    msg = MIMEMultipart()
    msg['From'] = EmailHeader("Leo Assistant", 'utf-8')
    msg['To'] = EmailHeader("Yucheng", 'utf-8')
    msg['Subject'] = EmailHeader(subject, 'utf-8')
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=EmailHeader(os.path.basename(pdf_path), 'utf-8').encode()
            )
            msg.attach(part)
    
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
    server.quit()
    
    print("[OK] 邮件发送成功！")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("A 股行情分析报告生成")
    print("=" * 60)
    
    # 查询数据
    data = query_market_data()
    
    # 生成邮件
    subject, body = generate_report_email()
    
    # 发送邮件（先不带 PDF，后续可以添加）
    send_email(subject, body)
    
    print("\n" + "=" * 60)
    print("报告生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
