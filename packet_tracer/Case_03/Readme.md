# NET-003 – PCs in Different VLANs

## Problem

Two PCs should communicate with each other because both are supposed to be in VLAN 10, but the ping fails because the two PCs are assigned to different VLANs.

## Topology

- 1 Cisco 2960 Switch
- 2 PCs
- PC0 → Fa0/1
- PC1 → Fa0/2

## IP Configuration

**PC0:** `192.168.10.10 / 255.255.255.0`  
**PC1:** `192.168.10.11 / 255.255.255.0`

Both PCs are configured in the same IP network.

## Correct VLAN Configuration

Both PCs should be assigned to VLAN 10.

```bash
vlan 10
name STUDENTS

interface fa0/1
switchport mode access
switchport access vlan 10

interface fa0/2
switchport mode access
switchport access vlan 10
```

## Fault Introduced

To create the troubleshooting problem, PC1's switch port `Fa0/2` was intentionally assigned to VLAN 20 instead of VLAN 10.

```bash
vlan 20
name DIFFERENT_VLAN

interface fa0/2
switchport mode access
switchport access vlan 20
```

The resulting configuration was:

```text
PC0 → Fa0/1 → VLAN 10
PC1 → Fa0/2 → VLAN 20
```

Since the two PCs are in different VLANs and there is no router providing inter-VLAN routing, they cannot communicate with each other.

## Symptom

Two PCs that should communicate cannot ping each other.

The following command was used from PC0:

```bash
ping 192.168.10.11
```

**Result:** Ping failed. ❌

## Evidence Collection

The VLAN configuration was checked using:

```bash
show vlan brief
```

The actual output showed:

```text
10   STUDENTS          active   Fa0/1
20   DIFFERENT_VLAN    active   Fa0/2
```

This shows that the two PC ports are assigned to different VLANs.

## Expected Evidence

```text
Fa0/1 → VLAN 10
Fa0/2 → VLAN 20
```

Both ports should have been assigned to VLAN 10.

## Root Cause

**PCs are in different VLANs.**

PC0 is connected to VLAN 10 while PC1 is connected to VLAN 20. Because there is no inter-VLAN routing in the topology, the PCs cannot communicate.

## OSI Layer

**Layer 2 – Data Link Layer**

## Concept

**VLAN / Access Port Configuration**

## Severity

**Low**

## Solution

PC1's switch port `Fa0/2` was moved from VLAN 20 to VLAN 10:

```bash
interface fa0/2
switchport mode access
switchport access vlan 10
```

The VLAN configuration was then verified using:

```bash
show vlan brief
```

The corrected result was:

```text
10   STUDENTS   active   Fa0/1, Fa0/2
```

## Verification

Connectivity was tested again from PC0:

```bash
ping 192.168.10.11
```

The ping was successful after placing both PCs in VLAN 10. ✅

## Screenshots

### VLAN Configuration

_Add screenshot of the `show vlan brief` output showing Fa0/1 in VLAN 10 and Fa0/2 in VLAN 20._

### Ping Failure

_Add screenshot showing the failed ping before fixing the VLAN configuration._

### Corrected VLAN Configuration

_Add screenshot of the `show vlan brief` output showing Fa0/1 and Fa0/2 in VLAN 10._

### Ping Verification

_Add screenshot showing the successful ping after fixing the VLAN configuration._

## Result

The communication problem was successfully diagnosed as a Layer 2 VLAN configuration issue. The `show vlan brief` command showed that the two PC ports were assigned to different VLANs. After assigning both ports to VLAN 10, connectivity between the PCs was successfully restored.

## Evidence Used

The troubleshooting decision was based on the actual Packet Tracer command:

```bash
show vlan brief
```

The command showed:

```text
Fa0/1 → VLAN 10
Fa0/2 → VLAN 20
```

This evidence directly identified that the PCs were connected to different VLANs.

## What I Learned

- How to create multiple VLANs
- How to assign switch ports to different VLANs
- How different VLANs can prevent communication between PCs
- How to use `show vlan brief` for troubleshooting
- How to identify a Layer 2 VLAN problem
- How to correct an incorrect VLAN assignment
- How to verify connectivity using `ping`