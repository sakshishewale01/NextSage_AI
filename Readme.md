# 🛜 NetSage AI — AI-Powered Network Troubleshooting Assistant

> **Project 2 | Applied AI + Network Troubleshooting**

NetSage AI is an **AI-assisted network troubleshooting helper** designed for Cisco-style networking labs and Packet Tracer scenarios.

The system takes **network symptoms, topology notes, and `show` command outputs** as input and uses AI to identify a likely root cause, determine the relevant OSI layer, recommend the next troubleshooting command, and suggest evidence-backed fix steps.

A key feature of NetSage AI is **Human-in-the-Loop (HITL) review** — every AI diagnosis must be reviewed and either **Accepted, Edited, or Rejected** by a human before the proposed fix is considered valid.

---

# 🔎 Overview

Junior network engineers often understand individual networking commands but may struggle to connect a **network symptom** with its actual **root cause**.

For example:

> A PC successfully receives an IP address but cannot communicate with a server.

Several possible causes may exist:

* VLAN configuration
* Default gateway
* DHCP
* DNS
* Routing
* ACL
* NAT
* Wireless configuration

NetSage AI helps narrow down these possibilities by combining **AI-based reasoning with deterministic network checks**.

The assistant analyzes the available evidence and provides:

1. Likely root cause
2. Confidence level
3. Evidence supporting the diagnosis
4. Relevant OSI layer
5. Next troubleshooting command
6. Recommended fix steps

The project requires human review for every diagnosis to ensure that AI-generated recommendations are not blindly applied.

---

# 🎯 Problem Statement

Network troubleshooting in lab environments can become difficult when multiple networking components interact with each other.

For example:

```text
PC
 ↓
Switch
 ↓
Router
 ↓
Server
```

If the PC receives an IP address but cannot reach the server, the engineer needs to determine whether the problem is related to:

```text
VLAN
Gateway
DHCP
DNS
Routing
ACL
NAT
Wireless
```

NetSage AI provides an AI-assisted troubleshooting workflow that connects:

```text
Symptom
   ↓
Network Evidence
   ↓
Rule Checks
   ↓
AI Diagnosis
   ↓
Human Review
   ↓
Fix
   ↓
Verification
```

---

# 🎯 Objectives

The main objectives of NetSage AI are:

* Build an AI-assisted troubleshooting assistant for Cisco-style networks.
* Create a dataset containing at least 30 network troubleshooting cases.
* Use actual network evidence such as `show` command outputs.
* Develop structured AI prompts for consistent diagnosis.
* Create a deterministic Python rule checker.
* Identify likely root causes and relevant OSI layers.
* Recommend the next command required for troubleshooting.
* Provide evidence-backed troubleshooting steps.
* Introduce Human-in-the-Loop review.
* Record AI mistakes and human corrections.
* Create a dashboard showing issue categories and AI-human agreement.
* Demonstrate the complete troubleshooting process on a broken lab network.

The official project requirements specify at least **30 cases** and coverage across VLAN, gateway, DHCP, DNS, routing, ACL, NAT, and wireless issues.

---

# ✨ Key Features

## 1. 🧠 AI-Based Diagnosis

NetSage AI analyzes the provided network symptoms and evidence to suggest a probable root cause.

Example:

```text
Root Cause:
Inter-VLAN routing or ACL configuration issue

Confidence:
Medium

Evidence:
Gateway ping succeeds but server communication fails.

Next Command:
show ip route
```

---

## 2. 🔍 Evidence-Based Troubleshooting

The AI should not simply guess the answer.

It should refer to actual evidence such as:

```text
show ip route
show access-lists
show interfaces trunk
show vlan brief
show ip interface brief
```

The project specifically requires AI responses to reference actual `show` command evidence.

---

## 3. 🐍 Rule-Based Network Checker

A Python script performs deterministic checks for common configuration mistakes.

The checker is designed to identify problems such as:

* Duplicate IP addresses
* Incorrect subnet masks
* Gateway mismatch
* Interface down
* Missing VLAN
* Missing routes

These checks provide a deterministic layer before or alongside the AI diagnosis.

---

## 4. 👨‍💻 Human-in-the-Loop Review

AI output is **not automatically accepted**.

Every diagnosis is reviewed by a human.

The reviewer can mark the diagnosis as:

```text
Accepted
Edited
Rejected
```

If the AI is incorrect, the reviewer records:

* What the AI suggested
* What was actually wrong
* Why the AI diagnosis was incorrect
* What the corrected diagnosis should be

---

## 5. 📊 Troubleshooting Dashboard

The dashboard provides a simple summary of:

* Issue types
* Severity
* Number of cases
* AI diagnosis results
* Human corrections
* AI-human agreement rate

Example:

