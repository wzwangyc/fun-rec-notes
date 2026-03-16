#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日日记生成并推送到 GitHub 私有仓库 (lobster-diary)
使用 gh CLI api 直接创建文件
"""

import subprocess
import base64
from datetime import datetime
import sys

# 配置
GITHUB_REPO = "wzwangyc/lobster-diary"

def generate_diary():
    """生成今日日记内容"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    weekday = today.strftime("%A")
    time_str = today.strftime("%Y-%m-%d %H:%M")
    
    content = f"""# 📅 每日日记 - {date_str}

**日期：** {date_str} ({weekday})  
**记录时间：** {time_str}

---

## 🎓 学习进展

<!-- 记录今天学习的内容、课程、书籍等 -->

## 🛠️ 工作/项目

<!-- 记录完成的工作、项目进展等 -->

## 💡 想法/洞察

<!-- 记录今天的思考、灵感、心得 -->

## 📝 明日计划

<!-- 记录明天的计划和目标 -->

## 📊 今日状态

- **心情：** 
- **精力：** ⭐⭐⭐⭐⭐
- **专注度：** ⭐⭐⭐⭐⭐

---

> 🦞 龙虾日记 | 自动记录于 {time_str}
"""
    return date_str, content, weekday

def push_to_github(date_str, content, weekday):
    """使用 gh CLI 创建文件"""
    try:
        # Base64 编码内容
        content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        commit_msg = f"Add daily diary: {date_str} ({weekday})"
        
        # 使用 gh api 创建文件
        result = subprocess.run(
            ["gh", "api",
             "--method", "PUT",
             f"/repos/{GITHUB_REPO}/contents/{date_str}.md",
             "-H", "Accept: application/vnd.github.v3+json",
             "-f", f"message={commit_msg}",
             "-f", f"content={content_b64}",
             "-f", "branch=main"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"[SUCCESS] Pushed {date_str}.md to {GITHUB_REPO}")
            print(f"[URL] https://github.com/{GITHUB_REPO}/blob/main/{date_str}.md")
            return True
        else:
            print(f"[ERROR] {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Request timeout")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("[LOBSTER] Starting daily diary process...")
    
    # 1. 生成日记
    date_str, content, weekday = generate_diary()
    print(f"[DIARY] Generated diary for {date_str} ({weekday})")
    
    # 2. 推送到 GitHub
    success = push_to_github(date_str, content, weekday)
    
    if success:
        print("[SUCCESS] Daily diary completed!")
        return True
    else:
        print("[ERROR] Failed to push diary")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
