# NET-011 – Wrong DHCP Network

## Problem

The DHCP pool on the router was configured with the wrong network address.

The LAN is using the `192.168.11.0/24` network, but the DHCP pool was incorrectly configured for the `192.168.20.0/24` network.

As a result, the PC was unable to obtain a usable IPv4 address through DHCP.

## Topology

- 1 Cisco 1941 Router
- 1 Cisco 2960 Switch
- 1 PC
- PC0 → Switch → Router0

## IP Configuration

**Router LAN Interface:**

`192.168.11.1 / 255.255.255.0`

**Correct LAN Network:**

`192.168.11.0 / 24`

**DHCP Client:**

PC0 was configured to obtain its IP address automatically using DHCP.

## Fault Created

The DHCP pool was intentionally configured with the wrong network:

```bash
ip dhcp pool LANPOOL
network 192.168.20.0 255.255.255.0
default-router 192.168.11.1