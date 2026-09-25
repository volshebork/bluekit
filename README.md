# Bluekit

A unified, terminal-driven toolkit for blue team incident response exercises. Run `main.py` and navigate with the arrow keys.

Bluekit is built to make quick, ad hoc tasks available in one central locatoin. It wraps existing tools (such as nmap) with sensible defaults rather than exposing every option. This program is intentionally not feature rich and does offer the full scope of any underlying tool. For anything beyond what this program offers, use the underlying tool directly.

## Requirements

- Python 3
- nmap
- sudo/root access

## Usage

```bash
python3 main.py
```

## Features

### Network Enumeration (nmap)

`Get hostnames (ping sweep)` will run a basic nmap scan to get hostnames, IPs, and MAC addresses. Results will be exported to logs.

## Upcoming Features
