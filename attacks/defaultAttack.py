import utils.packetUtils as pUtils
import utils.ethernetUtils as eUtils

from utils.loadingAnim import showAnimation

def getTcpPacket(dstHost, srcHost, tcpFlags):
    ethernetHeader = pUtils.buildEthernet(eUtils.getMacAsByteArray(dstHost.mac), eUtils.getMacAsByteArray(srcHost.mac), pUtils.IPV6_ETH_HEADER)
    tcpHeader = pUtils.buildTcpPacket(dstHost.ipv6, srcHost.ipv6, int(dstHost.port), int(srcHost.port), flags = tcpFlags)
    ipHeader = pUtils.buildIPv6Packet(dstHost.ipv6, srcHost.ipv6, len(tcpHeader))

    return ethernetHeader + ipHeader + tcpHeader

def doTcpAttack(dstHost, srcHost, tcpFlags, onPacketReceive):

    sniffingSocket = eUtils.getSniffingSocket()
    eUtils.sendeth(getTcpPacket(dstHost, srcHost, tcpFlags), srcHost.interface, srcHost.port)

    portOpen = False
    for i in range(0, 50):
        showAnimation(i)
        packet = sniffingSocket.recvfrom(65565)
        packet = packet[0]
        ethernetPacket = pUtils.ethernet_frame(packet)
        
        if ethernetPacket["protocol"] == 56710:
            ipv6Packet = pUtils.ipv6_unpack(ethernetPacket['payload'])

            if ( ipv6Packet['source'] == dstHost.ipv6.upper() and
            ipv6Packet['target'] == srcHost.ipv6.upper() ): 

                tcpPacket = pUtils.tcp_unpack(ipv6Packet['payload'])
                portOpen = portOpen and onPacketReceive(dstHost, srcHost, tcpPacket)

    sniffingSocket.close()
    print("\r", '', end="") 
    return portOpen





