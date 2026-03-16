# 📈 A 股行情日报配置说明

## ✅ 配置完成

**定时任务已创建：**
- **任务名称：** A 股行情日报 - 每个工作日
- **执行时间：** 每个工作日下午 4:00 (Asia/Singapore 时区)
- **收件邮箱：** wangreits@163.com
- **任务 ID：** 54d31a73-8de0-4dba-aafe-7e38e43ac5d8

---

## 📊 报告内容

每日 A 股行情分析报告包含：

### 1. 主要指数
- 上证指数
- 深证成指
- 创业板指
- 沪深 300

### 2. 板块涨跌
- 领涨板块前 10
- 领跌板块后 10

### 3. 资金流向
- 北向资金净流入/流出
- 主力资金流向

### 4. 市场情绪
- 上涨/下跌家数
- 涨停/跌停家数

### 5. 后市展望
- 技术面分析
- 资金面分析
- 操作建议

---

## 📁 相关文件

| 文件 | 路径 | 用途 |
|------|------|------|
| `a_share_daily_full.py` | `workspace/scripts/` | 主脚本（生成报告 + 发送邮件） |
| `a_share_daily_report.py` | `workspace/scripts/` | 简化版报告生成脚本 |

---

## 🔧 手动运行

如需手动运行（测试或补发报告）：

```bash
py C:\Users\28916\.openclaw\workspace\scripts\a_share_daily_full.py
```

---

## 📧 邮件配置

**SMTP 配置：**
- 服务器：smtp.163.com
- 端口：465 (SSL)
- 发件人：wangreits@163.com
- 收件人：wangreits@163.com

---

## ⏰ 定时任务详情

**Cron 表达式：** `0 16 * * 1-5`
- **分钟：** 0（整点）
- **小时：** 16（下午 4 点）
- **日期：** 每天
- **月份：** 每月
- **星期：** 周一到周五（工作日）

**时区：** Asia/Singapore (新加坡时间 = 北京时间)

---

## 🎯 下次运行时间

系统会自动计算下一个工作日下午 4 点执行。

---

## 💡 自定义配置

### 修改发送时间

编辑 cron 任务：
```bash
openclaw cron update 54d31a73-8de0-4dba-aafe-7e38e43ac5d8 --schedule "0 17 * * 1-5"
```
改为下午 5 点。

### 修改收件人

编辑 `a_share_daily_full.py`：
```python
RECEIVER_EMAIL = "your-email@example.com"
```

### 修改查询内容

编辑 `query_market_data()` 函数中的查询语句。

---

## 📊 使用 MX-FinSkills 查询数据

脚本已配置使用东方财富妙想 MX-FinSkills：

```python
# 查询指数
py scripts/get_data.py --query "上证指数、深证成指、创业板指、沪深 300 的收盘价、涨跌幅"

# 查询板块
py scripts/get_data.py --query "今日 A 股行业板块涨跌幅排行"

# 查询资金流向
py scripts/get_data.py --query "北向资金流向、主力资金净流入"
```

---

## ✅ 测试记录

**首次测试：** 2026-03-16 01:25
- ✅ 脚本运行成功
- ✅ 邮件发送成功
- ✅ 定时任务已启用

---

## 📞 技术支持

- **数据来源：** 东方财富妙想金融大模型
- **API Key：** em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI
- **客服：** 400-620-1818

---

**© 2026 Leo Assistant. All Rights Reserved.**
