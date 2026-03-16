#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并两个 PDF 为一个
"""

from pypdf import PdfReader, PdfWriter

main_pdf = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_CompleteAnalysis.pdf"
swot_pdf = r"C:\Users\28916\.openclaw\workspace\reports\SWOT_Analysis_Complete.pdf"
output_pdf = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_FINAL_Complete.pdf"

# 读取主报告
reader_main = PdfReader(main_pdf)
writer = PdfWriter()

# 添加主报告所有页面
for page in reader_main.pages:
    writer.add_page(page)

# 读取 SWOT 报告
reader_swot = PdfReader(swot_pdf)

# 添加 SWOT 报告所有页面
for page in reader_swot.pages:
    writer.add_page(page)

# 写入合并后的 PDF
with open(output_pdf, 'wb') as f:
    writer.write(f)

import os
print(f"SUCCESS: Merged PDF created - {output_pdf}")
print(f"File size: {os.path.getsize(output_pdf) / 1024:.1f} KB")
print(f"Main report pages: {len(reader_main.pages)}")
print(f"SWOT report pages: {len(reader_swot.pages)}")
print(f"Total pages: {len(reader_main.pages) + len(reader_swot.pages)}")
