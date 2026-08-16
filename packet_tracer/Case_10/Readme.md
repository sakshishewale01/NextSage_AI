## NET-010 – DHCP Pool Missing

## Problem
The DHCP pool was not initially present on the Cisco router.

## Topology
- 1 Cisco 1941 Router
- 1 Cisco 2960 Switch
- 1 PC
- PC0 → Switch → Router

## IP Configuration

**Router LAN Interface:** `192.168.10.1 / 255.255.255.0`

**PC0:** Configured to obtain an IP address using DHCP.

## Solution

The DHCP pool was intentionally left missing to create the required test-case condition.

The DHCP configuration was checked using:

```bash
show ip dhcp pool
```

No DHCP pool was displayed.

The running configuration was checked using:

```bash
show running-config
```

No matching DHCP pool configuration was present.

## Verification

PC0 was tested using:

```bash
ipconfig /release
ipconfig /renew
ipconfig
```

The result showed:

```text
DHCP request failed.
IPv4 Address : 0.0.0.0
Subnet Mask : 0.0.0.0
Default Gateway : 0.0.0.0
```

**Result:** The PC could not obtain a usable IP address because the DHCP pool was missing. ✅

## Screenshots

### DHCP Pool Verification



### Running Configuration Verification



### DHCP Failure on PC0



## Result

The missing DHCP pool condition was successfully created and verified. PC0 was unable to obtain an IP address through DHCP, confirming the NET-010 test case.

## What I Learned

- How to check DHCP pools using `show ip dhcp pool`
- How to verify router configuration using `show running-config`
- How DHCP provides IP addresses automatically
- How to identify a missing DHCP pool
- How to verify DHCP failure using `ipconfig`
