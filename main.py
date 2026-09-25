# Bluekit: main menu entry point.

from modules.common.ensure_dependencies import ensure_venv, ensure_dependencies

ensure_venv()  # Linux: relaunches under .venv if not already in it
ensure_dependencies()  # must run before importing third-party packages below

import questionary

from modules.ui.title import title
from modules.nmap.get_hostnames import get_hostnames
from modules.nmap.get_host_details import get_host_details


def run(command):
    # runs a menu command; Ctrl+C cancels back to the menu instead of crashing
    try:
        command()
    except KeyboardInterrupt:
        print("\nCancelled.")
    input("\nPress Enter to return to the menu...")


def nmap_menu():
    while True:
        choice = questionary.select(
            "Network Enumeration (nmap)",
            choices=[
                "1. Discover hosts (ping sweep)",
                "2. Host details (OS + services)",
                "Back to Main Menu",
            ],
        ).ask()

        if choice == "1. Discover hosts (ping sweep)":
            run(get_hostnames)
        elif choice == "2. Host details (OS + services)":
            run(get_host_details)
        else:  # Back to Main Menu, or Ctrl+C (questionary returns None)
            return


def main():
    title()
    while True:
        choice = questionary.select(
            "Main Menu",
            choices=["Network Enumeration (nmap)", "Exit"],
        ).ask()

        if choice == "Network Enumeration (nmap)":
            nmap_menu()
        else:  # Exit, or Ctrl+C
            break


if __name__ == "__main__":
    main()