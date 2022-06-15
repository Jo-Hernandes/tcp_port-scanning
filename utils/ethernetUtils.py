import socket as sock
from struct import *

def sendeth(eth_frame, interface="eth0", port=9001):
    s = sock.socket(sock.AF_PACKET, sock.SOCK_RAW)
    s.bind((interface, port))
    return s.send(eth_frame)

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
