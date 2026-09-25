# This module installs required Python packages if they're missing.

import importlib
import subprocess
import sys

# variables
required_packages = ["questionary"]  # packages the menu needs before it can start


def ensure_dependencies(packages=required_packages):
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            # install with the same Python that's running bluekit, so it lands in the right place
            print(f"Installing missing package: {package}")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package])
            if result.returncode != 0:
                print(f"Error: failed to install {package}. Install it manually with:")
                print(f"  {sys.executable} -m pip install {package}")
                sys.exit(1)

    # refresh Python's module cache so newly installed packages can be imported
    importlib.invalidate_caches()