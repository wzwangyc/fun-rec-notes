#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
发送 PDF 报告邮件
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
SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"  # SMTP 授权码
RECEIVER_EMAIL = "wangreits@163.com"

def send_pdf_report(pdf_path, subject, email_body):
    """发送带附件的邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EmailHeader("Leo Assistant", 'utf-8')
        msg['To'] = EmailHeader("Yucheng", 'utf-8')
        msg['Subject'] = EmailHeader(subject, 'utf-8')
        
        # 添加正文
        msg.attach(MIMEText(email_body, 'html', 'utf-8'))
        
        # 添加合并后的 PDF 附件
        with open(merged_pdf, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=EmailHeader('EastMoney_vs_Ths_FINAL_Complete.pdf', 'utf-8').encode()
            )
            msg.attach(part)
        
        # 连接 SMTP 服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("SUCCESS: Email sent!")
        print(f"To: {RECEIVER_EMAIL}")
        print(f"Subject: {subject}")
        print(f"Attachment: EastMoney_vs_Ths_FINAL_Complete.pdf (12 pages, 378 KB)")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    # 报告路径 - 发送合并后的完整报告
    merged_pdf = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_FINAL_Complete.pdf"
    pdf_path = merged_pdf
    
    # 邮件正文
    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #003366; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        .emoji {{ font-size: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background: #003366; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 深度研报已生成 (完整数据版)</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">东方财富 vs 同花顺 - 基本面全面对比分析</p>
    </div>
    
    <div class="content">
        <p>Yucheng，你好！👋</p>
        
        <p>你要的<strong>完整数据版研报</strong>已经生成，<strong>所有数据已直接填充到 PDF 中</strong>，请查收附件。</p>
        
        <div class="highlight">
            <strong>📋 报告概览：</strong>
            <ul style="margin: 10px 0;">
                <li>📄 报告类型：企业基本面深度研究 (完整数据版)</li>
                <li>🏢 研究对象：东方财富 (300059.SZ) vs 同花顺 (300033.SZ)</li>
                <li>📅 报告日期：{datetime.now().strftime('%Y年%m月%d日')}</li>
                <li>📊 数据来源：东方财富妙想金融大模型 (MX-FinSkills 全套)</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📈 核心数据对比</h2>
            <table>
                <tr><th>指标</th><th>东方财富</th><th>同花顺</th></tr>
                <tr><td>2025 营收</td><td>115.9 亿元 (+58.67%)</td><td>60.29 亿元 (+44%)</td></tr>
                <tr><td>2025 净利润</td><td>90.97 亿元 (+50.57%)</td><td>32.05 亿元 (+75.79%)</td></tr>
                <tr><td>毛利率</td><td>71.07%</td><td>91.54%</td></tr>
                <tr><td>ROE</td><td>10.73%</td><td>36.7%</td></tr>
                <tr><td>PE(TTM)</td><td>26.33</td><td>53.37</td></tr>
                <tr><td>PB(MRQ)</td><td>3.75</td><td>18.02</td></tr>
                <tr><td>总市值</td><td>3335 亿元</td><td>-</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📰 最新资讯</h2>
            <p><b>东方财富：</b>高管持股计划完成、债券发行、短期融资券兑付</p>
            <p><b>同花顺：</b>2025 年报发布、10 派 51 元 +10 转 4、机构维持买入评级</p>
        </div>
        
        <div class="section">
            <h2>📁 报告章节</h2>
            <p>1. 估值指标对比 (PE/PB/PS/市值)</p>
            <p>2. 财务数据对比 (盈利能力/健康度/成长性)</p>
            <p>3. 最新资讯与机构观点</p>
            <p>4. SWOT 分析</p>
            <p>5. 投资建议</p>
            <p>6. 结论</p>
        </div>
        
        <p style="margin-top: 30px;"><strong>📄 报告内容 (12 页，378 KB)：</strong></p>
        <ul>
            <li><b>Part 1:</b> 估值指标对比 (PE/PB/PS/市值)</li>
            <li><b>Part 2:</b> 财务数据对比 (盈利能力/健康度/成长性)</li>
            <li><b>Part 3:</b> 最新资讯与机构观点</li>
            <li><b>Part 4:</b> SWOT 深度分析 (基于最新财报和机构研报)</li>
            <li><b>Part 5:</b> 投资建议与结论</li>
        </ul>
        <p style="margin-top: 20px;">所有数据已直接填充到 PDF 中，无需查看 Excel！🦁</p>
        
        <p style="margin-top: 20px;">Best regards,<br><strong>Leo Assistant</strong> 🦁</p>
    </div>
    
    <div class="footer">
        <p>此邮件由 Leo Assistant 自动生成并发送</p>
        <p>© 2026 Leo Assistant. All rights reserved.</p>
        <p>东方财富客服：400-620-1818 | 妙想 Cl 官网：https://ai.eastmoney.com/chat</p>
    </div>
</body>
</html>
"""
    
    # 邮件主题
    subject = f"【完整合并版】东方财富 vs 同花顺 - 深度对比研报 (12 页含 SWOT) ({datetime.now().strftime('%Y-%m-%d')})"
    
    # 邮件正文
    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #003366; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        .emoji {{ font-size: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 深度研报已生成</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">东方财富 vs 同花顺 - 基本面全面对比分析</p>
    </div>
    
    <div class="content">
        <p>Yucheng，你好！👋</p>
        
        <p>你要的<strong>麦肯锡风格专业研报</strong>已经生成，请查收附件中的 PDF 文件。</p>
        
        <div class="highlight">
            <strong>📋 报告概览：</strong>
            <ul style="margin: 10px 0;">
                <li>📄 报告类型：企业基本面深度研究</li>
                <li> 研究对象：东方财富 (300059.SZ) vs 同花顺 (300033.SZ)</li>
                <li>📅 报告日期：{datetime.now().strftime('%Y年%m月%d日')}</li>
                <li>📊 数据来源：东方财富妙想金融大模型</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📈 报告内容</h2>
            <p><strong>一、执行摘要</strong> - 核心发现速览</p>
            <p><strong>二、公司概况</strong> - 业务架构与竞争优势</p>
            <p><strong>三、商业模式对比</strong> - 收入结构与变现逻辑</p>
            <p><strong>四、财务数据对比</strong> - 估值、盈利、成长性</p>
            <p><strong>五、SWOT 分析</strong> - 优势、劣势、机会、威胁</p>
            <p><strong>六、投资建议</strong> - 投资亮点与风险提示</p>
            <p><strong>七、结论</strong> - 配置建议</p>
        </div>
        
        <div class="section">
            <h2>🎯 核心发现</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #003366; color: white;">
                    <th style="padding: 12px; text-align: left;">维度</th>
                    <th style="padding: 12px;">东方财富</th>
                    <th style="padding: 12px;">同花顺</th>
                    <th style="padding: 12px;">优势方</th>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">商业模式</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">证券 + 基金 + 数据</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">AI+ 软件 + 广告</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">东财 (牌照壁垒)</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">收入规模</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">较大</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">中等</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">东财</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">盈利能力</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">稳健</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">高毛利</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">同花顺</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">成长驱动</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">市占率提升</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">AI 技术变现</td>
                    <td style="padding: 12px; border-bottom: 1px solid #ddd;">待观察</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📁 数据文件</h2>
            <p>报告中引用的原始数据文件已保存至：</p>
            <code style="background: #f0f0f0; padding: 10px; display: block; border-radius: 4px;">
            C:\\Users\\28916\\.openclaw\\workspace\\skills\\MX_FinData\\workspace\\MX_FinData\\<br>
            • MX_FinData_79a8392b.xlsx (估值指标)<br>
            • MX_FinData_bf89c123.xlsx (财务数据)
            </code>
        </div>
        
        <p style="margin-top: 30px;">如有任何问题或需要进一步分析，随时告诉我！🦁</p>
        
        <p style="margin-top: 20px;">Best regards,<br><strong>Leo Assistant</strong> 🦁</p>
    </div>
    
    <div class="footer">
        <p>此邮件由 Leo Assistant 自动生成并发送</p>
        <p>© 2026 Leo Assistant. All rights reserved.</p>
        <p>东方财富客服：400-620-1818 | 妙想 Cl 官网：https://ai.eastmoney.com/chat</p>
    </div>
</body>
</html>
"""
    
    # 发送邮件
    send_pdf_report(pdf_path, subject, email_body)
