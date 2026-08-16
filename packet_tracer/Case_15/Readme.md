# NET-015 – DNS Service Disabled

## Problem

The DNS service on the DNS server was intentionally disabled. As a result, the PC can communicate with the DNS server using its IP address, but it cannot resolve the hostname `www.test.com`.

## Topology

- 1 PC
- 1 Cisco 2960 Switch
- 1 Server
- PC0 → Fa0/1
- Server0 → Fa0/2

## IP Configuration

**PC0:** `192.168.15.10 / 255.255.255.0`  
**DNS Server:** `192.168.15.2 / 255.255.255.0`

**DNS Server configured on PC0:** `192.168.15.2`

## Correct Configuration

The DNS server was initially configured with the following A record:

```text
Name:    www.test.com
Type:    A Record
Address: 192.168.15.2
```

The DNS service was initially turned ON to verify that the correct configuration was working.

Initial Verification

Connectivity between PC0 and the DNS server was tested using:

ping 192.168.15.2

Result: 4 packets received, 0% packet loss. ✅

DNS hostname resolution was also tested using:

ping www.test.com

The hostname successfully resolved to:

192.168.15.2

Result: 4 packets received, 0% packet loss. ✅

## Fault Created

After verifying the correct connection, the DNS service on Server0 was intentionally turned OFF.

The DNS A record was kept unchanged:

www.test.com → 192.168.15.2

The fault is that the DNS service itself is disabled.

Verification After Fault

IP connectivity was tested again using:

ping 192.168.15.2

Result: 4 packets received, 0% packet loss. ✅

This confirms that the PC can still communicate with the DNS server.

Hostname resolution was then tested using:

ping www.test.com

## The result was:

Ping request could not find host www.test.com.
Please check the name and try again.

This confirms that hostname resolution fails because the DNS service is disabled.

Expected Fault
DNS Server IP       : 192.168.15.2
DNS Record          : www.test.com → 192.168.15.2
DNS Service         : OFF  ← WRONG


ping 192.168.15.2   : SUCCESS
ping www.test.com   : FAILED

This reproduces the NET-015 – DNS Service Disabled fault.

## Expected Fix

The DNS service on Server0 should be turned ON.

The DNS A record should remain:

www.test.com → 192.168.15.2

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.


## Topology

DNS Configuration

PC IP Configuration

Successful IP Ping Before Fault

Successful DNS Resolution Before Fault

DNS Service Disabled

IP Ping After Fault

Failed Hostname Resolution

## Result

The NET-015 – DNS Service Disabled fault was successfully created.

The PC can still reach the DNS server using its IP address, but hostname resolution fails because the DNS service on Server0 is turned OFF.

This reproduces the condition where the hostname cannot be resolved even though IP connectivity to the DNS server is working.

## What I Learned
How to configure a DNS server in Cisco Packet Tracer
How to create an A record
How to configure a PC to use a DNS server
How to test DNS resolution using ping
How to identify the difference between IP connectivity and DNS resolution
How to disable the DNS service to reproduce a DNS failure
How to verify a DNS service fault