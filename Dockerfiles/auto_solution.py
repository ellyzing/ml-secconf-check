import os
from attributes.EndOfInstallationCleaning import EndOfInstallationCleaning
from attributes.ExposedPorts import ExposePort
from attributes.FileAccessPermissions import FileAccessPermissions
from attributes.NonLatestImageUsagePolicy import NonLatestImageUsagePolicy
from attributes.NonRootUser import NonRootUser
from attributes.OfficialBaseImage import OfficialBaseImage
from attributes.PackageUpdates import PackageUpdate
from attributes.SafeCommands import SafeCommands
from attributes.SafeCopy import SafeCopy

def find_dockerfiles(directory):
    dockerfile_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "Dockerfile":
                dockerfile_paths.append(os.path.join(root, file))
    return dockerfile_paths

def estimation(dockerfile_path):
    points = list()
    # 9
    has_non_root_user = NonRootUser(dockerfile_path)
    if has_non_root_user:
        points.append(9)
    else:
        points.append(0)
        print("Dockerfile is not secure")
        

    # 8
    file_access_permissions = FileAccessPermissions(dockerfile_path)
    has_setuid_setgid = file_access_permissions.has_setuid_setgid()
    if has_setuid_setgid:
        points.append(0)
        print("Dockerfile is not secure")
        
    else:
        points.append(8)

    # 7
    safe_commands = SafeCommands(dockerfile_path)
    if safe_commands.has_potentially_dangerous_commands():
        points.append(0)
        print("Dockerfile is not secure")
        
    else:
        points.append(7)

    # 7
    official_base_image = OfficialBaseImage(dockerfile_path)
    results = official_base_image.is_official_docker_image()
    if all(results):
        points.append(7)
    else:
        points.append(0)

    # 5
    non_latest_image_usage_policy = NonLatestImageUsagePolicy(dockerfile_path)
    is_latest = non_latest_image_usage_policy.is_latest_tag()
    if is_latest:
        points.append(0)
    else:
        points.append(5)

    # 5
    package_update = PackageUpdate(dockerfile_path)
    has_update_commands = package_update.has_package_update_commands()
    if has_update_commands:
        points.append(5)
    else:
        points.append(0)

    # 4
    safe_copy = SafeCopy(dockerfile_path)
    has_add_instruction = safe_copy.has_add_instruction()
    if has_add_instruction:
        points.append(0)
    else:
        points.append(4)

    # 4
    end_of_installation_cleaning = EndOfInstallationCleaning(dockerfile_path)
    if end_of_installation_cleaning.has_required_instructions():
        points.append(4)
    else:
        points.append(0)

    # 1
    expose_port = ExposePort(dockerfile_path)
    has_exposed_ports = expose_port.has_exposed_ports()
    if has_exposed_ports:
        points.append(1)
    else:
        points.append(0)

    # если сумма признаков >= 30, то безопасно
    if sum(points) >= 30:
        print("Dockerfile is secure")
        estimation_res = 0
    else:
        print("Dockerfile is not secure")
        estimation_res = 1
    
    return estimation_res

def main():
    directory = "./archive/dockerfiles-1.0.0"
    dockerfile_paths = find_dockerfiles(directory)
    
    for index, dockerfile_path in enumerate(dockerfile_paths, start=1):

        print(f"Dockerfile #{index}: {dockerfile_path}")
        estimation(dockerfile_path)
        
        

if __name__ == "__main__":
    main()
