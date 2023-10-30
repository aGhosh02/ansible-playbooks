#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess

def main():
    module = AnsibleModule(
        argument_spec=dict(
            package_url=dict(required=True, type='str'),
        )
    )

    package_url = module.params['package_url']
    package_name = os.path.basename(package_url)

    # Download the package
    download_command = f"wget {package_url}  -P ~/Downloads"
    download_result = subprocess.run(download_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if download_result.returncode != 0:
        module.fail_json(msg=f"Failed to download {package_url}", stderr=download_result.stderr)

    # Install the package
    install_command = f"sudo apt install ~/Downloads/{package_name}"
    install_result = subprocess.run(install_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if install_result.returncode != 0:
        module.fail_json(msg=f"Failed to install {package_name}", stderr=install_result.stderr)

    module.exit_json(changed=True, msg=f"Google Chrome installed successfully")

if __name__ == '__main__':
    main()
