#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
    module = AnsibleModule(
        argument_spec={
            "version": {"required": True, "type": "str"},
        },
        supports_check_mode=True
    )

    version = module.params["version"]

    try:
        # Download dotnet-install.sh script
        subprocess.run(['wget', 'https://dot.net/v1/dotnet-install.sh', '-O', 'dotnet-install.sh'], check=True)

        # Make dotnet-install.sh executable
        subprocess.run(['chmod', '+x', './dotnet-install.sh'], check=True)

        # Run dotnet-install.sh with the specified channel
        subprocess.run(['./dotnet-install.sh', '--channel', version], check=True)

        # Add export command to .zshrc
        subprocess.run(['echo', 'export DOTNET_ROOT=/home/arghya/.dotnet', '>>', '/home/arghya/.zshrc'], check=True)
        subprocess.run(['echo', 'export PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools', '>>', '/home/arghya/.zshrc'], check=True)

        module.exit_json(changed=True, msg=f".NET Core {version} installation completed")

    except subprocess.CalledProcessError as e:
        module.fail_json(msg="Error running a command", stderr=e.stderr)

if __name__ == '__main__':
    main()
