/* 0-1背包问题实验 —— 蛮力法、动态规划法、贪心法、回溯法 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

#ifdef _WIN32
#include <windows.h>
#define MKDIR(path) CreateDirectoryA(path, NULL)
#else
#include <sys/stat.h>
#include <sys/types.h>
#define MKDIR(path) mkdir(path, 0755)
#endif

#define DP_MAX_OPS 50000000000LL  /* 跳过超过此操作量的DP */
#define BT_MAX_N   10000           /* 回溯法最大物品数(配合节点数限制使用) */
#define BT_MAX_NODES 5000000       /* 回溯法最大搜索节点数 */

typedef struct {
    int weight;
    double value;
} Item;

typedef struct {
    int *selected;      /* 记录选择的物品 */
    double total_value;
    int total_weight;
    double time_ms;
} Result;

/* 全局数据 */
Item *items;
int n, capacity;

/* 取得当前时间(毫秒) */
double get_time_ms() {
#ifdef _WIN32
    LARGE_INTEGER freq, count;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&count);
    return (double)count.QuadPart * 1000.0 / freq.QuadPart;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000.0 + ts.tv_nsec / 1000000.0;
#endif
}

/* 读取数据文件 */
int read_data(const char *filepath) {
    FILE *fp = fopen(filepath, "r");
    if (!fp) {
        printf("无法打开文件: %s\n", filepath);
        return 0;
    }
    if (fscanf(fp, "%d %d", &n, &capacity) != 2) {
        fclose(fp);
        return 0;
    }
    items = (Item *)malloc((size_t)n * sizeof(Item));
    if (!items) { fclose(fp); return 0; }
    for (int i = 0; i < n; i++) {
        fscanf(fp, "%d %lf", &items[i].weight, &items[i].value);
    }
    fclose(fp);
    return 1;
}

/* ==================== 蛮力法 ==================== */
Result knapsack_bruteforce() {
    Result res;
    res.selected = (int *)calloc((size_t)n, sizeof(int));
    res.total_value = 0;
    res.total_weight = 0;

    if (n > 26) {
        res.time_ms = -1.0;
        res.total_value = -1.0;
        return res;
    }

    double start = get_time_ms();
    long long total = 1LL << n;  /* n <= 26, safe */
    int *best = (int *)malloc((size_t)n * sizeof(int));
    double best_val = -1.0;
    int best_wt = 0;

    for (long long mask = 0; mask < total; mask++) {
        int cur_wt = 0;
        double cur_val = 0.0;
        int overflow = 0;
        for (int i = 0; i < n && !overflow; i++) {
            if (mask & (1LL << i)) {
                cur_wt += items[i].weight;
                cur_val += items[i].value;
                if (cur_wt > capacity) overflow = 1;
            }
        }
        if (!overflow && cur_val > best_val) {
            best_val = cur_val;
            best_wt = cur_wt;
            for (int i = 0; i < n; i++)
                best[i] = (mask >> i) & 1;
        }
    }

    res.time_ms = get_time_ms() - start;
    res.total_value = best_val;
    res.total_weight = best_wt;
    if (best_val >= 0)
        memcpy(res.selected, best, (size_t)n * sizeof(int));
    free(best);
    return res;
}

/* ==================== 动态规划法 ==================== */
Result knapsack_dp() {
    Result res;
    res.selected = (int *)calloc((size_t)n, sizeof(int));
    res.total_value = 0;
    res.total_weight = 0;

    long long est_ops = (long long)n * (capacity + 1);
    if (est_ops > DP_MAX_OPS) {
        res.time_ms = -1.0;
        res.total_value = -1.0;
        return res;
    }

    double start = get_time_ms();

    /* 一维DP数组 */
    double *dp = (double *)calloc((size_t)(capacity + 1), sizeof(double));
    if (!dp) {
        res.time_ms = -1.0;
        res.total_value = -1.0;
        return res;
    }

    /* trace数组用于回溯选中物品，仅当内存可承受时分配 */
    int need_trace = ((long long)n * (capacity + 1) < 200000000LL);
    char *trace = NULL;
    if (need_trace) {
        trace = (char *)calloc((size_t)n * (capacity + 1), sizeof(char));
    }

    for (int i = 0; i < n; i++) {
        int w = items[i].weight;
        double v = items[i].value;
        char *trace_row = trace ? trace + (long long)i * (capacity + 1) : NULL;
        for (int j = capacity; j >= w; j--) {
            double new_val = dp[j - w] + v;
            if (new_val > dp[j]) {
                dp[j] = new_val;
                if (trace_row) trace_row[j] = 1;
            }
        }
    }

    res.total_value = dp[capacity];

    /* 回溯找出选中物品 */
    if (trace) {
        int j = capacity;
        for (int i = n - 1; i >= 0; i--) {
            char *trace_row = trace + (long long)i * (capacity + 1);
            if (trace_row[j]) {
                res.selected[i] = 1;
                res.total_weight += items[i].weight;
                j -= items[i].weight;
                if (j < 0) break;
            }
        }
        free(trace);
    }

    free(dp);
    res.time_ms = get_time_ms() - start;
    return res;
}

