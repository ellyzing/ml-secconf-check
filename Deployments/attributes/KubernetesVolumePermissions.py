import yaml

class KubernetesVolumePermissions:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def check_volume_permissions(self):
        
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        volumes = deployment_content_dict.get('spec', {}).get('volumes', [])
        for volume in volumes:
            if 'emptyDir' in volume:
                if not isinstance(volume, dict):
                    continue
                permissions = volume['emptyDir'].get('medium', 'None')
                if permissions != 'None' and int(permissions, 8) > 0o400:
                    return False
            elif 'hostPath' in volume:
                if not isinstance(volume, dict):
                    continue
                permissions = volume['hostPath'].get('mode', 'None')
                if permissions != 'None' and int(permissions, 8) > 0o400:
                    return False
        return True
