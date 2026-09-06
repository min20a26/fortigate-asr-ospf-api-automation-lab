# Project 2 - Commands Used

This file records the main verification and troubleshooting commands used in the FortiGate + Cisco ASR OSPF and API Automation Lab.

## Cisco ASR - Interface Verification

```text
show ip interface brief
show running-config interface GigabitEthernet0/0/1
show running-config interface GigabitEthernet0/0/3
```

Verified addresses:

```text
GigabitEthernet0/0/1  192.168.30.110
GigabitEthernet0/0/3  192.168.40.1
```

## Cisco ASR - Routing and OSPF

```text
show ip route
show ip ospf neighbor
```

Verified OSPF neighbor:

```text
Neighbor ID: 2.2.2.2
State: FULL/DR
Address: 192.168.30.1
Interface: GigabitEthernet0/0/1
```

Verified dynamically learned default route:

```text
O*E2 0.0.0.0/0 via 192.168.30.1
```

Route code reminder:

```text
C     Connected network
L     Local interface address
O     OSPF-learned route
*     Candidate default route
E2    OSPF External Type 2
```

## Cisco ASR - Connectivity Testing

From the ASR:

```text
ping 192.168.40.10
```

The test completed successfully with a 100% success rate.

## Windows Workstation - Connectivity Testing

From PowerShell:

```powershell
ping 192.168.40.1
```

The repeat test completed with 0% packet loss.

To review IPv4 addressing:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
    Format-Table InterfaceAlias,IPAddress,PrefixLength
```

## SSH Access

Example format used to access the Cisco ASR:

```text
ssh <username>@192.168.30.110
```

Do not place real passwords in repository files.

## FortiGate - OSPF Verification

FortiGate CLI commands used during the routing recap:

```text
show router ospf
show full-configuration router ospf
```

The configuration confirmed:

```text
router-id 2.2.2.2
area 0.0.0.0
network 192.168.30.0/24
default-information-originate enable
default metric 10
metric type 2
```

## FortiGate - IPsec VPN Verification

Phase 1 and Phase 2 configuration were reviewed with:

```text
show full-configuration vpn ipsec phase1-interface
show full-configuration vpn ipsec phase2-interface
```

Address groups and selector objects were checked with:

```text
show firewall addrgrp ASR-VPN_local
show firewall addrgrp ASR-VPN_remote
show firewall address ASR-VPN_local_subnet_1
show firewall address ASR-VPN_remote_subnet_1
```

The protected subnets resolved to:

```text
Local:  192.168.50.0/24
Remote: 192.168.40.0/24
```

## FortiGate REST API Endpoint

```text
/api/v2/monitor/system/status
```

During PowerShell/cURL testing, the token was stored in a variable rather than written directly into documentation.

Example:

```powershell
curl.exe -k -H "Authorization: Bearer $token" `
  "https://192.168.30.1/api/v2/monitor/system/status"
```

`-k` was used only for this self-signed lab environment. Production systems should validate TLS certificates.

## Python Automation

Run the automation from a terminal:

```text
python fortigate_api.py
```

The script is stored at:

```text
automation/fortigate_api.py
```

It prompts for the API token at runtime and does not hardcode the credential.
