"""将排序实验③的子问题规模完整数据转为 Excel"""
import os
import openpyxl
from sort_experiment import read_sort_data, merge_sort, quick_sort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SORT_DIR = os.path.join(BASE_DIR, "data", "sort")
RESULT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]

wb = openpyxl.Workbook()
wb.remove(wb.active)

for size in sizes:
    filepath = os.path.join(SORT_DIR, f"sort_{size:06d}.txt")
    arr = read_sort_data(filepath)

    _, _, merge_subs = merge_sort(arr)
    _, _, quick_subs = quick_sort(arr)

    # 提取子问题规模: subproblems 列表中每个元素是 (lo, hi, size)，取 size = s[2]
    merge_sizes = [s[2] for s in merge_subs]
    quick_sizes = [s[2] for s in quick_subs]

    ws = wb.create_sheet(title=f"n={size}")

    # 列标题
    ws.append(["序号", "合并排序子问题规模", "快速排序子问题规模"])

    max_len = max(len(merge_sizes), len(quick_sizes))
    for i in range(max_len):
        m_val = merge_sizes[i] if i < len(merge_sizes) else ""
        q_val = quick_sizes[i] if i < len(quick_sizes) else ""
        ws.append([i + 1, m_val, q_val])

    # 底部汇总行
    ws.append([])
    ws.append(["子问题总数", len(merge_sizes), len(quick_sizes)])
    ws.append(["最小值", min(merge_sizes), min(quick_sizes)])
    ws.append(["最大值", max(merge_sizes), max(quick_sizes)])

    # 调列宽
    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 24

    print(f"n={size:>7}: 合并排序={len(merge_sizes):>6} 个子问题, 快速排序={len(quick_sizes):>6} 个子问题")

outpath = os.path.join(RESULT_DIR, "sort_subproblem_sizes.xlsx")
wb.save(outpath)
print(f"\n已生成: {outpath}")
