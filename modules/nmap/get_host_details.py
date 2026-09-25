# This module runs nmap OS and service/version detection against live hosts found by get_hostnames.

import os
import shutil
import subprocess

from modules.common.logs import logs_dir, raw_dir, archive_previous

# variables
ips_file = raw_dir / "ips.txt"  # produced by get_hostnames
xml_file = raw_dir / "host_details.xml"
txt_file = logs_dir / "host_details.txt"
tmp_xml = raw_dir / "host_details.xml.tmp"  # nmap writes here first; replaces xml_file only on success
tmp_txt = raw_dir / "host_details.txt.tmp"  # nmap writes here first; replaces txt_file only on success


def get_host_details():
    # confirm nmap is installed and on PATH
    if shutil.which("nmap") is None:
        print("Error: nmap not found. Install it and make sure it's on PATH.")
        return

    # confirm there are live hosts to scan
    if not ips_file.exists() or not ips_file.read_text().strip():
        print("Error: no live hosts found. Run 'Discover hosts (ping sweep)' first.")
        return

    host_count = len(ips_file.read_text().split())
    print(f"Scanning {host_count} live hosts (top 1000 ports). This may take a few minutes...")

    # OS + service/version detection against live hosts, saved as XML and plain text (to temp files)
    # Linux needs sudo; Windows needs to be run from an admin terminal instead
    command = ["nmap", "-sV", "-O", "-iL", str(ips_file), "-oX", str(tmp_xml), "-oN", str(tmp_txt)]
    if os.name != "nt":
        command.insert(0, "sudo")

    try:
        # run the scan; leave previous results untouched if nmap failed
        result = subprocess.run(command)
        if result.returncode != 0:
            print("Error: nmap scan failed. Previous results were kept.")
            return

        # insert a blank line before each host entry and the closing summary, for readability
        # (rewritten as a new file, since on Linux the sudo-created one is owned by root)
        text = tmp_txt.read_text()
        text = text.replace("\nNmap scan report for", "\n\nNmap scan report for")
        text = text.replace("\n# Nmap done at", "\n\n# Nmap done at")
        tmp_txt.unlink()
        tmp_txt.write_text(text)

        # scan succeeded; archive previous results, then swap in the new ones
        archive_previous(txt_file, xml_file)
        tmp_xml.replace(xml_file)
        tmp_txt.replace(txt_file)
        print(f"Results saved to {logs_dir}")

    finally:
        # clean up temp files left behind by a failed or cancelled scan
        tmp_xml.unlink(missing_ok=True)
        tmp_txt.unlink(missing_ok=True)


# allows standalone testing before it's wired into main.py
if __name__ == "__main__":
    get_host_details()