# NetSage AI – Network Troubleshooting Assistant

> An AI-assisted network troubleshooting system that analyzes Cisco Packet Tracer evidence, identifies possible networking faults, suggests diagnostic commands and fixes, and keeps a human reviewer in the loop.

---

## 📌 Project Overview

NetSage AI is a network troubleshooting assistant designed to help identify common network configuration problems.

The project uses networking lab cases created in Cisco Packet Tracer. Each case contains a network topology, a problem or fault, observed symptoms, and troubleshooting evidence such as `show` command outputs.

The system analyzes this evidence using two approaches:

1. **Rule-Based Troubleshooting**
2. **AI-Assisted Diagnosis**

The rule-based system handles simple and predictable networking faults, while the AI component helps analyze more complex evidence and explain the possible root cause.

The final diagnosis is reviewed by a human before it is considered accepted.

---

## 🎯 Project Objective

The main objective of NetSage AI is to create a simple and practical network troubleshooting assistant that can:

- Collect real networking troubleshooting cases.
- Analyze Cisco Packet Tracer evidence.
- Identify common configuration problems.
- Suggest the probable root cause.
- Recommend the next diagnostic command.
- Suggest possible corrective steps.
- Provide an AI confidence score.
- Reference the evidence used for the diagnosis.
- Allow a human reviewer to accept, edit, or reject the AI diagnosis.
- Maintain a record of human corrections.
- Display troubleshooting information through a simple dashboard.

---

## 🧩 Problem Statement

Network troubleshooting can be difficult for beginners because a single connectivity problem can have many possible causes.

For example, if a PC cannot communicate with another device, the problem could be:

- Incorrect IP address
- Incorrect subnet mask
- Wrong default gateway
- Incorrect VLAN
- DHCP failure
- DNS problem
- Routing problem
- ACL blocking traffic
- NAT configuration problem
- Wireless configuration problem

A beginner may not know which command to execute first or how to interpret the output.

NetSage AI attempts to simplify this process.

Instead of only giving a final answer, the system aims to provide:

```text
Observed Problem
       ↓
Evidence
       ↓
Possible Root Cause
       ↓
Next Diagnostic Command
       ↓
Explanation
       ↓
Suggested Fix
       ↓
Human Review



System Architecture

The basic architecture of NetSage AI is:



                Cisco Packet Tracer
                        │
                        │
                        ▼
              Network Troubleshooting
                       Case
                        │
                        ▼
                Evidence Collection
                        │
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       Rule-Based Checker       AI Diagnosis
             │                     │
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                 Combined Result
                        │
                        ▼
                 Human Reviewer
                        │
             ┌──────────┼──────────┐
             │          │          │
             ▼          ▼          ▼
          Accepted    Edited     Rejected
             │          │          │
             └──────────┼──────────┘
                        ▼
                  Review Log
                        │
                        ▼
                   Dashboard