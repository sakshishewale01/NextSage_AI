# NET-019 – Router Interface Down

## Problem
A router interface was administratively shut down, causing the routed link between the two routers to stop communicating.

## Topology
- 2 Cisco 1941 Routers
- 2 Cisco 2960 Switches
- 2 PCs
- PC0 → Switch0 → R1
- R1 → R2
- R2 → Switch1 → PC1

## IP Configuration

**R1 LAN:** `192.168.19.1 / 255.255.255.0`

**R2 LAN:** `192.168.20.1 / 255.255.255.0`

**R1-R2 Link:**
- R1 GigabitEthernet0/1: `10.0.0.1 / 255.255.255.252`
- R2 GigabitEthernet0/1: `10.0.0.2 / 255.255.255.252`

**PC0:** `192.168.19.10 / 255.255.255.0`
- Default Gateway: `192.168.19.1`

**PC1:** `192.168.20.10 / 255.255.255.0`
- Default Gateway: `192.168.20.1`

## Initial Verification

Before creating the fault, the R1-R2 connection was tested from R1 using:

```bash
ping 10.0.0.2

``

The ping was successful:

Success rate is 100 percent (5/5)

This confirmed that the routed link was working before the fault was introduced.

Fault Created

The fault was intentionally created by administratively shutting down R1's GigabitEthernet0/1 interface:

enable
configure terminal
interface gigabitEthernet 0/1
shutdown
Fault Verification

The interface status was checked using:

do show ip interface brief

The output confirmed:

GigabitEthernet0/1    10.0.0.1    administratively down    down

This confirmed that the router interface was intentionally placed in the administratively down state.

Expected Fault Behavior

Because R1's GigabitEthernet0/1 interface is shut down, the connection between R1 and R2 cannot communicate.

Traffic from the R1 LAN toward the R2 LAN will therefore be unable to cross the router-to-router link.

## Correction

The fault will be corrected later during the fault-correction phase.

The interface can be restored using:

no shutdown

After restoring the interface, connectivity can be tested again using:

ping 10.0.0.2

The expected result after correction is:

Success rate is 100 percent
Screenshots
R1 Interface Down Verification

## Result

NET-019 was successfully created with R1's GigabitEthernet0/1 interface intentionally shut down. The show ip interface brief command confirmed that the interface was in the administratively down state.

The fault has been intentionally left unfixed for the later fault-correction phase.

## What I Learned
How to configure router interfaces
How to verify interface status using show ip interface brief
How the shutdown command administratively disables an interface
How an interface shutdown can interrupt routed communication
How to identify an administratively down interface
How to restore an interface using no shutdown