```text
Total Cases        : 30+
AI Accepted        : 22
AI Edited          : 5
AI Rejected        : 3

Agreement Rate     : 73.3%
```

---

## 6. 🛡️ Responsible AI Logging

NetSage AI maintains a record of situations where AI needed human correction.

At least **5 corrected AI cases** are documented as part of the project.

This demonstrates that AI is being used as an **assistant rather than an unquestioned authority**.

---

# 🔄 System Workflow

The complete workflow is:

```text
                ┌──────────────────────┐
                │  Packet Tracer Case  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Network Symptoms     │
                │ Topology Notes       │
                │ Show Commands        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Python Rule Checker  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   AI Diagnosis       │
                └──────────┬───────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Root Cause              │
              │ Confidence              │
              │ Evidence                │
              │ OSI Layer               │
              │ Next Command            │
              │ Fix Steps               │
              └────────────┬────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Human Reviewer     │
                └──────────┬───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Accepted       Edited      Rejected
              │            │            │
              └────────────┼────────────┘
                           ▼
                ┌──────────────────────┐
                │ Fix & Verification   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Dashboard / Logging  │
                └──────────────────────┘
```

---

# 🏗️ Architecture

NetSage AI consists of five major components:

```text
┌────────────────────────────────────────────┐
│               NetSage AI                   │
├────────────────────────────────────────────┤
│                                            │
│  1. Case Dataset                            │
│          ↓                                 │
│  2. Rule-Based Checker                     │
│          ↓                                 │
│  3. AI Prompt / Diagnosis Engine            │
│          ↓                                 │
│  4. Human Review System                    │
│          ↓                                 │
│  5. Dashboard & Responsible AI Logs        │
│                                            │
└────────────────────────────────────────────┘
```

---

# 🌐 Network Issues Covered

The troubleshooting dataset covers multiple common network fault categories.

| Issue    | Example Problem                              |
| -------- | -------------------------------------------- |
| VLAN     | Incorrect VLAN assignment                    |
| Gateway  | Incorrect default gateway                    |
| DHCP     | Client fails to obtain correct configuration |
| DNS      | Domain resolution failure                    |
| Routing  | Missing or incorrect route                   |
| ACL      | Traffic blocked by access-control rule       |
| NAT      | Incorrect address translation                |
| Wireless | Incorrect wireless/VLAN configuration        |

The project specification explicitly asks for cases covering these categories.

---

# 📂 Case Dataset

The project includes a dataset containing **at least 30 troubleshooting cases**.

Each case contains structured information such as:

```text
Case ID
Symptom
Topology Note
Show Command Output
Expected Fault
OSI Layer
Concept
Severity
```

Example:

```csv
case_id,symptom,expected_fault,osi_layer,concept,severity
NET001,PC cannot reach server,ACL blocking traffic,Layer 3/4,ACL,High
NET002,PC has wrong IP,DHCP configuration,Layer 3,DHCP,Medium
NET003,Inter-VLAN communication fails,Missing route,Layer 3,Routing,High
```

The required submission format includes symptom, show outputs, expected fault, OSI layer, concept, and severity.

---

# 🤖 AI Prompt Library

The AI diagnosis uses structured prompts designed to produce consistent results.

The prompt forces the model to return fields such as:

```json
{
  "root_cause": "",
  "confidence": "",
  "evidence": [],
  "osi_layer": "",
  "next_command": "",
  "fix_steps": []
}
```

## Required AI Output

### Root Cause

The most likely networking problem.

### Confidence

Example:

```text
High
Medium
Low
```

### Evidence

The actual information from the supplied network outputs supporting the diagnosis.

### OSI Layer

The networking layer associated with the problem.

### Next Command

The next Cisco troubleshooting command that should be executed.

### Fix Steps

Recommended steps to resolve the issue.

The project requires structured prompts that return fields including `root_cause`, `confidence`, `evidence`, `next_command`, and `fix_steps`.

---

# 🐍 Rule-Based Checker

The Python rule checker provides deterministic validation.

## Checks Performed

### Duplicate IP Detection

Identifies multiple devices configured with the same IP address.

```text
Device A → 192.168.1.10
Device B → 192.168.1.10

Result:
Duplicate IP detected
```

### Subnet Mask Validation

Checks whether the configured subnet mask is appropriate for the expected network.

### Gateway Validation

Checks whether the device's default gateway matches the expected network.

### Interface Status

Checks whether an interface is administratively or operationally down.

### VLAN Validation

Checks whether the required VLAN exists.

### Route Validation

Checks whether a required route exists in the routing table.

---

# 🧠 AI Diagnosis Process

For every troubleshooting case:

