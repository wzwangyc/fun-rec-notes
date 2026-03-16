#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从配置文件读取 ETF 列表
"""

def parse_config(config_path):
    """解析配置文件，返回 ETF 列表、金额、回看天数"""
    etf_list = []
    total_amount = 10000
    lookback_days = 365
    send_email = True
    email_to = "wangreits@163.com"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 解析 ETF_LIST
    import re
    etf_match = re.search(r'ETF_LIST\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if etf_match:
        etf_text = etf_match.group(1)
        etf_codes = re.findall(r'(\d{6})', etf_text)
        etf_list = etf_codes
    
    # 解析 TOTAL_AMOUNT
    amount_match = re.search(r'TOTAL_AMOUNT\s*=\s*(\d+)', content)
    if amount_match:
        total_amount = float(amount_match.group(1))
    
    # 解析 LOOKBACK_DAYS
    lookback_match = re.search(r'LOOKBACK_DAYS\s*=\s*(\d+)', content)
    if lookback_match:
        lookback_days = int(lookback_match.group(1))
    
    # 解析 SEND_EMAIL
    email_match = re.search(r'SEND_EMAIL\s*=\s*(True|False)', content)
    if email_match:
        send_email = email_match.group(1) == 'True'
    
    # 解析 EMAIL_TO
    email_to_match = re.search(r'EMAIL_TO\s*=\s*"([^"]+)"', content)
    if email_to_match:
        email_to = email_to_match.group(1)
    
    return etf_list, total_amount, lookback_days, send_email, email_to

if __name__ == "__main__":
    # 测试
    config_path = r"C:\Users\28916\.openclaw\workspace\skills\AllWeatherStrategy\config.ini"
    etf_list, amount, days, send_email, email_to = parse_config(config_path)
    
    print("ETF 列表:", etf_list)
    print("总金额:", amount)
    print("回看天数:", days)
    print("发送邮件:", send_email)
    print("邮箱地址:", email_to)
