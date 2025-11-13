import os
import matplotlib.pyplot as plt
import pandas as pd

FILEPATH="./output/"
RESULTS_PATH="./output/results/"
PDFPATH="./graphs/results/"
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

def plot_graph(results, title, approx, threshold=None):
    threads = ["1", "2", "4", "8"]

    plt.figure(figsize=(12, 8))

    plt.bar(threads, results, color=['red', 'green', 'blue', 'orange'])

    plt.title(f'Kmeans MCR {title}', fontsize=35)
    plt.xlabel('Threads', fontsize=32)
    plt.ylabel('MCR (%)', fontsize=32)
    plt.grid(True, axis='y')

    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    plt.tight_layout()
    if threshold == None:
        plt.savefig(PDFPATH + "kmeans_" + approx + '.pdf')
    else:
        plt.savefig(PDFPATH + "kmeans_" + approx + "_" + threshold + '.pdf')
    
    plt.close()

def calculate_mean(dirpath):
    results = []
    for file in os.listdir(dirpath):
        print(file)
        results.append(pd.read_csv(dirpath + "/" + file).mean().values[0])

    return results


for approx in APPROXIMATION:
    if "fast" in approx:
        dirpath = RESULTS_PATH + approx
        results = calculate_mean(dirpath)
        plot_graph(results, approx.title(), approx)
    else:
        for i in range(1, 6):
            if approx == "memo":
                dirpath = RESULTS_PATH + approx + "/threshold" + str(i * 10)
                results = calculate_mean(dirpath)
                graph_title = approx.title() + " Threshold " + str(i * 10)
                plot_graph(results, graph_title, approx, "threshold" + str(i * 10))

            else:
                dirpath = RESULTS_PATH + approx + "/drop" + str(i / 10)
                results = calculate_mean(dirpath)

                graph_title = approx
                if "perfo" in approx:
                    graph_title = approx.replace('_', ' ')
                
                graph_title = graph_title.title() + " Drop " + str(i / 10)
                plot_graph(results, graph_title, approx, "drop" + str(i / 10))
