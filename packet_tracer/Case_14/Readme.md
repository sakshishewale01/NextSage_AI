# NET-014 – Wrong DNS Server

## Problem

PC0 was configured with an incorrect DNS server address. IP connectivity to the DNS server works when the correct DNS address is used, but hostname resolution fails when an incorrect DNS server is configured.

## Topology

- 1 PC
- 1 Cisco 2960 Switch
- 1 DNS Server
- PC0 → Switch0
- Switch0 → Server0

## IP Configuration

**PC0:** `192.168.14.10 / 255.255.255.0`

**Server0:** `192.168.14.2 / 255.255.255.0`

**Correct DNS Server:** `192.168.14.2`

**Faulty DNS Server:** `192.168.14.99`

No router is used in this test case because the PC and DNS server are on the same LAN.

## Correct Configuration Verification

Before creating the fault, the correct DNS configuration was verified.

PC0 was configured with:

```text
IP Address: 192.168.14.10
Subnet Mask: 255.255.255.0
DNS Server: 192.168.14.2

```
Connectivity to the DNS server was tested using:

ping 192.168.14.2

Result: 4 packets received, 0% packet loss. ✅

Hostname resolution was also verified using:

ping www.test.com

The hostname successfully resolved to:

192.168.14.2

This confirmed that the original DNS configuration was working correctly.

## Fault Created

After verifying the correct configuration, the DNS server address on PC0 was intentionally changed to an incorrect address:

DNS Server: 192.168.14.99

The correct DNS server is:

192.168.14.2

The incorrect DNS server is:

192.168.14.99

Only the DNS server address was changed. The PC IP address and subnet mask remained unchanged.

Verification

The faulty DNS configuration was verified using:

ipconfig

The PC configuration showed:

IPv4 Address:    192.168.14.10
Subnet Mask:     255.255.255.0
DNS Server:      192.168.14.99

IP connectivity to the actual DNS server was tested using:

ping 192.168.14.2

Result: 4 packets received, 0% packet loss. ✅

The incorrect DNS server was tested using:

ping 192.168.14.99

Result: Request timed out. ❌

Hostname resolution was tested using:

ping www.test.com

The result was:

Ping request could not find host www.test.com.
Please check the name and try again.

This confirmed that the PC could communicate with the network, but hostname resolution failed because the DNS server address was incorrect.

## Expected Fault
PC IP Address       : 192.168.14.10
Subnet Mask         : 255.255.255.0
Correct DNS Server  : 192.168.14.2
Configured DNS      : 192.168.14.99  ← WRONG

This reproduces the NET-014 – Wrong DNS Server fault.

Expected Fix

The DNS server address on PC0 should be corrected to:

192.168.14.2

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.


## Topology

Correct DNS Configuration

Correct DNS Verification

Wrong DNS Configuration

Fault Verification

## Result

The NET-014 – Wrong DNS Server fault was successfully created.

PC0 has a valid IP configuration and can communicate with the DNS server at 192.168.14.2, but it cannot resolve www.test.com because the configured DNS server address 192.168.14.99 is incorrect.

This successfully reproduces the condition where IP connectivity works but hostname resolution fails due to a wrong DNS server address.

## What I Learned
How DNS works in a local network
How to configure a DNS server address on a PC
How to verify IP connectivity using ping
How to test hostname resolution using ping
How an incorrect DNS server affects hostname resolution
How to identify a wrong DNS server configuration
How to create and verify a DNS troubleshooting fault in Cisco Packet Tracer