import time
import json
import getpass

from netmiko import ConnectHandler

# Ask for username and password
username = input("Username: ")
password = getpass.getpass()

# Define parameters
REPLAY = 2
MIN_POWER = 2
MAX_POWER = 21
STEP_POWER = -3
COUNTDOWN = 10
SHOW_ARGS = "EIRP|Channel|BSSID"
CHANNEL = {1: 149, 2: 157}

# Get devices dictionary from file
with open('devices.json') as devices_file:
    devices = json.load(devices_file)


def show_command(include_args):
    return(f"show ap debug driver-config | inc {include_args}")


def change_power_command(current_channel, current_tx_power):
    return(f"a-channel {current_channel} {current_tx_power}")


# Function runs full round at one device
def run_device(current_ap):
    current_ap['username'] = username
    current_ap['password'] = password

    print("\n" + "====" * 12)
    print("Connecting to AP", ap_counter, "...")
    net_connect = ConnectHandler(**device)
    print("Successful!")

    # Change power - step by step
    for tx_power in range(MAX_POWER, MIN_POWER, STEP_POWER):
        print("\nTX power ->", tx_power, "dBm")

        # Send command to change power
        change_power = change_power_command(str(CHANNEL[ap_counter]), str(tx_power))
        net_connect.send_command(change_power)

        # Send command to show current values and wait a second
        output = net_connect.send_command(show_command(SHOW_ARGS))
        print(*output.split('\n')[0:3], sep='\n')
        time.sleep(1)

    # Give some time to roam and revert power back to the max value
    print("\nReverting back to", MAX_POWER, "dBm in...")
    for i in range(COUNTDOWN, 0, -1):
        print(i)
        time.sleep(1)
    print("Now!")
    print("\nTX power ->", MAX_POWER, "dBm")

    # Send command to change power
    change_power = change_power_command(str(CHANNEL[ap_counter]), str(MAX_POWER))
    net_connect.send_command(change_power)

    # Send command to show current values
    output = net_connect.send_command(show_command(SHOW_ARGS))
    print(*output.split('\n')[0:3], sep='\n')


# It all starts here
print("\nIt's roaming time!")

for n in range(REPLAY):
    print("\nRound", n+1)
    ap_counter = 1

    # Full round for each device
    for device in devices:
        run_device(device)
        # Setting counter for the next AP
        ap_counter += 1

print("\nHope it was seamless...")  # mheh
