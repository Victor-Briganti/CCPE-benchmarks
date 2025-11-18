import duckdb
import pandas as pd

CSV_PATH="./output/csv/"
RESULTS_PATH="./output/results/"
DEFAULT=CSV_PATH + "default/test_default1.csv"
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

def calculate_smape(filepath):
    with duckdb.connect() as db:
        create_query = f"""
            CREATE TEMP TABLE common 
            AS 
            SELECT row_number() OVER() as id, CAST(column0 AS DOUBLE) AS column0 
            FROM read_csv_auto('{DEFAULT}')
            """
        db.sql(create_query)


        results = []
        for i in range(0, 10):
            csv_path = filepath + '-' + str(i) + '.csv'
            query = f"""
            WITH 
            approx AS (
                SELECT row_number() OVER() as id, CAST(column0 AS DOUBLE) AS column0 
                FROM read_csv_auto('{csv_path}')
            )
            SELECT SUM(ABS(a.column0 - c.column0) / (ABS(c.column0) + ABS(a.column0) + 1e-39)) / COUNT(*) * 100 AS smape_result
            FROM approx AS a
            INNER JOIN common AS c ON a.id = c.id
            """

            results.append(db.sql(query).df())

        return pd.concat(results, ignore_index=True)

for approx in APPROXIMATION:
    for thread in [1, 2, 4, 8]:
        if approx == "fast" or approx == "default":
            print(approx + str(thread))
            csv_path = CSV_PATH + approx + "/test_" + approx + str(thread)
            results_path = RESULTS_PATH + approx + "/test_" + approx + str(thread)
            df = calculate_smape(csv_path)
            df.to_csv(results_path, index=False)
        else:
            if approx == "memo":
                for i in range(1, 6):
                    print(approx + str(thread) + "-threshold" + str(i * 10))
                    approx_path = approx +  "/threshold" + str(i * 10) + "/test_" + approx + str(thread) + "-" + "threshold" + str(i * 10)
                    csv_path = CSV_PATH + approx_path
                    results_path = RESULTS_PATH + approx_path
                    df = calculate_smape(csv_path)
                    df.to_csv(results_path, index=False)
            else:
                for i in range(1, 6):
                    print(approx + str(thread) + "-drop" + str(i / 10))
                    approx_path = approx +  "/drop" + str(i / 10) + "/test_" + approx + str(thread) + "-" + "drop" + str(i / 10)
                    csv_path = CSV_PATH + approx_path
                    results_path = RESULTS_PATH + approx_path
                    df = calculate_smape(csv_path)
                    df.to_csv(results_path, index=False)
