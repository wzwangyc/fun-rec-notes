#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz

doc = fitz.open(r'C:\Users\28916\.openclaw\workspace\learning\manuscript.pdf')
page_count = len(doc)
text = ''
for page in doc:
    text += page.get_text()
doc.close()

with open(r'C:\Users\28916\.openclaw\workspace\learning\pdf_content.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'PDF 共{page_count}页')
print(f'已提取到 pdf_content.txt')
print(f'\n前 3000 字符预览：\n{text[:3000]}')
