import time
import json
import getpass

from netmiko import ConnectHandler

username = input("Username: ")
password = getpass.getpass()

# Define variables
replay = 2
min_power = 2
max_power = 21
step_power = -3
countdown = 10
show_comand = "show ap debug driver-config | inc EIRP|Channel|BSSID"
channel = {1: 149, 2: 157}

with open('devices.json') as devices_file:
    devices = json.load(devices_file)


# Function runs full round at one device
def run_device(current_ap):
    current_ap['username'] = username
    current_ap['password'] = password

    print("\n" + "====" * 12)
    print("Connecting to AP", ap_counter, "...")
    net_connect = ConnectHandler(**device)
    print("Successful!")

        # Send command to show current values and wait a second
    
    output = net_connect.send_command(show_comand)
    # for line in output.split("\n"): print(line)
    # print(output)
    # listed_output = output.split("\n")
    print(*output.split('\n')[0:3], sep='\n')
    # print(*listed_output[0:3], sep='\n')
    # for i in range(10):
    #     print(listed_output[i])
    # time.sleep(1)

# It all starts here
print("\nIt's roaming time!")

for n in range(replay):
    print("\nRound", n+1)
    ap_counter = 1

    # Full round for each device
    for device in devices:
        run_device(device)
        # Setting counter for the next AP
        ap_counter += 1

print("\nHope it was seamless...")  # mheh
