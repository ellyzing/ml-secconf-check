import yaml

class KubernetesReadOnlyRootFS:
    def __init__(self, deployment_content):
        if isinstance(deployment_content, str):
            self.deployment_content = yaml.safe_load(deployment_content)
        else:
            self.deployment_content = deployment_content

    def check_read_only_root_fs(self):
        containers = self.deployment_content.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        for container in containers:
            security_context = container.get('securityContext', {})
            if 'readOnlyRootFilesystem' in security_context and security_context['readOnlyRootFilesystem']:
                return True
        return False
