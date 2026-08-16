# NET-017 – Missing Static Route

## Problem

The remote network could not be reached because the required static routes were missing from the routers.

## Topology

- 2 Cisco 1941 Routers
- 2 Cisco 2960 Switches
- 2 PCs
- R1 → Switch0 → PC0
- R2 → Switch1 → PC1
- R1 → R2 using GigabitEthernet0/1

## IP Configuration

### R1

**GigabitEthernet0/0:** `192.168.17.1 / 255.255.255.0`  
**GigabitEthernet0/1:** `10.0.0.1 / 255.255.255.252`

### R2

**GigabitEthernet0/0:** `192.168.18.1 / 255.255.255.0`  
**GigabitEthernet0/1:** `10.0.0.2 / 255.255.255.252`

### PC0

**IP Address:** `192.168.17.10`  
**Subnet Mask:** `255.255.255.0`  
**Default Gateway:** `192.168.17.1`

### PC1

**IP Address:** `192.168.18.10`  
**Subnet Mask:** `255.255.255.0`  
**Default Gateway:** `192.168.18.1`

## Correct Connection Verification

The R1 and R2 interfaces were verified using:

```bash
show ip interface brief

R1 showed:

GigabitEthernet0/0    192.168.17.1    up    up
GigabitEthernet0/1    10.0.0.1        up    up

R2 showed:

GigabitEthernet0/0    192.168.18.1    up    up
GigabitEthernet0/1    10.0.0.2        up    up

The direct connection between R1 and R2 was tested using:

ping 10.0.0.2

from R1.

Result: 100% success. ✅

The reverse connection was also tested from R2:

ping 10.0.0.1

Result: 100% success. ✅

LAN Connectivity Verification

PC0 was able to reach its local router:

ping 192.168.17.1

Result: 4 packets received, 0% packet loss. ✅

PC1 was also configured with the R2 LAN gateway:

192.168.18.1
Fault Created

The required static routes between the two LAN networks were intentionally not configured.

R1 does not have a route to:

192.168.18.0/24

R2 does not have a route to:

192.168.17.0/24

Therefore, the remote network cannot be reached.

Verification

The routing table on R1 was checked using:

show ip route

R1 contained:

C    10.0.0.0/30 is directly connected, GigabitEthernet0/1
C    192.168.17.0/24 is directly connected, GigabitEthernet0/0

However, the following route was missing:

192.168.18.0/24

The routing table on R2 was also checked using:

show ip route

R2 contained:

C    10.0.0.0/30 is directly connected, GigabitEthernet0/1
C    192.168.18.0/24 is directly connected, GigabitEthernet0/0

However, the following route was missing:

192.168.17.0/24
Fault Verification

From PC0, connectivity to PC1 was tested using:

ping 192.168.18.10

The result was:

Reply from 192.168.17.1: Destination host unreachable.

Result: 4 packets sent, 0 packets received, 100% packet loss. ❌

This confirms that PC0 can reach its local router but cannot reach the remote LAN because the required static route is missing.

## Expected Fix

The missing route on R1 should be:

ip route 192.168.18.0 255.255.255.0 10.0.0.2

The missing route on R2 should be:

ip route 192.168.17.0 255.255.255.0 10.0.0.1

The fix is intentionally not applied in this test-case file because the purpose of this file is to preserve the faulty state for the AI troubleshooting dataset.


## Network Topology

R1-R2 Connectivity

PC0 Local Connectivity

Failed Remote Connectivity

R1 Routing Table

R2 Routing Table

## Result

The NET-017 – Missing Static Route fault was successfully created.

The routers and local networks are correctly configured, and the R1-R2 connection is working. However, the static routes to the remote LANs are missing from the routing tables.

As a result, PC0 cannot reach the remote PC1 network, reproducing the condition where the remote network cannot be reached because the required static route is missing.

## What I Learned
How to configure IP addresses on router interfaces
How to connect two routers using a point-to-point network
How to verify router interfaces using show ip interface brief
How to verify routing tables using show ip route
How static routes provide paths to remote networks
How a missing static route causes remote network connectivity failure
How to troubleshoot Layer 3 routing problems using ping