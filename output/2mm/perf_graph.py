import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FILEPATH="./perf/"
CSVPATH="./perf/csv/"
DEFAULT="./perf/csv/default/2mm_default1"
PDFPATH="./graphs/perf/"
APPROXIMATION = [
    # "default",
    "fast",
    "memo",
    "task",
    "perfo_init",
    "perfo_fini",
    "perfo_large",
    "perfo_small",
    "perfo_default",
]

def plot_graph(default_results, results, title, approx, threshold=None):
    threads = [1, 2, 4, 8]

    plt.figure(figsize=(12, 8))

    plt.plot(threads, default_results, label='accurate', color='blue', marker='o', linewidth=3, markersize=30)
    plt.plot(threads, results, label='approximate', color='orange', marker='^', linewidth=3, markersize=30)

    plt.title(f'2MM Speedup {title}', fontsize=35)
    plt.xlabel('Threads', fontsize=32)
    plt.ylabel('Speedup', fontsize=32)
    plt.grid(True)
    plt.legend(fontsize=34)

    plt.xticks(threads, fontsize=30)
    plt.yticks(fontsize=30)

    plt.tight_layout()
    if threshold == None:
        plt.savefig(PDFPATH + "2mm_" + approx + '.pdf')
    else:
        plt.savefig(PDFPATH + "2mm_" + approx + "_" + threshold + '.pdf')
    
    plt.close()


def calculate_speedup(dirpath, approx, thread):
    default_df = pd.read_csv(DEFAULT)

    results = []
    for file in sorted(os.listdir(dirpath)):
        if (approx + thread) in file:
            approx_df = pd.read_csv(dirpath + "/" + file)
            for value in approx_df['real']:
                results.append(default_df['real'] / value)

    df = pd.concat(results, ignore_index=True)
    return df.mean()


default_results = []
for thread in [1, 2, 4, 8]:
    dirpath = CSVPATH + "default"
    default_results.append(calculate_speedup(dirpath, "default", str(thread)))


for approx in APPROXIMATION:
    threshold = None
    results = []

    if approx == "fast":
        for thread in [1, 2, 4, 8]:
            dirpath = CSVPATH + approx
            results.append(calculate_speedup(dirpath, approx, str(thread)))
        
        plot_graph(default_results, results, approx.title(), approx)
        results = []
    else:
        for i in range(1, 6):
            if approx == "memo":
                for thread in [1, 2, 4, 8]:
                    dirpath = CSVPATH + approx + "/threshold" + str(i * 10)
                    results.append(calculate_speedup(dirpath, approx, str(thread)))

                graph_title = approx.title() + " Threshold " + str(i * 10)
                plot_graph(default_results, results, graph_title, approx, "threshold" + str(i * 10))
                results = []
            else:
                for thread in [1, 2, 4, 8]:
                    dirpath = CSVPATH + approx + "/drop" + str(i / 10)
                    results.append(calculate_speedup(dirpath, approx, str(thread)))

                graph_title = approx
                if "perfo" in approx:
                    graph_title = approx.replace('_', ' ')
                
                graph_title = graph_title.title() + " Drop " + str(i / 10)
                plot_graph(default_results, results, graph_title, approx, "drop" + str(i / 10))
                results = []
                