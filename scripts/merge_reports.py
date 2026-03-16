#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并主报告和 SWOT 报告
"""

import os
from pathlib import Path

# 读取两个 PDF 文件
main_pdf = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_CompleteAnalysis.pdf"
swot_pdf = r"C:\Users\28916\.openclaw\workspace\reports\SWOT_Analysis_Complete.pdf"
output_pdf = r"C:\Users\28916\.openclaw\workspace\reports\EastMoney_vs_Ths_FINAL.pdf"

try:
    from pypdf import PdfMerger
    
    merger = PdfMerger()
    merger.append(main_pdf)
    merger.append(swot_pdf)
    merger.write(output_pdf)
    merger.close()
    
    print(f"SUCCESS: Merged PDF created - {output_pdf}")
    print(f"File size: {os.path.getsize(output_pdf) / 1024:.1f} KB")
    
except ImportError:
    print("pypdf not installed, installing...")
    import subprocess
    subprocess.check_call(["py", "-m", "pip", "install", "pypdf", "-q"])
    
    from pypdf import PdfMerger
    merger = PdfMerger()
    merger.append(main_pdf)
    merger.append(swot_pdf)
    merger.write(output_pdf)
    merger.close()
    
    print(f"SUCCESS: Merged PDF created - {output_pdf}")
    print(f"File size: {os.path.getsize(output_pdf) / 1024:.1f} KB")
