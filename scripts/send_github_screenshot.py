import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

msg = MIMEMultipart()
msg['From'] = Header('Leo Assistant', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[GitHub 截图] GitHub 首页截图', 'utf-8')

content = """Yucheng,你好!

这是你要的 GitHub 首页截图。

【截图信息】
- 网站：https://github.com
- 时间：2026 年 3 月 13 日 13:44
- 状态：已成功访问

【GitHub 账号信息】
- 用户名：wzwangyc
- 仓库数：5 个
- 已验证：Token 正常工作

截图已附加在邮件中，请查看!

—— Leo 助手"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

with open(r'C:\Users\28916\.openclaw\media\browser\e3880559-c969-4d1e-bc10-d2af6d2e53d3.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<github-screenshot>')
    img.add_header('Content-Disposition', 'attachment', filename='github-homepage.jpg')
    msg.attach(img)

server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: Email with screenshot sent!')