/* ==================== 贪心法 ==================== */
typedef struct {
    int orig_idx;
    int weight;
    double value;
    double ratio;
} GreedyItem;

static int cmp_ratio_desc(const void *a, const void *b) {
    double ra = ((const GreedyItem *)a)->ratio;
    double rb = ((const GreedyItem *)b)->ratio;
    if (rb > ra) return 1;
    if (rb < ra) return -1;
    return 0;
}

Result knapsack_greedy() {
    Result res;
    res.selected = (int *)calloc((size_t)n, sizeof(int));
    res.total_value = 0;
    res.total_weight = 0;

    double start = get_time_ms();

    GreedyItem *gi = (GreedyItem *)malloc((size_t)n * sizeof(GreedyItem));
    for (int i = 0; i < n; i++) {
        gi[i].orig_idx = i;
        gi[i].weight = items[i].weight;
        gi[i].value = items[i].value;
        gi[i].ratio = items[i].value / items[i].weight;
    }
    qsort(gi, n, sizeof(GreedyItem), cmp_ratio_desc);

    int cur_wt = 0;
    double cur_val = 0.0;
    for (int i = 0; i < n; i++) {
        int idx = gi[i].orig_idx;
        if (cur_wt + items[idx].weight <= capacity) {
            res.selected[idx] = 1;
            cur_wt += items[idx].weight;
            cur_val += items[idx].value;
        }
    }

    res.total_weight = cur_wt;
    res.total_value = cur_val;
    res.time_ms = get_time_ms() - start;
    free(gi);
    return res;
}

/* ==================== 回溯法 ==================== */
typedef struct {
    int orig_idx;
    int weight;
    double value;
    double ratio;
} BacktrackItem;

static int cmp_bt_ratio(const void *a, const void *b) {
    double ra = ((const BacktrackItem *)a)->ratio;
    double rb = ((const BacktrackItem *)b)->ratio;
    if (rb > ra) return 1;
    if (rb < ra) return -1;
    return 0;
}

/* 分数背包上界：对bt_items[idx..n-1]计算 */
static double compute_bound(const BacktrackItem *bt_items, int idx, int n_bt,
                             int rem_cap, double cur_val) {
    for (int i = idx; i < n_bt && rem_cap > 0; i++) {
        if (bt_items[i].weight <= rem_cap) {
            cur_val += bt_items[i].value;
            rem_cap -= bt_items[i].weight;
        } else {
            cur_val += bt_items[i].value * rem_cap / bt_items[i].weight;
            break;
        }
    }
    return cur_val;
}

