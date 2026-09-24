# This module runs an nmap ping sweep with reverse DNS to discover live hosts on the network.

import os
import shutil
import subprocess
from pathlib import Path

# variables
logs_dir = Path(__file__).resolve().parents[2] / "logs"  # bluekit/logs
xml_file = logs_dir / "hostnames.xml"
txt_file = logs_dir / "hostnames.txt"


def get_hostnames():
    # confirm nmap is installed and on PATH
    if shutil.which("nmap") is None:
        print("Error: nmap not found. Install it and make sure it's on PATH.")
        return

    # prompt for target range; blank input is an error
    target_range = input("Enter the target IP range to scan (e.g. 192.168.1.0/24): ").strip()
    if not target_range:
        print("Error: target range cannot be blank.")
        return

    # create logs dir if it doesn't exist yet
    logs_dir.mkdir(exist_ok=True)

    # ping sweep + reverse DNS, saved as XML and plain text
    # Linux needs sudo; Windows needs to be run from an admin terminal instead
    command = ["nmap", "-sn", target_range, "-oX", str(xml_file), "-oN", str(txt_file)]
    if os.name != "nt":
        command.insert(0, "sudo")

    subprocess.run(command)


# allows standalone testing before it's wired into main.py
if __name__ == "__main__":
    get_hostnames()