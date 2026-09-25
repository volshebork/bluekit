# This module sets up a virtual environment on Linux and installs required Python packages if they're missing.

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

# variables
required_packages = ["questionary"]  # packages the menu needs before it can start
venv_dir = Path(__file__).resolve().parents[2] / ".venv"  # bluekit/.venv
venv_python = venv_dir / "bin" / "python"


def ensure_venv():
    # Linux only; Windows pip installs without restriction
    if os.name == "nt":
        return

    # already running inside a virtual environment
    if sys.prefix != sys.base_prefix:
        return

    # create the venv on first run; remove partial leftovers if creation fails
    if not venv_python.exists():
        print("Creating virtual environment in .venv ...")
        result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        if result.returncode != 0:
            shutil.rmtree(venv_dir, ignore_errors=True)
            print("Error: failed to create virtual environment.")
            print("  On Ubuntu/Debian, install venv support with: sudo apt install python3-venv")
            sys.exit(1)

    # replace this process with bluekit running under the venv's Python
    os.execv(venv_python, [str(venv_python), *sys.argv])


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