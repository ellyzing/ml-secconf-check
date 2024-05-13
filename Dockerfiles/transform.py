import os


from auto_solution import estimation

import pandas as pd
import csv
import dask.dataframe as dd
import pyarrow as pa
import pyarrow.parquet as pq


csv_path = 'parsed_lines.csv'
parquet_path = 'parsed_lines.parquet'

df = dd.read_csv(csv_path, on_bad_lines='skip', sep=';')

schema = {
    "has_install_or_update": pa.bool_(),
    "has_clean_commands": pa.bool_(),
    "has_exposed_port": pa.bool_(),
    "port_number": pa.int64(),
    "has_setuid_setgid": pa.bool_(),
    "image_tag": pa.string(),
    "user": pa.string(),
    "image": pa.string(),
    "has_package_update_commands": pa.bool_(),
    "dangerous_commands_count": pa.int64(),
    "safe_copy": pa.bool_(),
    "result": pa.int64(),
}
df = df.repartition(npartitions=1)
df.to_parquet(parquet_path, schema=schema, write_index=False)

