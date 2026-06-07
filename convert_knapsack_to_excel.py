"""将三个 knap_n001000_c*.txt 转为一个 Excel 文件"""
import os
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "knapsack")
RESULT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

# 三个输入文件
files = [
    ("knap_n001000_c0010000.txt",  "C=10000"),
    ("knap_n001000_c0100000.txt",  "C=100000"),
    ("knap_n001000_c1000000.txt",  "C=1000000"),
]

wb = openpyxl.Workbook()
# 删除默认 sheet
wb.remove(wb.active)

for filename, sheet_name in files:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    n, C = lines[0].strip().split()
    items = [line.strip().split() for line in lines[1:]]

    ws = wb.create_sheet(title=sheet_name)

    # 写表头信息
    ws.append(["物品数量 n", n])
    ws.append(["背包容量 C", C])
    ws.append([])  # 空行
    # 列标题
    ws.append(["物品编号", "重量 (weight)", "价值 (value)"])

    for idx, (w, v) in enumerate(items, start=1):
        ws.append([idx, float(w), float(v)])

    # 调整列宽
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 18

outpath = os.path.join(RESULT_DIR, "knapsack_n1000_data.xlsx")
wb.save(outpath)
print(f"已生成: {outpath}")
