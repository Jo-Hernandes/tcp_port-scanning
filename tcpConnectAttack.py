
import packetUtils as pUtils
import ethernetUtils as eUtils



def doTcpConnect(destIp, destMac, dstPort, srcIp, srcMac, srcPort):
    ethernetHeader = pUtils.buildEthernet(eUtils.getMacAsByteArray(destMac), eUtils.getMacAsByteArray(srcMac), pUtils.IPV6_ETH_HEADER)
    tcpHeader = pUtils.buildTcpPacket(destIp, srcIp, int(dstPort), int(srcPort))

    ipHeader = pUtils.buildIPv6Packet(destIp, srcIp, len(tcpHeader))
    

    eUtils.sendeth(tcpHeader)
    print("packet send")