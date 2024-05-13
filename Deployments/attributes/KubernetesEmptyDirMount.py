import yaml

class KubernetesEmptyDirMount:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content
        self.dirs_to_check = [
            "/bin", "/boot", "/dev", "/lib", "/lib32", "/lib64", "/opt",
            "/proc", "/root", "/run", "/sys", "/sbin", "/usr", "/etc/"
        ]

    def check_emptydir_mount(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        emptydir_mounts = []
        for container in containers:
            volume_mounts = container.get('volumeMounts', [])
            for mount in volume_mounts:
                if mount.get('name') == 'emptydir':
                    emptydir_mounts.append(mount.get('mountPath'))
        return any(directory in mounted_dir for mounted_dir in emptydir_mounts for directory in self.dirs_to_check)
    
    def count_dangerous_dirs(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        emptydir_mounts = []
        for container in containers:
            volume_mounts = container.get('volumeMounts', [])
            for mount in volume_mounts:
                if mount.get('name') == 'emptydir':
                    emptydir_mounts.append(mount.get('mountPath'))

        count = sum(1 for mounted_dir in emptydir_mounts for directory in self.dirs_to_check if directory in mounted_dir)
        return count