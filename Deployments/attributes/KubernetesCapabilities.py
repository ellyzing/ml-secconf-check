import re

class KubernetesCapabilities:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content


    def check_dangerous_capabilities(self):
        dangerous_capabilities = [
            "SYS_ADMIN",
            "DAC_OVERRIDE",
            "NET_ADMIN",
            "SYS_PTRACE",
            "SYS_RAWIO",
            "SYS_MODULE",
            "SYS_BOOT",
            "SYS_NICE",
            "SYS_TIME",
            "SYSLOG",
            "SETUID",
            "SETGID"
        ]

        for cap in dangerous_capabilities:
            if re.search(cap, self.deployment_content):
                return True

        return False

    def get_dangerous_capabilities(self):
        dangerous_capabilities = [
            "SYS_ADMIN",
            "DAC_OVERRIDE",
            "NET_ADMIN",
            "SYS_PTRACE",
            "SYS_RAWIO",
            "SYS_MODULE",
            "SYS_BOOT",
            "SYS_NICE",
            "SYS_TIME",
            "SYSLOG",
            "SETUID",
            "SETGID"
        ]
        counter = 0
        for cap in dangerous_capabilities:
            if re.search(cap, self.deployment_content):
                counter+=1

        return counter