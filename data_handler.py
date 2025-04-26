import duckdb
import pandas as pd
import os

def handle_file_upload(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[-1]
    if ext == '.csv':
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    table_name = "uploaded_data"
    duckdb.sql(f"DROP TABLE IF EXISTS {table_name}")
    duckdb.sql(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    return table_name
