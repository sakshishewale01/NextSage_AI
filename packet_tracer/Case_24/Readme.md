# NET-024 – NAT Not Configured

## Problem

A private PC needs to communicate with an outside server, but NAT is not configured on the router.

## Topology

```text
PC0 ─── Switch0 ─── Router0 ─── Server0

Devices used:

1 PC
1 Cisco 2960 Switch
1 Cisco 1941 Router
1 Server
IP Addressing
PC0 – Private Network
IP Address:       192.168.10.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.10.1
Router0
G0/0: 192.168.10.1
G0/1: 192.168.20.1
Server0 – Outside Network
IP Address:       192.168.20.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.20.1
Step 1 – Check Router Interfaces

The router interfaces were checked using:

show ip interface brief

Both interfaces were configured and enabled.

Step 2 – Check NAT Translation

The NAT table was checked using:

show ip nat translations

Initially, no NAT translation was present.

Step 3 – Check Running Configuration

The router configuration was checked using:

show running-config

No NAT configuration was present.

Root Cause

The router did not have NAT configured.

Therefore, private network traffic was not being translated.

Solution

The private router interface was configured as the NAT inside interface:

interface gigabitEthernet 0/0
ip nat inside

The outside interface was configured as:

interface gigabitEthernet 0/1
ip nat outside

A NAT ACL was created:

access-list 1 permit 192.168.10.0 0.0.0.255

PAT was configured using:

ip nat inside source list 1 interface gigabitEthernet 0/1 overload
Step 4 – Verify NAT Configuration

The configuration was checked again using:

show running-config

The NAT configuration was now present.

Step 5 – Generate Traffic

Traffic was generated from PC0 using:

ping 192.168.20.10
Step 6 – Verify NAT Translation

The NAT table was checked again:

show ip nat translations

A NAT translation appeared after traffic was generated.

Result

The NAT configuration problem was successfully identified and fixed.

Initially, no NAT translation was present. After configuring NAT and generating traffic, a NAT translation appeared.