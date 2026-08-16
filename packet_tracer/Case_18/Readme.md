# NET-018 – Wrong Static Route

## Problem
The static route to the remote network was configured with the wrong next-hop address, making the remote network unreachable.

## Topology
- 2 Cisco 1941 Routers
- 2 Cisco 2960 Switches
- 2 PCs
- PC0 → Switch0 → R1
- R1 → R2
- R2 → Switch1 → PC1

## IP Configuration

**R1 LAN:** `192.168.17.1 / 255.255.255.0`

**R2 LAN:** `192.168.18.1 / 255.255.255.0`

**R1-R2 Link:**
- R1: `10.0.0.1 / 255.255.255.252`
- R2: `10.0.0.2 / 255.255.255.252`

**PC0:** `192.168.17.10 / 255.255.255.0`
- Default Gateway: `192.168.17.1`

**PC1:** `192.168.18.10 / 255.255.255.0`
- Default Gateway: `192.168.18.1`

## Fault Created

A static route was intentionally configured on R1 with the wrong next-hop address:

```bash
ip route 192.168.18.0 255.255.255.0 10.0.0.3
```

The correct next-hop address should be:

10.0.0.2

However, 10.0.0.3 was intentionally used to create the faulty scenario.

Verification of Fault

The routing table on R1 was checked using:

show ip route

## The output showed:

S    192.168.18.0/24 [1/0] via 10.0.0.3

This confirmed that the route points to the wrong next hop.

Connectivity from PC0 to the remote PC was tested using:

ping 192.168.18.10

The ping failed, confirming that the remote network was unreachable.

## Expected Fault Behavior

PC0 cannot successfully reach PC1 because R1 forwards traffic toward the incorrect next-hop address.

## Correction

The fault will be corrected later during the fault-correction phase.

The incorrect route will be removed:

no ip route 192.168.18.0 255.255.255.0 10.0.0.3

The correct static route will then be added:

ip route 192.168.18.0 255.255.255.0 10.0.0.2

After correction, connectivity will be tested using:

ping 192.168.18.10

The expected result will be:

Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
Screenshots
R1 Routing Table

PC0 Ping Test

## Result

NET-018 was successfully created with an intentionally incorrect static route. The routing table confirmed the wrong next-hop address, and the remote network was unreachable as expected.

The fault has been intentionally left unfixed for the later fault-correction phase.

## What I Learned
How static routes work
How to configure a static route using a next-hop address
How to verify routes using show ip route
How an incorrect next-hop address can make a remote network unreachable
How to test network connectivity using ping