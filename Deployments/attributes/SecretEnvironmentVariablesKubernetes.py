import yaml

class SecretEnvironmentVariablesKubernetes:
    def __init__(self, deployment_content):
        self.deployment_content = yaml.safe_load(deployment_content)

    def has_secret_environment_variables(self):
        if isinstance(self.deployment_content, dict) and 'spec' in self.deployment_content:
            template_spec = self.deployment_content.get('spec', {}).get('template', {}).get('spec', {})
            if 'containers' in template_spec:
                for container in template_spec['containers']:
                    env_vars = container.get('env', [])
                    for env_var in env_vars:
                        if 'valueFrom' in env_var:
                            return True
        return False
