import re

class FileAccessPermissions:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path

    def has_setuid_setgid(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.read()

        setuid_setgid_pattern = r'chmod .*(u\+s|g\+s|\d{4}([0-7]1[0-7]))'

        matches = re.findall(setuid_setgid_pattern, dockerfile_content)
        if matches:
            #print("The Dockerfile contains instructions to set setuid or setgid bits. True")
            return True
        else:
            #print("The Dockerfile does not contain instructions to set setuid or setgid bits. False")
            return False
