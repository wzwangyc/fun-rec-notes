#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
美股行情简报邮件发送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
from datetime import datetime

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "wangreits@163.com"
SENDER_PASSWORD = "UUvrFFxwUCp4SKFW"  # SMTP 授权码
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
    # 获取日期
    today = datetime.now().strftime("%Y年%m月%d日")
    
    subject = f"【美股简报】{today} - 三大指数全线收跌，私人信贷担忧引发市场波动"
    
    content = f"""
═══════════════════════════════════════════════════
              美股行情简报
         {today} (美东时间 3 月 12 日收盘)
═══════════════════════════════════════════════════

📊 一、三大指数收盘数据
───────────────────────────────────────────────────

  道琼斯工业平均指数 (^DJI)：46,677.85 点
  ▼ 下跌 739.42 点  (-1.56%)

  标准普尔 500 指数 (^GSPC)：6,672.62 点
  ▼ 下跌 1.52%

  纳斯达克综合指数 (^IXIC)：22,311.98 点
  ▼ 下跌 1.78%

  其他重要指数:
  • 罗素 2000 指数：2,488.99 点  ▼ -2.12%
  • VIX 恐慌指数：27.29 点  ▲ +12.63%

═══════════════════════════════════════════════════

📰 二、市场动态
───────────────────────────────────────────────────

1️⃣ 私人信贷市场担忧引发金融股抛售
   主要银行宣布相关消息后，投资者对私人信贷市场稳定性
   产生担忧，导致多家金融机构股价下跌：
   • 摩根士丹利 (MS) ▼ -4.5%
   • 黑石集团 (BX) ▼ -4.3%
   • LPL Financial (LPLA) ▼ -3.5%
   • Affirm (AFRM) 等支付股也受到影响

2️⃣ 原油价格突破 100 美元/桶
   地缘政治冲突推动油价上涨，引发对运营成本上升和
   消费者支出下降的担忧，餐饮休闲股普遍下跌：
   • Dine Brands, Wingstop, Dutch Bros 等均收跌

3️⃣ 科技股表现分化
   • Adobe (ADBE) CEO 宣布将在 18 年后离职，股价 ▼ -1.43%
   • Himax (HIMX) 因 AI 基础设施报道 ▲ +11.7%
   • 比特币上涨 2.25% 至 71,130 美元

4️⃣ 市场波动性显著上升
   VIX 恐慌指数飙升 12.63% 至 27.29，显示市场不确定性增加

═══════════════════════════════════════════════════

🎯 三、重点关注
───────────────────────────────────────────────────

⚠️ 风险提示:
   1. 私人信贷市场稳定性 - 密切关注后续银行财报和信贷数据
   2. 油价上涨对通胀的影响 - 可能延缓美联储降息步伐
   3. 市场波动性上升 - VIX 突破 27，短期波动可能加剧

📈 机会观察:
   1. 半导体板块 - Himax 因 AI 概念大涨，关注产业链机会
   2. 加密货币 - 比特币突破 7.1 万美元，相关股票可能受益
   3. 防御性板块 - 市场波动时关注公用事业、必需消费品

💡 后市展望:
   短期市场可能继续震荡，建议:
   • 保持适度仓位，避免过度杠杆
   • 关注下周美联储会议和经济数据
   • 分散配置，平衡风险和收益

═══════════════════════════════════════════════════

数据来源：Yahoo Finance
发送时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} (新加坡时间)

—— Leo 助手 🦁
"""
    
    send_email(subject, content)
