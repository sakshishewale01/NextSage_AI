# NET-030 – AP Connected to Wrong VLAN

## Problem

The Access Point is connected to the wrong VLAN on the switch.

Because of the incorrect VLAN configuration, the wireless laptop cannot communicate with the intended network.

---

## Topology

The topology contains:

- 1 Laptop
- 1 Access Point
- 1 Switch
- 1 Router

The basic connection is:

```text
Laptop
   )))
Wi-Fi
   ↓
Access Point
   |
   | Copper Straight-Through
   ↓
Switch
   |
   | Copper Straight-Through
   ↓
Router
 
---
```
Network Configuration
Router

## Router interface:

Interface: GigabitEthernet 0/0
IP Address: 192.168.10.1
Subnet Mask: 255.255.255.0
VLANs

## The required VLAN is:

 VLAN 10
 Name: STUDENTS

A second VLAN was created to demonstrate the fault:

 VLAN 20
 Name: WRONG_VLAN
 Access Point Configuration

The Access Point was configured with the wireless network:

SSID: CampusWiFi

The laptop connects to this wireless network.

## Problem Created

The Access Point was connected to Switch port Fa0/1.

The port was intentionally configured with the wrong VLAN:

Access Point
      ↓
Switch Fa0/1
      ↓
VLAN 20 ❌

However, the intended network was:

VLAN 10 – STUDENTS

Therefore, the Access Point was connected to the wrong VLAN.

## Evidence

The VLAN configuration was checked using:

show vlan brief

The command showed that the Access Point's switch port Fa0/1 was assigned to VLAN 20 instead of VLAN 10.

The switch interface status was also checked using:

show interfaces status
Root Cause

The root cause was an incorrect VLAN assignment on the switch port connected to the Access Point.

The configuration was:

Fa0/1 → VLAN 20 ❌

The required configuration was:

Fa0/1 → VLAN 10 ✅

## Solution

The Access Point's switch port was changed to VLAN 10.

## The following commands were used:

enable
configure terminal
interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit
end

After applying the configuration, the VLAN assignment was checked again using:

show vlan brief

The Access Point port was now correctly assigned to VLAN 10.

## Laptop Configuration

The laptop was connected to the Access Point using:

SSID: CampusWiFi

The laptop was configured with:

IP Address: 192.168.10.2
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.10.1
Connectivity Test

After correcting the VLAN configuration, connectivity was tested from the laptop.

The following command was used:

ping 192.168.10.1

The laptop successfully received replies from the router.

## Result

The problem was successfully resolved.

Before the fix:

Access Point
     ↓
Switch Fa0/1
     ↓
VLAN 20 ❌

After the fix:

Access Point
     ↓
Switch Fa0/1
     ↓
VLAN 10 ✅

The laptop was then able to communicate with the intended network.

## What I Learned

A switch port can be assigned to a specific VLAN.

The Access Point must be connected to the correct VLAN.

show vlan brief can be used to check VLAN assignments.

show interfaces status can be used to check switch port information.

switchport access vlan is used to assign an access port to a VLAN.

A wrong VLAN assignment can prevent devices from reaching the intended network.

Ping can be used to verify connectivity after fixing the configuration.
