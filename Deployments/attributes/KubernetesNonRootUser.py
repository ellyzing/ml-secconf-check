import yaml
class KubernetesNonRootUser:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def check_non_root_execution(self):
        non_root_exec_indicators = ["user: root", "runAsUser: 0"]

        for line in self.deployment_content.split('\n'):
            if any(indicator in line for indicator in non_root_exec_indicators):
                return False

        return True
    
    def check_user(self):
        user_indicators = ["user: "]

        for line in self.deployment_content.split('\n'):
            if any(indicator in line for indicator in user_indicators):
                user = line.split(':')[1].strip()
                return user

        return "None"

    def check_id(self):
        deployment_content_dict = yaml.safe_load(self.deployment_content)
        containers = deployment_content_dict.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])

        # Iterate over the containers list
        for container in containers:
            security_context = container.get('securityContext')

            # Check if the 'runAsUser' key is defined in the security_context dictionary
            if security_context:
                if 'runAsUser' in security_context:
                    # Get the 'runAsUser' value from the security_context dictionary
                    run_as_user = security_context.get('runAsUser')

                    return run_as_user
        return 0