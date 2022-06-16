
import utils.packetUtils as pUtils
import utils.ethernetUtils as eUtils


def doTcpConnect(dstHost, srcHost):
    ethernetHeader = pUtils.buildEthernet(eUtils.getMacAsByteArray(dstHost.mac), eUtils.getMacAsByteArray(srcHost.mac), pUtils.IPV6_ETH_HEADER)
    tcpHeader = pUtils.buildTcpPacket(dstHost.ipv6, srcHost.ipv6, int(dstHost.port), int(srcHost.port))
    ipHeader = pUtils.buildIPv6Packet(dstHost.ipv6, srcHost.ipv6, len(tcpHeader))
    
    sniffingSocket = eUtils.getSniffingSocket(srcHost.interface, 0)

    eUtils.sendeth(ethernetHeader + ipHeader + tcpHeader, srcHost.interface, srcHost.port)
    
    while True:
        packet = sniffingSocket.recvfrom(65565)
        packet = packet[0]
        ethernetPacket = pUtils.ethernet_frame(packet)
        
        if ethernetPacket["protocol"] == 56710:
            ipv6Packet = pUtils.ipv6_unpack(ethernetPacket['payload'])

            if ( ipv6Packet['source'] == dstHost.ipv6.upper() and
            ipv6Packet['target'] == srcHost.ipv6.upper() ): 

                tcpPacket = pUtils.tcp_unpack(ipv6Packet["payload"])
                print(pUtils.print_header(ipv6Packet, tcpPacket))

