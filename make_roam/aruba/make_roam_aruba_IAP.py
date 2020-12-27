"""
This script creates conditions that drive a Wi-Fi client to roam.

It's achieved by controlling power settings of APs.
Client doesn't need to move. It roams from AP with low power.
"""

import time
import json
import getpass
import os

from netmiko import ConnectHandler

# Dirty hacks to make peace with import from subfolders nightmare
try:
    import config
except ImportError:
    from . import config

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DEVICES_JSON = os.path.join(THIS_FOLDER, 'devices.json')


def show_cmd(include_args):
    return(f"show ap debug driver-config | inc {include_args}")


def change_pwr_cmd(current_channel, current_tx_power):
    return(f"a-channel {current_channel} {current_tx_power}")


# Function runs full round at one device
def run_device(device, username, password):
    # Form dictionary that is supported by netmiko
    netmiko_device = device.copy()
    netmiko_device['username'] = username
    netmiko_device['password'] = password

    # Netmiko doesn't accept 'channel' in it's dictionary
    channel = netmiko_device.pop('channel')
    ap_name = netmiko_device.pop('ap_name')
    host = netmiko_device['host']

    print("\n" + "====" * 12)
    print(f"Connecting to {ap_name} [{host}] ...")
    net_connect = ConnectHandler(**netmiko_device)
    print("Successful!")

    # Change power - step by step
    for tx_power in range(config.MAX_POWER, config.MIN_POWER, config.STEP_POWER):
        print(f"\nTX power -> {tx_power} dBm")

        # Send command to change power
        change_power = change_pwr_cmd(str(channel), str(tx_power))
        net_connect.send_command(change_power)

        # Send command to show current values and wait a second
        output = net_connect.send_command(show_cmd(config.SHOW_ARGS))
        print(*output.split('\n')[0:3], sep='\n')
        time.sleep(1)

    # Give some time to roam and revert power back to the max value
    print(f"\nReverting back to {config.MAX_POWER} dBm in...")
    for i in range(config.COUNTDOWN, 0, -1):
        print(i)
        time.sleep(1)
    print("Now!")
    print(f"\nTX power -> {config.MAX_POWER} dBm")

    # Send command to change power
    change_power = change_pwr_cmd(str(channel), str(config.MAX_POWER))
    net_connect.send_command(change_power)

    # Send command to show current values
    output = net_connect.send_command(show_cmd(config.SHOW_ARGS))
    print(*output.split('\n')[0:3], sep='\n')


def main():
    username = input("Username: ")
    password = getpass.getpass()

    # Get devices dictionary from file
    with open(DEVICES_JSON) as devices_file:
        devices = json.load(devices_file)

    print("\nIt's roaming time!")

    # Replay as many times as REPLAY parameter dictates
    for n in range(config.REPLAY):

        print("\nRound", n+1)

        # Full round for each device
        for device in devices:
            run_device(device, username, password)

    print("\nHope it was seamless...")  # mheh


# It all starts here
if __name__ == '__main__':
    main()
