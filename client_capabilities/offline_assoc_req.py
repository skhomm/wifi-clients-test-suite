from glob import glob

# It's bad to do wildcard imports. There should be a better way.
from scapy.all import *


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
                [first_channel+i*4
                 for i in range(0, num_of_channels)])

        return supported_channels
    except AttributeError:
        # Return an empty list of supported channels
        # if a client doesn't advertise them
        return supported_channels


def assoc_req_parse(frame):
    if frame.haslayer(Dot11AssoReq):
        ssid = frame.getlayer(Dot11Elt, ID=0).info.decode("utf-8")
        client_mac = frame.addr2
        bssid = frame.addr3
        supported_channels = parse_supported_channels(frame)
        print(f"{supported_channels}")



def main():
    print("####Analyzing *.pcap files####")
    pcap_list = glob("*.pcap")

    for pcap in pcap_list:
        # print("="*60)
        print(pcap)
        sniff(offline=pcap,
                prn=assoc_req_parse, store=0)
        # print("="*60)
        print()


if __name__ == '__main__':
    main()