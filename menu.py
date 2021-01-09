"""
This is the main module of the test suite.

It runs submodules
and possibly helps to configure parameters by going through menus.
"""

from make_roam.aruba import iap


def menu():
    print("Select task\n")
    print("[0] Change adapter mode")
    print("[1] Start packet capture")
    print("[2] Association Request analysis")
    print("[3] Start roaming test")


def option_0():
    print("\nCurrently not supported...\n")


def option_1():
    print("\nCurrently not supported...\n")


def option_2():
    print("\nCurrently not supported...\n")


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
    else:
        print("\nInput not recognized")


menu()
task_chosen = input("\nType number and press Enter\n")

if task_chosen == "0":
    option_0()
elif task_chosen == "1":
    option_1()
elif task_chosen == "2":
    option_2()
elif task_chosen == "3":
    option_3()
else:
    print("\nInput not recognized")
