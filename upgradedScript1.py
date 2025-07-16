from netmiko import ConnectHandler
import pwinput
import re

def normalize_interface_name(name):
    name = name.replace("Gig", "Gi").replace("Fas", "Fa")
    name = name.replace("Ethernet", "")
    name = name.replace(" ", "")
    return name
while True:
    # Step 0: write the output to the file specified by u 
    logfile = input("Enter the file name:")
    logfile = open(logfile, "w", encoding="utf-8")
    # Step 1: Get credentials and IPs
    username = input("Username: ")
    password = pwinput.pwinput(prompt="Password: ", mask="*")
    ip_input = input("Enter switch IPs (comma-separated): ")
    ip_list = [ip.strip() for ip in ip_input.split(",")]

    # Step 2: Loop through each IP
    for device_ip in ip_list:
        print(f"\n================ CONNECTING TO {device_ip} ================\n")
        print(f"\n================ CONNECTING TO {device_ip} ================\n", file=logfile)
        device = {
            'device_type': 'cisco_ios',
            'ip': device_ip,
            'username': username,
            'password': password,
        }

        try:
            net_connect = ConnectHandler(**device)
        except Exception as e:
            print(f"❌ Connection failed to {device_ip}: {e}")
            print(f"❌ Connection failed to {device_ip}: {e}", file=logfile)
            continue
        hostname=net_connect.find_prompt().rstrip('#>')
        print(f"✅ Connected to -->|| {hostname} ||<--")
        print(f"✅ Connected to -->|| {hostname} ||<--", file=logfile)
        # Step 3: Get CDP data
        print("🔍 Getting CDP neighbors...")
        print("🔍 Getting CDP neighbors...", file=logfile)
        cdp_output = net_connect.send_command("show cdp neighbors", use_textfsm=True)

        access_point_keywords = [ 
            'air', 'AIR-AP113', 'access point',
            'air-lap', 'AIR-SAP26'
        ]
        access_point_ports = []

        for neighbor in cdp_output:
            platform = neighbor.get('platform', '').lower()
            if any(keyword in platform for keyword in access_point_keywords):
                access_point_ports.append(neighbor['local_interface'])

        print(f"📡 Access Points are connected to ports: {access_point_ports}")
        print(f"📡 Access Points are connected to ports: {access_point_ports}", file=logfile)
        # Step 4: Check descriptions
        interfaces_output = net_connect.send_command("show interfaces description")

        descriptive_keywords = [
            'access point', 'access-point', 'air', 'AIR-AP113', 'air-lap', 'AIR-SAP26', 'ap'
        ]
        descriptive_ports = []

        for line in interfaces_output.splitlines():
            match = re.match(r"(\S+)\s+.+?\s+(.+)", line)
            if not match:
                continue
            interface = match.group(1)
            description = match.group(2).strip().lower()
            if any(keyword in description for keyword in descriptive_keywords):
                descriptive_ports.append(interface)

        print(f"📝 Ports with access point description: {descriptive_ports}")
        print(f"📝 Ports with access point description: {descriptive_ports}", file=logfile)
        # Normalize AP ports
        normalized_access_ports = [normalize_interface_name(p) for p in access_point_ports]

        # Step 5: Remove incorrect descriptions
        for interface in descriptive_ports:
            if interface not in normalized_access_ports:
                print(f"{interface}: ❌ No AP connected, removing description...")
                print(f"{interface}: ❌ No AP connected, removing description...", file=logfile)
                net_connect.send_config_set([
                    f"interface {interface}",
                    "no description"
                ])  # burada small bug var check edir ve butun mahsinlarda no description edir ve daha sornra acceess port hissesinde tezeden onlara access point tag i verir. problemsizdir ishleyir lakin small misinformation verir. 

        # Step 6: Set correct descriptions
        print("\n🛠 Setting Access Point descriptions...")
        print("\n🛠 Setting Access Point descriptions...", file=logfile)
        for port in access_point_ports:
            print(f"{port}: ✅ Description set to 'Access Point'")
            print(f"{port}: ✅ Description set to 'Access Point'", file=logfile)
            net_connect.send_config_set([
                f"interface {port}",
                "description Access-Point"
            ])

        # Step 7: Show CDP neighbors
        print("\n==================== CDP NEIGHBORS ====================")
        print("\n==================== CDP NEIGHBORS ====================", file=logfile)
        for neighbor in cdp_output:
            device_id = neighbor.get('device_id', 'N/A')
            local_interface = neighbor.get('local_interface', 'N/A')
            platform = neighbor.get('platform', 'N/A')
            port_id = neighbor.get('port_id', 'N/A')
            capability = neighbor.get('capability', 'N/A')

            # print(f"Device ID     : {device_id}")
            print(f"Local Intf    : {local_interface}")
            print(f"Local Intf    : {local_interface}", file=logfile)
            print(f"Platform      : {platform}")
            print(f"Platform      : {platform}", file=logfile)
            # print(f"Capability    : {capability}")
            # print(f"Port ID       : {port_id}")
            print("-" * 50)
            print("-" * 50, file=logfile)

        # Step 8: Show updated descriptions only for AP ports
        interfaces_output1 = net_connect.send_command("show interfaces description")

        print("\n================ AP PORT DESCRIPTIONS ===============")
        print("\n================ AP PORT DESCRIPTIONS ===============", file=logfile)

        for line in interfaces_output1.splitlines():
            for ap_port in normalized_access_ports:
                if ap_port in line:
                    print(line)
                    print(line, file=logfile)

        print("=" * 55)
        print("=" * 55, file=logfile)

        # Step 9: Save configuration
        net_connect.send_command("end")
        net_connect.send_command("write memory")
        net_connect.disconnect()

        print(f"✅ Disconnected from {device_ip}. Configuration saved.\n")
        print(f"✅ Disconnected from {device_ip}. Configuration saved.\n", file=logfile)

    print("🔔 Notification: Some N/A entries may appear if CDP info is incomplete on the device.")
    print("🔔 Notification: Some N/A entries may appear if CDP info is incomplete on the device.", file=logfile)
    logfile.close()
    choice = input("\n❓ Want to continue? Press 1 and Enter\n❌ Want to exit? Press 2 and Enter\n➡ Your choice: ")
    if choice.strip() == '2':
        break
print("End...")
# Authors: Ismayil Ismayilov, Zulfiyye Safarli
