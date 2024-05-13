import requests

class OfficialBaseImage:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.image = "-"

    def get_image(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.read()

        from_lines = [line for line in dockerfile_content.split('\n') if line.startswith('FROM ')]
        
        if len(from_lines)>0: 
            image_name_with_tag = from_lines[0].split(' ')[1]
            self.image, _ = image_name_with_tag.split(':', 1) if ':' in image_name_with_tag else (image_name_with_tag, None)
        return self.image

    def is_official_docker_image(self):
        with open(self.dockerfile_path, 'r') as file:
            dockerfile_content = file.read()

        from_lines = [line for line in dockerfile_content.split('\n') if line.startswith('FROM ')]
        results = []

        for from_line in from_lines:
            image_name_with_version = from_line.split(' ')[1]
            image_name, version = image_name_with_version.split(':', 1) if ':' in image_name_with_version else (image_name_with_version, None)

            is_official = self._check_if_image_is_official(image_name, version)
            results.append(is_official)

        return results

    def _check_if_image_is_official(self, image_name, version):
        try:
            image_name_without_labels = image_name.split()[0]

            response = requests.get(f'https://hub.docker.com/v2/repositories/library/{image_name_without_labels}')
            response_data = response.json()
            full_description = response_data.get('full_description', None)
            if full_description and version in full_description:
                return True
            return False
        except Exception as e:
            print(f"Error checking image: {str(e)}")
            return False
