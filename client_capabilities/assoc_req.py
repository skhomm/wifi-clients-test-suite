"""
This module sniffs association requests and parses them live.

Filtering for association requests is achieved with BPF filter,
thus Scapy doesn't suffer from a big number of frames.
Frames are parsed on the fly and values for some fields are
logged to console as well as to a file. Frames themselves are
also written to a pcap file for further investigation.
"""

import logging
import sys
# It's bad to do wildcard imports. There should be a better way.
from scapy.all import *

# Use adapter_control module to set interface.
INTERFACE = "wlan0"

# Logging should be implemented better (system wide logging module)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def parse_supported_channels(frame):
    supported_channels = []
    try:
        # Convert info field of the IE (b'' string) to hex
        channels_raw = frame.getlayer(Dot11Elt, ID=36).info.hex()
        # IEEE802.11 defines the following format for supported channels:
        # 1 byte (2 hex digits) for 'first channel number'
        # 1 byte (2 hex digits) for 'number of channels'
        for i in range(0, len(channels_raw), 4):
            tmp = channels_raw[i:i+4]
            first_channel = int(tmp[:2], 16)
            num_of_channels = int(tmp[2:], 16)
            supported_channels.extend(
                [first_channel+num_of_channels*i
                 for i in range(0, num_of_channels)])

        return supported_channels
    except AttributeError:
        # Return an empty list of supported channels
        # if a client doesn't advertise them
        return supported_channels


def assoc_req_parse(frame):
    wrpcap("assoc_req.pcap", frame, append=True, sync=True)
    ssid = frame.getlayer(Dot11Elt, ID=0).info.decode("utf-8")
    client_mac = frame.addr2
    bssid = frame.addr3

    supported_channels = parse_supported_channels(frame)

    message = f"AssocReq, Client {client_mac}, BSSID {bssid}, SSID {ssid}"
    if not supported_channels:
        message1 = "Supported channels: No Info"
    else:
        message1 = f"Supported channels: {supported_channels}"
    logging.info(message + ", " + message1)


def main():
    print("####Catching Association Request####")
    sniff(iface=INTERFACE, monitor=True, filter="type mgt subtype assoc-req",
          prn=assoc_req_parse, store=0)


if __name__ == '__main__':
    main()
