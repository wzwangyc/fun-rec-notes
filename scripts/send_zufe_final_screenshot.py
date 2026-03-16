import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

msg = MIMEMultipart()
msg['From'] = Header('Leo Assistant', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[高清截图] 浙江财经大学金融学院官网（等待 5 秒加载）', 'utf-8')

content = """Yucheng,你好!

这是等待 5 秒加载后的高清截图，网页元素已完全加载。

【截图信息】
- 网站：浙江财经大学金融学院
- 网址：https://jrxy.zufe.edu.cn
- 时间：2026 年 3 月 13 日 13:51
- 加载等待：5 秒
- 截图范围：可见区域（非全页）

【页面内容】
- 学院新闻（最新：2026-03-12）
- 通知公告（最新：2026-03-12）
- 党建工作
- 本科生教育（含 CFA&FRM 双证实验班）
- 研究生教育
- 国际教育
- 本科生工作
- 研究生工作
- 考研榜（2015-2023）

截图已附加在邮件中，请查看!

—— Leo 助手"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

with open(r'C:\Users\28916\.openclaw\media\browser\baca2407-4e55-47c6-9953-a3df1328f606.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<zufe-final-screenshot>')
    img.add_header('Content-Disposition', 'attachment', filename='zufe-finance-final.jpg')
    msg.attach(img)

server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: Final HD email sent!')
