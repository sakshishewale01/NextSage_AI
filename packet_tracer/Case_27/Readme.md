# NET-027 – Wrong SSID

## Problem

The laptop cannot join the intended Wi-Fi network.

## Topology

- 1 Access Point
- 1 Laptop

## Configuration

The Access Point was configured with the SSID:

`CampusWiFi`

![AP SSID](screenshots/02-ap-ssid.png)

## Initial Connection

The laptop was able to connect successfully to the Access Point.

![Successful Connection](screenshots/03-connected.png)

## Fault Created

The Access Point SSID was changed to:

`WrongWiFi`

This created an SSID mismatch between the intended wireless network and the configured network.

![Wrong SSID](screenshots/04-wrong-ssid.png)

## Root Cause

The SSID was incorrect.

The laptop was intended to connect to:

`CampusWiFi`

but the Access Point was using:

`WrongWiFi`

Therefore, the laptop could not join the intended Wi-Fi network.

## Solution

The Access Point SSID was changed back to:

`CampusWiFi`

The laptop was then connected to the correct wireless network.

![Connection Successful](screenshots/05-connection-success.png)

## Result

The wireless connection was successfully restored by using the correct SSID.

## What I Learned

- SSID is the name of a Wi-Fi network.
- The correct wireless network must be selected.
- An incorrect SSID can prevent a device from joining the intended Wi-Fi network.
- Checking the wireless settings helps identify the problem.