class NonRootUser:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.user = "root"

    def has_non_root_user(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.readlines()

        for line in dockerfile_content:
            if line.strip().startswith("#"):
                continue

            if line.strip().lower().startswith("user"):
                parts = line.strip().split()
                if len(parts) > 1 and parts[1].lower() != "root":
                    return True
                else:
                    return False

        return False
    
    def get_user(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.readlines()

        for line in dockerfile_content:
            if line.strip().startswith("#"):
                continue

            if line.strip().lower().startswith("user"):
                parts = line.strip().split()
                if len(parts) > 1: self.user = parts[1].lower()

        return self.user
