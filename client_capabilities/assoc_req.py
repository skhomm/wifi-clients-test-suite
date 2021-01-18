from scapy.all import *

# Check whether a wireless adapter is in monitor mode.
# Can be done using a function from module that sets
# adapter to a monitor mode.

INTERFACE = "wlan0"
SSID = "lab-iap"

def assoc_req_parse(frame):
    if frame.haslayer(Dot11AssoReq) and frame.getlayer(Dot11Elt, ID=0).info.decode("utf-8") == SSID:
        client_mac = frame.addr2
        bssid = frame.addr3
        # Convert info field of the IE (b'' string) to hex
        channels_raw = frame.getlayer(Dot11Elt, ID=36).info.hex()
        supported_channels = []
        # IEEE802.11 defines the following format for supported channels:
        # 1 byte (2 hex digits) for 'first channel number'
        # 1 byte (2 hex digits) for 'number of channels'
        for i in range(0, len(channels_raw), 4):
            tmp = channels_raw[i:i+4]
            first_channel = int(tmp[:2], 16)
            num_of_channels = int(tmp[2:], 16)
            supported_channels.extend([first_channel+num_of_channels*i for i in range(0, num_of_channels)]) 

        print(f"Client {client_mac} sent Assoc Req to BSSID {bssid}")
        print("Supported channels")
        print(*supported_channels, sep = ", ")

def main():
    print("####Catching Association Request####")
    sniff(iface=INTERFACE, prn=assoc_req_parse, store=0)

if __name__ == '__main__':
    main()
