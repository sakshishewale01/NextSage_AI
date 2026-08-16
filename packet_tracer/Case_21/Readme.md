# NET-021 – ACL Blocks Ping

## Problem
The network was working normally, but an Access Control List (ACL) was configured to block ICMP traffic. As a result, the PC could no longer ping the server.

## Topology
- 1 Cisco 1941 Router
- 2 Cisco 2960 Switches
- 1 PC
- 1 Server
- PC0 → Switch0 → R1 → Switch1 → Server0

## IP Configuration

**R1 G0/0:** `192.168.21.1 / 255.255.255.0`  
**R1 G0/1:** `192.168.22.1 / 255.255.255.0`

**PC0:** `192.168.21.10 / 255.255.255.0`  
**Default Gateway:** `192.168.21.1`

**Server0:** `192.168.22.10 / 255.255.255.0`  
**Default Gateway:** `192.168.22.1`

## Initial Verification

Before applying the ACL, connectivity between PC0 and Server0 was tested using:

```bash
ping 192.168.22.10

```

The result was:

Reply from 192.168.22.10
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)

This confirmed that the network was working correctly before the fault was introduced.

## Fault Creation

An extended ACL numbered 100 was created on R1 to deny ICMP traffic:

configure terminal
access-list 100 deny icmp any any
access-list 100 permit ip any any

The ACL was then applied to the interface connected toward the server LAN:

interface gigabitEthernet 0/1
ip access-group 100 out
exit
end
Verification

The ACL configuration was checked using:

show access-lists

The configuration contains:

Extended IP access list 100
    deny icmp any any
    permit ip any any

The applied ACL was verified using:

show running-config

The interface configuration contains:

interface GigabitEthernet0/1
 ip access-group 100 out
Fault Testing

After applying the ACL, PC0 attempted to ping the server again:

ping 192.168.22.10

## The result was:

Reply from 192.168.21.1: Destination host unreachable.
Packets: Sent = 4, Received = 0, Lost = 4 (100% loss)

The ping failure confirms that ICMP traffic is being blocked by the ACL.

Successful Ping Before ACL

Failed Ping After ACL

ACL Configuration

## Result

The ACL fault was successfully created. Before applying the ACL, PC0 could communicate with Server0 successfully. After applying ACL 100 to R1 GigabitEthernet0/1, ICMP traffic was denied and the ping from PC0 to Server0 failed with 100% packet loss.

## What I Learned
How Access Control Lists (ACLs) work
How to create an extended ACL
How to deny ICMP traffic using an ACL
How to permit other IP traffic using an ACL
How to apply an ACL to a router interface
How to verify ACL configuration using show access-lists
How to verify interface ACL configuration using show running-config
How to test the effect of an ACL using ping