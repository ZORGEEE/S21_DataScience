#!/usr/bin/env python3

import os
import subprocess
import sys
from shutil import make_archive

def check_environment():
    """Check if running in the correct virtual environment"""
    if not os.environ.get('VIRTUAL_ENV'):
        raise EnvironmentError("This script must be run within your virtual environment")
    
    # Check if the environment name matches your expected name
    env_path = os.environ['VIRTUAL_ENV']
    expected_env_name = 'posidons'  # Replace with your actual env name
    if expected_env_name not in env_path:
        raise EnvironmentError(f"Wrong virtual environment. Expected '{expected_env_name}'")

def install_requirements():
    """Install packages from requirements.txt"""
    print("Installing requirements...")
    
    # First ensure pip and setuptools are up to date
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools'])
    
    # Then install our requirements
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def list_installed_packages():
    """List all installed packages and save to requirements.txt"""
    try:
        # Try the modern way first (pip 10+)
        from pip._internal.operations import freeze
        installed_packages = freeze.freeze()
    except ImportError:
        # Fallback to older method
        output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = output.decode('utf-8').split('\n')
    
    installed_packages = sorted([pkg for pkg in installed_packages if pkg.strip()])
    
    print("Installed packages:")
    for package in installed_packages:
        print(package)
    
    # Save to requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(installed_packages))

def archive_environment():
    """Create an archive of the virtual environment"""
    env_path = os.environ['VIRTUAL_ENV']
    print(f"Archiving virtual environment at {env_path}...")
    make_archive('posidons', 'zip', os.path.dirname(env_path), os.path.basename(env_path))
    print("Environment archived as posidons.zip")

def main():
    try:
        check_environment()
        install_requirements()
        list_installed_packages()
        archive_environment()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()