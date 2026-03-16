import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import os

# 邮件配置
msg = MIMEMultipart()
msg['From'] = Header('Leo 智能投研', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[专业研究报告] 中兵红箭 (000519.SZ) - 增持评级 目标价 20-22 元', 'utf-8')

# 邮件正文
content = """
尊敬的 Yucheng：

您好！

按照高盛、摩根大通、麦肯锡的专业标准，我已完成中兵红箭 (000519.SZ) 的深度投资价值分析报告。

【核心结论】
投资评级：增持 (Overweight)
当前股价：18.97 元 (2026/3/13)
目标价格：20-22 元 (6-12 个月)
上涨空间：5.4% - 16.0%

【核心投资亮点】
1. 军工央企背景，智能弹药核心供应商
2. 培育钻石业务提供业绩弹性
3. 国防预算稳定增长，行业景气度向上
4. 估值处于合理区间，具备配置价值

【关键财务指标】
2024E 营收：71.2 亿元
2024E 净利润：6.8 亿元
毛利率：29.5%
ROE: 5.2%
资产负债率：34.0%

【风险因素】
1. 军品定价机制改革压力
2. 培育钻石价格继续下跌风险
3. 应收账款占比较高
4. 市场竞争加剧
5. 宏观经济下行风险

详细分析请见附件专业 PDF 报告（按照投行标准格式制作）。

报告说明：
- 框架：高盛/摩根大通专业投研框架
- 语言：中文
- 数据来源：AKShare、Wind、公司公告
- 生成时间：2026 年 3 月 13 日
- 编制：Leo 智能投研

如有任何问题，欢迎随时沟通！

此致
敬礼

Leo
Leo 智能投研助手
"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

# 附加 PDF 报告
pdf_path = r"C:\Users\28916\.openclaw\workspace\scripts\中兵红箭投资价值分析报告_专业版.pdf"
filename = "中兵红箭投资价值分析报告_专业版.pdf"

with open(pdf_path, "rb") as f:
    part = MIMEApplication(f.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)

# 发送邮件
server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: Professional PDF report sent!')
print(f'PDF: {filename}')
print(f'Size: {os.path.getsize(pdf_path)} bytes')
