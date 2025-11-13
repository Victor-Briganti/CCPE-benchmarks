import pandas as pd

CSV_PATH="./output/csv/"
RESULTS_PATH="./output/results/"
DEFAULT=CSV_PATH + "default/kdd_cup_default1.csv"
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
default_df = pd.read_csv(DEFAULT, header=None)
# default_df = default_df.drop(default_df.columns[[34]], axis=1) # pyright: ignore[reportCallIssue, reportArgumentType]

def calculate_mcr(filepath):
    results = []
    for i in range(0, 10):
        csv_path = filepath + '-' + str(i) + ".csv"
        approx_df = pd.read_csv(csv_path, header=None)
        # approx_df = approx_df.drop(approx_df.columns[[34]], axis=1)  # pyright: ignore[reportCallIssue, reportArgumentType]

        results.append(((default_df != approx_df).sum().sum() / default_df.size))

    return pd.DataFrame(results)


for approx in APPROXIMATION:
     for thread in [1, 2, 4, 8]:
        if approx == "fast" or approx == "default":
            print(approx + str(thread))
            csv_path = CSV_PATH + approx + "/kdd_cup_" + approx + str(thread)
            results_path = RESULTS_PATH + approx + "/kdd_cup_" + approx + str(thread)
            df = calculate_mcr(csv_path)
            df.to_csv(results_path + ".csv", index=False)
        else:
            if approx == "memo":
                for i in range(1, 6):
                    print(approx + str(thread) + "-threshold" + str(i * 10))
                    approx_path = approx +  "/threshold" + str(i * 10) + "/kdd_cup_" + approx + str(thread) + "-" + "threshold" + str(i * 10)
                    csv_path = CSV_PATH + approx_path
                    results_path = RESULTS_PATH + approx_path
                    df = calculate_mcr(csv_path)
                    df.to_csv(results_path + ".csv", index=False)
            else:
                for i in range(1, 6):
                    print(approx + str(thread) + "-drop" + str(i / 10))
                    approx_path = approx +  "/drop" + str(i / 10) + "/kdd_cup_" + approx + str(thread) + "-" + "drop" + str(i / 10)
                    csv_path = CSV_PATH + approx_path
                    results_path = RESULTS_PATH + approx_path
                    df = calculate_mcr(csv_path)
                    df.to_csv(results_path + ".csv", index=False)