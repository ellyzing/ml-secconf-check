import os

from attributes.EndOfInstallationCleaning import EndOfInstallationCleaning
from attributes.ExposedPorts import ExposePort
from attributes.FileAccessPermissions import FileAccessPermissions
from attributes.NonLatestImageUsagePolicy import NonLatestImageUsagePolicy
from attributes.NonRootUser import NonRootUser
from attributes.OfficialBaseImage import OfficialBaseImage
from attributes.PackageUpdates import PackageUpdate
from attributes.SafeCommands import SafeCommands
from attributes.SafeCopy import SafeCopy

from auto_solution import estimation

import pandas as pd
import csv
import dask.dataframe as dd
import pyarrow as pa
import pyarrow.parquet as pq

def write_parsed_lines_to_csv(parsed_lines, csv_path):
    mode = 'a' if os.path.exists(csv_path) else 'w'

    with open(csv_path, mode, newline='') as file:
        writer = csv.writer(file, delimiter=";")
        if mode == 'w':
            writer.writerow(["has_install_or_update", 
                             "has_clean_commands", 
                             "has_exposed_port", 
                             "port_number", 
                             "has_setuid_setgid", 
                             "image_tag", 
                             "user",
                             "image",
                             "has_package_update_commands",
                             "dangerous_commands_count",
                             "safe_copy",
                             "result"])
        writer.writerows([parsed_lines])

def find_dockerfiles(directory):
    dockerfile_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "Dockerfile":
                dockerfile_paths.append(os.path.join(root, file))
    return dockerfile_paths

csv_path = 'parsed_lines.csv'
parquet_path = 'parsed_lines.parquet'

def main():
    directory = "./archive/dockerfiles-1.0.0"
    dockerfile_paths = find_dockerfiles(directory)
    counter = 0
    for index, dockerfile_path in enumerate(dockerfile_paths, start=1):
        print(counter)
        if counter < 129136:
            counter+=1
            continue
        counter+=1
        parsed_lines = list()
        points = list()
        print(f"Dockerfile #{index}: {dockerfile_path}")
        print("Results:")

        end_of_installation_cleaning = EndOfInstallationCleaning(dockerfile_path)
        has_install_or_update, has_clean_commands = end_of_installation_cleaning.parse_package_related_lines()
        parsed_lines.append(has_install_or_update)
        parsed_lines.append(has_clean_commands)


        expose_port = ExposePort(dockerfile_path)
        parsed_lines.append(expose_port.has_exposed_ports())
        parsed_lines.append(expose_port.port)

        file_access_permissions = FileAccessPermissions(dockerfile_path)
        parsed_lines.append(file_access_permissions.has_setuid_setgid())

        non_latest_image_usage_policy = NonLatestImageUsagePolicy(dockerfile_path)
        parsed_lines.append(non_latest_image_usage_policy.get_tag())

        non_root_user = NonRootUser(dockerfile_path)
        parsed_lines.append(non_root_user.get_user())

        official_base_image = OfficialBaseImage(dockerfile_path)
        parsed_lines.append(official_base_image.get_image())

        package_update = PackageUpdate(dockerfile_path)
        parsed_lines.append(package_update.has_package_update_commands())

        safe_commands = SafeCommands(dockerfile_path)
        safe_commands.get_dangerous_commands()
        parsed_lines.append(len(safe_commands.dangerous_commands))

        safe_copy = SafeCopy(dockerfile_path)
        parsed_lines.append(safe_copy.has_add_instruction())

        

        print(parsed_lines)
        write_parsed_lines_to_csv(parsed_lines, csv_path)
    

    

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

    


if __name__ == "__main__":
    main()