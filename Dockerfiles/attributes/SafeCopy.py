class SafeCopy:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path

    def has_add_instruction(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.readlines()

        for line in dockerfile_content:
            if "#" in line:
                continue

            if line.strip().lower().startswith("add"):
                return True

        return False
