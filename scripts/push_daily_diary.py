#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Diary Push Script

自动将日记推送到 GitHub 私有仓库 lobster-diary

用法:
    python push_daily_diary.py [日期]
    python push_daily_diary.py 2026-04-02
    python push_daily_diary.py  # 默认使用昨天日期
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def get_yesterday_date():
    """获取昨天的日期"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_diary_content(date_str):
    """读取日记内容"""
    diary_file = Path(__file__).parent.parent / f"diary_{date_str}.md"
    
    if not diary_file.exists():
        print(f"[ERROR] 日记文件不存在：{diary_file}")
        return None
    
    with open(diary_file, 'r', encoding='utf-8') as f:
        return f.read()


def clone_or_pull_repo(repo_path):
    """克隆或拉取仓库"""
    repo_url = "https://github.com/wzwangyc/lobster-diary.git"
    
    if repo_path.exists():
        print(f"[INFO] 仓库已存在，拉取最新代码...")
        os.chdir(repo_path)
        subprocess.run(['git', 'pull'], check=True, capture_output=True)
    else:
        print(f"[INFO] 克隆仓库...")
        parent_dir = repo_path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', repo_url], cwd=parent_dir, check=True, capture_output=True)
    
    return True


def commit_and_push(repo_path, date_str, content):
    """提交并推送日记"""
    diary_file = repo_path / f"{date_str}.md"
    
    # 写入日记内容
    with open(diary_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[INFO] 日记已写入：{diary_file}")
    
    # Git 操作
    os.chdir(repo_path)
    
    try:
        # 添加文件
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        print(f"[INFO] 文件已添加到暂存区")
        
        # 提交
        commit_msg = f"Add diary for {date_str}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
        print(f"[INFO] 已提交：{commit_msg}")
        
        # 推送
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print(f"[INFO] 已推送到 GitHub")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git 操作失败：{e}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("Daily Diary Push")
    print("="*60)
    
    # 获取日期
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = get_yesterday_date()
    
    print(f"\n[INFO] 日期：{date_str}")
    
    # 读取日记内容
    diary_content = get_diary_content(date_str)
    if diary_content is None:
        print(f"[ERROR] 无法读取日记内容")
        return False
    
    print(f"[INFO] 日记内容长度：{len(diary_content)} 字符")
    
    # 克隆或拉取仓库
    workspace = Path(__file__).parent.parent
    repo_path = workspace.parent / "lobster-diary"
    
    if not clone_or_pull_repo(repo_path):
        print(f"[ERROR] 无法克隆/拉取仓库")
        return False
    
    # 提交并推送
    if commit_and_push(repo_path, date_str, diary_content):
        print("\n" + "="*60)
        print("[SUCCESS] 日记已成功推送到 GitHub!")
        print("="*60)
        print(f"\n查看：https://github.com/wzwangyc/lobster-diary")
        return True
    else:
        print("\n" + "="*60)
        print("[FAILED] 推送失败")
        print("="*60)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
