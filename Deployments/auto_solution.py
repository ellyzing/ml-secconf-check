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

def main():
    ds = load_dataset("substratusai/the-stack-yaml-k8s", split="train", token="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 ")
    counter = 1
    for data in ds:
        points = []

        deployment_content = data["content"]
        print(f"Deployment #{counter}")

        # 10
        host_separation_checker = KubernetesHostSeparation(deployment_content)
        if host_separation_checker.check_host_separation():
            points.append(10)
        else:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue

        # 10
        privileged_checker = PrivilegedSecurityContextKubernetes(deployment_content)
        result = privileged_checker.has_privileged_security_context()
        if result:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(10)

        # 10
        security_checker = KubernetesCapabilities(deployment_content)
        if security_checker.check_dangerous_capabilities():
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(10)

        # 10
        non_root_checker = KubernetesNonRootUser(deployment_content)
        if non_root_checker.check_non_root_execution():
            points.append(10)
        else:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue

        # 8
        secrets_checker = KubernetesSecrets(deployment_content)
        result = secrets_checker.has_mounted_secrets()
        if result:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(8)

        # 8
        secrets_checker = SecretEnvironmentVariablesKubernetes(deployment_content)
        result = secrets_checker.has_secret_environment_variables()
        if result:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(8)

        # 7
        read_only_root_fs_checker = KubernetesReadOnlyRootFS(deployment_content)
        if read_only_root_fs_checker.check_read_only_root_fs():
            points.append(7)
        else:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue

        # 6
        dangerous_commands_checker = KubernetesDeploymentDangerousCommandsChecker(deployment_content)
        has_dangerous_commands = dangerous_commands_checker.has_dangerous_commands()
        if has_dangerous_commands:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(6)

        # 6
        emptydir_mount_checker = KubernetesEmptyDirMount(deployment_content)
        result = emptydir_mount_checker.check_emptydir_mount()
        if result:
            points.append(0)
            print("Deployment is not secure")
            counter += 1
            continue
        else:
            points.append(6)

        # 6
        port_checker = ExposePortKubernetes(deployment_content)
        result = port_checker.has_exposed_ports()
        if result:
            points.append(6)
        else:
            points.append(0)

        # 5
        latest_tag_checker = KubernetesDeploymentLatestTagChecker(deployment_content)
        has_latest_tag = latest_tag_checker.has_latest_tag()
        if has_latest_tag:
            points.append(0)
        else:
            points.append(5)

        # 4
        volume_permissions_checker = KubernetesVolumePermissions(deployment_content)
        if volume_permissions_checker.check_volume_permissions():
            points.append(4)
        else:
            points.append(0)

        # 4
        resource_checker = KubernetesResourceChecker(deployment_content)
        result = resource_checker.check_resources()
        if result:
            points.append(4)
        else:
            points.append(0)

        # 3
        probe_checker = KubernetesProbeChecker(deployment_content)
        result = probe_checker.check_probes()
        if result:
            points.append(3)
        else:
            points.append(0)

        # если сумма признаков >= 78, то безопасно
        if sum(points) >= 78:
            print("Deployment is secure")
        else:
            print("Deployment is not secure")

        counter += 1

if __name__ == "__main__":
    main()
97