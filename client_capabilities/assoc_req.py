from scapy.all import *

# Check whether a wireless adapter is in monitor mode.
# Can be done using a function from module that sets
# adapter to a monitor mode.

def assoc_req_parse(frame):
    print(frame.addr2)

#sniff(iface='wlan0', lfilter = lambda x: x.haslayer(Dot11AssoReq), prn=assoc_req_parse, store=0)
#s = AsyncSniffer(iface="wlan0", lfilter = lambda x: x.haslayer(Dot11AssoReq), prn=assoc_req_parse)

def sniff(interface, func):
    sniff(iface=interface, prn=func, store=0)

def main():
    sniff(wlan0, assoc_req_parse)

if __name__ == '__main__':
    main()

