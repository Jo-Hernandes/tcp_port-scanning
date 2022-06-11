import socket as sock
# from socket import AF_PACKET, SOCK_RAW
from struct import *
import re, uuid


# def sendeth(eth_frame, interface="eth0"):
#     s = sock.socket(AF_PACKET, SOCK_RAW)
#     s.bind((interface, 0))
#     return s.send(eth_frame)


def getMac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getMacAsByteArray(readableMac):
    return bytearray.fromhex(readableMac.translate(str.maketrans('', '', ':')))

def getReadableMac(byteArray):
    return "%02x:%02x:%02x:%02x:%02x:%02x" % unpack("BBBBBB", byteArray)


def getSniffingSocket(interface="eth0"):
    s = sock.socket(sock.AF_PACKET, sock.SOCK_RAW, sock.htons(3))
    s.bind((interface, 0))
    return s
