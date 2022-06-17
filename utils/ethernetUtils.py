import socket as sock
from socket import AF_PACKET, SOCK_RAW
from struct import *

def sendeth(eth_frame, interface="eth0", port=9001):
    s = sock.socket(AF_PACKET, SOCK_RAW)
    s.bind((interface, port))
    s.send(eth_frame)

def getSniffingSocket():
    s = sock.socket(AF_PACKET, SOCK_RAW, sock.htons(0x0003))
    return s

def getMacAsByteArray(readableMac):
    return bytearray.fromhex(readableMac.translate(str.maketrans('', '', ':')))

def getReadableMac(byteArray):
    return "%02x:%02x:%02x:%02x:%02x:%02x" % unpack("BBBBBB", byteArray)
