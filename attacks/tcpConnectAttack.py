
import utils.packetUtils as pUtils
import utils.ethernetUtils as eUtils



def doTcpConnect(dstHost, srcHost):
    ethernetHeader = pUtils.buildEthernet(eUtils.getMacAsByteArray(dstHost.mac), eUtils.getMacAsByteArray(srcHost.mac), pUtils.IPV6_ETH_HEADER)
    tcpHeader = pUtils.buildTcpPacket(dstHost.ipv6, srcHost.ipv6, int(dstHost.port), int(srcHost.port))
    ipHeader = pUtils.buildIPv6Packet(dstHost.ipv6, srcHost.ipv6, len(tcpHeader))
    

    eUtils.sendeth(ethernetHeader + ipHeader + tcpHeader, srcHost.interface, srcHost.port)
    print("packet send")