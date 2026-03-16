#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
邮件总结 + 待办事项清单生成
读取 163 邮箱邮件，总结内容并生成待办清单发送到邮箱
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import re
import json

# ========== 邮箱配置 ==========
# TODO: 获取 IMAP 授权码后替换此处
IMAP_SERVER = "imap.163.com"
IMAP_PORT = 993
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
EMAIL_ACCOUNT = "wangreits@163.com"
EMAIL_PASSWORD = "UUvrFFxwUCp4SKFW"  # TODO: 替换为 IMAP 授权码
RECEIVER_EMAIL = "wangreits@163.com"
# ===============================

def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ""
    decoded = ""
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            try:
                decoded += word.decode(encoding or 'utf-8', errors='ignore')
            except:
                decoded += word.decode('latin-1', errors='ignore')
        else:
            decoded += word
    return decoded

def get_email_body(msg):
    """获取邮件正文"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if "attachment" in content_disposition:
                continue
            
            if content_type == "text/plain":
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body += part.get_payload(decode=True).decode(charset, errors='ignore')
                except:
                    pass
            elif content_type == "text/html":
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    html = part.get_payload(decode=True).decode(charset, errors='ignore')
                    body += re.sub(r'<[^>]+>', ' ', html)
                except:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='ignore')
        except:
            pass
    
    return body

def extract_todos(body):
    """从邮件正文中提取待办事项"""
    todos = []
    
    # 常见待办关键词
    todo_patterns = [
        r'(请 | 需要 | 必须 | 务必 | 记得|要).{0,50}(完成 | 处理 | 回复 | 提交|参加|准备)',
        r'(截止日期|DDL|截止时间|最后期限).{0,30}[:：]?\s*(\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2})',
        r'(任务|工作|事项|项目).{0,20}[12345][:：．.]',
        r'□|☐|✓|✔|✗|✘|[ ]|[*]',
    ]
    
    lines = body.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) < 5 or len(line) > 200:
            continue
        
        # 检查是否包含待办关键词
        for pattern in todo_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # 提取截止日期
                date_match = re.search(r'(\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}|今天 | 明天 | 本周|下周)', line)
                deadline = date_match.group(1) if date_match else "未指定"
                
                # 判断紧急程度
                urgency = "一般"
                if any(kw in line for kw in ["紧急", "急", "立即", "马上", "今天"]):
                    urgency = "紧急"
                elif any(kw in line for kw in ["重要", "务必", "必须", "一定"]):
                    urgency = "重要"
                elif any(kw in line for kw in ["本周", "下周", "本月"]):
                    urgency = "一般"
                
                todos.append({
                    "content": line[:100],
                    "deadline": deadline,
                    "urgency": urgency,
                    "line_num": i + 1
                })
                break
    
    return todos

def summarize_email(subject, body, todos):
    """总结邮件内容"""
    # 提取关键信息
    summary = {
        "subject": subject,
        "from": "",
        "date": "",
        "key_points": [],
        "todos": todos,
        "action_required": len(todos) > 0
    }
    
    # 提取前 3 个关键句
    sentences = re.split(r'[。！？.!?]', body)
    key_sentences = [s.strip() for s in sentences if 20 < len(s) < 150][:3]
    summary["key_points"] = key_sentences
    
    return summary

def generate_todo_email(summaries):
    """生成待办清单邮件"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 按紧急程度排序待办
    all_todos = []
    for summary in summaries:
        for todo in summary["todos"]:
            todo["source_subject"] = summary["subject"]
            all_todos.append(todo)
    
    # 排序：紧急 > 重要 > 一般
    urgency_order = {"紧急": 0, "重要": 1, "一般": 2}
    all_todos.sort(key=lambda x: urgency_order.get(x["urgency"], 3))
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; }}
        .content {{ padding: 30px; }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; background: #f9f9f9; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ color: #667eea; border-bottom: 2px solid #764ba2; padding-bottom: 10px; }}
        .todo-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
        .todo-urgent {{ border-left-color: #dc3545; background: #fff5f5; }}
        .todo-important {{ border-left-color: #ffc107; background: #fffdf5; }}
        .todo-normal {{ border-left-color: #28a745; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; color: white; margin-left: 10px; }}
        .badge-urgent {{ background: #dc3545; }}
        .badge-important {{ background: #ffc107; color: #333; }}
        .badge-normal {{ background: #28a745; }}
        .summary {{ background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; min-width: 100px; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
        .stat-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 邮件待办清单</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{today} | 自动总结生成</p>
        </div>
        
        <div class="content">
            <p>Yucheng，你好！👋</p>
            <p>这是你今日邮箱的待办事项清单：</p>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{len(summaries)}</div>
                    <div class="stat-label">📧 邮件总数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len([t for t in all_todos if t['urgency'] == '紧急'])}</div>
                    <div class="stat-label">🔴 紧急事项</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len([t for t in all_todos if t['urgency'] == '重要'])}</div>
                    <div class="stat-label">🟡 重要事项</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(all_todos)}</div>
                    <div class="stat-label">✅ 待办总数</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 今日待办事项</h2>
"""
    
    if all_todos:
        for i, todo in enumerate(all_todos, 1):
            badge_class = f"badge-{todo['urgency'].lower()}"
            todo_class = f"todo-{todo['urgency'].lower()}"
            
            html_content += f"""
                <div class="todo-item {todo_class}">
                    <strong>#{i}. {todo['content']}</strong>
                    <span class="badge {badge_class}">{todo['urgency']}</span>
                    <br/><br/>
                    <small>📅 截止日期：{todo['deadline']} | 📧 来源：{todo['source_subject']}</small>
                </div>
"""
    else:
        html_content += """
                <div class="summary">
                    <p>🎉 太棒了！目前没有待办事项。</p>
                </div>
"""
    
    html_content += """
            </div>
            
            <div class="section">
                <h2>📬 邮件摘要</h2>
"""
    
    for summary in summaries[:5]:  # 最多显示 5 封
        html_content += f"""
                <div class="summary">
                    <strong>📧 {summary['subject']}</strong><br/>
"""
        for point in summary['key_points']:
            html_content += f"• {point[:100]}...<br/>"
        html_content += "</div>"
    
    html_content += f"""
            </div>
            
            <div class="section">
                <h2>💡 建议优先级</h2>
                <div class="todo-item todo-urgent">
                    <strong>今天完成：</strong>所有标记为"紧急"的事项
                </div>
                <div class="todo-item todo-important">
                    <strong>本周完成：</strong>所有标记为"重要"的事项
                </div>
                <div class="todo-item todo-normal">
                    <strong>可延后：</strong>标记为"一般"且截止日期较远的事项
                </div>
            </div>
            
            <p style="margin-top: 30px; color: #666; font-size: 12px;">
                📝 <strong>注：</strong>本清单由 Leo Assistant 自动生成，如有遗漏请查看原始邮件。
            </p>
            
            <p style="margin-top: 20px;">祝工作顺利！🦁</p>
        </div>
        
        <div class="footer">
            <p>此邮件由 Leo Assistant 自动生成并发送</p>
            <p>© 2026 Leo Assistant. All rights reserved.</p>
            <p>发送时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} (新加坡时间)</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def send_todo_email(html_content):
    """发送待办清单邮件"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = Header("Leo Assistant 🦁", 'utf-8')
        msg['To'] = Header("Yucheng", 'utf-8')
        msg['Subject'] = Header(f"📋 邮件待办清单 ({datetime.now().strftime('%Y年%m月%d日')})", 'utf-8')
        
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("[OK] 待办清单发送成功！")
        return True
        
    except Exception as e:
        print(f"[ERROR] 发送失败：{e}")
        return False

def read_and_analyze_emails():
    """读取邮件并分析"""
    print("=" * 60)
    print("读取邮箱并生成待办清单")
    print("=" * 60)
    
    summaries = []
    
    try:
        # 连接 IMAP
        print(f"\n[连接] {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # 登录
        print(f"[登录] 登录邮箱...")
        login_result = mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print(f"[登录] 结果：{login_result[0]}")
        
        # 选择收件箱
        print(f"[选择] 选择收件箱...")
        select_result = mail.select("INBOX")
        print(f"[选择] 结果：{select_result[0]}")
        
        if select_result[0] != "OK":
            print("[错误] 无法选择收件箱，请检查 IMAP 授权码")
            return []
        
        # 搜索最近 7 天的邮件
        since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
        print(f"[搜索] 搜索 {since_date} 以来的邮件...")
        
        status, messages = mail.search(None, 'ALL')
        
        if status != "OK":
            print("[错误] 搜索失败")
            return []
        
        email_ids = messages[0].split()
        print(f"[找到] 共 {len(email_ids)} 封邮件")
        
        # 读取最近 30 封
        recent_ids = email_ids[-30:] if len(email_ids) > 30 else email_ids
        
        print(f"\n[读取] 读取最近 {len(recent_ids)} 封邮件...\n")
        
        for email_id in reversed(recent_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    from_ = decode_mime_words(decode_header(msg["From"])[0][0] if decode_header(msg["From"]) else "")
                    to_ = decode_mime_words(decode_header(msg["To"])[0][0] if decode_header(msg["To"]) else "")
                    subject = decode_mime_words(decode_header(msg["Subject"])[0][0] if decode_header(msg["Subject"]) else "")
                    
                    # 排除自己发给自己的
                    if EMAIL_ACCOUNT in from_ and EMAIL_ACCOUNT in to_:
                        continue
                    
                    body = get_email_body(msg)
                    
                    # 提取待办
                    todos = extract_todos(body)
                    
                    # 总结
                    summary = summarize_email(subject, body, todos)
                    summary["from"] = from_
                    summaries.append(summary)
                    
                    if todos:
                        print(f"📧 找到待办：{subject[:50]}... ({len(todos)} 项)")
        
        mail.close()
        mail.logout()
        
        print(f"\n[完成] 成功分析 {len(summaries)} 封邮件")
        return summaries
        
    except Exception as e:
        print(f"\n[错误] 读取失败：{e}")
        print("\n可能原因：")
        print("1. IMAP 授权码不正确（需单独获取，不是 SMTP 授权码）")
        print("2. 邮箱未开启 IMAP 服务")
        print("3. 网络连接问题")
        return []

def main():
    """主函数"""
    # 读取并分析邮件
    summaries = read_and_analyze_emails()
    
    if not summaries:
        print("\n[取消] 没有邮件可分析")
        return
    
    # 生成待办清单邮件
    html_content = generate_todo_email(summaries)
    
    # 发送
    send_todo_email(html_content)
    
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
