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

print("\nIt's roaming time!")

for n in range(replay):
    print("\nRound", n+1)

    # One full round starts here
    ap_counter = 1
    for device in devices:
        device['username'] = username
        device['password'] = password

        print("\n" + "====" * 12)
        print("Connecting to AP", ap_counter, "...")
        net_connect = ConnectHandler(**device)
        print("Successful!")

        # Change power - step by step
        for tx_power in range(max_power, min_power, step_power):
            print("\nTX power ->", tx_power, "dBm")

            # Send command to change power
            change_power = "a-channel " + str(channel[ap_counter]) + " " + str(tx_power)
            net_connect.send_command(change_power)

            # Send command to show current values and wait a second
            output = net_connect.send_command(show_comand)
            listed_output = output.split("\n")
            for i in range(3):
                print(listed_output[i])
            time.sleep(1)

        # Give some time to roam and revert power back to the max value
        print("\nReverting back to", max_power, "dBm in...")
        for i in range(countdown, 0, -1):
            print(i)
            time.sleep(1)
        print("Now!")
        print("\nTX power ->", max_power, "dBm")

        # Send command to change power
        change_power = "a-channel " + str(channel[ap_counter]) + " " + str(max_power)
        net_connect.send_command(change_power)

        # Send command to show current values
        output = net_connect.send_command(show_comand)
        listed_output = output.split("\n")
        for i in range(3):
            print(listed_output[i])

        # Setting counter for the next AP
        ap_counter += 1
    # One full round finishes here

print("\nHope it was seamless...")  # mheh
