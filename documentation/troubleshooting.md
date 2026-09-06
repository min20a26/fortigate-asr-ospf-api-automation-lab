# Project 2 - Troubleshooting

This document summarizes the main troubleshooting scenarios from the FortiGate + Cisco ASR OSPF and API Automation Lab and the method used to isolate each issue.

## 1. Verify the Physical and Interface Layer First

Before changing routing or firewall settings, interface state and addressing were checked.

Cisco ASR:

```text
show ip interface brief
```

Windows:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
    Format-Table InterfaceAlias,IPAddress,PrefixLength
```

Verified key addresses:

- ASR Gi0/0/1: `192.168.30.110`
- ASR Gi0/0/3: `192.168.40.1`
- Windows Ethernet 2: `192.168.40.10/24`

This prevented higher-layer troubleshooting from being performed on top of an incorrect interface or IP configuration.

## 2. Direct Connectivity Test

The Windows workstation tested the directly connected ASR interface:

```powershell
ping 192.168.40.1
```

The first test showed one initial timeout followed by replies. A repeat test returned four successful replies with 0% loss.

Because the second test was clean and the ASR could also ping the workstation successfully, the initial loss was treated as transient neighbor/ARP resolution rather than a persistent routing problem.

From the ASR:

```text
ping 192.168.40.10
```

Result: 100% success.

## 3. OSPF Neighbor Troubleshooting

OSPF was verified independently from IP reachability.

```text
show ip ospf neighbor
show ip route
```

The final verified neighbor was:

```text
Neighbor ID 2.2.2.2
State       FULL/DR
Address     192.168.30.1
Interface   GigabitEthernet0/0/1
```

The routing table also showed:

```text
O*E2 0.0.0.0/0 via 192.168.30.1
```

This proved two separate things:

1. The OSPF adjacency formed successfully.
2. The FortiGate advertised a default route that the ASR installed as OSPF External Type 2.

When the Cisco ASR was powered off, the FortiGate neighbor naturally disappeared. That behavior is expected and is different from a configuration failure.

## 4. FortiGate OSPF Configuration Review

On the FortiGate, Advanced Routing had to be visible in the GUI before OSPF could be reviewed.

The working configuration included:

- Router ID `2.2.2.2`
- Area `0.0.0.0`
- Network `192.168.30.0/24`
- Neighbor `192.168.30.110`
- Default route injection enabled for regular areas
- Metric type 2
- Metric 10

An important lesson was that forming an OSPF adjacency and advertising a route are separate functions. The network/area configuration allowed the neighbor relationship to form, while default-route injection created the `O*E2` default route on the ASR.

## 5. IPsec VPN Verification

The VPN was reviewed at both Phase 1 and Phase 2.

The FortiGate configuration confirmed:

- Remote peer `192.168.30.110`
- Outgoing interface VLAN20
- Pre-shared-key authentication
- IKEv1 / Main mode
- AES256-SHA256
- DH group 14
- Local selector `192.168.50.0/24`
- Remote selector `192.168.40.0/24`

A key conceptual distinction was:

- `192.168.30.0/24` = transport/underlay network used by the VPN peers
- `192.168.50.0/24` and `192.168.40.0/24` = protected networks carried by the VPN configuration

The actual pre-shared key is intentionally excluded from the repository.

## 6. Firewall Policy Review

FortiGate policies were checked to make sure traffic was allowed in both VPN directions.

The VPN policy pairs used:

- `ASR-VPN` -> `VLAN50`
- `VLAN50` -> `ASR-VPN`

NAT was disabled on the VPN policies. This preserves the private source and destination addresses rather than translating them before encrypted traffic processing.

## 7. REST API Authentication Troubleshooting

API testing produced authentication/request errors before the final successful result.

Observed responses included:

```text
401 Unauthorized
429 Too Many Requests
```

The troubleshooting process checked:

- Correct FortiGate IP address
- Correct API endpoint
- Correct `Authorization: Bearer ...` header format
- Valid API token
- Request frequency
- HTTPS/self-signed-certificate behavior

The endpoint used was:

```text
/api/v2/monitor/system/status
```

After correcting the request/authentication flow, the API returned `status: success`.

## 8. Separate API Problems from Python Problems

PowerShell/cURL testing was performed before relying on the Python script.

This was useful because a successful manual API request proved that:

- The workstation could reach the FortiGate.
- HTTPS was working.
- The API endpoint was valid.
- The token was accepted.

Only after those points were verified was Python automation treated as the next troubleshooting layer.

## 9. Python Automation Troubleshooting

The Python script was checked for:

- Correct FortiGate URL
- Correct REST endpoint
- Authorization header
- JSON parsing
- Runtime API-token entry
- Script filename and path
- Python execution environment

The token is requested at runtime with `getpass()` instead of being stored in the script.

The script uses an unverified SSL context because the home lab uses a self-signed certificate. This is acceptable for this controlled demonstration but should not be copied into production practice.


## 10. MacBook Management Access

The MacBook Air was used as a separate management workstation for FortiGate GUI administration and project documentation. During the lab, browser access to the FortiGate GUI was also part of troubleshooting, which helped distinguish a browser/certificate behavior issue from a network reachability problem.

This provided a useful second management path independent of the Windows workstation used for ASR connectivity and API/Python testing.

## 11. Command Syntax Errors

One troubleshooting screenshot shows a PowerShell command entered without the required space:

```text
ping192.168.40.1
```

PowerShell correctly returned `CommandNotFoundException`.

The command was corrected to:

```text
ping 192.168.40.1
```

This is a useful reminder to distinguish a command-syntax problem from a network problem before changing device configuration.

## Troubleshooting Method Used

The project reinforced this sequence:

1. Verify cabling and device power.
2. Verify interface state.
3. Verify IP addressing and subnet masks.
4. Test direct Layer 3 reachability.
5. Inspect the routing table.
6. Verify OSPF neighbor state.
7. Verify route advertisement separately from adjacency.
8. Review firewall/VPN policy and selectors.
9. Test the REST API independently.
10. Verify authentication.
11. Run the Python automation.
12. Confirm management access from the MacBook Air.
13. Document the final evidence.

This layered approach made it easier to identify whether a failure belonged to the physical, IP, routing, firewall, VPN, authentication, API, or automation layer.
