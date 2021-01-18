"""
This script creates conditions that drive a Wi-Fi client to roam.

It's achieved by controlling power settings of APs.
Client doesn't need to move. It roams from AP with low power.
"""

import sys
import time
import getpass

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import AuthenticationException

from make_roam.aruba import config


def show_cmd(include_args):
    return(f"show ap debug driver-config | inc {include_args}")


def show_assoc():
    return("show ap association")


def change_pwr_cmd(current_channel, current_power):
    return(f"a-channel {current_channel} {current_power}")


# Function runs full round at one device
def run_device(device, username, password):
    # Form dictionary that is supported by netmiko
    netmiko_device = device.copy()
    netmiko_device['username'] = username
    netmiko_device['password'] = password

    # Netmiko doesn't accept 'channel' or 'ap_name' in it's dictionary
    channel = netmiko_device.pop('channel')
    ap_name = netmiko_device.pop('ap_name')
    host = netmiko_device['host']

    print("\n" + "====" * 12)
    print(f"Connecting to {ap_name} [{host}] ...")

    try:
        net_connect = ConnectHandler(**netmiko_device)
        print("Successful!")
    except AuthenticationException:
        sys.exit("Authentication failed!")
    except NetMikoTimeoutException:
        sys.exit("TCP connection to the device failed!")

    # Print some information about current AP
    print("\nCollecting information ...\n")

    output = net_connect.send_command(show_cmd(config.SHOW_ARGS))
    print(*output.split('\n')[0:3], sep='\n')

    # We definitely should use a better approach to parse parameters (textfsm?)
    current_bssid = output.split('\n')[0].split()[1]
    print(f"\nDima, here is your BSSID value:\n{current_bssid}")

    output = net_connect.send_command(show_assoc())
    print(*output.split('\n')[9:-1], sep='\n')
    time.sleep(1)
    print("\n" + "====" * 12)

    # Change power - step by step
    for power in range(config.MAX_POWER, config.MIN_POWER, config.STEP_POWER):
        print(f"\nTransmit EIRP -> {power} dBm")

        # Send command to change power
        change_power = change_pwr_cmd(str(channel), str(power))
        net_connect.send_command(change_power)

        # Check if the power has changed
        output = net_connect.send_command(show_cmd(config.SHOW_ARGS))
        real_power = output.split('\n')[2].split()[2]
        if float(real_power) == float(power):
            print("Done!")
        else:
            print("Power has not changed, check the code")
            break
        time.sleep(1)

    # Give some time to roam and revert power back to the max value
    print(f"\nBack to {config.MAX_POWER} dBm in {config.COUNTDOWN} seconds:")
    for i in range(config.COUNTDOWN, 0, -1):
        print(i, sep=' ', end=' ', flush=True)
        time.sleep(1)
    print("Now!")
    print(f"\nTransmit EIRP -> {config.MAX_POWER} dBm")

    # Send command to change power
    change_power = change_pwr_cmd(str(channel), str(config.MAX_POWER))
    net_connect.send_command(change_power)

    # Send command to show current values
    output = net_connect.send_command(show_cmd(config.SHOW_ARGS))
    print(*output.split('\n')[0:3], sep='\n')


def main():
    username = input("Username: ")
    password = getpass.getpass()

    print("\nIt's roaming time!")

    # Replay as many times as REPLAY parameter dictates
    for n in range(config.REPLAY):

        print("\nRound", n+1)

        # Full round for each device
        for device in config.DEVICES:
            run_device(device, username, password)

    print("\nHope it was seamless...")  # mheh


# It all starts here
if __name__ == '__main__':
    main()
