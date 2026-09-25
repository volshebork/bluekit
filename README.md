# Bluekit

A unified, terminal-driven toolkit for blue team incident response exercises. Run `main.py` and navigate with the arrow keys.

Bluekit is built to make quick, ad hoc tasks available in one central location. It wraps existing tools (such as nmap) with sensible defaults rather than exposing every option. This program is intentionally not feature rich and does not offer the full scope of any underlying tool. For anything beyond what this program offers, use the underlying tool directly.

Proper credentials and authorized access are required to use this program. This program will not bypass any access controls. It is intended only for use by those authorized to access the target network.

## Requirements

- Python 3.8
- nmap
- sudo access (Linux)

## Usage

Windows:

```powershell
python main.py
```

Linux:

```bash
python3 main.py
```

On Linux, Bluekit creates a `.venv` virtual environment on first run and automatically relaunches itself inside it. No manual activation is needed.

## Features

### Network Enumeration (nmap)

- `Discover hosts (ping sweep)` finds live hosts on a target IP range, with hostnames and MAC addresses where available.
- `Host details (OS + services)` detects the operating system and service versions on the top 1000 ports of each live host found by the ping sweep. Run the ping sweep first.

Results are saved to `logs/`. Previous results are moved to `logs/history/` with a timestamp.

## Upcoming Features

### Active Directory

- Session setup (DC, credentials, base DN auto-discovery)
- Enumerate privileged group members (including nested membership)
- Remove a list of accounts from privileged groups
- Disable a list of accounts
- Get single user details
- Delete an account
- Reset the password of an account (requires LDAPS)
- Get a list of all groups in the domain
- Get a list of all accounts created in the last 7 days and list the creation date
