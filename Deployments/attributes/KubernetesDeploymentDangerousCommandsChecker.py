import yaml
import re

class KubernetesDeploymentDangerousCommandsChecker:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def has_dangerous_commands(self):
        deployment = yaml.safe_load(self.deployment_content)
        spec = deployment.get('spec', {})
        template = spec.get('template', {})
        spec_inside_template = template.get('spec', {})
        containers = spec_inside_template.get('containers', [])

        dangerous_commands = [
            "wget",
            "curl",
            "git clone",
            "add-apt-repository",
            "ppa:",
            "ssh"
        ]

        for container in containers:
            args = container.get('args', [])
            for arg in args:
                for cmd in dangerous_commands:
                    if re.search(re.escape(cmd), arg):
                        return True

            command = container.get('command', None)
            if command:
                for cmd in command:
                    for dangerous_cmd in dangerous_commands:
                        if re.search(re.escape(dangerous_cmd), cmd):
                            return True

        return False
    
    def get_dangerous_commands(self):
        deployment = yaml.safe_load(self.deployment_content)
        spec = deployment.get('spec', {})
        template = spec.get('template', {})
        spec_inside_template = template.get('spec', {})
        containers = spec_inside_template.get('containers', [])

        dangerous_commands = [
            "wget",
            "curl",
            "git clone",
            "add-apt-repository",
            "ppa:",
            "ssh"
        ]
        counter=0
        for container in containers:
            args = container.get('args', [])
            for arg in args:
                for cmd in dangerous_commands:
                    if re.search(re.escape(cmd), arg):
                        counter+=1

            command = container.get('command', None)
            if command:
                for cmd in command:
                    for dangerous_cmd in dangerous_commands:
                        if re.search(re.escape(dangerous_cmd), cmd):
                            counter+=1

        return counter
