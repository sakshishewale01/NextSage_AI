# NET-016 – DNS Record Missing

## Problem

The required DNS record for the hostname `www.test.com` was missing from the DNS server.

As a result, the PC could communicate with the DNS server using its IP address, but it could not resolve the hostname `www.test.com`.

## Topology

- 1 PC
- 1 Cisco 2960 Switch
- 1 DNS Server
- PC0 → Fa0/1
- Server0 → Fa0/2

## IP Configuration

**PC0:** `192.168.16.10 / 255.255.255.0`  
**DNS Server:** `192.168.16.2 / 255.255.255.0`

**DNS Server configured on PC0:** `192.168.16.2`

## Correct Configuration

The DNS server was initially configured with the following A record:

```text
Name:    www.test.com
Type:    A Record
Address: 192.168.16.2

```
The DNS service was kept ON.

Initial Verification

Connectivity between PC0 and the DNS server was tested using:

ping 192.168.16.2

Result: 4 packets received, 0% packet loss. ✅

Hostname resolution was also tested using:

ping www.test.com

The hostname successfully resolved to:

192.168.16.2

Result: 4 packets received, 0% packet loss. ✅

This confirmed that the original DNS configuration was working correctly.

Fault Created

After verifying the correct configuration, the DNS A record for www.test.com was intentionally removed from Server0.

The DNS service remained ON.

The record that was removed was:

www.test.com → 192.168.16.2

After removal, the DNS record table was empty.

Verification After Fault

IP connectivity was tested again using:

ping 192.168.16.2

Result: 4 packets received, 0% packet loss. ✅

This confirmed that the PC could still communicate with the DNS server.

Hostname resolution was then tested using:

ping www.test.com

The result was:

Ping request could not find host www.test.com.
Please check the name and try again.

This confirmed that the hostname could not be resolved because its DNS record was missing.

Expected Fault
DNS Server IP       : 192.168.16.2
DNS Service         : ON
DNS Record          : www.test.com → MISSING


ping 192.168.16.2   : SUCCESS
ping www.test.com   : FAILED

This reproduces the NET-016 – DNS Record Missing fault.

Expected Fix

The missing DNS A record should be added back to the DNS server:

Name:    www.test.com
Type:    A Record
Address: 192.168.16.2

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.


## Topology

Correct DNS Record Configuration

Successful IP Connectivity

Successful DNS Resolution Before Fault

DNS Record Removed

Successful IP Connectivity After Fault

Failed Hostname Resolution

## Result

The NET-016 – DNS Record Missing fault was successfully created.

The PC can communicate with the DNS server using its IP address, but the hostname www.test.com cannot be resolved because the required DNS A record is missing.

This reproduces the condition where IP connectivity works but one hostname cannot be resolved due to a missing DNS record.

## What I Learned
How to configure a DNS server in Cisco Packet Tracer
How to create an A record
How to remove a DNS record
How to configure a PC to use a DNS server
How to verify IP connectivity using ping
How to test hostname resolution using ping
How to identify a missing DNS record
How to distinguish a missing DNS record from a disabled DNS service