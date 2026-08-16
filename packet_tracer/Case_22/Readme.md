# NET-022 – ACL Blocks Web

## Problem
The web server was reachable by ping, but HTTP access was blocked by an incorrectly configured ACL.

## Topology
- 1 Cisco 1941 Router
- 2 Cisco 2960 Switches
- 1 PC
- 1 Web Server
- PC0 → Switch0 → R1
- R1 → Switch1 → Server0

## IP Configuration

**PC0:** `192.168.22.10 / 255.255.255.0`  
**R1 LAN Interface:** `192.168.22.1 / 255.255.255.0`  
**Server0:** `192.168.23.10 / 255.255.255.0`  
**R1 Server Interface:** `192.168.23.1 / 255.255.255.0`

## Solution

An extended ACL was created to block HTTP traffic to the web server:

```bash
access-list 101 deny tcp any host 192.168.23.10 eq 80
access-list 101 permit ip any any

```
The ACL was applied to the router interface connected to the server network:

interface gigabitEthernet 0/1
ip access-group 101 out

The first ACL rule blocks TCP traffic on port 80 (HTTP) to the web server, while the second rule permits all other IP traffic.

Verification

The ACL configuration was checked using:

show access-lists

## The result showed:

Extended IP access list 101
10 deny tcp any host 192.168.23.10 eq www (68 matches)
20 permit ip any any (4 matches)

The match count on the deny rule confirmed that HTTP traffic was being blocked.

Connectivity was tested using:

ping 192.168.23.10

Result: Ping continued to work because ICMP traffic was not blocked. ✅

HTTP access was tested from PC0 using:

http://192.168.23.10

Result: The web page was blocked by the ACL. ❌



## Result

The ACL successfully blocked HTTP traffic to the web server while allowing other IP traffic such as ICMP ping. The fault condition for NET-022 was successfully created and verified.

## What I Learned
How to create an extended ACL
How to block HTTP traffic using TCP port 80
How to apply an ACL to a router interface
How to use show access-lists for verification
How ACLs can selectively block specific types of network traffic
How to allow other traffic using permit ip any any