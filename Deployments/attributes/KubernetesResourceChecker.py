import yaml

class KubernetesResourceChecker:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def check_resources(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        for container in containers:
            resources = container.get('resources', {})
            if 'requests' in resources or 'limits' in resources:
                return True
        return False
    
    def check_qos(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        qos_class = "None"
        for container in containers:
            resources = container.get('resources', {})
            if 'limits' in resources and 'requests' in resources:
                if resources['limits'] == resources['requests']:
                    qos_class = 'Guaranteed'
                elif 'memory' in resources['limits'] and 'memory' in resources['requests'] and resources['limits']['memory'] == resources['requests']['memory'] and 'cpu' in resources['limits'] and 'cpu' in resources['requests'] and resources['limits']['cpu'] > resources['requests']['cpu']:
                    qos_class = 'Burstable'
            elif 'limits' in resources:
                qos_class = 'BestEffort'

        return qos_class