import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

msg = MIMEMultipart()
msg['From'] = Header('Leo Assistant', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[截图] 浙江财经大学金融学院官网', 'utf-8')

content = """Yucheng,你好!

这是你要的浙江财经大学金融学院官网截图。

【截图信息】
- 网站：浙江财经大学金融学院
- 网址：https://jrxy.zufe.edu.cn
- 时间：2026 年 3 月 13 日 13:46
- 状态：已成功访问

【网站内容】
- 学院新闻
- 通知公告
- 党建工作
- 本科生教育
- 研究生教育
- 国际教
- 本科生工作
- 研究生工作

截图已附加在邮件中，请查看!

—— Leo 助手"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

with open(r'C:\Users\28916\.openclaw\media\browser\0c4c7138-bc9b-4da6-adb2-22978d36b1bf.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<zufe-finance-screenshot>')
    img.add_header('Content-Disposition', 'attachment', filename='zufe-finance-school.jpg')
    msg.attach(img)

server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: Email with screenshot sent!')
