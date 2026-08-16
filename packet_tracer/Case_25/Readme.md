# NET-025 – Wrong NAT Inside/Outside Interface

## Problem

Private network traffic is not being translated because the NAT inside and outside interfaces are configured incorrectly.

## Topology

```text
PC0 ─── Switch0 ─── Router0 ─── Server0

IP Addressing
PC0
IP Address:       192.168.10.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.10.1
Router0
G0/0: 192.168.10.1
G0/1: 192.168.20.1
Server0
IP Address:       192.168.20.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.20.1
Problem Creation

The NAT interfaces were intentionally configured incorrectly.

The private interface was configured as:

G0/0 → ip nat outside

The outside interface was configured as:

G0/1 → ip nat inside

The correct configuration should be:

G0/0 → ip nat inside
G0/1 → ip nat outside
Evidence

The router configuration was checked using:

show running-config

The NAT roles were found to be incorrect.

The NAT translation table was also checked using:

show ip nat translations

The expected NAT translation was not created.

Root Cause

The NAT inside and outside interfaces were reversed.

The private interface was incorrectly marked as outside, and the outside interface was incorrectly marked as inside.

Solution

The private interface was corrected:

interface gigabitEthernet 0/0
no ip nat outside
ip nat inside

The outside interface was corrected:

interface gigabitEthernet 0/1
no ip nat inside
ip nat outside
Verification

The router configuration was checked again using:

show running-config

The correct NAT roles were now visible.

Traffic was generated from PC0 using:

ping 192.168.20.10

The NAT translation table was checked again:

show ip nat translations

A NAT translation was now created.

Result

The wrong NAT inside/outside interface configuration was successfully identified and corrected.

After assigning the correct NAT roles, NAT translation worked correctly.

What I Learned
What NAT inside means.
What NAT outside means.
How to identify inside and outside interfaces.
How to check NAT configuration using show running-config.
How to check NAT translations using show ip nat translations.
Why incorrect NAT interface roles can prevent NAT translation.