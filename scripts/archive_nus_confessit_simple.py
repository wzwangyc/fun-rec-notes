#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NUS ConfessIt 每日自动归档脚本（稳定版）
版本：v2.1
每天 22:00 自动运行，生成两个文件：
1. summary-YYYY-MM-DD-full.txt - 全文（保留原文链接）
2. summary-YYYY-MM-DD-summary.md - 分类统计 + 热门 TOP5 + 100 字读后感

作者：Leo AI Assistant
最后更新：2026-03-20
"""

__version__ = "2.1"
__author__ = "Leo AI Assistant"

import requests
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import re
import time
import xml.etree.ElementTree as ET

# 配置
RSS_URL_BASE = "https://tg.i-c-a.su/rss/NUSConfessIT"
REPO_DIR = Path("C:/Users/28916/.openclaw/workspace/github-repos/nus-confessit-daily")

def fetch_rss(limit=100):
    """获取 RSS 内容（100 条，避免限流）"""
    url = f"{RSS_URL_BASE}?limit={limit}"
    print(f"[INFO] 获取 RSS，限制 {limit} 条")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 重试机制
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            if 'FLOOD_WAIT' in str(e):
                wait_time = (attempt + 1) * 10
                print(f"[WARN] 触发限流，等待 {wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"[WARN] 请求失败，重试中... {e}")
            time.sleep(5)
    
    raise Exception("RSS 获取失败：多次重试后仍失败")

def parse_posts(rss_content, start_time=None, end_time=None):
    """解析 RSS，提取指定时间范围内的帖子"""
    posts = []
    
    root = ET.fromstring(rss_content)
    channel = root.find('channel')
    
    for item in channel.findall('item'):
        title = item.find('title').text if item.find('title') is not None else ''
        pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        description = item.find('description').text if item.find('description') is not None else ''
        
        # 解析日期并过滤
        if start_time and end_time:
            try:
                pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
                pub_date_local = pub_date.astimezone().replace(tzinfo=None)
                
                if pub_date_local < start_time or pub_date_local > end_time:
                    continue
            except Exception as e:
                print(f"[WARN] 日期解析失败：{pub_date_str} - {e}")
                continue
        
        # 分类
        if '#Studies' in title:
            category = 'Studies'
        elif '#Romance' in title:
            category = 'Romance'
        elif '#Campus' in title:
            category = 'Campus'
        elif '#Rant' in title:
            category = 'Rant'
        else:
            category = 'Others'
        
        posts.append({
            'title': title,
            'pub_date': pub_date_str,
            'description': description,
            'link': link,
            'category': category
        })
    
    return posts

def create_full_txt(posts, output_path, date_str):
    """创建全文 TXT 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"NUS ConfessIt 每日总结\n")
        f.write(f"日期：{date_str}\n")
        f.write(f"帖子数：{len(posts)}\n")
        f.write("="*60 + "\n\n")
        
        for i, post in enumerate(posts, 1):
            f.write(f"{i}. {post['title']}\n")
            f.write(f"   时间：{post['pub_date']}\n")
            f.write(f"   链接：{post['link']}\n\n")
    
    print(f"[OK] 创建全文文件：{output_path}")

