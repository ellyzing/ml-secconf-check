import re

class KubernetesHostSeparation:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def check_host_separation(self):
        host_network = self._check_spec_property("hostNetwork")
        host_pid = self._check_spec_property("hostPID")
        host_ipc = self._check_spec_property("hostIPC")

        return not (host_network or host_pid or host_ipc)

    def _check_spec_property(self, property_name):
        property_pattern = rf'\b{property_name}\s*:\s*(true|false)'
        match = re.search(property_pattern, self.deployment_content)
        if match:
            value = match.group(1)
            return value.lower() == "false"
        return False