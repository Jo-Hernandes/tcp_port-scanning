import socket as sock
from struct import *
from getmac import get_mac_address

def sendeth(eth_frame, interface="eth0"):

    addrs = sock.getaddrinfo('2804:14d:4c87:85a7:f0e9:9253:c637:1d58', 1, sock.AF_INET6, 0, sock.SOL_IP)
    print(addrs)

    s = sock.socket(sock.AF_INET6, sock.SOCK_RAW, 0)
    s.setsockopt(sock.IPPROTO_IPV6, sock.IP_HDRINCL, 1)

    # s.bind(('2804:14d:4c87:85a7:f0e9:9253:c637:1d58', 1, 0, 0))
    
    return s.sendto( bytes("minha bunda", "ascii"), ('2804:14d:4c87:85a7:f0e9:9253:c637:1d58', 1, 0, 0))

def getMac(int):
    return get_mac_address(interface=int)

def getMacAsByteArray(readableMac):
    return bytearray.fromhex(readableMac.translate(str.maketrans('', '', ':')))

def getReadableMac(byteArray):
    return "%02x:%02x:%02x:%02x:%02x:%02x" % unpack("BBBBBB", byteArray)


def getSniffingSocket(interface="eth0"):
    s = sock.socket(sock.AF_PACKET, sock.SOCK_RAW, sock.htons(3))
    s.bind((interface, 0))
    return s

def getIPv6fromMac(mac):
    # only accept MACs separated by a colon
    parts = mac.split(":")

    # modify parts to match IPv6 value
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6Parts = []
    for i in range(0, len(parts), 2):
        ipv6Parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s" % (":".join(ipv6Parts))
    return ipv6