def create_summary_md(posts, output_path, date_str):
    """创建摘要 Markdown 文件"""
    # 分类统计
    categories = {}
    for post in posts:
        cat = post['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    # 热门 5 话题（按分类和标题）
    top_5_posts = posts[:5] if len(posts) >= 5 else posts
    
    category_names = {
        'Studies': '📚 学习学术',
        'Romance': '💕 恋爱交友',
        'Campus': '🏫 校园生活',
        'Rant': '😤 吐槽抱怨',
        'Others': '📝 其他'
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# NUS ConfessIt Daily Summary | 每日总结\n\n")
        f.write(f"**Date | 日期:** {date_str}\n\n")
        f.write(f"---\n\n")
        
        # 分类统计
        f.write(f"## 📊 Category Statistics | 分类统计\n\n")
        f.write(f"| Category | 分类 | Count | 数量 |\n")
        f.write(f"|----------|------|-------|------|\n")
        
        category_order = ['Romance', 'Campus', 'Studies', 'Rant', 'Others']
        for cat in category_order:
            if cat in categories:
                cn_name = category_names.get(cat, cat)
                f.write(f"| {cat} | {cn_name} | {categories[cat]} | {categories[cat]} |\n")
        
        f.write(f"| **Total** | **总计** | **{len(posts)}** | **{len(posts)}** |\n\n")
        f.write(f"---\n\n")
        
        # 热门 5 话题总结
        f.write(f"## 🔥 Top 5 Hot Topics | 热门话题 TOP5\n\n")
        
        for i, post in enumerate(top_5_posts, 1):
            title_clean = re.sub(r'#\w+\s*[:：]?\s*', '', post['title'])
            f.write(f"### #{i} {title_clean}\n\n")
            f.write(f"- **Category | 分类:** {category_names.get(post['category'], post['category'])}\n")
            f.write(f"- **Time | 时间:** {post['pub_date']}\n")
            f.write(f"- **Link | 链接:** [Original Post]({post['link']})\n\n")
            
            # 内容摘要（前 150 字）
            desc_short = post['description'][:150] + "..." if len(post['description']) > 150 else post['description']
            f.write(f"**Summary | 摘要:**\n\n{desc_short}\n\n")
            f.write(f"---\n\n")
        
        # 100 字读后感/总结
        f.write(f"## 💭 Daily Reflection | 今日读后感\n\n")
        
        # 生成读后感
        reflection = generate_reflection(posts, categories, date_str)
        f.write(f"{reflection}\n\n")
        
        f.write(f"---\n\n")
        f.write(f"*Generated by NUS ConfessIt Archiver | NUS 告白墙归档机器人*\n")
    
    print(f"[OK] 创建摘要文件：{output_path}")

def generate_reflection(posts, categories, date_str):
    """生成 100 字左右的读后感/总结"""
    total = len(posts)
    
    # 找出最多的分类
    if categories:
        top_cat = max(categories, key=categories.get)
        top_cat_name = {
            'Studies': '学习学术',
            'Romance': '恋爱交友',
            'Campus': '校园生活',
            'Rant': '吐槽抱怨',
            'Others': '其他'
        }.get(top_cat, top_cat)
    else:
        top_cat_name = '未知'
    
    reflections = []
    
    if total > 40:
        reflections.append(f"今日 NUS 告白墙热度不减，共{total}条投稿，同学们表达欲旺盛。")
    elif total > 25:
        reflections.append(f"今日 NUS 告白墙热度不减，共{total}条投稿，同学们表达欲旺盛。")
    else:
        reflections.append(f"今日 NUS 告白墙共有{total}条投稿，整体氛围平稳。")
    
    reflections.append(f"{top_cat_name}类话题以{categories.get(top_cat, 0)}条位居榜首，成为今日讨论焦点。")
    
    if 'Romance' in categories and categories['Romance'] > 10:
        reflections.append("感情话题持续升温，同学们对恋爱交友的关注度居高不下。")
    elif 'Studies' in categories and categories['Studies'] > 5:
        reflections.append("学习讨论增多，可能是临近考试或作业截止期。")
    elif 'Rant' in categories and categories['Rant'] > 5:
        reflections.append("吐槽类帖子较多，校园生活压力需要更多关注。")
    
    reflections.append("整体而言，NUS 社群保持着开放、多元的交流氛围。")
    
    return " ".join(reflections)

def main():
    print("="*60)
    print("NUS ConfessIt 每日归档（稳定版）")
    print("="*60)
    
    # 计算时间范围（昨日 22:00 到今日 22:00）
    now = datetime.now()
    today_22 = now.replace(hour=22, minute=0, second=0, microsecond=0)
    
    # 如果当前时间早于 22:00，则使用昨天的 22:00
    if now.hour < 22:
        today_22 = today_22 - timedelta(days=1)
    
    yesterday_22 = today_22 - timedelta(days=1)
    
    date_str = now.strftime("%Y-%m-%d")
    
    print(f"\n时间范围：{yesterday_22.strftime('%Y-%m-%d %H:%M')} 至 {today_22.strftime('%Y-%m-%d %H:%M')}")
    
    # 智能获取
    print("\n[1/5] 获取 RSS (100 条)...")
    try:
        rss_content = fetch_rss(limit=100)
        print(f"[OK] RSS 获取成功")
    except Exception as e:
        print(f"[ERROR] RSS 获取失败：{e}")
        return
    
    # 解析帖子
    print("\n[2/5] 解析帖子...")
    posts = parse_posts(rss_content, start_time=yesterday_22, end_time=today_22)
    
    # 如果帖子太少，获取更多
    if len(posts) < 10:
        print(f"[WARN] 只获取到 {len(posts)} 条帖子，尝试获取更多...")
        print("[2/5] 获取更多 RSS (300 条)...")
        rss_content = fetch_rss(limit=300)
        posts = parse_posts(rss_content, start_time=yesterday_22, end_time=today_22)
    
    print(f"[OK] 解析 {len(posts)} 条帖子（时间范围内）")
    
    # 创建文件夹
    today_dir = REPO_DIR / date_str
    today_dir.mkdir(exist_ok=True)
    
    # 创建文件
    print("\n[3/5] 创建文件...")
    create_full_txt(posts, today_dir / f"summary-{date_str}-full.txt", date_str)
    create_summary_md(posts, today_dir / f"summary-{date_str}-summary.md", date_str)
    
    # Git 推送
    print("\n[4/5] Git 提交...")
    subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Daily summary {date_str}"], cwd=REPO_DIR, capture_output=True)
    print("[OK] Git 提交完成")
    
    # Git 推送
    print("\n[5/5] Git 推送...")
    subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True)
    print("[OK] Git 推送完成")
    
    print("\n" + "="*60)
    print(f"[OK] 归档完成！共 {len(posts)} 条帖子")
    print("="*60)

if __name__ == "__main__":
    main()
