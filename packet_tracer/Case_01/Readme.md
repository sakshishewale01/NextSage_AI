# NET-001 – Wrong Access VLAN

## Problem

Two PCs should communicate with each other because both are supposed to be in VLAN 10, but the ping fails because PC1's switch port is incorrectly assigned to VLAN 20.

## Topology

- 1 Cisco 2960 Switch
- 2 PCs
- PC0 → Fa0/1
- PC1 → Fa0/2

## IP Configuration

**PC0:** `192.168.10.10 / 255.255.255.0`  
**PC1:** `192.168.10.11 / 255.255.255.0`

Both PCs are in the same IP network.

## Correct VLAN Configuration

Both PC ports should belong to VLAN 10.

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

To create the troubleshooting problem, PC1's port `Fa0/2` was intentionally assigned to VLAN 20 instead of VLAN 10.

```bash
vlan 20
name WRONG_VLAN

interface fa0/2
switchport mode access
switchport access vlan 20
```

The resulting configuration was:

```text
PC0 → Fa0/1 → VLAN 10
PC1 → Fa0/2 → VLAN 20
```

Because the two PCs are in different VLANs and there is no router for inter-VLAN communication, PC0 cannot communicate with PC1.

## Symptom

PC0 cannot ping PC1.

The following command was used from PC0:

```bash
ping 192.168.10.11
```

**Result:** Ping failed. ❌

## Evidence Collection

The switch VLAN configuration was checked using:

```bash
show vlan brief
```

The actual output showed:

```text
10   STUDENTS     active   Fa0/1
20   WRONG_VLAN   active   Fa0/2
```

This confirms that PC1's port `Fa0/2` is assigned to the wrong VLAN.

## Expected Evidence

```text
VLAN 10 → Fa0/1
VLAN 20 → Fa0/2
```

PC1's port should have appeared under VLAN 10.

## Root Cause

**Wrong access VLAN.**

PC1's switch port `Fa0/2` was assigned to VLAN 20 instead of the required VLAN 10.

## OSI Layer

**Layer 2 – Data Link Layer**

## Concept

**VLAN / Access Port Configuration**

## Severity

**Low**

## Solution

PC1's switch port was moved back to VLAN 10:

```bash
interface fa0/2
switchport mode access
switchport access vlan 10
```

The configuration was then verified using:

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

The ping was successful after correcting the VLAN assignment. ✅

## Screenshots

### VLAN Configuration

_Add screenshot of the `show vlan brief` output showing Fa0/1 and Fa0/2 in VLAN 10._

### Fault Evidence

_Add screenshot of the `show vlan brief` output showing Fa0/1 in VLAN 10 and Fa0/2 in VLAN 20._

### Ping Failure

_Add screenshot showing the failed ping before fixing the VLAN._

### Ping Verification

_Add screenshot showing the successful ping after fixing the VLAN._

## Result

The wrong access VLAN was successfully identified using the `show vlan brief` command. PC1's port was incorrectly assigned to VLAN 20 instead of VLAN 10. After correcting the VLAN assignment, both PCs were placed in VLAN 10 and connectivity was successfully restored.

## Evidence Used

The troubleshooting decision was based on the actual Packet Tracer command:

```bash
show vlan brief
```

The command showed that:

```text
Fa0/1 → VLAN 10
Fa0/2 → VLAN 20
```

This evidence directly identified the wrong access VLAN.

## What I Learned

- How to create a VLAN
- How to assign switch ports to a VLAN
- How to identify a wrong access VLAN
- How to use `show vlan brief` as troubleshooting evidence
- How to test connectivity using `ping`
- How to fix an incorrect VLAN assignment
- How Layer 2 VLAN configuration can affect communication between PCs