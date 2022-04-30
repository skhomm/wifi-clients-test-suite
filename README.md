# Wi-Fi client devices test suite

Set of tools for Wi-Fi client device testing

## Description

At the moment following features are supported:
* make client roam constantly by manipulating Aruba AP TX power settings
* check client capabilities by parsing its association request frame (offline or online)

You need Aruba Access Points to perform the roaming test.
And you need WLAN Pi to perform online association request parsing.

## Getting Started

### Dependencies

* netmiko
* scapy

### Installing

It's intended to run the tool using WLAN Pi, but any UNIX-like OS
will work if you are brave enough.

* Clone the repo
* Install netmiko and scapy using pip
* Execute the setup.sh in the repo directory to add it to $PYTHONPATH

### Executing program

**Roaming test**

To perform the roaming test make sure that your access points are reachable
from your network.
* Edit /make_roam/aruba/config.py to set up your test scenario.
* Run menu.py and follow the instructions to start the test.

**Client capabilities test**
* Under construction


## Authors

* Leonid Tekanov @skhomm
* Dmitrii Litovchenko @ttl256

## License

This project is licensed under the terms of the MIT license - see the LICENSE.md file for details

