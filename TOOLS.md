# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Email (NetEase 163)

- **Address:** `wangreits@163.com`
- **IMAP:** `imap.163.com:993` (SSL)
- **SMTP:** `smtp.163.com:465` (SSL)
- **Auth:** Authorization code (stored in `.env`, masked: `VWTc...DvyA`)
- **Note:** IMAP/SMTP 使用同一授权码

> ⚠️ 敏感信息存于 `.env` 文件，不提交到 git

---

## 金融数据源（优先级排序）

### 1️⃣ 东方财富 MX_MacroData（宏观数据首选）
- **API Key:** `em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI` (存于各脚本)
- **位置:** `skills/MX_MacroData/`
- **适用:** GDP/CPI/PMI 等宏观数据
- **输出:** CSV + TXT

### 2️⃣ akshare（A 股/中国数据）
- **版本:** 1.18.39
- **适用:** A 股历史数据、中国宏观指标
- **优势:** 完全免费，无需 API Key

### 3️⃣ yfinance（美股/ETF）
- **版本:** 1.2.0
- **适用:** 美股/ETF/债券利率
- **注意:** 不支持宏观数据

### 4️⃣ Trading Economics（快速验证）
- **网址:** https://tradingeconomics.com/
- **适用:** 网页快速查阅

---

## 数据获取优先级原则

1. **宏观数据** → 东方财富 MX_MacroData
2. **A 股数据** → akshare
3. **美股数据** → yfinance
4. **快速验证** → Trading Economics
5. **批量存档** → 东方财富 (CSV 输出)

详见：`memory/2026-03-16.md` 和 `reports/macro_data_source_comparison.md`
