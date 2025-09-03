# Cisco Access Point Port Description Automation

This Python script automates the process of managing **Access Point (AP) port descriptions** on Cisco switches using the Netmiko library.  

It connects to Cisco IOS devices, detects which interfaces are connected to APs using **CDP neighbors** and **interface descriptions**, and then automatically updates the interface descriptions to keep them consistent.

---

## ✨ Features
- Connects to multiple Cisco switches using SSH.
- Detects APs connected to switch ports via:
  - `show cdp neighbors`
  - `show interfaces description`
- Removes wrong "Access Point" descriptions from interfaces without APs.
- Sets correct descriptions (`description Access-Point`) for interfaces with APs.
- Saves configuration (`write memory`).
- Logs all results to a file chosen by the user.
- Handles connection failures gracefully.
- Supports multiple devices in one run.

---

## 🛠 Requirements
- Python 3.7+
- Required Python packages:
  ```bash
  pip install netmiko pwinput
