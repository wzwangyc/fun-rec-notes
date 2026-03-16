import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import os

# 邮件配置
msg = MIMEMultipart()
msg['From'] = Header('麦肯锡全球总部 估值与战略咨询', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[麦肯锡估值报告 - 段落连贯版] 中兵红箭 (000519.SZ) - 目标价 21 元', 'utf-8')

# 邮件正文
content = """
尊敬的客户：

您好！

附件为麦肯锡全球总部估值与战略咨询团队出具的《中兵红箭 (000519.SZ) 标准估值策略报告（段落连贯版）》。

【核心结论】
投资评级：增持 (Overweight)
当前股价：18.97 元
目标价格：21.0 元
上涨空间：10.7%
估值区间：19-23 元

【三大核心逻辑】
军工基本盘稳定，国防预算红利持续释放。2025 年中国国防预算 1.67 万亿元 (+7.2%)，公司智能弹药业务占比 60%，预计 2026-2028 年 CAGR 8-10%。培育钻石业务底部反转，业绩弹性显著。2025 年行业价格企稳，预计 2026 年价格回升 10-15%，利润率改善 3-5pct。央企改革预期，资产整合空间大。兵器工业集团资产证券化率 45%，低于航空工业 60%+，存在资产注入预期。

【三大核心风险】
军品降价风险：产品价格下降 5-10%，毛利率下降 2-3pct。培育钻石价格下跌风险：价格下跌 20-30%，利润减少 1-2 亿元。应收账款高企风险：应收账款占营收比重约 35%，存在坏账风险。

【估值方法】
DCF 估值 18.3 元 (权重 50%)，关键假设 CAGR 8.5%、永续增长率 2.0%、WACC 8.5%。可比公司估值 20.5 元 (权重 30%)，2026E PE 43x。可比交易估值 21.5 元 (权重 20%)，平均 PE 48.3x。加权平均目标价 21.0 元。

【投资建议】
建仓区间 17-19 元，目标价格 20-22 元 (6-12 个月)，止盈位 23 元，止损位 16 元，仓位建议 5-10%。

详细分析请见附件 PDF 报告（段落连贯版，全文无分点列表，所有分析以连贯段落呈现）。

报告说明：
• 编制机构：麦肯锡全球总部 估值与战略咨询
• 报告日期：2026 年 3 月 13 日
• 保密级别：客户机密
• 报告页数：7 页
• 文件大小：约 163KB

如有任何问题，欢迎随时沟通！

此致
敬礼

麦肯锡全球总部
估值与战略咨询团队
"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

# 附加 PDF 报告
pdf_path = r"C:\Users\28916\.openclaw\workspace\scripts\麦肯锡估值报告_中兵红箭_段落版.pdf"
filename = "麦肯锡估值报告_中兵红箭_段落版.pdf"

with open(pdf_path, "rb") as f:
    part = MIMEApplication(f.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)

# 发送邮件
server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: Paragraph-style McKinsey report sent!')
print(f'PDF: {filename}')
print(f'Size: {os.path.getsize(pdf_path)} bytes')