```text
1. Load Case
      ↓
2. Read Symptom
      ↓
3. Read Topology
      ↓
4. Analyze Show Output
      ↓
5. Run Rule Checker
      ↓
6. Send Evidence to AI
      ↓
7. Generate Structured Diagnosis
      ↓
8. Compare with Expected Fault
      ↓
9. Human Review
      ↓
10. Record Result
```

The project workflow requires the AI response to be saved and compared against the known correct answer.

---

# 👨‍💻 Human Review

Human review is one of the most important parts of NetSage AI.

The reviewer evaluates the AI diagnosis and selects one of three outcomes:

| Status   | Meaning                                                     |
| -------- | ----------------------------------------------------------- |
| Accepted | AI diagnosis is correct                                     |
| Edited   | AI diagnosis is partially correct but requires modification |
| Rejected | AI diagnosis is incorrect                                   |

Example:

```text
AI Diagnosis:
Missing route to VLAN 30

Human Review:
Edited

Correction:
ACL rule was blocking traffic.

Reason:
Routing table contained the correct route.
```

This creates an audit trail for AI decisions.

---

# 📊 Dashboard

The dashboard summarizes the collected troubleshooting cases.

## Suggested Metrics

```text
Total Cases
───────────
30+

Issue Categories
────────────────
VLAN
DHCP
DNS
Routing
ACL
NAT
Gateway
Wireless

AI Review Results
─────────────────
Accepted
Edited
Rejected

AI-Human Agreement
──────────────────
Agreement Rate %
```

The required dashboard can be implemented as a spreadsheet or a simple chart.

---

# 🛡️ Responsible AI

NetSage AI follows a **Human-in-the-Loop** approach.

The system does not automatically apply configuration changes based only on AI output.

Instead:

```text
AI Suggestion
      ↓
Human Verification
      ↓
Approval / Correction
      ↓
Fix
      ↓
Verification
```

At least five cases where the AI diagnosis was corrected by a human are documented.

This helps identify:

* AI hallucinations
* Incorrect assumptions
* Insufficient evidence
* Misinterpretation of command output
* Incorrect root-cause identification

---

# 📁 Project Structure

A suggested repository structure is:

```text
NetSage-AI/
│
├── README.md
│
├── data/
│   └── cases.csv
│
├── prompts/
│   ├── diagnose_prompt.md
│   └── helper_prompts.md
│
├── checker/
│   ├── rule_checker.py
│   └── sample_output.txt
│
├── ai/
│   ├── diagnosis.py
│   └── responses/
│
├── dashboard/
│   ├── dashboard.xlsx
│   └── charts/
│
├── responsible_ai/
│   └── review_log.csv
│
├── examples/
│   └── sample_case/
│
└── demo/
    └── demo_video_link.txt
```

---

# 🛠️ Technology Stack

## Programming

* Python

## AI

* Generative AI / LLM
* Structured prompting
* JSON-based AI responses

## Networking

* Cisco Packet Tracer
* Cisco IOS-style commands
* OSI model
* VLAN
* DHCP
* DNS
* Routing
* ACL
* NAT
* Wireless networking

## Data

* CSV
* JSON

## Visualization

* Spreadsheet charts or simple dashboard

---

# 📥 Input

NetSage AI accepts information such as:

```text
Network Symptom
Topology Notes
Packet Tracer Information
Show Command Outputs
```

Example:

```text
Symptom:
PC in VLAN 30 can ping its gateway but cannot reach the server.

Topology:
PC → Switch → Router → Server

Show Output:
show ip route
show access-lists
show interfaces trunk
```

---

# 📤 Output

The AI produces a structured diagnosis:

```json
{
  "root_cause": "Possible inter-VLAN routing or ACL issue",
  "confidence": "Medium",
  "osi_layer": "Layer 3/4",
  "evidence": [
    "Gateway ping succeeds",
    "Server is unreachable"
  ],
  "next_command": [
    "show ip route",
    "show access-lists",
    "show interfaces trunk"
  ],
  "fix_steps": [
    "Verify routing configuration",
    "Check ACL rules",
    "Verify trunk configuration"
  ]
}
```

---

# 🧪 Example Diagnosis

### Scenario

```text
Symptom:
PC gets IP but cannot reach server in VLAN 30.

Gateway:
Ping successful.
```

### NetSage AI Diagnosis

```text
Likely Cause:
Inter-VLAN routing or ACL issue.

OSI Layer:
Layer 3/4

Confidence:
Medium

Next Commands:
show ip route
show access-lists
show interfaces trunk
```

### Human Review

```text
Status:
Accepted

Reason:
The recommended commands provide the appropriate
evidence needed to confirm the suspected routing/ACL issue.
```

This follows the example diagnosis provided in the project specification.

---

# 📦 Deliverables

The project requires the following deliverables:

