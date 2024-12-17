# coding=utf-8
'''Figure 14'''

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'

one_core_latency = [
    # low medium high
    [33.879, 30.602, 25.681], # baseline
    [31.774, 29.411, 25.934], # SW-PF
    [40.302, 36.138, 30.085], # DP-HT
    [30.351, 16.883, 18.784], # MP-HT
    [25.882, 16.858, 21.231] # Integrated
]

one_core_throughput = [
    # low medium high
    [1889.070, 2091.394, 2492.162], # baseline
    [2014.251, 2176.080, 2467.845], # SW-PF
    [3175.986, 3541.985, 4254.542], # DP-HT
    [2108.688, 3790.838, 3407.133], # MP-HT
    [2472.728, 3796.399, 3014.407] # Integrated
]

multi_core_latency = [
    # low medium high
    [37.809, 32.143, 27.643], # baseline
    [38.485, 30.142, 24.808], # SW-PF
    [71.859, 54.812, 44.451], # DP-HT
    [32.928, 21.807, 22.266], # MP-HT
    [31.741, 21.741, 21.194] # Integrated
]

multi_core_throughput = [
    # low medium high
    [40624.984, 47786.940, 55565.237], # baseline
    [39911.887, 50958.692, 61915.986], # SW-PF
    [42750.286, 56046.246, 69109.604], # DP-HT
    [46647.299, 70436.526, 68984.643], # MP-HT
    [48391.759, 70651.247, 72473.204] # Integrated
]

def draw(data, fig_name, second_xlabel_distance=-0.25, type='latency'):
    datasets = ['低热度', '中热度', '高热度']
    algorithms = ['SW-PF', 'DP-HT', 'MP-HT', 'Integrated']
    one_core, multi_core = data
    # Baseline data
    one_core_baseline = one_core[0]
    multicore_baseline = multi_core[0]

    # Data for other algorithms
    one_core_data = one_core[1:]
    multicore_data = multi_core[1:]

    # Calculate speedup factors
    speedups = []
    for alg_data in one_core_data:
        if type == 'latency':
            speedup = [one_core_baseline[i] / alg_data[i] for i in range(len(one_core_baseline))]
        else:
            speedup = [alg_data[i] / one_core_baseline[i] for i in range(len(one_core_baseline))]
        speedups.append(speedup)

    multicore_speedups = []
    for alg_data in multicore_data:
        if type == 'latency':
            speedup = [multicore_baseline[i] / alg_data[i] for i in range(len(multicore_baseline))]
        else:
            speedup = [alg_data[i] / multicore_baseline[i]  for i in range(len(multicore_baseline))]
        multicore_speedups.append(speedup)

    # Set colors for each algorithm
    colors = ['#5494CE', '#FF8283', '#0D898A', '#F9CC52']

    # Plotting
    x = np.arange(len(datasets))
    width = 0.2

    bars = []

    _, ax = plt.subplots()
    for i, alg_speedup in enumerate(speedups):
        bar = ax.bar(x + i * width, alg_speedup, width, label=algorithms[i], 
            color=colors[i], 
            edgecolor='#363636',
            linewidth=1.5)
        bars.append(bar)
        for j in x:
            ax.text(j + i * width, alg_speedup[j] + 0.02, 
                    str('%.2f' % alg_speedup[j]), 
                    ha='center', va='bottom', 
                    fontsize=5, fontweight='bold')
        
    x = x + len(datasets)
    for i, alg_speedup in enumerate(multicore_speedups):
        ax.bar(x + i * width, alg_speedup, width, label=algorithms[i], 
            color=colors[i], 
            edgecolor='#363636',
            linewidth=1.5)
        for j in x:
            ax.text(j + i * width, alg_speedup[j - len(datasets)] + 0.02, 
                    str('%.2f' % alg_speedup[j - len(datasets)]), 
                    ha='center', va='bottom', 
                    fontsize=5, fontweight='bold')
        
    ax.set_ylabel('相对基线的提升', fontsize=12)
    x = np.arange(len(datasets)*2)
    ax.set_xticks(x + width * 1.5)
    datasets.extend(datasets)
    ax.set_xticklabels(datasets, fontsize=12)

    plt.text(1 + width * 1.5, second_xlabel_distance, '1C', ha='center', va='center', fontsize=12, transform=ax.transData)
    plt.text(4 + width * 1.5, second_xlabel_distance, '24C', ha='center', va='center', fontsize=12, transform=ax.transData)

    x_min, x_max = ax.get_xlim()
    ax.axvline(x=(x_max - x_min) / 2 - width * 2, color='k', linestyle='--')  # 中间线

    # 图例设置
    ax.legend(handles=bars, 
              labels=algorithms, 
              loc='lower center', 
              ncol=len(algorithms), 
              bbox_to_anchor=(0.5, -0.25),
              fontsize=12)

    plt.subplots_adjust(bottom=0.2)
    plt.tight_layout()
    plt.savefig(fig_name)


if __name__ == '__main__':
    draw((one_core_latency, multi_core_latency), 'draw_latency.pdf')
    draw((one_core_throughput, multi_core_throughput), 'draw_throughput.pdf', type='throughput')