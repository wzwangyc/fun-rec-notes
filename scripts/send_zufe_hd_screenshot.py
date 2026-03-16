import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

msg = MIMEMultipart()
msg['From'] = Header('Leo Assistant', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[高清截图] 浙江财经大学金融学院官网', 'utf-8')

content = """Yucheng,你好!

这是高清版的浙江财经大学金融学院官网截图。

【改进说明】
- 格式：PNG 格式（无损压缩）
- 范围：当前可见区域（非全页）
- 清晰度：比全页截图更清晰

【截图信息】
- 网站：浙江财经大学金融学院
- 网址：https://jrxy.zufe.edu.cn
- 时间：2026 年 3 月 13 日 13:47

截图已附加在邮件中，请查看!

—— Leo 助手"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

with open(r'C:\Users\28916\.openclaw\media\browser\21d529c3-308f-49f4-a988-296d9523655f.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<zufe-hd-screenshot>')
    img.add_header('Content-Disposition', 'attachment', filename='zufe-finance-hd.jpg')
    msg.attach(img)

server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: HD email sent!')
