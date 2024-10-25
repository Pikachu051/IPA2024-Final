from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.184"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip int br", use_textfsm=True)
        interface_messages = []
        
        for status in result:
            if status["interface"].startswith("GigabitEthernet"):
                status_msg = status["status"]
                interface_name = status["interface"]
                
                if status_msg == "up":
                    up += 1
                elif status_msg == "down":
                    down += 1
                elif status_msg == "administratively down":
                    admin_down += 1
                
                interface_messages.append(f"{interface_name} {status_msg}")
        
        status_summary_count = f"{up} up, {down} down, {admin_down} administratively down"
        ans = f"{', '.join(interface_messages)} -> {status_summary_count}"

        
        pprint(ans)
        return ans
