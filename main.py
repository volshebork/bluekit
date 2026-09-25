# bluekit: main menu entry point.

# import libraries
import questionary

# import functions
from modules.ui.title import title
from modules.nmap.get_hostnames import get_hostnames


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
            choices=["Get hostnames (ping sweep)", "Back to Main Menu"],
        ).ask()

        if choice == "Get hostnames (ping sweep)":
            run(get_hostnames)
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