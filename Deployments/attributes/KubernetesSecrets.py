class KubernetesSecrets:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def has_mounted_secrets(self):
        return "secrets:" in self.deployment_content