Result knapsack_backtrack() {
    Result res;
    res.selected = (int *)calloc((size_t)n, sizeof(int));
    res.total_value = 0;
    res.total_weight = 0;

    if (n > BT_MAX_N) {
        res.time_ms = -1.0;
        res.total_value = -1.0;
        return res;
    }

    double start = get_time_ms();

    /* 按价值密度排序 */
    BacktrackItem *bt = (BacktrackItem *)malloc((size_t)n * sizeof(BacktrackItem));
    for (int i = 0; i < n; i++) {
        bt[i].orig_idx = i;
        bt[i].weight = items[i].weight;
        bt[i].value = items[i].value;
        bt[i].ratio = items[i].value / items[i].weight;
    }
    qsort(bt, n, sizeof(BacktrackItem), cmp_bt_ratio);

    double best_val = 0.0;
    int *best_sel = (int *)calloc((size_t)n, sizeof(int));
    int *cur_sel  = (int *)calloc((size_t)n, sizeof(int));
    long long node_count = 0;

    /* 迭代栈: (index, cur_wt, cur_val, state)
       state=0: 首次进入
       state=1: 已尝试左子树(选)
       state=2: 已尝试右子树(不选), 即将弹出 */
    typedef struct { int idx, cur_wt, state; double cur_val; } Frame;
    Frame *stack = (Frame *)malloc(((size_t)n + 2) * sizeof(Frame));
    int top = 1;
    int exceeded = 0;

    stack[0].idx = 0;
    stack[0].cur_wt = 0;
    stack[0].cur_val = 0.0;
    stack[0].state = 0;

    while (top > 0 && !exceeded) {
        node_count++;
        if (node_count > BT_MAX_NODES) { exceeded = 1; break; }

        Frame *sf = &stack[top - 1];
        int i = sf->idx;

        /* 到达叶节点 */
        if (i >= n) {
            if (sf->cur_val > best_val) {
                best_val = sf->cur_val;
                memcpy(best_sel, cur_sel, (size_t)n * sizeof(int));
            }
            top--;
            continue;
        }

        double bound_val;

        switch (sf->state) {
        case 0:
            /* 尝试选当前物品（左子树） */
            if (sf->cur_wt + bt[i].weight <= capacity) {
                bound_val = compute_bound(bt, i + 1, n,
                    sf->cur_wt + bt[i].weight, sf->cur_val + bt[i].value);
                if (bound_val > best_val) {
                    cur_sel[i] = 1;
                    sf->state = 1;
                    stack[top].idx = i + 1;
                    stack[top].cur_wt = sf->cur_wt + bt[i].weight;
                    stack[top].cur_val = sf->cur_val + bt[i].value;
                    stack[top].state = 0;
                    top++;
                    continue;
                }
            }
            sf->state = 1;
            /* fall through */

        case 1:
            /* 尝试不选当前物品（右子树） */
            cur_sel[i] = 0;
            bound_val = compute_bound(bt, i + 1, n, sf->cur_wt, sf->cur_val);
            if (bound_val > best_val) {
                sf->state = 2;
                stack[top].idx = i + 1;
                stack[top].cur_wt = sf->cur_wt;
                stack[top].cur_val = sf->cur_val;
                stack[top].state = 0;
                top++;
                continue;
            }
            sf->state = 2;
            /* fall through */

        case 2:
            top--;
            break;
        }
    }

    /* 映射回原始物品 */
    res.time_ms = get_time_ms() - start;
    res.total_value = best_val;
    res.total_weight = 0;
    if (best_val > 0) {
        for (int i = 0; i < n; i++) {
            if (best_sel[i]) {
                int oi = bt[i].orig_idx;
                res.selected[oi] = 1;
                res.total_weight += bt[i].weight;
            }
        }
    }
    if (exceeded) {
        res.time_ms = -res.time_ms;  /* 负值表示超时 */
    }

    free(bt);
    free(best_sel);
    free(cur_sel);
    free(stack);
    return res;
}

/* 辅助函数 */
static void free_result(Result *res) {
    if (res && res->selected) free(res->selected);
}

static void print_selected_items(Result *res, FILE *fp) {
    int total_sel = 0;
    for (int i = 0; i < n; i++) if (res->selected[i]) total_sel++;
    int shown = 0;
    for (int i = 0; i < n && shown < 15; i++) {
        if (res->selected[i]) {
            fprintf(fp, "  物品%d: 重量=%d, 价值=%.2f\n",
                    i + 1, items[i].weight, items[i].value);
            shown++;
        }
    }
    if (total_sel > 15)
        fprintf(fp, "  ... (共选择 %d 件物品)\n", total_sel);
}

