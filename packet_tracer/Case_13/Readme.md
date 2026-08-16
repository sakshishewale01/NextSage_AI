
# NET-013 – Wrong DHCP DNS

## Problem

The DHCP server provides an incorrect DNS server address to the PC.

The PC receives a valid IP address and can communicate using IP addresses, but DNS name resolution fails because the DHCP pool provides the wrong DNS server.

## Topology

- 1 Cisco 1941 Router
- 1 Cisco 2960 Switch
- 1 PC
- 1 Server (DNS Server)

### Connections

- Router0 GigabitEthernet0/0 → Switch0 GigabitEthernet0/1
- Switch0 FastEthernet0/1 → PC0 FastEthernet0
- Switch0 FastEthernet0/2 → Server0 FastEthernet0

## IP Configuration

### Router0

**GigabitEthernet0/0**

```text
IP Address: 192.168.13.1
Subnet Mask: 255.255.255.0

Server0 – DNS Server
IP Address: 192.168.13.2
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.13.1

The DNS service contains the following A record:

Name: www.test.com
Type: A Record
Address: 192.168.13.1
PC0

PC0 is configured to obtain its IPv4 configuration automatically using DHCP.

Correct DHCP Configuration

Initially, the DHCP pool was configured correctly:

ip dhcp excluded-address 192.168.13.1 192.168.13.2

ip dhcp pool LANPOOL
 network 192.168.13.0 255.255.255.0
 default-router 192.168.13.1
 dns-server 192.168.13.2

The correct configuration was verified using:

do show running-config

PC0 successfully received an IP address from the DHCP server.

Correct Connectivity Verification

The router was tested using:

ping 192.168.13.1

Result: 4 packets received, 0% packet loss. ✅

The DNS server was tested using:

ping 192.168.13.2

Result: 4 packets received, 0% packet loss. ✅

DNS name resolution was tested using:

ping www.test.com

The hostname successfully resolved to:

192.168.13.1

Result: 4 packets received, 0% packet loss. ✅

This confirmed that the original configuration was working correctly before creating the fault.

Fault Created

After verifying the correct configuration, the DHCP DNS server was intentionally changed to an incorrect address.

The faulty DHCP configuration is:

ip dhcp pool LANPOOL
 network 192.168.13.0 255.255.255.0
 default-router 192.168.13.1
 dns-server 192.168.13.254

The network and default gateway remain correct.

Only the DHCP DNS server was changed.

Actual DNS Server
192.168.13.2
Incorrect DHCP DNS Server
192.168.13.254

Therefore, PC0 receives an incorrect DNS server address through DHCP.

PC Verification

PC0 was refreshed using DHCP.

The PC received a valid IP address, subnet mask, and default gateway, but the DNS server supplied by DHCP was incorrect.

The important fault condition is:

IPv4 Address     : 192.168.13.x
Subnet Mask      : 255.255.255.0
Default Gateway  : 192.168.13.1
DNS Server       : 192.168.13.254

The exact IP address may vary depending on DHCP allocation.

Fault Verification

IP connectivity to the router was tested using:

ping 192.168.13.1

Result: 4 packets received, 0% packet loss. ✅

IP connectivity to the DNS server was tested using:

ping 192.168.13.2

Result: 4 packets received, 0% packet loss. ✅

DNS name resolution was tested using:

ping www.test.com

Result:

Ping request could not find host www.test.com.
Please check the name and try again.

This confirms that IP connectivity is working, but DNS name resolution is failing.

Expected Fault
Actual Router IP     : 192.168.13.1
Actual DNS Server    : 192.168.13.2
DHCP Network         : 192.168.13.0/24
DHCP Gateway         : 192.168.13.1
DHCP DNS             : 192.168.13.254  ← WRONG

This reproduces the NET-013 – Wrong DHCP DNS fault.

Expected Fix

The DHCP DNS server should be corrected to the actual DNS server:

ip dhcp pool LANPOOL
 dns-server 192.168.13.2

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.

Screenshots
Topology

Save a screenshot showing:

Router0
Switch0
PC0
Server0
All network connections
Correct Configuration

Save screenshots showing the original working DHCP configuration and PC configuration.

Wrong DHCP DNS Configuration

Save a screenshot showing:

ip dhcp pool LANPOOL
 network 192.168.13.0 255.255.255.0
 default-router 192.168.13.1
 dns-server 192.168.13.254
Fault Verification

Save the PC command prompt screenshot showing:

ping 192.168.13.1

with successful replies,

ping 192.168.13.2

with successful replies, and

ping www.test.com

with the DNS resolution failure.

Result

The NET-013 – Wrong DHCP DNS fault was successfully created and verified.

The PC receives a valid IP address and can communicate with the router and DNS server using their IP addresses. However, the PC cannot resolve www.test.com because DHCP provides an incorrect DNS server address (192.168.13.254) instead of the actual DNS server (192.168.13.2).

This successfully reproduces the condition:

"IP connectivity works but names fail."