| Deliverable          | Description                       |
| -------------------- | --------------------------------- |
| `cases.csv`          | All troubleshooting cases         |
| `diagnose_prompt.md` | Main AI diagnosis prompt          |
| Helper prompts       | Additional prompt templates       |
| Python checker       | Deterministic validation script   |
| Dashboard            | Issue summary and AI agreement    |
| Responsible AI log   | At least 5 corrected AI responses |
| Demo video           | 5–10 minute project demonstration |

These deliverables are specified in the official project document.

---

# 🎥 Demo

The project demonstration should show the complete troubleshooting lifecycle:

```text
Broken Network
      ↓
Identify Symptoms
      ↓
Collect Show Outputs
      ↓
Run Rule Checker
      ↓
AI Diagnosis
      ↓
Human Review
      ↓
Apply Fix
      ↓
Verify Network
      ↓
Update Dashboard
```

The required demo video duration is **5–10 minutes**.

---

# ✅ Evaluation Criteria

NetSage AI is evaluated on:

### Case Coverage

At least **30 troubleshooting cases** covering multiple network fault types.

### Evidence Usage

AI responses must reference actual network evidence.

### Human Oversight

The review log must contain:

```text
Accepted
Edited
Rejected
```

diagnoses.

### Deterministic Checks

The Python rule checker should correctly identify basic configuration errors.

### Responsible AI

At least five cases must demonstrate situations where AI required human correction.

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/NetSage-AI.git
```

Navigate to the project:

```bash
cd NetSage-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

## Step 1 — Prepare a Case

Add the network problem to:

```text
data/cases.csv
```

Include:

```text
Symptom
Topology
Show Outputs
Expected Fault
OSI Layer
Concept
Severity
```

---

## Step 2 — Run the Rule Checker

```bash
python checker/rule_checker.py
```

The checker analyzes common configuration mistakes.

---

## Step 3 — Run AI Diagnosis

Provide the case information to the AI diagnosis component.

The AI generates:

```text
Root Cause
Confidence
Evidence
OSI Layer
Next Command
Fix Steps
```

---

## Step 4 — Human Review

Review the generated diagnosis and mark it:

```text
Accepted
Edited
Rejected
```

---

## Step 5 — Fix and Verify

After human approval:

```text
Apply Fix
   ↓
Run Verification Commands
   ↓
Check Connectivity
```

---

## Step 6 — Update Dashboard

Record the result and update:

```text
Issue Type
Severity
AI Result
Human Result
Agreement
```

---

# 📈 Future Scope

Possible future improvements include:

* Integration with live Cisco devices.
* Automated collection of `show` command outputs.
* Interactive web-based troubleshooting interface.
* Real-time network monitoring.
* More advanced network configuration validation.
* Larger troubleshooting dataset.
* Retrieval-Augmented Generation (RAG) using Cisco documentation.
* Historical troubleshooting case retrieval.
* Automated topology analysis.
* Network configuration comparison.
* Improved confidence scoring.
* Multi-agent troubleshooting architecture.
* Automated verification after applying a fix.

---

# 🔐 Safety Principle

NetSage AI follows a simple principle:

> **AI recommends. Humans decide.**

The system is designed to assist network engineers rather than replace human judgment.

Every diagnosis should be supported by network evidence and reviewed by a human before the fix is accepted.

---

# 👥 Team

**Project:** NetSage AI
**Domain:** Applied AI + Network Troubleshooting
**Environment:** Cisco-style Networking Labs
**Team Member 1 :** Sakshi Shewale
**Team Member 2 :** Rajnandani Shinde
**Team Member 3 :** Shruti Thorat
**Team Member 4 :** Vedangi Patil

---

# 📌 Project Summary

NetSage AI combines:

```text
Networking
     +
Artificial Intelligence
     +
Python
     +
Rule-Based Validation
     +
Human Review
     +
Responsible AI
```

to create an AI-assisted troubleshooting workflow for Cisco-style lab networks.

The goal is not simply to make an AI guess the network problem. Instead, the project focuses on **evidence-based diagnosis, deterministic validation, human oversight, and responsible use of AI**.

---

## ⭐ Key Takeaway

```text
                 NETSAGE AI

       Network Problem / Symptom
                  │
                  ▼
          Collect Evidence
                  │
                  ▼
        Python Rule Checker
                  │
                  ▼
            AI Diagnosis
                  │
                  ▼
          Evidence + Confidence
                  │
                  ▼
           Human Review
          ┌───────┼───────┐
          ▼       ▼       ▼
       Accept   Edit   Reject
          │       │       │
          └───────┼───────┘
                  ▼
              Fix Issue
                  │
                  ▼
             Verify Fix
                  │
                  ▼
              Dashboard
```

**NetSage AI — Making network troubleshooting smarter, evidence-driven, and human-controlled.** 🚀
