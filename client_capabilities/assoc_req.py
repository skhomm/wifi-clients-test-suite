from scapy.all import *

# Check whether a wireless adapter is in monitor mode.
# Can be done using a function from module that sets
# adapter to a monitor mode.

INTERFACE = "wlan0"
SSID = "lab-iap"
assoc_req_file = "assoc_req.pcap"

def write_pcap(frame, pcap_file = "assoc_req.pcap"):
    wrpcap(pcap_file, frame, append=True, sync=True)

def supported_channels_parse(frame):
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
                [first_channel+num_of_channels*i for i in range(0, num_of_channels)])

        return supported_channels
    except AttributeError:
        # Return an empty list of supported channels if a client doesn't advertise them
        return supported_channels   

def assoc_req_parse(frame):
    write_pcap(frame, assoc_req_file)
    ssid = frame.getlayer(Dot11Elt, ID=0).info.decode("utf-8")
    client_mac = frame.addr2
    bssid = frame.addr3
    
    supported_channels = supported_channels_parse(frame)

    print(f"AssocReq, Client {client_mac}, BSSID {bssid}, SSID {ssid}")
    print("Supported channels")

    if not supported_channels:
        print("No info")
    else:
        print(*supported_channels, sep = ", ")

def main():
    print("####Catching Association Request####")
    sniff(iface=INTERFACE, filter="type mgt subtype assoc-req", prn=assoc_req_parse, store=0)

if __name__ == '__main__':
    main()

