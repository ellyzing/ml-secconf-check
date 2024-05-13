import yaml

class PrivilegedSecurityContextKubernetes:
    def __init__(self, deployment_content):
        self.deployment_content = yaml.safe_load(deployment_content)

    def has_privileged_security_context(self):
        if isinstance(self.deployment_content, dict) and 'spec' in self.deployment_content and 'template' in self.deployment_content['spec'] and 'spec' in self.deployment_content['spec']['template']:
            template_spec = self.deployment_content['spec']['template']['spec']
            if 'securityContext' in template_spec and 'privileged' in template_spec['securityContext'] and template_spec['securityContext']['privileged']:
                return True
        return False
