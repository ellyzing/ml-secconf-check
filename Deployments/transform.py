import os


import pandas as pd
import csv
import dask.dataframe as dd
import pyarrow as pa
import pyarrow.parquet as pq


csv_path = 'parsed_lines.csv'
parquet_path = 'parsed_lines.parquet'

df = dd.read_csv(csv_path, on_bad_lines='skip', sep=';')

schema = {
        "hostNetwork": pa.bool_(),
        "hostPID": pa.bool_(),
        "hostIPC": pa.bool_(),
        "has_privileged_security_context": pa.bool_(),
        "count_of_dangerous_caps": pa.int64(),
        "user": pa.string(),
        "UID": pa.int64(),
        "has_mounted_secrets": pa.bool_(),
        "has_secret_environment_variables": pa.bool_(),
        "read_only_root_fs_checker": pa.bool_(),
        "has_dangerous_commands": pa.bool_(),
        "count_dangerous_dirs": pa.int64(),
        "exposed_ports": pa.int64(),
        "image": pa.string(),
        "tag": pa.string(),
        "has_wide_permissions": pa.bool_(),
        "qos": pa.string(),
        "has_probes": pa.bool_(),
        "result": pa.int64(),
       
    }
df = df.repartition(npartitions=1)
df.to_parquet(parquet_path, schema=schema, write_index=False)

