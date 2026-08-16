# NET-026 – NAT ACL Wrong

## Problem

One private PC is translated by NAT, but another private PC is not translated.

## Topology

```text
PC0 ──┐
      │
PC1 ──┼── Switch0 ── Router0 ── Server0

IP Addressing
PC0
IP Address:       192.168.10.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.10.1
PC1
IP Address:       192.168.10.11
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

The NAT ACL was intentionally configured to allow only PC0:

access-list 1 permit host 192.168.10.10

Therefore:

PC0 → NAT allowed
PC1 → NAT not allowed
Evidence

The ACL was checked using:

show access-lists

The ACL only allowed PC0.

Traffic was generated from both PCs and the NAT table was checked using:

show ip nat translations

PC0 produced a NAT translation, while PC1 was not included because it was not permitted by the ACL.

Root Cause

The NAT ACL did not include PC1.

The ACL only permitted:

192.168.10.10

but PC1 had:

192.168.10.11

Therefore, PC1 did not match the NAT ACL.

Solution

The incorrect ACL was removed:

no access-list 1

A new ACL was created for the complete private network:

access-list 1 permit 192.168.10.0 0.0.0.255

This allows both PC0 and PC1 to be translated.

Verification

The corrected ACL was checked using:

show access-lists

Traffic was generated from PC1:

ping 192.168.20.10

The NAT translation table was checked again:

show ip nat translations

PC1 was now eligible for NAT translation.

Result

The NAT ACL mismatch was successfully identified and corrected.

Initially, the ACL allowed only PC0. After changing the ACL to allow the complete private network, both PCs were allowed to participate in NAT.

What I Learned
What a NAT ACL does.
How an ACL controls which private addresses are translated.
How to check an ACL using show access-lists.
How to check NAT translations using show ip nat translations.
How to correct a NAT ACL mismatch.