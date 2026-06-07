"""排序问题实验 —— 冒泡排序、合并排序、快速排序"""
import os
import sys
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SORT_DIR = os.path.join(BASE_DIR, "data", "sort")
RESULT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def read_sort_data(filepath):
    """读取排序测试数据文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        n = int(f.readline().strip())
        arr = [int(line.strip()) for line in f]
    return arr


# ==================== 冒泡排序 ====================
def bubble_sort(arr):
    comparisons = 0
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a, comparisons


# ==================== 合并排序 ====================
def merge_sort(arr):
    comparisons = [0]
    subproblems = []

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort_range(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        size = hi - lo + 1
        subproblems.append((lo, hi, size))
        left_size = mid - lo + 1
        right_size = hi - mid
        subproblems.append((lo, mid, left_size))
        subproblems.append((mid + 1, hi, right_size))

        sort_range(lo, mid)
        sort_range(mid + 1, hi)
        a[lo:hi + 1] = merge(a[lo:mid + 1], a[mid + 1:hi + 1])

    a = arr.copy()
    sort_range(0, len(a) - 1)
    return a, comparisons[0], subproblems


# ==================== 快速排序 ====================
def quick_sort(arr):
    comparisons = [0]
    subproblems = []

    def partition(lo, hi):
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            comparisons[0] += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        return i + 1

    def sort_range(lo, hi):
        if lo >= hi:
            return
        size = hi - lo + 1
        subproblems.append((lo, hi, size))
        p = partition(lo, hi)
        left_size = p - lo
        right_size = hi - p
        if left_size > 0:
            subproblems.append((lo, p - 1, left_size))
        if right_size > 0:
            subproblems.append((p + 1, hi, right_size))
        sort_range(lo, p - 1)
        sort_range(p + 1, hi)

    a = arr.copy()
    sort_range(0, len(a) - 1)
    return a, comparisons[0], subproblems


# ==================== 实验①: 等价类分析 ====================
def experiment_1():
    print("=" * 60)
    print("实验①: 输入数据等价类分析 (100个数据, 两组)")
    print("=" * 60)

    results = []
    for batch in [1, 2]:
        filepath = os.path.join(SORT_DIR, f"sort_0100_batch{batch}.txt")
        arr = read_sort_data(filepath)
        print(f"\n批次{batch}数据(前10个): {arr[:10]}...")

        _, bc = bubble_sort(arr)
        _, mc, _ = merge_sort(arr)
        _, qc, _ = quick_sort(arr)

        print(f"  冒泡排序比较次数: {bc}")
        print(f"  合并排序比较次数: {mc}")
        print(f"  快速排序比较次数: {qc}")
        results.append((batch, bc, mc, qc))

    # 写入结果文件
    outpath = os.path.join(RESULT_DIR, "sort_experiment_1.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("排序实验①: 输入数据等价类分析\n")
        f.write("=" * 50 + "\n")
        for batch, bc, mc, qc in results:
            f.write(f"批次{batch}: 冒泡={bc}, 合并={mc}, 快速={qc}\n")
        f.write("\n分析: 两组不同的输入数据，虽然数据值不同，但排序算法\n")
        f.write("的比较次数主要取决于输入规模n和数据的初始有序程度，\n")
        f.write("而非具体数值——这正是输入等价类的含义。\n")
    print(f"\n结果已保存至: {outpath}")


# ==================== 实验②: 不同规模对比 ====================
def experiment_2():
    print("\n" + "=" * 60)
    print("实验②: 不同输入规模下三种排序算法比较次数对比")
    print("=" * 60)

    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    results = []

    for size in sizes:
        filepath = os.path.join(SORT_DIR, f"sort_{size:06d}.txt")
        arr = read_sort_data(filepath)

        _, bc = bubble_sort(arr)
        _, mc, _ = merge_sort(arr)
        _, qc, _ = quick_sort(arr)

        results.append((size, bc, mc, qc))
        print(f"n={size:>7}: 冒泡={bc:>12}, 合并={mc:>12}, 快速={qc:>12}")

    # 保存文本结果
    outpath = os.path.join(RESULT_DIR, "sort_experiment_2.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("排序实验②: 不同输入规模下比较次数\n")
        f.write(f"{'n':>8} {'冒泡排序':>14} {'合并排序':>14} {'快速排序':>14}\n")
        f.write("-" * 52 + "\n")
        for size, bc, mc, qc in results:
            f.write(f"{size:>8} {bc:>14} {mc:>14} {qc:>14}\n")

    # 绘制图表
    sizes_arr = np.array([r[0] for r in results])
    bubble_arr = np.array([r[1] for r in results], dtype=float)
    merge_arr = np.array([r[2] for r in results], dtype=float)
    quick_arr = np.array([r[3] for r in results], dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左图: 普通坐标
    ax = axes[0]
    ax.plot(sizes_arr, bubble_arr, "o-", label="Bubble Sort", color="red", linewidth=2)
    ax.plot(sizes_arr, merge_arr, "s-", label="Merge Sort", color="blue", linewidth=2)
    ax.plot(sizes_arr, quick_arr, "^-", label="Quick Sort", color="green", linewidth=2)
    ax.set_xlabel("Input Size n")
    ax.set_ylabel("Comparison Count")
    ax.set_title("Sorting Algorithm Comparison (Linear Scale)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 右图: 双对数坐标
    ax = axes[1]
    ax.loglog(sizes_arr, bubble_arr, "o-", label="Bubble Sort", color="red", linewidth=2)
    ax.loglog(sizes_arr, merge_arr, "s-", label="Merge Sort", color="blue", linewidth=2)
    ax.loglog(sizes_arr, quick_arr, "^-", label="Quick Sort", color="green", linewidth=2)
    ax.set_xlabel("Input Size n (log scale)")
    ax.set_ylabel("Comparison Count (log scale)")
    ax.set_title("Sorting Algorithm Comparison (Log-Log Scale)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_path = os.path.join(RESULT_DIR, "sort_comparison.png")
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)
    print(f"\n图表已保存至: {plot_path}")
    print(f"结果已保存至: {outpath}")

    return results


# ==================== 实验③: 递归子问题规模分析 ====================
def experiment_3():
    print("\n" + "=" * 60)
    print("实验③: 合并排序和快速排序子问题规模分析")
    print("=" * 60)

    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    all_merge = {}
    all_quick = {}

    for size in sizes:
        filepath = os.path.join(SORT_DIR, f"sort_{size:06d}.txt")
        arr = read_sort_data(filepath)

        _, _, merge_subs = merge_sort(arr)
        _, _, quick_subs = quick_sort(arr)

        # 统计合并排序子问题规模分布
        merge_sizes = [s[2] for s in merge_subs]
        all_merge[size] = merge_sizes

        # 统计快速排序子问题规模分布
        quick_sizes = [s[2] for s in quick_subs]
        all_quick[size] = quick_sizes

        print(f"n={size:>7}: 合并排序子问题数={len(merge_subs):>6}, 快速排序子问题数={len(quick_subs):>6}")

    # 保存详细结果
    outpath = os.path.join(RESULT_DIR, "sort_experiment_3.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("排序实验③: 递归子问题规模分析\n")
        f.write("=" * 50 + "\n\n")

        for size in sizes:
            f.write(f"\n{'='*40}\n")
            f.write(f"输入规模 n = {size}\n")
            f.write(f"{'='*40}\n")

            f.write(f"\n合并排序子问题规模分布 (共{len(all_merge[size])}个子问题):\n")
            merge_sizes_sorted = sorted(all_merge[size])
            f.write(f"  最小值: {min(merge_sizes_sorted)}, 最大值: {max(merge_sizes_sorted)}\n")
            f.write(f"  前10个: {merge_sizes_sorted[:10]}\n")
            if len(merge_sizes_sorted) > 20:
                f.write(f"  后10个: {merge_sizes_sorted[-10:]}\n")

            f.write(f"\n快速排序子问题规模分布 (共{len(all_quick[size])}个子问题):\n")
            quick_sizes_sorted = sorted(all_quick[size])
            f.write(f"  最小值: {min(quick_sizes_sorted)}, 最大值: {max(quick_sizes_sorted)}\n")
            f.write(f"  前10个: {quick_sizes_sorted[:10]}\n")
            if len(quick_sizes_sorted) > 20:
                f.write(f"  后10个: {quick_sizes_sorted[-10:]}\n")

        f.write("\n\n分析:\n")
        f.write("合并排序: 每次将问题等分为两个规模为n/2的子问题，递归树是平衡的，\n")
        f.write("子问题规模分布规律: 每个规模n产生两个n/2子问题，递归深度为log2(n)。\n\n")
        f.write("快速排序: 子问题规模取决于基准元素(pivot)的划分位置，\n")
        f.write("使用末尾元素作为pivot时，数据随机则期望平衡，最坏情况退化为冒泡排序。\n")

    print(f"\n结果已保存至: {outpath}")
    return all_merge, all_quick


if __name__ == "__main__":
    print("排序问题实验开始\n")
    t0 = time.time()

    experiment_1()
    results_2 = experiment_2()
    all_merge, all_quick = experiment_3()

    elapsed = time.time() - t0
    print(f"\n全部排序实验完成，总耗时: {elapsed:.2f} 秒")
