# 算法设计与分析实验


本仓库包含《算法设计与分析》课程的实验代码、测试数据和实验结果，涵盖**排序问题**（冒泡排序、合并排序、快速排序）和**0-1 背包问题**（蛮力法、动态规划、贪心法、回溯法）两大类算法的实现与对比分析。

---

## 目录结构

```
.
├── data_generator.py               # 数据生成器（固定随机种子）
├── sort_experiment.py              # 排序实验主程序（Python）
├── knapsack_experiment.c           # 0-1 背包实验主程序（C）
├── knapsack_plot.py                # 背包结果画图脚本
├── convert_*.py                    # Excel 转换脚本
├── 算法伪代码.txt                   # 全部算法伪代码及复杂度一览
├── 实验报告.md                      # 完整实验报告
│
├── data/
│   ├── sort/                       # 排序测试数据（10 个文件）
│   └── knapsack/                   # 背包测试数据（47 个文件）
│
└── results/
    ├── sort_experiment_*.txt       # 排序实验结果
    ├── sort_comparison.png         # 排序比较次数对比图
    ├── knapsack_results.txt        # 背包实验汇总表
    ├── knapsack_detail_n1000.txt   # n=1000 详细物品选择方案
    ├── knapsack_time_comparison.png
    ├── knapsack_value_comparison.png
    ├── knapsack_scalability.png
    └── *.xlsx                      # 转换为 Excel 的数据文件
```

---

## 实验内容

### 一、排序算法实验

| 实验 | 内容 | 关键指标 |
|------|------|---------|
| 实验① | 输入数据等价类分析 | 两组 n=100 数据的比较次数对比 |
| 实验② | 不同规模下比较次数对比 | n=10~100000，7 种规模 × 3 种算法 |
| 实验③ | 递归子问题规模分析 | 合并排序 vs 快速排序的子问题规模分布 |

**涉及算法：**

| 算法 | 时间复杂度 | 稳定性 |
|------|----------|--------|
| 冒泡排序 | 最好 O(n) / 平均 O(n²) / 最坏 O(n²) | 稳定 |
| 合并排序 | Θ(n log n) | 稳定 |
| 快速排序 | 平均 O(n log n) / 最坏 O(n²) | 不稳定 |

### 二、0-1 背包问题实验

**实验④：** 在 15 种物品规模 × 3 种背包容积 = 45 组数据上对比三种算法。

| 算法 | 时间复杂度 | 是否最优 | 适用规模 |
|------|----------|---------|---------|
| 蛮力法 | O(n·2ⁿ) | 最优 | n ≤ 25 |
| 动态规划 | O(n·C) | 最优 | 大 |
| 贪心法 | O(n log n) | 近似解 | 任意 |
| 回溯法 | 最坏 O(2ⁿ) | 最优 | 小→中 |

---

## 快速开始

### 环境要求

- **Python 3.x**：`matplotlib`、`openpyxl`
- **C 编译器**：gcc / MSVC（编译 `knapsack_experiment.c`）
- **Windows**（计时使用 `QueryPerformanceCounter`）

### 安装依赖

```bash
pip install matplotlib openpyxl
```

### 第一步：生成测试数据

```bash
python data_generator.py
```

所有数据文件将生成至 `data/sort/` 和 `data/knapsack/`。随机种子固定为 `20260401`，确保数据可重现。

### 第二步：运行排序实验

```bash
python sort_experiment.py
```

输出：
- `results/sort_experiment_1.txt` — 等价类分析结果
- `results/sort_experiment_2.txt` — 规模对比结果
- `results/sort_experiment_3.txt` — 子问题规模分布
- `results/sort_comparison.png` — 比较次数对比图（线性 + 对数坐标）

### 第三步：编译并运行背包实验

```bash
# Windows / MSVC
cl knapsack_experiment.c /O2 /Fe:knapsack_experiment.exe

# 或使用 gcc
gcc knapsack_experiment.c -O2 -o knapsack_experiment.exe

# 批量模式（跑全部 45 组数据）
knapsack_experiment.exe
```

输出：
- `results/knapsack_results.txt` — 汇总结果表
- `results/knapsack_c*.txt` — 按容量分列的详细结果
- `results/knapsack_detail_n1000.txt` — n=1000 的具体物品选择方案

### 第四步：绘制背包结果图表

```bash
python knapsack_plot.py
```

输出：
- `results/knapsack_time_comparison.png` — 时间对比（6 子图）
- `results/knapsack_value_comparison.png` — 价值对比（3 子图）
- `results/knapsack_scalability.png` — 可扩展性全景（2 子图）

### 可选：导出 Excel

```bash
python convert_all_data_to_excel.py
```

将所有原始数据和实验结果转为 Excel 文件，便于在 Excel 中进一步查看和分析。

---

## 核心结果速览

### 排序算法：n=100000 时比较次数

| 算法 | 比较次数 | 与合并排序的差距 |
|------|---------|----------------|
| 冒泡排序 | ≈ 50 亿 | 慢 3254 倍 |
| 合并排序 | ≈ 154 万 | 基准 |
| 快速排序 | ≈ 210 万 | 慢 1.37 倍 |

### 0-1 背包：n=1000 时三种算法对比

| 算法 | C=10000 | C=100000 |
|------|---------|----------|
| DP | 263,098.69 (9.71 ms) | 561,622.07 (101 ms) |
| GR | 263,068.44 (0.09 ms) | 561,622.07 (0.13 ms) |
| BT | 263,098.69 (超时) | 561,622.07 (0.53 ms) |

贪心法近似解与最优解的相对误差仅约 0.01%，速度却快 100 倍以上。

---

## 数据文件格式

### 排序数据（`data/sort/sort_*.txt`）

```
<n>
<整数1>
<整数2>
...
```

### 背包数据（`data/knapsack/knap_n*_c*.txt`）

```
<n> <C>
<重量1> <价值1>
<重量2> <价值2>
...
```

---

## 实验报告

完整实验报告（含算法思想、伪代码、实验步骤、结果分析）见 [实验报告.md](实验报告.md)。

---

## 许可证

本项目仅用于课程学习与学术交流。