int main(int argc, char *argv[]) {
    const char *knap_dir = "data/knapsack";
    const char *result_dir = "results";

    if (argc >= 2) {
        /* 单文件测试模式 */
        if (!read_data(argv[1])) return 1;
        printf("物品数: %d, 容量: %d\n\n", n, capacity);
        Result r;

        printf("[蛮力法] "); r = knapsack_bruteforce();
        if (r.time_ms < 0) printf("跳过 (n>26)\n");
        else { printf("价值=%.2f, 时间=%.2f ms\n", r.total_value, r.time_ms);
            print_selected_items(&r, stdout); }
        free_result(&r);

        printf("[动态规划] "); r = knapsack_dp();
        if (r.time_ms < 0) printf("跳过 (操作量过大)\n");
        else { printf("价值=%.2f, 时间=%.2f ms\n", r.total_value, r.time_ms);
            print_selected_items(&r, stdout); }
        free_result(&r);

        printf("[贪心法]   "); r = knapsack_greedy();
        printf("价值=%.2f, 时间=%.2f ms\n", r.total_value, r.time_ms);
        print_selected_items(&r, stdout);
        free_result(&r);

        printf("[回溯法]   "); r = knapsack_backtrack();
        if (r.time_ms < 0) printf("跳过 (n过大)\n");
        else { printf("价值=%.2f, 时间=%.2f ms\n", r.total_value, r.time_ms);
            print_selected_items(&r, stdout); }
        free_result(&r);

        free(items);
        return 0;
    }

    /* 批量模式 */
    MKDIR(result_dir);

    int item_counts[] = {1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000,
                         9000, 10000, 20000, 40000, 80000, 160000, 320000};
    int capacities[] = {10000, 100000, 1000000};
    int num_counts = sizeof(item_counts) / sizeof(item_counts[0]);
    int num_caps = sizeof(capacities) / sizeof(capacities[0]);

    /* 汇总文件 */
    char path[256];
    sprintf(path, "%s/knapsack_results.txt", result_dir);
    FILE *sum = fopen(path, "w");
    fprintf(sum, "0-1背包问题实验结果\n");
    fprintf(sum, "算法: DP=动态规划, GR=贪心法, BT=回溯法\n");
    fprintf(sum, "%-8s %-8s %-12s %-10s %-12s %-10s %-12s %-10s\n",
            "n", "C", "DP_value", "DP_ms", "GR_value", "GR_ms", "BT_value", "BT_ms");
    fprintf(sum, "-------- -------- ------------ ---------- "
            "------------ ---------- ------------ ----------\n");

    /* 每个容量的独立文件 */
    FILE *cap_fp[3];
    for (int ci = 0; ci < num_caps; ci++) {
        sprintf(path, "%s/knapsack_c%d.txt", result_dir, capacities[ci]);
        cap_fp[ci] = fopen(path, "w");
        fprintf(cap_fp[ci], "容量C=%d\n%-8s %-12s %-10s %-12s %-10s %-12s %-10s\n",
                capacities[ci], "n", "DP_value", "DP_ms", "GR_value", "GR_ms",
                "BT_value", "BT_ms");
    }

    /* 详细文件(n=1000) */
    sprintf(path, "%s/knapsack_detail_n1000.txt", result_dir);
    FILE *det = fopen(path, "w");
    fprintf(det, "0-1背包问题 n=1000 详细结果\n\n");

    double total_time = get_time_ms();

    for (int ii = 0; ii < num_counts; ii++) {
        int cnt = item_counts[ii];
        printf("n=%-7d", cnt);

        for (int ci = 0; ci < num_caps; ci++) {
            int cap = capacities[ci];
            printf(" C=%-8d", cap);
            fflush(stdout);

            sprintf(path, "%s/knap_n%06d_c%07d.txt", knap_dir, cnt, cap);
            if (!read_data(path)) { printf(" [ERR]"); continue; }

            Result dp = knapsack_dp();
            Result gr = knapsack_greedy();
            Result bt = knapsack_backtrack();

            /* 写入汇总 */
            fprintf(sum, "%-8d %-8d %-12.2f %-10.2f %-12.2f %-10.2f %-12.2f %-10.2f\n",
                    cnt, cap,
                    dp.total_value, dp.time_ms,
                    gr.total_value, gr.time_ms,
                    bt.total_value, bt.time_ms);

            /* 写入容量文件 */
            fprintf(cap_fp[ci], "%-8d %-12.2f %-10.2f %-12.2f %-10.2f %-12.2f %-10.2f\n",
                    cnt,
                    dp.total_value, dp.time_ms,
                    gr.total_value, gr.time_ms,
                    bt.total_value, bt.time_ms);

            /* n=1000时写详细信息 */
            if (cnt == 1000) {
                fprintf(det, "\n========== C=%d ==========\n", cap);
                fprintf(det, "[DP] 价值=%.2f, 时间=%.2f ms\n", dp.total_value, dp.time_ms);
                print_selected_items(&dp, det);
                fprintf(det, "[GR] 价值=%.2f, 时间=%.2f ms\n", gr.total_value, gr.time_ms);
                print_selected_items(&gr, det);
                fprintf(det, "[BT] 价值=%.2f, 时间=%.2f ms\n", bt.total_value, bt.time_ms);
                print_selected_items(&bt, det);
            }

            free_result(&dp);
            free_result(&gr);
            free_result(&bt);
            free(items);

            printf(" ✓");
            fflush(stdout);
        }
        fprintf(sum, "\n");
        fflush(sum);
        printf("\n");
    }

    total_time = get_time_ms() - total_time;
    fprintf(sum, "\n总耗时: %.2f 秒\n", total_time / 1000.0);
    fclose(sum);
    for (int ci = 0; ci < num_caps; ci++) fclose(cap_fp[ci]);
    fclose(det);

    printf("\n全部完成! 总耗时: %.2f 秒\n", total_time / 1000.0);
    return 0;
}
