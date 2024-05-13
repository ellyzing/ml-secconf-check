import yaml

class KubernetesProbeChecker:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def check_probes(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        for container in containers:
            if 'livenessProbe' in container or 'readinessProbe' in container or 'startupProbe' in container:
                return True
        return False
