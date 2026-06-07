"""0-1背包实验结果绘图"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(BASE_DIR, "results")

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def parse_results(filepath):
    """解析结果文件.
    格式: n dp_val dp_ms gr_val gr_ms bt_val bt_ms  (共7列)"""
    n_list = []
    data = {"DP_val": [], "DP_ms": [], "GR_val": [], "GR_ms": [],
            "BT_val": [], "BT_ms": []}
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[2:]:  # 跳过标题行和表头行
        parts = line.strip().split()
        if len(parts) < 7:
            continue
        try:
            n_list.append(int(parts[0]))
            data["DP_val"].append(float(parts[1]))
            data["DP_ms"].append(float(parts[2]))
            data["GR_val"].append(float(parts[3]))
            data["GR_ms"].append(float(parts[4]))
            data["BT_val"].append(float(parts[5]))
            data["BT_ms"].append(float(parts[6]))
        except ValueError:
            continue
    return n_list, data


def filter_valid(n_list, y_list, allow_negative_time=False):
    """过滤有效数据对.
    allow_negative_time=True时负时间视为有效（表示超时），取其绝对值."""
    result_n, result_y = [], []
    for n, y in zip(n_list, y_list):
        if y == -1.0:
            continue
        if y < 0 and not allow_negative_time:
            continue
        result_n.append(n)
        result_y.append(abs(y) if allow_negative_time and y < 0 else y)
    return result_n, result_y


def plot_knapsack():
    capacities = [10000, 100000, 1000000]
    cap_labels = ["C=10,000", "C=100,000", "C=1,000,000"]

    colors = {"DP": "#2196F3", "GR": "#4CAF50", "BT": "#F44336"}
    markers = {"DP": "o", "GR": "s", "BT": "^"}
    linestyles = {"DP": "-", "GR": "--", "BT": "-."}
    algs = ["DP", "GR", "BT"]

    # ============ 图1: 时间对比 (6个子图) ============
    fig1, axes1 = plt.subplots(3, 2, figsize=(14, 18))
    fig1.suptitle("0-1 Knapsack Problem — Algorithm Time Comparison",
                  fontsize=14, fontweight="bold", y=0.98)

    for ci, cap in enumerate(capacities):
        filepath = os.path.join(RESULT_DIR, f"knapsack_c{cap}.txt")
        if not os.path.exists(filepath):
            continue
        n_list, data = parse_results(filepath)

        # 左列: 线性坐标
        ax = axes1[ci, 0]
        for alg in algs:
            nn, tt = filter_valid(n_list, data[f"{alg}_ms"], allow_negative_time=True)
            if nn:
                ax.plot(nn, tt, color=colors[alg], marker=markers[alg],
                        linestyle=linestyles[alg], label=alg, linewidth=1.8,
                        markersize=6)
        ax.set_xlabel("Number of Items (n)")
        ax.set_ylabel("Time (ms)")
        ax.set_title(f"Time Comparison — {cap_labels[ci]}")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)

        # 右列: log-log坐标
        ax = axes1[ci, 1]
        for alg in algs:
            nn, tt = filter_valid(n_list, data[f"{alg}_ms"], allow_negative_time=True)
            if nn:
                tt_pos = [max(t, 0.01) for t in tt]
                ax.loglog(nn, tt_pos, color=colors[alg], marker=markers[alg],
                          linestyle=linestyles[alg], label=alg, linewidth=1.8,
                          markersize=6)
        ax.set_xlabel("n (log scale)")
        ax.set_ylabel("Time ms (log scale)")
        ax.set_title(f"Time (Log-Log) — {cap_labels[ci]}")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path1 = os.path.join(RESULT_DIR, "knapsack_time_comparison.png")
    fig1.savefig(path1, dpi=150)
    plt.close(fig1)
    print(f"[OK] {path1}")

    # ============ 图2: 价值对比 ============
    fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5))
    fig2.suptitle("0-1 Knapsack — Total Value vs. n",
                  fontsize=13, fontweight="bold")

    for ci, cap in enumerate(capacities):
        filepath = os.path.join(RESULT_DIR, f"knapsack_c{cap}.txt")
        if not os.path.exists(filepath):
            continue
        n_list, data = parse_results(filepath)

        ax = axes2[ci]
        for alg in algs:
            nn, vv = filter_valid(n_list, data[f"{alg}_val"])
            if nn:
                ax.plot(nn, vv, color=colors[alg], marker=markers[alg],
                        linestyle=linestyles[alg], label=alg, linewidth=1.8,
                        markersize=6)
        ax.set_xlabel("Number of Items (n)")
        ax.set_ylabel("Total Value")
        ax.set_title(f"{cap_labels[ci]}")
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path2 = os.path.join(RESULT_DIR, "knapsack_value_comparison.png")
    fig2.savefig(path2, dpi=150)
    plt.close(fig2)
    print(f"[OK] {path2}")

    # ============ 图3: 算法可扩展性全景 ============
    fig3, axes3 = plt.subplots(1, 2, figsize=(14, 6))
    fig3.suptitle("0-1 Knapsack — Scalability Overview (All Capacities)",
                  fontsize=13, fontweight="bold")

    all_n = []
    all_dp_t, all_gr_t, all_bt_t = [], [], []

    for ci, cap in enumerate(capacities):
        filepath = os.path.join(RESULT_DIR, f"knapsack_c{cap}.txt")
        if not os.path.exists(filepath):
            continue
        n_list, data = parse_results(filepath)

        nn_dp, tt_dp = filter_valid(n_list, data["DP_ms"], allow_negative_time=True)
        nn_gr, tt_gr = filter_valid(n_list, data["GR_ms"], allow_negative_time=True)
        nn_bt, tt_bt = filter_valid(n_list, data["BT_ms"], allow_negative_time=True)

        if nn_dp:
            label_dp = f"DP C={cap}"
            axes3[0].plot(nn_dp, tt_dp, "o-", color=colors["DP"],
                          alpha=0.5 + 0.25 * ci, linewidth=1.5, markersize=5,
                          label=label_dp)
            axes3[1].loglog(nn_dp, [max(t, 0.01) for t in tt_dp], "o-",
                            color=colors["DP"], alpha=0.5 + 0.25 * ci,
                            linewidth=1.5, markersize=5, label=label_dp)
        if nn_gr:
            label_gr = f"Greedy C={cap}"
            axes3[0].plot(nn_gr, tt_gr, "s--", color=colors["GR"],
                          alpha=0.5 + 0.25 * ci, linewidth=1.5, markersize=5,
                          label=label_gr)
        if nn_bt:
            label_bt = f"BT C={cap}"
            axes3[0].plot(nn_bt, tt_bt, "^:", color=colors["BT"],
                          alpha=0.5 + 0.25 * ci, linewidth=1.5, markersize=5,
                          label=label_bt)

    axes3[0].set_xlabel("Number of Items (n)")
    axes3[0].set_ylabel("Time (ms)")
    axes3[0].set_title("Time Comparison (Linear Scale)")
    axes3[0].legend(loc="upper left", fontsize=8)
    axes3[0].grid(True, alpha=0.3)

    for ci, cap in enumerate(capacities):
        filepath = os.path.join(RESULT_DIR, f"knapsack_c{cap}.txt")
        if not os.path.exists(filepath):
            continue
        n_list, data = parse_results(filepath)
        nn_dp, tt_dp = filter_valid(n_list, data["DP_ms"], allow_negative_time=True)
        if nn_dp:
            axes3[1].loglog(nn_dp, [max(t, 0.01) for t in tt_dp], "o-",
                            color=colors["DP"], alpha=0.5 + 0.25 * ci,
                            linewidth=1.5, markersize=5, label=f"DP C={cap}")

    axes3[1].set_xlabel("n (log scale)")
    axes3[1].set_ylabel("Time ms (log scale)")
    axes3[1].set_title("DP Time Scaling (Log-Log)")
    axes3[1].legend(loc="upper left", fontsize=8)
    axes3[1].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path3 = os.path.join(RESULT_DIR, "knapsack_scalability.png")
    fig3.savefig(path3, dpi=150)
    plt.close(fig3)
    print(f"[OK] {path3}")


if __name__ == "__main__":
    print("Generating 0-1 knapsack charts...")
    plot_knapsack()
    print("Done!")
