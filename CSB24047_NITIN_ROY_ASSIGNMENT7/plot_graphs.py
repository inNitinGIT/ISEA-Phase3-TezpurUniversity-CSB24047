import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_FILE = "performance_results.csv"
GRAPH_DIR = "graphs"

def generate_graphs():
    if not os.path.exists(RESULTS_FILE):
        print(f"[-] Cannot find '{RESULTS_FILE}'. Run benchmarks first.")
        return

    os.makedirs(GRAPH_DIR, exist_ok=True)
    df = pd.read_csv(RESULTS_FILE)

    stages = df['stage'].unique()
    if len(stages) < 2:
        print("[-] Need at least 2 stages in performance_results.csv to plot comparison graphs.")
        return

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # Visual styling configuration to handle exact overlapping data points
    style_config = {
        'Baseline':  {'color': '#e74c3c', 'linestyle': '--', 'marker': 's', 'alpha': 0.8, 'linewidth': 2.5},
        'Before':    {'color': '#e74c3c', 'linestyle': '--', 'marker': 's', 'alpha': 0.8, 'linewidth': 2.5},
        'Optimized': {'color': '#2ecc71', 'linestyle': '-',  'marker': 'o', 'alpha': 0.8, 'linewidth': 2.0},
        'After':     {'color': '#2ecc71', 'linestyle': '-',  'marker': 'o', 'alpha': 0.8, 'linewidth': 2.0}
    }

    metrics = [
        ("avg_latency_ms", "1. Delay / Latency (ms)", "Latency (ms)", "1_delay_latency_comparison.png"),
        ("throughput_msg_per_sec", "2. Throughput (msg/sec)", "Throughput (msg/sec)", "2_throughput_comparison.png"),
        ("cpu_usage_pct", "3. CPU Usage (%)", "CPU Usage (%)", "3_cpu_usage_comparison.png"),
        ("memory_usage_mb", "4. Memory Usage (MB)", "RAM (MB)", "4_memory_usage_comparison.png")
    ]

    # --- 1. Generate Individual Standalone Graphs ---
    for col, title, ylabel, filename in metrics:
        fig, ax = plt.subplots(figsize=(8, 5))
        for stage in stages:
            cfg = style_config.get(stage, {'color': 'blue', 'linestyle': '-', 'marker': 'd', 'alpha': 1.0, 'linewidth': 2})
            data = df[df['stage'] == stage]
            ax.plot(
                data['concurrent_clients'], data[col], 
                label=f"{stage}", 
                color=cfg['color'], 
                linestyle=cfg['linestyle'], 
                marker=cfg['marker'], 
                alpha=cfg['alpha'],
                linewidth=cfg['linewidth'],
                markersize=7
            )
            
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Concurrent Clients', fontweight='bold')
        ax.set_ylabel(ylabel, fontweight='bold')
        ax.legend(loc='best')
        ax.margins(y=0.15)  # Add vertical padding so flat lines aren't pinned to edge
        plt.tight_layout()
        
        save_path = os.path.join(GRAPH_DIR, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"[+] Saved graph: '{save_path}'")

    # --- 2. Generate Master 4-Panel Grid Chart ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Performance Evaluation: Baseline vs. Optimized Server', fontsize=16, fontweight='bold')

    coords = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for (col, title, ylabel, _), (r, c) in zip(metrics, coords):
        ax = axes[r, c]
        for stage in stages:
            cfg = style_config.get(stage, {'color': 'blue', 'linestyle': '-', 'marker': 'd', 'alpha': 1.0, 'linewidth': 2})
            data = df[df['stage'] == stage]
            ax.plot(
                data['concurrent_clients'], data[col], 
                label=stage, 
                color=cfg['color'], 
                linestyle=cfg['linestyle'], 
                marker=cfg['marker'], 
                alpha=cfg['alpha'],
                linewidth=cfg['linewidth'],
                markersize=6
            )
        ax.set_title(title, fontweight='bold')
        ax.set_xlabel('Concurrent Clients')
        ax.set_ylabel(ylabel)
        ax.legend(loc='best')
        ax.margins(y=0.15)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    master_path = os.path.join(GRAPH_DIR, "all_metrics_summary.png")
    plt.savefig(master_path, dpi=300)
    plt.close()
    print(f"[+] Saved master dashboard graph: '{master_path}'")

if __name__ == "__main__":
    generate_graphs()