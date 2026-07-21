import subprocess
import time
import os
import sys
import pandas as pd

BASELINE_SERVER = "server_base.py"
OPTIMIZED_SERVER = "server.py"
RESULTS_FILE = "performance_results.csv"

def start_server_process(script_name):
    print(f"[*] Launching server process '{script_name}'...")
    # Uses sys.executable to dynamically match python3 / python executable path
    process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Wait for socket binding
    return process

def stop_server_process(process):
    print("[*] Terminating server process...")
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

def run_benchmark_stage(stage_name):
    print(f"\n==================================================")
    print(f"       EXECUTING BENCHMARK STAGE: {stage_name.upper()}")
    print(f"==================================================")
    subprocess.run([sys.executable, "benchmark.py", stage_name], check=True)

def generate_summary():
    print("\n[*] Generating comparison graphs...")
    subprocess.run([sys.executable, "plot_graphs.py"], check=True)
    
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        stages = df['stage'].unique()
        
        if len(stages) >= 2:
            base_df = df[df['stage'] == stages[0]]
            opt_df = df[df['stage'] == stages[1]]
            
            avg_lat_base = base_df['avg_latency_ms'].mean()
            avg_lat_opt = opt_df['avg_latency_ms'].mean()
            lat_imp = ((avg_lat_base - avg_lat_opt) / avg_lat_base) * 100

            avg_tp_base = base_df['throughput_msg_per_sec'].mean()
            avg_tp_opt = opt_df['throughput_msg_per_sec'].mean()
            tp_imp = ((avg_tp_opt - avg_tp_base) / avg_tp_base) * 100

            avg_cpu_base = base_df['cpu_usage_pct'].mean()
            avg_cpu_opt = opt_df['cpu_usage_pct'].mean()
            cpu_imp = ((avg_cpu_base - avg_cpu_opt) / avg_cpu_base) * 100

            print("\n==================================================")
            print("         PERFORMANCE EVALUATION SUMMARY           ")
            print("==================================================")
            print(f" * Delay / Latency Improvement : {lat_imp:+.2f}% ({avg_lat_base:.2f} ms -> {avg_lat_opt:.2f} ms)")
            print(f" * Throughput Gain             : {tp_imp:+.2f}% ({avg_tp_base:.2f} -> {avg_tp_opt:.2f} msg/sec)")
            print(f" * CPU Utilization Reduction   : {cpu_imp:+.2f}% ({avg_cpu_base:.1f}% -> {avg_cpu_opt:.1f}%)")
            print("==================================================\n")

def main():
    # Remove previous results file to start fresh
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)
        print(f"[*] Cleared old '{RESULTS_FILE}'.")

    # --- STAGE 1: BASELINE SERVER ---
    if not os.path.exists(BASELINE_SERVER):
        print(f"[-] Error: '{BASELINE_SERVER}' not found! Make sure it exists in the current directory.")
        return

    proc1 = start_server_process(BASELINE_SERVER)
    try:
        run_benchmark_stage("Baseline")
    finally:
        stop_server_process(proc1)

    time.sleep(2) # Cool down period between server runs

    # --- STAGE 2: OPTIMIZED SERVER ---
    if not os.path.exists(OPTIMIZED_SERVER):
        print(f"[-] Error: '{OPTIMIZED_SERVER}' not found!")
        return

    proc2 = start_server_process(OPTIMIZED_SERVER)
    try:
        run_benchmark_stage("Optimized")
    finally:
        stop_server_process(proc2)

    # --- STAGE 3: GRAPHS & REPORT ---
    generate_summary()

if __name__ == "__main__":
    main()