# NET-020 – Missing Default Route

## Problem
The default route was missing on the edge router, so the PC could communicate with its local router but could not reach the remote network.

## Topology
- 2 Cisco 1941 Routers
- 2 Cisco 2960 Switches
- 2 PCs
- PC0 → Switch0 → R1
- R1 → R2
- R2 → Switch1 → PC1

## IP Configuration

**PC0:** `192.168.20.10 / 255.255.255.0`  
**R1 G0/0:** `192.168.20.1 / 255.255.255.0`  
**R1 G0/1:** `10.0.0.1 / 255.255.255.252`  
**R2 G0/1:** `10.0.0.2 / 255.255.255.252`  
**R2 G0/0:** `172.16.0.1 / 255.255.255.0`  
**PC1:** `172.16.0.10 / 255.255.255.0`

## Solution

The network was configured with two routers connected through the `10.0.0.0/30` network.

R1 was configured with:

```bash
interface gigabitEthernet 0/0
ip address 192.168.20.1 255.255.255.0
no shutdown

```

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.252
no shutdown

R2 was configured with:

interface gigabitEthernet 0/0
ip address 172.16.0.1 255.255.255.0
no shutdown


interface gigabitEthernet 0/1
ip address 10.0.0.2 255.255.255.252
no shutdown

The default route was intentionally left missing on R1 to demonstrate the fault.

Verification

The R1-R2 connection was tested using:

ping 10.0.0.2

Result: Successful connectivity between R1 and R2. ✅

PC0 was tested against its local gateway:

ping 192.168.20.1

Result: 4 packets received, 0% packet loss. ✅

The remote network was then tested:

ping 172.16.0.10

The result was:

Reply from 192.168.20.1: Destination host unreachable.

Result: 4 packets lost, 100% loss. ❌

The routing table on R1 was checked using:

show ip route

The routing table showed that no default route was configured.

R1 Routing Table

PC0 Local Gateway Ping

Remote Network Ping Failure

## Result

The missing default route fault was successfully created and demonstrated. PC0 could communicate with its local router, and R1 could communicate with R2, but PC0 could not reach the remote network because R1 did not have a default route.

## What I Learned
How routers use routing tables to forward packets
How to configure router interfaces
How to verify routes using show ip route
How a missing default route can prevent communication with unknown networks
How to test connectivity using ping
How to identify a routing problem from a Destination host unreachable message