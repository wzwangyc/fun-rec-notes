#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取并分析 163 邮箱邮件（排除自己发给自己的）
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import re

# 邮箱配置
IMAP_SERVER = "imap.163.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = "wangreits@163.com"
EMAIL_PASSWORD = "VWTcb3AnHgZbDvyA"  # IMAP/SMTP 授权码

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
            
            # 跳过附件
            if "attachment" in content_disposition:
                continue
            
            # 优先获取文本部分
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
                    # 简单提取 HTML 中的文本
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

def read_emails(num_emails=10, days_back=7):
    """读取最近邮件"""
    print("=" * 60)
    print(f"读取邮箱：{EMAIL_ACCOUNT}")
    print("=" * 60)
    
    emails_data = []
    
    try:
        # 连接 IMAP 服务器
        print(f"\n[连接] 正在连接 {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # 登录
        print(f"[登录] 登录邮箱...")
        login_result = mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print(f"[登录] 结果：{login_result[0]}")
        
        # 选择收件箱
        print(f"[选择] 选择收件箱...")
        select_result = mail.select("INBOX")
        print(f"[选择] 结果：{select_result[0]}, 邮件数：{select_result[1][0] if select_result[1] else '未知'}")
        
        # 搜索邮件（最近 N 天）
        since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
        print(f"[搜索] 搜索 {since_date} 以来的邮件...")
        
        status, messages = mail.search(None, 'ALL')  # 先搜索所有
        
        if status != "OK":
            print("[错误] 搜索失败")
            return []
        
        email_ids = messages[0].split()
        print(f"[找到] 共 {len(email_ids)} 封邮件")
        
        # 读取最近的 N 封邮件
        recent_ids = email_ids[-num_emails:] if len(email_ids) > num_emails else email_ids
        
        print(f"\n[读取] 读取最近 {len(recent_ids)} 封邮件...\n")
        
        for email_id in reversed(recent_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 解码发件人、收件人、主题
                    from_ = decode_mime_words(decode_header(msg["From"])[0][0] if decode_header(msg["From"]) else "")
                    to_ = decode_mime_words(decode_header(msg["To"])[0][0] if decode_header(msg["To"]) else "")
                    subject = decode_mime_words(decode_header(msg["Subject"])[0][0] if decode_header(msg["Subject"]) else "")
                    date_ = msg["Date"]
                    
                    # 排除自己发给自己的邮件
                    if EMAIL_ACCOUNT in from_ and EMAIL_ACCOUNT in to_:
                        print(f"[跳过] 自己发给自己的邮件：{subject}")
                        continue
                    
                    # 获取邮件正文
                    body = get_email_body(msg)
                    
                    # 提取关键信息
                    email_info = {
                        "from": from_,
                        "to": to_,
                        "subject": subject,
                        "date": date_,
                        "body": body[:500] if len(body) > 500 else body,  # 限制长度
                        "is_self": False
                    }
                    
                    emails_data.append(email_info)
                    
                    # 打印摘要
                    print(f"{'-' * 60}")
                    print(f"📧 发件人：{from_}")
                    print(f"📎 主题：{subject}")
                    print(f"📅 日期：{date_}")
                    print(f"📄 正文预览：{body[:100]}...")
                    print()
        
        # 关闭连接
        mail.close()
        mail.logout()
        
        print("=" * 60)
        print(f"[完成] 成功读取 {len(emails_data)} 封邮件（排除自己发给自己的）")
        print("=" * 60)
        
        return emails_data
        
    except Exception as e:
        print(f"\n[错误] 读取失败：{e}")
        print("\n可能的原因：")
        print("1. IMAP 授权码不正确（注意：不是登录密码，是 SMTP/IMAP 授权码）")
        print("2. 邮箱未开启 IMAP 服务")
        print("3. 网络连接问题")
        return []

def analyze_emails(emails_data):
    """分析邮件内容"""
    if not emails_data:
        print("\n[分析] 没有邮件可分析")
        return
    
    print("\n" + "=" * 60)
    print("📊 邮件分析报告")
    print("=" * 60)
    
    # 统计发件人
    from_count = {}
    for email_info in emails_data:
        from_ = email_info["from"]
        from_count[from_] = from_count.get(from_, 0) + 1
    
    print("\n📬 发件人统计：")
    for from_, count in sorted(from_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {from_}: {count} 封")
    
    # 统计主题关键词
    print("\n🔑 主题关键词：")
    subjects = [e["subject"] for e in emails_data]
    for subject in subjects[:5]:
        print(f"  • {subject}")
    
    print("\n" + "=" * 60)

def main():
    """主函数"""
    # 读取邮件（最近 20 封，过去 7 天）
    emails_data = read_emails(num_emails=20, days_back=7)
    
    # 分析邮件
    analyze_emails(emails_data)
    
    return emails_data

if __name__ == "__main__":
    main()
