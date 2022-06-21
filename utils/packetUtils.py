import socket
import binascii
import sys

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


def buildEthernet(destinationMac, sourceMac, protocol):
    packet = pack(ETH_STRUCT_FORMAT, destinationMac, sourceMac, protocol)
    return packet

def buildIPv6Packet(destIp, sourceIp, len):
    version     = 6                       #4 bit
    traffic_class = 0                     #8 bit
    flow_level  = 1                       #20 bit
    payload_len = len                     #16 bit
    next_header = socket.IPPROTO_TCP      #8 bit
    hop_limit   = 255                     #8 bit
    saddr = socket.inet_pton ( socket.AF_INET6, sourceIp )  #128 bit
    daddr = socket.inet_pton ( socket.AF_INET6, destIp   )  #128 bit

    ver_traff_flow = (version << 8) + traffic_class
    ver_traff_flow = (ver_traff_flow << 20) + flow_level

    ip_header = pack(IPV6_STRUCT_FORMAT, ver_traff_flow, payload_len, next_header, hop_limit)
    return ip_header + saddr + daddr
    

def buildTcpPacket(destIp, sourceIp, destPort, sourcePort, sequence = 0, ackSeq = 0, flags = {'fin' : 0, 'syn' : 0, 'rst' : 0, 'psh' : 0, 'ack' : 0, 'urg' : 0 } ):
    seq = sequence
    ack_seq = ackSeq
    doff = 5    #4 bit field, size of tcp header, 5*4 = 20 bytes
    #tcp flags
    fin = flags['fin']
    syn = flags['syn']
    rst = flags['rst']
    psh = flags['psh']
    ack = flags['ack']
    urg = flags['urg']

    window = socket.htons (9000)
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


def ethernet_frame(data):
    """
        Unpacks our ethernet frame.
    """
    dest_mac, src_mac, proto = unpack('! 6s 6s H', data[:14])
    output = {
        "source": getReadableMac(dest_mac),
        "dest": getReadableMac(src_mac),
        "protocol": socket.htons(proto),
        "payload": data[14:],
    }
    return output


def get_ipv6_addr(mac_bytes):
    return socket.inet_ntop(socket.AF_INET6, mac_bytes).upper()


def ipv6_unpack(data):
    """
        Breaks open the ipv6 header and returns the payload while
        printing all the relevant information inside the header
    """
    version = data[0] >> 4
    traffic_class = (data[0] & 0xF) * 16 + (data[1] >> 4)
    payload_length = int(binascii.hexlify(data[4:6]).decode('ascii'), 16)
    next_header = data[6]
    hop_limit = data[7]
    src_address = get_ipv6_addr(data[8:24])
    target_address = get_ipv6_addr(data[24:40])
    # string = f'IPv{version} Source: {src_address}  Target: {target_address} Payload: {payload_length} bytes'
    output = {
        "version": version,
        "next_header": next_header,
        "source": src_address,
        "target": target_address,
        "payload": data[40:]
    }
    return output


def tcp_unpack(data):
    src_port, dest_port, sequence, ack, offset_r_flags = unpack('! H H L L H', data[:14])
    offset = (offset_r_flags >> 12) * 4
    flag_urg = (offset_r_flags & 32) >> 5
    flag_ack = (offset_r_flags & 16) >> 4
    flag_psh = (offset_r_flags & 8) >> 3
    flag_rst = (offset_r_flags & 4) >> 2
    flag_syn = (offset_r_flags & 2) >> 1
    flag_fin = offset_r_flags & 1
    output = {
        "source": src_port, "dest": dest_port, "sequence": sequence, "ack": ack, "offset_r_flags": offset_r_flags,
        "flag_ack": flag_ack, "flag_rst": flag_rst, "flag_syn": flag_syn, "flag_fin": flag_fin, 'flag_urg': flag_urg, 'flag_psh' : flag_psh
    }
    return output