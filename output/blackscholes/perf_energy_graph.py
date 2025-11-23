import os
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

APPLICATION="blackscholes"
FILEPATH="./perf"
CSVPATH="./perf/csv_energy"
DEFAULT="./perf/csv_energy/default"
PDFPATH="./graphs/energy"
APPROXIMATION = [
    "fast",
    "memo",
    "task",
    "perfo_init",
    "perfo_fini",
    "perfo_large",
    "perfo_small",
    "perfo_default",
]
THREAD = [1, 2, 4, 8]

def plot_graph(accurate, approx, approx_type, threshold = None):
    bar_width = 0.35
    x = np.arange(len(THREAD))
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.bar(x - bar_width/2, accurate, bar_width, label="accurate")
    ax.bar(x + bar_width/2, approx,  bar_width, label="approximate")
    
    ax.set_xticks(x)
    ax.set_xticklabels(["1", "2", "4", "8"], fontsize=20)
    
    ax.set_xlabel("Threads", fontsize=30)
    ax.set_ylabel("EDP (J·s)", fontsize=30)
    ax.set_title(f"Energy-Delay Product ({APPLICATION.title()} {approx_type.title()})", fontsize=35)
    
    ax.tick_params(axis='y', labelsize=20)
    ax.legend(fontsize=30, loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)
    
    file_path = ""
    if threshold is None:
        file_path = f"{APPLICATION}_{approx_type}.pdf"
    else:
        file_path = f"{APPLICATION}_{approx_type}_{threshold}.pdf"

    plt.savefig(f"{PDFPATH}/{file_path}", bbox_inches="tight")
    plt.close()


def calculate_edp(approx, threshold = None):
    array = []

    csv_path = ""
    if threshold is None:
        csv_path = f"{CSVPATH}/{approx}/{APPLICATION}_{approx}"
    else:
        csv_path = f"{CSVPATH}/{approx}/{threshold}/{APPLICATION}_{approx}"

    for t in THREAD:
        df = pd.read_csv(csv_path + str(t))
        edp = df['energy-cores'] * df['real']**2
        array.append(edp.mean())

    return pd.DataFrame(array)

default_vals = calculate_edp("default").iloc[:, 0].values

for approx in APPROXIMATION:
    if approx == "fast":
        approx_df = calculate_edp(approx)
        approx_vals = approx_df.iloc[:, 0].values
        plot_graph(default_vals, approx_vals, approx)
    else:
        for i in range(1, 6):
            if approx == "memo":
                threshold = f"threshold{i*10}"
                approx_df = calculate_edp(approx, threshold)
                approx_vals = approx_df.iloc[:, 0].values
                plot_graph(default_vals, approx_vals, approx, threshold)
            else:
                threshold = f"drop0.{i}"
                approx_df = calculate_edp(approx, threshold)
                approx_vals = approx_df.iloc[:, 0].values
                plot_graph(default_vals, approx_vals, approx, threshold)
