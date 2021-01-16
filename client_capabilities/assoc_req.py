from scapy.all import *

# Check whether a wireless adapter is in monitor mode.
# Can be done using a function from module that sets
# adapter to a monitor mode.

INTERFACE = "wlan0"
SSID = "lab-iap"

def assoc_req_parse(frame):
    if frame.haslayer(Dot11AssoReq) and frame.getlayer(Dot11Elt, ID=0).info.decode("utf-8") == SSID:
        client = frame.addr2
        bssid = frame.addr3
        channels_raw = frame.getlayer(Dot11Elt, ID=36).info.hex()
        channels = {}
        for i in range(0, len(channels_raw), 4):
            tmp = channels_raw[i:i+4]
            channel = int(tmp[:2], 16)
            range_ = int(tmp[2:], 16)
            channels[channel] = range_

        print(f"Client {client} sent Assoc Req to BSSID {bssid}")
        print("Channel : Range")
        for i in channels:
            print(f"{i} : {channels[i]}")

    #return channels

#sniff(iface='wlan0', lfilter = lambda x: x.haslayer(Dot11AssoReq), prn=assoc_req_parse, store=0)
#s = AsyncSniffer(iface="wlan0", lfilter = lambda x: x.haslayer(Dot11AssoReq), prn=assoc_req_parse)

#def sniff(interface, func):
    #sniff(iface=interface, prn=func, store=0)

def main():
    #sniff('wlan0', assoc_req_parse)
    print("####Catching Association Request####")
    sniff(iface=INTERFACE, prn=assoc_req_parse, store=0)

if __name__ == '__main__':
    main()

