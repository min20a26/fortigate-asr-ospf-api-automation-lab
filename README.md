
# FortiGate + Cisco ASR OSPF & API Automation Lab

## Project Overview

This project demonstrates the integration of a FortiGate 40F firewall with a Cisco ASR1001-X router in a physical home lab environment.

The lab focuses on dynamic routing with OSPF, routed network connectivity, FortiGate REST API access, Python automation, verification, and troubleshooting.

The goal was not only to establish connectivity, but also to understand how routing information is exchanged between network devices and how firewall management tasks can be accessed and automated programmatically.

## Technologies & Equipment

- Fortinet FortiGate 40F
- Cisco ASR1001-X
- Managed Ethernet switch
- Windows workstation
- macOS workstation
- Cisco IOS XE
- FortiOS
- OSPF
- REST API
- Python
- PowerShell
- SSH
- ICMP

## Lab Objectives

- Establish connectivity between the Cisco ASR and FortiGate environment
- Configure and verify routed interfaces
- Configure OSPF dynamic routing
- Establish an OSPF neighbor relationship
- Learn a default route through OSPF
- Verify routing using the Cisco routing table
- Test connectivity using ICMP
- Access the Cisco ASR securely through SSH
- Access the FortiGate REST API
- Authenticate API requests using an API token
- Retrieve FortiGate system information programmatically
- Build a Python script for FortiGate API automation
- Troubleshoot routing, API, authentication, and connectivity problems

## Network Addressing

| Device / Interface | IP Address | Purpose |
|---|---|---|
| FortiGate | 192.168.30.1 | FortiGate / routed gateway |
| Cisco ASR Gi0/0/1 | 192.168.30.110 | ASR connection toward FortiGate network |
| Cisco ASR Gi0/0/3 | 192.168.40.1 | Routed interface toward test workstation |
| Windows workstation | 192.168.40.10 | Test and management workstation |

## OSPF Dynamic Routing

OSPF was configured to allow dynamic route exchange between the Cisco ASR and the FortiGate environment.

The ASR successfully established an OSPF adjacency with the neighbor at:

`192.168.30.1`

Verification showed the neighbor in the `FULL/DR` state.

The Cisco routing table also showed the dynamically learned default route:

`O*E2 0.0.0.0/0 via 192.168.30.1`

This demonstrates that the default route was learned through OSPF as an External Type 2 route.

### OSPF Verification Commands

```text
show ip ospf neighbor
show ip route
show ip interface brief
```                


Connectivity Testing

Connectivity was verified at multiple points in the lab using ICMP.

Testing confirmed successful communication between the routed interfaces and workstation networks, including successful ping tests with 100% packet delivery during verification.

These tests helped confirm that interface addressing and routing were functioning correctly.

FortiGate REST API

The FortiGate REST API was tested from the Windows workstation.

API authentication was performed using a dedicated API token passed through the HTTP Authorization header.

A successful request to the FortiGate system status endpoint returned information including:

* Status: success
* Hostname: FortiGate-40F
* Model: 40F
* FortiOS version: v7.2.6
* Build: 1575

API credentials and tokens are intentionally excluded from this repository.

Python Automation

A Python script was created to automate the FortiGate API request.

Rather than storing the API token directly inside the source code, the script prompts for the token when executed.

The script retrieves FortiGate system information and displays selected results including:

* API request status
* Hostname
* FortiGate model
* FortiOS version
* Build number

This demonstrates a basic network automation workflow using Python and a firewall REST API.

Troubleshooting Experience

Several real-world issues were encountered and investigated during the project.

Examples included:

* Incorrect API protocol/connection attempts
* API authentication errors
* HTTP 401 Unauthorized responses
* HTTP 429 Too Many Requests responses
* API connectivity failures
* Python execution/path errors
* Secure token-input behavior in Python IDLE
* Routing and interface verification
* OSPF route and neighbor verification
* SSH compatibility requirements

Troubleshooting these problems was an important part of the project because it required identifying whether failures occurred at the physical, network, routing, authentication, application, or automation layer.

Security Considerations

Sensitive information is intentionally excluded from the public repository.

The following information should never be committed:

* FortiGate API tokens
* Passwords
* Pre-shared keys
* Private credentials
* Screenshots displaying active secrets

API tokens used during testing should be treated as credentials and protected accordingly.


Repository Structure

```
fortigate-asr-ospf-api-automation-lab/
│
├── README.md
├── automation/
│   └── fortigate_api.py
│
├── documentation/
│   ├── commands.md
│   └── troubleshooting.md
│
└── screenshots/
    └── project verification screenshots
   ``` 


Skills Demonstrated

This project demonstrates hands-on experience with:

* Network security
* Cisco routing
* FortiGate administration
* OSPF dynamic routing
* Routing-table analysis
* TCP/IP troubleshooting
* SSH administration
* REST APIs
* API authentication
* Python network automation
* PowerShell
* Connectivity testing
* Technical troubleshooting
* Security-conscious documentation

Key Result

The completed lab demonstrated successful communication between the Cisco ASR and FortiGate environment, an operational OSPF neighbor relationship, dynamic learning of the default route, successful FortiGate REST API communication, and successful retrieval of firewall system information through Python automation.

Project Status

Completed

This repository documents Project 2 of my hands-on network security and automation lab portfolio.


