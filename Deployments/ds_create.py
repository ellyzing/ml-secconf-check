import os

from datasets import load_dataset
from attributes.ExposePortKubernetes import ExposePortKubernetes
from attributes.KubernetesCapabilities import KubernetesCapabilities
from attributes.KubernetesDeploymentDangerousCommandsChecker import KubernetesDeploymentDangerousCommandsChecker
from attributes.KubernetesDeploymentLatestTagChecker import KubernetesDeploymentLatestTagChecker
from attributes.KubernetesEmptyDirMount import KubernetesEmptyDirMount
from attributes.KubernetesHostSeparation import KubernetesHostSeparation
from attributes.KubernetesNonRootUser import KubernetesNonRootUser
from attributes.KubernetesProbeChecker import KubernetesProbeChecker
from attributes.KubernetesReadOnlyRootFS import KubernetesReadOnlyRootFS
from attributes.KubernetesResourceChecker import KubernetesResourceChecker
from attributes.KubernetesSecrets import KubernetesSecrets
from attributes.KubernetesVolumePermissions import KubernetesVolumePermissions
from attributes.PrivilegedSecurityContextKubernetes import PrivilegedSecurityContextKubernetes
from attributes.SecretEnvironmentVariablesKubernetes import SecretEnvironmentVariablesKubernetes


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
            writer.writerow(["hostNetwork", 
                             "hostPID", 
                             "hostIPC", 
                             "has_privileged_security_context",
                             "count_of_dangerous_caps",
                             "user",
                             "UID",
                             "has_mounted_secrets",
                             "has_secret_environment_variables",
                             "read_only_root_fs_checker",
                             "has_dangerous_commands",
                             "count_dangerous_dirs",
                             "exposed_ports",
                             "image",
                             "tag",
                             "has_wide_permissions",
                             "qos",
                             "has_probes",
                             "result"])
        writer.writerows([parsed_lines])



csv_path = 'parsed_lines.csv'
parquet_path = 'parsed_lines.parquet'

def main():
    ds = load_dataset("substratusai/the-stack-yaml-k8s", split="train", token="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 ")
    counter = 1
    for data in ds:
        points = list()
        # print(counter)
        # if counter > 1000:
        #     break
        
        parsed_lines = list()
        deployment_content = data["content"]
        print(f"Deployment #{counter}")
        counter+=1
   
        host_separation_checker = KubernetesHostSeparation(deployment_content)
        parsed_lines.append(host_separation_checker._check_spec_property("hostNetwork"))
        parsed_lines.append(host_separation_checker._check_spec_property("hostPID"))
        parsed_lines.append(host_separation_checker._check_spec_property("hostIPC"))
        if host_separation_checker.check_host_separation():
            points.append(10)
        else:
            points.append(0)
        
        try:
            privileged_checker = PrivilegedSecurityContextKubernetes(deployment_content)
            result = privileged_checker.has_privileged_security_context()
            parsed_lines.append(result)
            if result:
                points.append(0)
            else:
                points.append(10)

            security_checker = KubernetesCapabilities(deployment_content)
            parsed_lines.append(security_checker.get_dangerous_capabilities())
            if security_checker.check_dangerous_capabilities():
                points.append(0)
            else:
                points.append(10)

            non_root_checker = KubernetesNonRootUser(deployment_content)
            parsed_lines.append(non_root_checker.check_user())
            parsed_lines.append(non_root_checker.check_id())
            if non_root_checker.check_non_root_execution():
                points.append(10)
            else:
                points.append(0)
            

            secrets_checker = KubernetesSecrets(deployment_content)
            result = secrets_checker.has_mounted_secrets()
            parsed_lines.append(result)
            if result:
                points.append(0)
            else:
                points.append(8)

        
            secrets_checker = SecretEnvironmentVariablesKubernetes(deployment_content)
            result = secrets_checker.has_secret_environment_variables()
            parsed_lines.append(result)
            if result:
                points.append(0)
            else:
                points.append(8)

            read_only_root_fs_checker = KubernetesReadOnlyRootFS(deployment_content)
            result = read_only_root_fs_checker.check_read_only_root_fs()
            parsed_lines.append(result)
            if result:
                points.append(7)
            else:
                points.append(0)
            
        
            dangerous_commands_checker = KubernetesDeploymentDangerousCommandsChecker(deployment_content)
            parsed_lines.append(dangerous_commands_checker.get_dangerous_commands())
            has_dangerous_commands = dangerous_commands_checker.has_dangerous_commands()
            if has_dangerous_commands:
                points.append(0)
            else:
                points.append(6)

            emptydir_mount_checker = KubernetesEmptyDirMount(deployment_content)
            parsed_lines.append(emptydir_mount_checker.count_dangerous_dirs())
            result = emptydir_mount_checker.check_emptydir_mount()
            if result:
                points.append(0)
            else:
                points.append(6)

            port_checker = ExposePortKubernetes(deployment_content)
            parsed_lines.append(port_checker.get_exposed_ports())
            result = port_checker.has_exposed_ports()
            if result:
                points.append(6)
            else:
                points.append(0)

        
            latest_tag_checker = KubernetesDeploymentLatestTagChecker(deployment_content)
            image, tag = latest_tag_checker.get_image_and_tag()
            parsed_lines.append(image)
            parsed_lines.append(tag)
            has_latest_tag = latest_tag_checker.has_latest_tag()
            if has_latest_tag:
                points.append(0)
            else:
                points.append(5)

            volume_permissions_checker = KubernetesVolumePermissions(deployment_content)
            result = volume_permissions_checker.check_volume_permissions()
            parsed_lines.append(result)
            if result:
                points.append(4)
            else:
                points.append(0)

            resource_checker = KubernetesResourceChecker(deployment_content)
            parsed_lines.append(resource_checker.check_qos())
            result = resource_checker.check_resources()
            if result:
                points.append(4)
            else:
                points.append(0)

            probe_checker = KubernetesProbeChecker(deployment_content)
            result = probe_checker.check_probes()
            parsed_lines.append(result)
            if result:
                points.append(3)
            else:
                points.append(0)

            if sum(points) >= 78:
                parsed_lines.append(0)
            else:
                parsed_lines.append(1)
            write_parsed_lines_to_csv(parsed_lines, csv_path)
        except:
            continue
    

    

    # df = dd.read_csv(csv_path, on_bad_lines='skip', sep=';')
    
    # schema = {
    #     "hostNetwork": pa.bool_(),
    #     "hostPID": pa.bool_(),
    #     "hostIPC": pa.bool_(),
    #     "has_privileged_security_context": pa.bool_(),
    #     "count_of_dangerous_caps": pa.int64(),
    #     "user": pa.string(),
    #     "UID": pa.int64(),
    #     "has_mounted_secrets": pa.bool_(),
    #     "has_secret_environment_variables": pa.bool_(),
    #     "read_only_root_fs_checker": pa.bool_(),
    #     "has_dangerous_commands": pa.bool_(),
    #     "count_dangerous_dirs": pa.int64(),
    #     "exposed_ports": pa.int64(),
    #     "image": pa.string(),
    #     "tag": pa.string(),
    #     "has_wide_permissions": pa.bool_(),
    #     "qos": pa.string(),
    #     "has_probes": pa.bool_(),
    #     "result": pa.int64(),
       
    # }
    # df = df.repartition(npartitions=1)
    # df.to_parquet(parquet_path, schema=schema, write_index=False)

    


if __name__ == "__main__":
    main()