import socket

from struct import *
from collections import namedtuple
from utils.ethernetUtils import getReadableMac

try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

IPV6_ETH_HEADER = 0x86DD

ETH_STRUCT_FORMAT = '!6s6sH'
IPV6_STRUCT_FORMAT = '!IHBB'
TCP_STRUCT_FORMAT = '!HHLLBBHHH'

ethernetPacket = namedtuple('Ethernet', 'macDst macAddr ethType')


def buildEthernet(destinationMac, sourceMac, protocol):
    packet = pack(ETH_STRUCT_FORMAT, destinationMac, sourceMac, protocol)
    return packet

def unpackEthernet(record):
    packet = ethernetPacket._make(unpack(ETH_STRUCT_FORMAT, record))
    return ethernetPacket._make([
        getReadableMac(packet.macDst),
        getReadableMac(packet.macAddr),
        packet.ethType
    ])

def buildIPv6Packet(destIp, sourceIp, len):
    # ip header fields
    version     = 6                       #4 bit
    traffic_class = 0                     #8 bit
    flow_level  = 1                       #20 bit
    payload_len = len #not true lenght, I just selected a random value        #16 bit
    next_header = socket.IPPROTO_TCP      #8 bit
    hop_limit   = 255                     #8 bit
    saddr = socket.inet_pton ( socket.AF_INET6, sourceIp )  #128 bit
    daddr = socket.inet_pton ( socket.AF_INET6, destIp   )  #128 bit

    ver_traff_flow = (version << 8) + traffic_class
    ver_traff_flow = (ver_traff_flow << 20) + flow_level

    ip_header = pack(IPV6_STRUCT_FORMAT, ver_traff_flow, payload_len, next_header, hop_limit)
    return ip_header + saddr + daddr
    

def buildTcpPacket(destIp, sourceIp, destPort, sourcePort):
    seq = 0
    ack_seq = 0
    doff = 5    #4 bit field, size of tcp header, 5*4 = 20 bytes
    #tcp flags
    fin = 0
    syn = 1
    rst = 0
    psh = 0
    ack = 0
    urg = 0
    window = socket.htons (5840)    #maximum allowed window size
    check = 0
    urg_ptr = 0

    offset_res = (doff << 4) + 0
    tcp_flags  = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)

    tcp_header = pack(TCP_STRUCT_FORMAT , sourcePort, destPort, seq, ack_seq, offset_res, tcp_flags,  window, check, urg_ptr)

    source_address = socket.inet_pton( socket.AF_INET6, sourceIp )
    dest_address = socket.inet_pton( socket.AF_INET6, destIp )

    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)
    psh = source_address + dest_address + pack('!BBH' , placeholder , protocol , tcp_length)
    psh = psh + tcp_header

    tcp_checksum = __checksum__(psh)
    # make the tcp header again and fill the correct checksum
    return pack(TCP_STRUCT_FORMAT , sourcePort, destPort, seq, ack_seq, offset_res, tcp_flags,  window, tcp_checksum , urg_ptr)
    
def __checksum__(data):
    """ Calculate checksum from data bytes.
    How to calculate checksum (RFC 2460):
        https://tools.ietf.org/html/rfc2460#page-27
    Args:
        data (bytes): input data from which checksum will be calculated
    Returns:
        int: calculated checksum
    """
    # Create halfwords from data bytes. Example: data[0] = 0x01, data[1] = 0xb2 => 0x01b2
    halfwords = [
        ((byte0 << 8) | byte1)
        for byte0, byte1 in zip_longest(data[::2], data[1::2], fillvalue=0x00)
    ]

    checksum = 0
    for halfword in halfwords:
        checksum += halfword
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum ^= 0xFFFF

    if checksum == 0:
        return 0xFFFF
    else:
        return checksum
