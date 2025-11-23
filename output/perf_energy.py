import os
import pandas as pd
from pathlib import Path

RESULT_PATH = "perf/energy/"
OUTPUT_PATH = "perf/csv_energy/"
THREADS = [1, 2, 4, 8]
APPLICATIONS = [
    "2mm",
    "blackscholes",
    "kmeans",
    "mm",
    "pi",
    #"particlefilter",
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

def parse_file(filepath):
    data= {}

    with open(filepath, "r") as file:
        for line in file:
            if "power/energy-pkg/" in line:
                data["energy-pkg"] = line.split()[0]
            
            if "power/energy-cores/" in line:
                data["energy-cores"] = line.strip().split()[0]
            
            if "power/energy-ram/" in line:
                data["energy-ram"] = line.strip().split()[0]

            if "seconds time" in line:
                data["real"] = line.strip().split()[0]

        df = pd.DataFrame([data])
        return df

def generate_csv(application_path: str, approx: str, threshold=None):
    if threshold == None:
        app_result = application_path + "/" + RESULT_PATH + approx + "/"
        app_csv = application_path + "/" + OUTPUT_PATH + approx + "/"
    else:
        if approx == "memo":
            threshold = "threshold" + str(threshold)
        else:
            threshold = "drop" + str(threshold)

        app_result = application_path + "/" + RESULT_PATH + approx + "/" + threshold + "/"
        app_csv = application_path + "/" + OUTPUT_PATH + approx + "/" + threshold + "/"
    
    pth = Path(app_result)

    for i in THREADS:
        data = []
        for file in pth.iterdir():
            if approx + str(i) in str(file):
                data.append(parse_file(file))

        df = pd.concat(data)
        df.to_csv(app_csv + os.path.basename(application_path + "_" + approx + str(i)), index=False)


for app in APPLICATIONS:
    for approx in APPROXIMATION:
        if approx == "memo":
            for i in range(1, 6):
                generate_csv(app, approx, i * 10)

        elif "perfo" in approx or approx == "task":
            for i in range(1, 6):
                generate_csv(app, approx, i / 10)

        else:
            generate_csv(app, approx)