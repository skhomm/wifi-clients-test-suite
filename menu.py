"""
This is the main module of the test suite.

It runs submodules
and possibly helps to configure parameters by going through menus.
"""

import os
import time

import adapter_control
from make_roam.aruba import iap
from client_capabilities import assoc_req


def menu():
    os.system('clear')

    print("====MAIN MENU====\n")
    print("Select task\n")
    print("[0] Start adapter control module")
    print("[1] Start packet capture")
    print("[2] Association Request analysis")
    print("[3] Start roaming test")

    task_chosen = input("\nType number and press Enter\n")

    if task_chosen == "0":
        option_0()
    elif task_chosen == "1":
        option_1()
    elif task_chosen == "2":
        option_2()
    elif task_chosen == "3":
        option_3()
    elif task_chosen == " ":
        os.system('clear')
    else:
        print("\nInput not recognized\n")
        time.sleep(1)

    menu()


def option_0():
    os.system('clear')
    adapter_control.menu()


def option_1():
    print("\nCurrently not supported...\n")
    time.sleep(1)


def option_2():
    print("\nSelect mode")
    print("[1] Online")
    print("[2] Offline")

    mode_chosen = input("\nType number and press Enter\n")

    if mode_chosen == "1":
        print("\nStarting capture...\n")
        assoc_req.main()
    elif mode_chosen == "2":
        print("\nCurrently not supported...\n")
    elif mode_chosen == "  ":
        return
    else:
        print("\nInput not recognized")
        time.sleep(1)

def option_3():
    print("\nSelect vendor")
    print("[1] Aruba")
    print("[2] Cisco")

    vendor_chosen = input("\nType number and press Enter\n")

    if vendor_chosen == "1":
        print("\nStarting suite for Aruba...\n")
        iap.main()
    elif vendor_chosen == "2":
        print("\nCurrently not supported...\n")
    elif vendor_chosen == "  ":
        return
    else:
        print("\nInput not recognized")
        time.sleep(1)


menu()
