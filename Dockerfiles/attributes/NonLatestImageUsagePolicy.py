class NonLatestImageUsagePolicy:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.tag = "latest"

    def is_latest_tag(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.read()

        from_line = next((line for line in dockerfile_content.split('\n') if line.startswith('FROM ')), None)

        if from_line:
            image_name_with_tag = from_line.split(' ')[1]
            if ':' in image_name_with_tag:
                _, self.tag = image_name_with_tag.split(':', 1)
                return self.tag.strip() == 'latest'
            else:
                return False
        else:
            return False

    def get_tag(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.read()

        from_line = next((line for line in dockerfile_content.split('\n') if line.startswith('FROM ')), None)

        if from_line:
            image_name_with_tag = from_line.split(' ')[1]
            if ':' in image_name_with_tag:
                _, self.tag = image_name_with_tag.split(':', 1)
        return self.tag