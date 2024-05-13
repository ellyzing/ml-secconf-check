class PackageUpdate:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path

    def has_package_update_commands(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.readlines()

        update_commands = ['apt-get update', 'apt-get upgrade', 'apt-get update && apt-get upgrade',
                           'yum update', 'dnf upgrade', 'zypper refresh', 'zypper update', 'apk update',
                           'pacman -Sy', 'pacman -Syu', 'emerge --sync', 'emerge -uDN @world']
        
        for line in dockerfile_content:
            if line.strip().startswith("#"):
                continue

            for command in update_commands:
                if command in line:
                    return True

        return False
