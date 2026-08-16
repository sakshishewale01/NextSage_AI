# NET-012 – Wrong DHCP Gateway

## Problem

The DHCP server was configured with the wrong default gateway.

The LAN network is `192.168.12.0/24` and the actual router gateway is `192.168.12.1`. However, the DHCP pool was intentionally configured to provide `192.168.12.254` as the default gateway.

As a result, the PC receives a valid IP address but is given an incorrect gateway and cannot properly reach the remote network.

## Topology

- 1 Cisco 1941 Router
- 1 Cisco 2960-24TT Switch
- 1 PC
- PC0 → Switch0 → Router0
- PC0 Fa0 → Switch0 Fa0/1
- Switch0 Gi0/1 → Router0 Gi0/0

## Cable Configuration

**PC0 → Switch0**

- PC0 FastEthernet0
- Switch0 FastEthernet0/1
- Cable: Copper Straight-Through

**Switch0 → Router0**

- Switch0 GigabitEthernet0/1
- Router0 GigabitEthernet0/0
- Cable: Copper Straight-Through

## IP Configuration

**Router0 GigabitEthernet0/0:**

`192.168.12.1 / 255.255.255.0`

**Correct LAN Network:**

`192.168.12.0 / 24`

**PC0:**

Configured to obtain its IP address automatically using DHCP.

## Correct DHCP Configuration

The network was first configured correctly using:

```bash
ip dhcp excluded-address 192.168.12.1

ip dhcp pool LANPOOL
network 192.168.12.0 255.255.255.0
default-router 192.168.12.1

The correct configuration was verified and PC0 successfully received an IP address from the DHCP server.

Connectivity to the router was also verified using:

ping 192.168.12.1

Result: 4 packets received, 0% packet loss. ✅

Fault Created

After verifying the correct connection, the DHCP gateway was intentionally changed to an incorrect address:

ip dhcp pool LANPOOL
network 192.168.12.0 255.255.255.0
default-router 192.168.12.254

The network address remains correct, but the DHCP default gateway is incorrect.

The actual router IP is:

192.168.12.1

The DHCP clients are incorrectly receiving:

192.168.12.254

as their default gateway.

Verification

The DHCP configuration was checked using:

do show running-config

The configuration showed:

ip dhcp pool LANPOOL
 network 192.168.12.0 255.255.255.0
 default-router 192.168.12.254

The router interface was verified using:

do show ip interface brief

The router's actual LAN address was confirmed as:

GigabitEthernet0/0    192.168.12.1    up    up
PC Verification

On PC0, the DHCP configuration was refreshed using:

ipconfig /release
ipconfig /renew
ipconfig

The PC received a valid IP address, for example:

IPv4 Address.............: 192.168.12.2
Subnet Mask..............: 255.255.255.0
Default Gateway..........: 192.168.12.254

The exact IP address may be different depending on DHCP allocation.

The important point is that the PC receives a valid IP address but the default gateway is wrong.

Expected Fault
Actual Router IP       : 192.168.12.1
LAN Network            : 192.168.12.0/24
DHCP Network           : 192.168.12.0/24
DHCP Default Gateway   : 192.168.12.254  ← WRONG

This reproduces the NET-012 – Wrong DHCP Gateway fault.

Expected Fix

The DHCP default gateway should be corrected to the actual router interface:

ip dhcp pool LANPOOL
default-router 192.168.12.1

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.

Screenshots
Topology

Correct Connection Verification

Wrong DHCP Gateway Configuration

Running Configuration

PC IP Configuration

Ping Verification

Result

The NET-012 – Wrong DHCP Gateway fault was successfully created.

The DHCP server provides a valid IP address to the PC, but the DHCP pool supplies an incorrect default gateway (192.168.12.254) instead of the actual router gateway (192.168.12.1).

This reproduces the condition where the PC gets an IP but cannot reach the remote network because the DHCP default gateway is incorrect.