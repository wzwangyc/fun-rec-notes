# 东方财富 MX-FinSkills 部署完成 ✅

**部署时间：** 2026-03-14  
**API Key：** 已配置（em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI）  
**测试状态：** ✅ MX_FinData 测试成功

---

## 📦 技能清单

| 技能名称 | 功能 | 输出格式 | 测试状态 |
|---------|------|---------|---------|
| **MX_FinData** | 金融数据查询（股票/债券/基金/指数等） | Excel + TXT | ✅ 已通过 |
| **MX_FinSearch** | 金融资讯搜索（新闻/公告/研报） | TXT | ⏳ 待测试 |
| **MX_MacroData** | 宏观经济数据（GDP/CPI/PMI 等） | CSV + TXT | ⏳ 待测试 |
| **MX_StockPick** | 选股/选板块/选基金 | CSV + TXT | ⏳ 待测试 |

---

## 📁 文件位置

```
C:\Users\28916\.openclaw\workspace\skills\
├── MX_FinData/          # 金融数据查询
├── MX_FinSearch/        # 金融资讯搜索
├── MX_MacroData/        # 宏观经济数据
├── MX_StockPick/        # 选股/选板块/选基金
└── MX-FinSkills-README.md  # 本说明文档
```

---

## 🔧 配置信息

### API Key 配置方式

**已配置到每个脚本中**，同时也创建了 `.env` 文件：

```bash
# 方式 1：环境变量（推荐）
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"

# 方式 2：脚本内已硬编码（已配置）
EM_API_KEY = "em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
```

### Python 依赖

已安装：
- ✅ httpx (HTTP 客户端)
- ✅ pandas (数据处理)
- ✅ openpyxl (Excel 读写)

---

## 🚀 使用方法

### 1️⃣ MX_FinData - 金融数据查询

**查询个股基本面：**
```bash
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
py scripts/get_data.py --query "东方财富的基本面"
```

**查询实时行情：**
```bash
py scripts/get_data.py --query "当前 300059 的实时买单"
```

**查询多实体对比：**
```bash
py scripts/get_data.py --query "东方财富、拼多多最近一年的营收、毛利、净利"
```

**输出：**
- `workspace/MX_FinData/MX_FinData_<id>.xlsx` - Excel 数据表
- `workspace/MX_FinData/MX_FinData_<id>_description.txt` - 说明文件

---

### 2️⃣ MX_FinSearch - 金融资讯搜索

**搜索个股资讯：**
```bash
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
cd skills/MX_FinSearch
py -m scripts.get_data "寒武纪 688256 最新研报与公告"
```

**搜索板块新闻：**
```bash
py -m scripts.get_data "商业航天板块近期新闻"
```

**输出：**
- `financial_search/<query>.txt` - 资讯正文

---

### 3️⃣ MX_MacroData - 宏观经济数据

**查询 GDP 数据：**
```bash
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
cd skills/MX_MacroData
py -m scripts.get_data "中国近五年 GDP"
```

**查询商品价格：**
```bash
py -m scripts.get_data "氧化镨钕、铜、铝的现货价格走势"
```

**⚠️ 注意：** 必须使用明确的实体名称，不能使用模糊表述
- ❌ `"查询华东地区 GDP"`
- ✅ `"查询上海市、江苏省、浙江省的 GDP 数据"`

**输出：**
- `workspace/macro_data/macro_data_<query>_<frequency>.csv`
- `workspace/macro_data/macro_data_<query>_description.txt`

---

### 4️⃣ MX_StockPick - 选股/选板块/选基金

**选股：**
```bash
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
cd skills/MX_StockPick
py -m scripts.get_data --query "股价大于 100 元的股票" --select-type "A 股"
```

**选板块：**
```bash
py -m scripts.get_data --query "今天涨幅最大板块" --select-type "板块"
```

**选基金：**
```bash
py -m scripts.get_data --query "白酒主题基金近一年收益排名" --select-type "基金"
```

**输出：**
- `workspace/MX_StockPick/MX_StockPick_<query>.csv`
- `workspace/MX_StockPick/MX_StockPick_<query>_description.txt`

---

## ✅ 测试记录

### MX_FinData 测试（2026-03-14 19:40）

**查询：** "东方财富的基本面"

**结果：**
```
✅ 文件：workspace\MX_FinData\MX_FinData_5a368dfc.xlsx
✅ 描述：workspace\MX_FinData\MX_FinData_5a368dfc_description.txt
✅ 行数：22
✅ 表数量：3
✅ Sheet 列表：
   - 东方财富 (300059.SZ) 的市盈率 PE(TTM)、市净率 P
   - 东方财富 (300059.SZ) 当前的市净率、市销率 TTM 等
   - 东方财富 (300059.SZ) 的营业总收入、归属于母公司股东的
```

---

## 🎯 快速调用示例

### 在 OpenClaw 中使用

可以直接对我说：

```
"用 MX_FinData 查询贵州茅台的基本面"
"用 MX_FinSearch 搜索宁德时代最新研报"
"用 MX_MacroData 查询中国 CPI 数据"
"用 MX_StockPick 筛选股价大于 100 元的 A 股"
```

我会自动执行对应的脚本并返回结果！

---

## 📞 支持信息

**东方财富妙想Claw 官网：** https://ai.eastmoney.com/chat  
**客服电话：** 400-620-1818  
**API Key 申请：** https://ai.eastmoney.com/mxClaw

---

## 🐛 常见问题

### Q1: 提示 "EM_API_KEY is not set"
**解决：** 确保已设置环境变量
```bash
$env:EM_API_KEY="em_3flFbHCB73Vlfu6gZfe1jVtD3upCKkaI"
```

### Q2: 查询超时或无结果
**可能原因：**
- API Key 无效或过期
- 网络问题
- 查询语句不清晰

**解决：** 检查 API Key，简化查询语句重试

### Q3: 输出文件在哪里？
**位置：** 每个技能的 `workspace/` 子目录下
```
skills/MX_FinData/workspace/MX_FinData/
skills/MX_FinSearch/workspace/financial_search/
skills/MX_MacroData/workspace/macro_data/
skills/MX_StockPick/workspace/MX_StockPick/
```

---

**部署完成！** 🦁
