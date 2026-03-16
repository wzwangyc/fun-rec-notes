#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
5 分钟延迟执行脚本
运行此脚本后，5 分钟后会自动发送邮件提醒
"""

import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(subject, content):
    """发送邮件"""
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 465
    SENDER_EMAIL = "wangreits@163.com"
    SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"
    RECEIVER_EMAIL = "wangreits@163.com"
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header('Leo Assistant', 'utf-8')
    msg['To'] = Header('Yucheng', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
    server.quit()
    print("Email sent!")

if __name__ == "__main__":
    print("等待 5 分钟...")
    time.sleep(300)  # 300 秒 = 5 分钟
    
    subject = "[5 分钟提醒] 流程执行提醒"
    content = """
Yucheng，你好！

5 分钟时间已到，请回来继续执行流程。

已完成的上次任务：
1. 文档处理技能安装
2. PDF 论文读取
3. 论文学习教学
4. 邮件功能配置

请回来告诉我下一步做什么！

—— Leo 助手
"""
    
    send_email(subject, content)
    print("提醒邮件已发送！")
