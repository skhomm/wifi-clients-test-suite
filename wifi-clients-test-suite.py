"""
This is the main module of the test suite.

It runs submodules
and possibly helps to configure parameters by going through menus.
"""

from make_roam.aruba import make_roam_aruba_IAP

print("""
Please choose a vendor

1. Aruba
2. Cisco
""")

vendor_chosen = input("Type number and press Enter\n")

if vendor_chosen == "1":
    make_roam_aruba_IAP.main()
    print("Starting suite for Aruba...")
elif vendor_chosen == "2":
    print("Cisco is not yet supported")
else:
    print("Input not recognized")
