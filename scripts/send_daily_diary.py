#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日日记生成和发送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime, timedelta
import os

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "VWTcb3AnHgZbDvyA"
RECEIVER_EMAIL = "wangreits@163.com"

def send_email(subject, content):
    """发送邮件"""
    try:
        msg = MIMEMultipart()
        msg['From'] = Header("Leo Assistant", 'utf-8')
        msg['To'] = Header("Yucheng", 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("SUCCESS: Email sent!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def generate_diary():
    """生成今日日记"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    content = f"""Yucheng，你好！

这是你今天的回顾 (2026-03-16)：

### 🎓 学习进展
- Datawhale fun-rec 推荐系统课程 - 第 1 章完成
- 学习了序列生成模式、Transformer、Tokenizer 语义 ID、KV caching 等核心概念
- 笔记已上传到 GitHub: wzwangyc/fun-rec-notes

### 🛠️ 工作/项目
- 完成宏观数据源对比测试（东方财富/akshare/yfinance/Trading Economics）
- 生成完整报告：reports/macro_data_source_comparison.md
- 配置 GitHub 自动化：以后学习笔记可以自动整理上传

### 💡 想法/洞察
- 推荐系统的序列建模思路与量化金融的时间序列分析有异曲同工之妙
- 语义 ID 和特征降维的逻辑可以应用到金融预测模型中
- 自动化能节省大量重复工作时间

### 📝 明日计划
- 继续 fun-rec 课程学习（第 2 章）
- 保持学习节奏，学完把心得发给我整理上传

继续加油！有我在呢~

—— Leo 🦁
2026-03-16 深夜
"""
    
    subject = f"📅 每日日记 - 2026-03-16"
    return subject, content

if __name__ == "__main__":
    subject, content = generate_diary()
    send_email(subject, content)
