# NET-029 – Wireless Client Gets No IP

## Problem

The laptop can connect to the wireless network, but it does not receive a usable IP address.

## Topology

- 1 Router
- 1 Access Point
- 1 Laptop

## Network Configuration

Router LAN IP:

`192.168.30.1`

Wireless SSID:

`CampusWiFi`

## Problem Created

The router interface was configured with an IP address, but DHCP was not configured.

Therefore, the laptop could connect to the Access Point but could not receive a usable IP address.

![Laptop No IP](screenshots/03-laptop-no-ip.png)

## Root Cause

The DHCP service was not configured for the wireless network.

The laptop requested an IP address, but there was no DHCP pool available to provide one.

## Solution

A DHCP pool was created on the router.

## text

ip dhcp pool WIFI

network 192.168.30.0 255.255.255.0

default-router 192.168.30.1

Result

The laptop successfully received an IP address from the DHCP server.

Example:

IPv4 Address: 192.168.30.x
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.30.1

Connectivity Test

The laptop successfully pinged the router.

Conclusion

The problem was caused by missing DHCP configuration.

After configuring DHCP on the router, the wireless client successfully received an IP address and communicated with the router.

## What I Learned

A device can connect to Wi-Fi without having a usable IP address.

DHCP automatically provides IP addresses to devices.

The router can be configured as a DHCP server.

ipconfig can be used to check the client's IP configuration.

ping can be used to test connectivity.