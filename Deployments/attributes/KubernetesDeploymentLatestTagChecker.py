import yaml

class KubernetesDeploymentLatestTagChecker:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def has_latest_tag(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        for container in containers:
            image = container.get('image')
            if image and 'latest' in image:
                return True
        return False

    def get_image_and_tag(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)

        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        for container in containers:
            image = container.get('image')
            if image:
                tag = image.split(':')[-1]
                return image.split(':')[0], tag
        return "None", "latest"
