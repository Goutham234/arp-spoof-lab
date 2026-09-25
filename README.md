# ARP Spoof Lab

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Powered%20by-Scapy-2ea44f)
![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)

A Python networking project for exploring ARP resolution and ARP reply construction using Scapy in an isolated lab.

> Use only on networks you own or have explicit permission to test. ARP manipulation can interrupt connectivity and affect other devices.

## Overview

Address Resolution Protocol (ARP) maps IPv4 addresses to MAC addresses on a local network. Because ARP does not authenticate these mappings, forged replies can cause devices to associate an IP address with an incorrect MAC address.

This project explores that behavior through a small command-line Python implementation.

## Current capabilities

- Accepts a network interface, target IPv4 address, and gateway IPv4 address.
- Validates IPv4 address syntax.
- Rejects identical target and gateway addresses.
- Validates the requested duration between 1 and 300 seconds.
- Retrieves the local interface's MAC address.
- Resolves target and gateway MAC addresses using ARP requests.
- Constructs Ethernet frames containing ARP replies.

## Project status

**This project is incomplete and is not a finished spoofing utility.**

The current implementation sends ARP discovery requests and constructs reply packets in memory. It does not yet transmit those constructed replies.

The `--seconds` argument is parsed and validated, but no timed transmission loop currently uses it. Forwarding, interruption handling, and ARP restoration are not implemented.

## Requirements

- Linux
- Python 3.10 or later
- Scapy
- A network interface connected to the authorized lab's Layer 2 network
- Appropriate privileges for raw Ethernet operations

ARP operates on the local network segment; it does not resolve devices across routers.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/arp-spoof-lab.git
cd arp-spoof-lab

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

Replace `YOUR_USERNAME` with your GitHub username.

## Usage

Display available arguments:

```bash
python arp_spoof.py --help
```

Example invocation in an isolated, authorized lab:

```bash
sudo .venv/bin/python arp_spoof.py \
  --iface eth0 \
  --target 192.168.56.10 \
  --gateway 192.168.56.1 \
  --seconds 30
```

Replace the interface and addresses with values from your lab.

**Current behavior:** resolves MAC addresses and prepares reply packets. It does not send the constructed spoofed replies.

### Arguments

| Argument    | Description                                                                     | Default  |
| ----------- | ------------------------------------------------------------------------------- | -------- |
| `--iface`   | Network interface used for ARP discovery                                        | Required |
| `--target`  | Target device's IPv4 address                                                    | Required |
| `--gateway` | Gateway's IPv4 address                                                          | Required |
| `--seconds` | Intended run duration, from 1 to 300 seconds; currently unused after validation | `30`     |

## How the code is organized

| Function        | Purpose                                                          |
| --------------- | ---------------------------------------------------------------- |
| `resolve_mac()` | Sends ARP requests and returns a responding device's MAC address |
| `arp_reply()`   | Constructs an Ethernet frame containing an ARP reply             |
| `main()`        | Parses arguments, checks inputs, and prepares packets            |

## Limitations

- IPv4 only.
- Designed for Linux; other platforms have not been validated.
- Requires local Layer 2 connectivity to both devices.
- ARP discovery can fail when a device is offline or ARP traffic is filtered.
- MAC resolution trusts received ARP responses.
- The current implementation is not a complete interception or forwarding tool.

## Development

Check Python syntax without sending network traffic:

```bash
python -m compileall -q arp_spoof.py
```

Suggested improvements:

- Unit tests for argument validation and packet construction.
- Clearer errors for invalid interfaces and unanswered ARP requests.
- Structured logging.
- An offline packet-inspection mode.
- Documentation of lab setup and limitations.

Tests should mock network operations rather than send packets on a live network.

## Contributing

Issues and pull requests are welcome. Include a clear explanation of the change and avoid publishing packet captures, addresses, or other data from networks you do not own.

## License

See [LICENSE](LICENSE) for the project’s license.
