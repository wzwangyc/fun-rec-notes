import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

msg = MIMEMultipart()
msg['From'] = Header('Leo Assistant', 'utf-8')
msg['To'] = Header('Yucheng', 'utf-8')
msg['Subject'] = Header('[高清截图] 浙江财经大学官网（等待 5 秒加载）', 'utf-8')

content = """Yucheng,你好!

这是浙江财经大学官网截图（等待 5 秒加载后）。

【截图信息】
- 网站：浙江财经大学
- 网址：https://www.zufe.edu.cn
- 时间：2026 年 3 月 13 日 14:21
- 加载等待：5 秒

【页面内容】
- 要闻新闻（最新：2026-03-13 省教育厅调研）
- 浙财动态
- 科研动态
- 教学动态
- 校园活动
- 人物故事
- 校地/国际合作
- 历史沿革（1974-2023）
- 媒体矩阵

截图已附加在邮件中，请查看!

—— Leo 助手"""

msg.attach(MIMEText(content, 'plain', 'utf-8'))

with open(r'C:\Users\28916\.openclaw\media\browser\32da8f7d-1c3b-47ae-9b44-6494f9fd5b2a.jpg', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<zufe-university-screenshot>')
    img.add_header('Content-Disposition', 'attachment', filename='zufe-university.jpg')
    msg.attach(img)

server = smtplib.SMTP_SSL('smtp.163.com', 465, timeout=10)
server.login('wangreits@163.com', 'UUvrFFxwUCp4SKFW')
server.sendmail('wangreits@163.com', ['wangreits@163.com'], msg.as_string())
server.quit()

print('SUCCESS: ZUFE email sent!')
