class ExposePortKubernetes:
    def __init__(self, deployment_content):
        self.deployment_content = deployment_content

    def has_exposed_ports(self):
        ports_found = False

        for line in self.deployment_content.split('\n'):
            if "ports:" in line:
                ports_found = True
                break

        return ports_found
    
    def get_exposed_ports(self):
       
        for line in self.deployment_content.split('\n'):
            if "ports:" in line:
                for next_line in self.deployment_content.split('\n')[self.deployment_content.split('\n').index(line)+1:]:
                    if next_line.lstrip().startswith("-"):
                        port_info = next_line.strip().split()
                        for info in port_info:
                            if info.isdigit() and self._is_valid_unix_port(info):
                                return int(info)
        return 0
        
    
    def _is_valid_unix_port(self, port):
        try:
            port_number = int(port)
            if port_number >= 0 and port_number <= 65535:
                return True
            else:
                return False
        except ValueError:
            return False