# This module runs an nmap ping sweep with reverse DNS to discover live hosts on the network.

import ipaddress
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

from modules.common.logs import logs_dir, raw_dir, archive_previous

# variables
xml_file = raw_dir / "hostnames.xml"
txt_file = logs_dir / "hostnames.txt"
ips_file = raw_dir / "ips.txt"  # live host IPs, one per line; used by get_host_details
tmp_xml = raw_dir / "hostnames.xml.tmp"  # nmap writes here first; replaces xml_file only on success
tmp_txt = raw_dir / "hostnames.txt.tmp"  # nmap writes here first; replaces txt_file only on success
tmp_ips = raw_dir / "ips.txt.tmp"  # built from tmp_xml; replaces ips_file only on success


def get_hostnames():
    # confirm nmap is installed and on PATH
    if shutil.which("nmap") is None:
        print("Error: nmap not found. Install it and make sure it's on PATH.")
        return

    # prompt for target(s); multiple IPs or CIDR ranges can be space-separated
    targets = input("Enter target IP(s) or CIDR range(s) (e.g. 192.168.1.0/24): ").split()
    if not targets:
        print("Error: target cannot be blank.")
        return

    # validate each target so nmap never interprets bad input (e.g. 123123123 as an IP)
    for target in targets:
        try:
            ipaddress.IPv4Network(target, strict=False)
        except ValueError:
            print(f"Error: '{target}' is not a valid IPv4 address or CIDR range.")
            return

    # create logs and raw dirs if they don't exist yet
    raw_dir.mkdir(parents=True, exist_ok=True)

    # ping sweep + reverse DNS, saved as XML and plain text (to temp files)
    # Linux needs sudo; Windows needs to be run from an admin terminal instead
    command = ["nmap", "-sn", *targets, "-oX", str(tmp_xml), "-oN", str(tmp_txt)]
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

        # extract the IPs of live hosts from the XML into a plain list, one per line
        root = ET.parse(tmp_xml).getroot()
        ips = [
            host.find("address[@addrtype='ipv4']").get("addr")
            for host in root.findall("host")
            if host.find("status").get("state") == "up"
        ]
        tmp_ips.write_text("".join(f"{ip}\n" for ip in ips))

        # scan succeeded; archive previous results, then swap in the new ones
        archive_previous(txt_file, xml_file, ips_file)
        tmp_xml.replace(xml_file)
        tmp_txt.replace(txt_file)
        tmp_ips.replace(ips_file)
        print(f"{len(ips)} live hosts found. Results saved to {logs_dir}")

    finally:
        # clean up temp files left behind by a failed or cancelled scan
        tmp_xml.unlink(missing_ok=True)
        tmp_txt.unlink(missing_ok=True)
        tmp_ips.unlink(missing_ok=True)


# allows standalone testing before it's wired into main.py
if __name__ == "__main__":
    get_hostnames()