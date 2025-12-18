# Technical Advisory: Insecure BLE Implementation in Smartwatch Ecosystems

## Overview
- **Vulnerability Type:** Improper Encryption ([CWE-311](https://cwe.mitre.org/data/definitions/311.html)), Cleartext Transmission of Sensitive Information ([CWE-319](https://cwe.mitre.org/data/definitions/319.html))
- **Advisory Date:** December 18, 2025
- **Affected Device:** Pebble Prism Ultra (PFB20)
- **Vendor:** SRK Powertech Pvt Ltd
- **Status:** Public Disclosure

## Summary
Research into several smartwatch and fitness tracker ecosystems revealed critical security flaws in Bluetooth Low Energy (BLE) communication. Over 30+ vendors share a common codebase that fails to implement standard BLE encryption or bonding. This allows an attacker within Bluetooth range to intercept private notifications (SMS, Caller ID, App alerts) in cleartext and inject spoofed notifications onto the wearable device.

---

## Technical Analysis

### 1. Protocol Architecture
The devices utilize the **Generic Attribute Profile (GATT)** over BLE. The investigation focused on the primary service responsible for data synchronization.

- **Service UUID:** `0000fee7-0000-1000-8000-00805f9b34fb`
- **Security Mode:** "Just Works" (No MITM protection, no encryption).

### 2. Cleartext Data Transmission
Analysis of the `HCI Snoop Logs` via Wireshark confirms that the companion application writes notification data to the GATT characteristic in an unencrypted format. 

**Packet Structure Example:**
| Byte Index | Field | Value | Description |
|:---|:---|:---|:---|
| 0 | OpCode | `0x03` | Notification Command |
| 1 | Length | `0x0C` | Payload Size |
| 2 | Category | `0x01` | Message/SMS Icon |
| 3-N | Payload | `4d006f006d00` | "Mom" (UTF-16LE) |

### 3. Proof of Concept (PoC)
Because there is no cryptographic binding between the phone and the watch, a third-party device can connect and send arbitrary `Write Requests`.

**Spoofing Command:**
Using `gatttool` on Linux, a spoofed message can be sent to the device:
```bash
# Writing "Alert" to the notification handle
gatttool -b [TARGET_MAC] --char-write-req -a 0x0012 -n 030a0141006c00650072007400
```

---

### Impact

* Confidentiality: Personal messages and caller identities are exposed to local sniffing. Anyone with a $10 Bluetooth dongle can intercept private data.
* Integrity: The device display can be manipulated to show fraudulent alerts (Social Engineering). Attackers can trigger fake 2FA prompts or emergency alerts.
* Supply Chain: The vulnerability originates from a shared SDK used by 30+ manufacturers, magnifying the attack surface across different brands.

### Disclosure Timeline

* August 2023: Initial discovery.
* August 25, 2023: Outreach to identified vendors.
* November 2023: No response received; follow-up sent.
* December 2025: Public disclosure for CVE registration.

**Researcher**
Mukund Bhuva
Project: BLEached Security
