import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import os

# 邮件配置
msg = MIMEMultipart()
msg['From'] = Header('Leo 智能投研助手', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[投资报告] 中兵红箭 (000519) 投资价值分析报告', 'utf-8')

# 邮件正文
content = """
Yucheng，你好！

按照麦肯锡分析框架，我已完成中兵红箭 (000519) 的投资价值分析报告。

【核心结论】
- 投资评级：增持
- 目标价格：20-22 元（6-12 个月）
- 当前股价：约 18.35 元

【核心亮点】
1. 军工央企背景，智能弹药核心供应商
2. 培育钻石业务提供业绩弹性
3. 国防预算稳定增长，行业景气度向上

【主要风险】
1. 军品定价机制改革压力
2. 民品业务竞争激烈
3. 应收账款占比较高

详细分析请见附件 PDF 报告。

报告说明：
- 数据来源：AKShare、公开信息
- 生成时间：2026 年 3 月 13 日
- 编制：Leo 智能投研助手

如有任何问题，欢迎随时沟通！

—— Leo

"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

# 附加 PDF 文件（使用正确的 MIME 类型）
pdf_path = r"C:\Users\28916\.openclaw\workspace\scripts\中兵红箭投资价值分析报告.pdf"
filename = os.path.basename(pdf_path)

with open(pdf_path, "rb") as f:
    # 使用 MIMEApplication 并指定正确的类型
    part = MIMEApplication(f.read(), Name=filename)
    
# 添加 Content-Disposition header，确保正确显示文件名
part['Content-Disposition'] = f'attachment; filename="{filename}"'
msg.attach(part)

# 发送邮件
server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: PDF email sent with correct format!')
print(f'PDF 文件：{filename}')
print(f'文件大小：{os.path.getsize(pdf_path)} bytes')
