#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邮件发送工具
用于任务完成提醒
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "VWTcb3AnHgZbDvyA"  # SMTP 授权码
RECEIVER_EMAIL = "wangreits@163.com"

def send_email(subject, content):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = Header("Leo Assistant", 'utf-8')
        msg['To'] = Header("Yucheng", 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 连接 SMTP 服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("SUCCESS: Email sent!")
        print(f"Subject: {subject}")
        print(f"To: {RECEIVER_EMAIL}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    # 支持命令行参数：python send_email.py "主题" "内容"
    if len(sys.argv) >= 3:
        subject = sys.argv[1]
        content = sys.argv[2]
    else:
        # 测试邮件
        subject = "[任务完成提醒] 论文学习已完成"
        content = """
Yucheng，你好！

已完成的任务：
1. 安装文档处理技能（nano-pdf, pdf-to-structured, openocr-skill）
2. 安装 Python 文档处理库（python-docx, openpyxl, python-pptx, PyMuPDF）
3. 读取 manuscript.pdf 论文内容
4. 按学习法进行教学讲解

交付成果：
- 论文核心要点总结
- 技术架构解析
- 实验结果分析
- 下一步学习建议

文件位置：
C:\\Users\\28916\\.openclaw\\workspace\\learning\\pdf_content.txt

请回来查看，如有问题随时继续！

—— Leo 助手
"""
    
    send_email(subject, content)
