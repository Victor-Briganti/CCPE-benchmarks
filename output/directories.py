import os
from pathlib import Path

FILEPATH = "./"
APPLICATIONS = [
    "2mm",
    "blackscholes",
    "kmeans",
    "mandelbrot",
    "mm",
    "particlefilter",
    "pi",
]
APPROXIMATION = [
    "default",
    "fast",
    "memo",
    "task",
    "perfo_init",
    "perfo_fini",
    "perfo_large",
    "perfo_small",
    "perfo_default",
]

for app in APPLICATIONS:
    app_dir = FILEPATH + app 
    graph_dir = app_dir + "/graphs/" 
    output_dir = app_dir + "/output/" 
    output_raw_dir = app_dir + "/output/raw/" 
    output_results_dir = app_dir + "/output/results/" 
    perf_dir = app_dir + "/perf/" 
    perf_csv_dir = app_dir + "/perf/csv/" 
    perf_results_dir = app_dir + "/perf/results/" 

    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(graph_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_raw_dir, exist_ok=True)
    os.makedirs(output_results_dir, exist_ok=True)
    os.makedirs(perf_dir, exist_ok=True)
    os.makedirs(perf_csv_dir, exist_ok=True)
    os.makedirs(perf_results_dir, exist_ok=True)

    for approx in APPROXIMATION:
        approx_output_raw_dir = output_raw_dir + approx
        approx_output_results_dir = output_results_dir + approx
        approx_perf_csv_dir = perf_csv_dir + approx
        approx_perf_results_dir = perf_results_dir + approx

        os.makedirs(approx_output_raw_dir, exist_ok=True)
        os.makedirs(approx_output_results_dir, exist_ok=True)
        os.makedirs(approx_perf_csv_dir, exist_ok=True)
        os.makedirs(approx_perf_results_dir, exist_ok=True)
        if approx == "memo":
            for i in range(1, 6):
                thresh_output_raw_dir = approx_output_raw_dir + "/threshold" + str(i * 10) 
                thresh_output_results_dir = approx_output_results_dir + "/threshold" + str(i * 10) 
                thresh_perf_csv_dir = approx_perf_csv_dir + "/threshold" + str(i * 10) 
                thresh_perf_result_dir = approx_perf_results_dir + "/threshold" + str(i * 10) 
                os.makedirs(thresh_output_raw_dir, exist_ok=True)
                os.makedirs(thresh_output_results_dir, exist_ok=True)
                os.makedirs(thresh_perf_csv_dir, exist_ok=True)
                os.makedirs(thresh_perf_result_dir, exist_ok=True)

        elif approx != "default" and approx != "fast":
            for i in range(1, 6):
                drop_output_raw_dir = approx_output_raw_dir + "/drop0." + str(i)
                drop_output_results_dir = approx_output_results_dir + "/drop0." + str(i)
                drop_perf_csv_dir = approx_perf_csv_dir + "/drop0." + str(i)
                drop_perf_result_dir = approx_perf_results_dir + "/drop0." + str(i)
                os.makedirs(drop_output_raw_dir, exist_ok=True)
                os.makedirs(drop_output_results_dir, exist_ok=True)
                os.makedirs(drop_perf_csv_dir, exist_ok=True)
                os.makedirs(drop_perf_result_dir, exist_ok=True)

