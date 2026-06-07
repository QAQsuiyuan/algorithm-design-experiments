"""生成所有测试数据文件"""
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SORT_DIR = os.path.join(BASE_DIR, "data", "sort")
KNAP_DIR = os.path.join(BASE_DIR, "data", "knapsack")

random.seed(20260401)


def generate_sort_data():
    os.makedirs(SORT_DIR, exist_ok=True)
    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    for size in sizes:
        nums = [random.randint(0, 100000) for _ in range(size)]
        filepath = os.path.join(SORT_DIR, f"sort_{size:06d}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{size}\n")
            for num in nums:
                f.write(f"{num}\n")
        print(f"生成排序数据: {filepath} ({size} 个数)")

    # 额外生成两组100个数据用于对比等价类分析
    for batch in [1, 2]:
        nums = [random.randint(0, 100000) for _ in range(100)]
        filepath = os.path.join(SORT_DIR, f"sort_0100_batch{batch}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"100\n")
            for num in nums:
                f.write(f"{num}\n")
        print(f"生成排序数据(等价类): {filepath}")


def generate_knapsack_data():
    os.makedirs(KNAP_DIR, exist_ok=True)
    item_counts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                   10000, 20000, 40000, 80000, 160000, 320000]
    capacities = [10000, 100000, 1000000]

    for count in item_counts:
        # 预生成所有物品
        weights = [random.randint(1, 100) for _ in range(count)]
        values = [round(random.uniform(100, 1000), 2) for _ in range(count)]
        for cap in capacities:
            filename = f"knap_n{count:06d}_c{cap:07d}.txt"
            filepath = os.path.join(KNAP_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"{count} {cap}\n")
                for w, v in zip(weights, values):
                    f.write(f"{w} {v:.2f}\n")
            print(f"生成背包数据: {filepath} (n={count}, C={cap})")


if __name__ == "__main__":
    print("=" * 50)
    print("生成排序测试数据...")
    print("=" * 50)
    generate_sort_data()
    print()
    print("=" * 50)
    print("生成0-1背包测试数据...")
    print("=" * 50)
    generate_knapsack_data()
    print()
    print("所有数据生成完毕!")
