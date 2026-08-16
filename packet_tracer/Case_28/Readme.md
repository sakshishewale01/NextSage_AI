# NET-028 – Wrong Wi-Fi Password

## Problem

The laptop can see the Wi-Fi network but cannot authenticate because the wireless password is incorrect.

## Topology

- 1 Access Point
- 1 Laptop

## Access Point Configuration

SSID:

`CampusWiFi`

Wi-Fi Password:

`Cisco123`

![AP Security](screenshots/02-ap-security.png)

## Problem Created

The laptop was configured with the wrong Wi-Fi password:

`Wrong123`

The password did not match the password configured on the Access Point.

![Wrong Password](screenshots/03-wrong-password.png)

## Observed Problem

The laptop could see the Wi-Fi network but authentication failed because the password was incorrect.

![Authentication Failed](screenshots/04-authentication-failed.png)

## Root Cause

The wireless client was using a different password from the Access Point.

```text
Access Point Password: Cisco123
Laptop Password: Wrong123

Solution

The laptop password was changed to the correct password:

Cisco123

Result

The laptop successfully authenticated and connected to the Access Point.

What I Learned
A Wi-Fi network can be visible even when the password is incorrect.
The wireless client must use the correct security key/password.
If the password does not match the Access Point, authentication fails.
Entering the correct Wi-Fi password restores the connection.