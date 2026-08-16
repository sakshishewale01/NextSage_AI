# NET-023 – ACL Wrong Interface/Direction

## Problem
An ACL was applied to the wrong interface and direction on the router, causing network traffic to be blocked unexpectedly.

## Topology
- 1 Cisco 1941 Router
- 2 Cisco 2960 Switches
- 1 PC
- 1 Server
- PC0 → Switch0 → R1 → Switch1 → Server0

## IP Configuration

**PC0:** `192.168.22.10 / 255.255.255.0`  
**R1 GigabitEthernet0/0:** `192.168.22.1 / 255.255.255.0`  
**R1 GigabitEthernet0/1:** `192.168.23.1 / 255.255.255.0`  
**Server0:** `192.168.23.10 / 255.255.255.0`

## Solution

An extended ACL was created to deny traffic from the server network to the PC network:

```bash
access-list 101 deny ip 192.168.23.0 0.0.0.255 192.168.22.0 0.0.0.255
access-list 101 permit ip any any

```
The ACL was intentionally applied to the wrong interface and direction to create the fault:

interface gigabitEthernet 0/0
ip access-group 101 out

This caused traffic from PC0 toward the remote server network to be blocked unexpectedly.

Verification

The ACL configuration was checked using:

show access-lists

The interface configuration was checked using:

show running-config

The configuration confirmed that ACL 101 was applied to GigabitEthernet0/0 in the outbound direction:

interface GigabitEthernet0/0
ip access-group 101 out

Connectivity was tested from PC0 using:

ping 192.168.23.10

The result was:

Packets: Sent = 4, Received = 0, Lost = 4 (100% loss)

Result: Traffic was blocked unexpectedly. ❌



Ping Verification

## Result

The ACL was successfully configured and intentionally applied to the wrong interface and direction. As a result, communication from PC0 to the server network was blocked, successfully reproducing the NET-023 fault condition.

## What I Learned
How to create an extended ACL
How to apply an ACL to a router interface
How inbound and outbound ACL directions affect traffic
How an ACL applied to the wrong interface can block valid traffic
How to verify ACL configuration using show access-lists
How to verify interface ACL placement using show running-config
How to test network connectivity using ping