from attacks.defaultAttack import *
from domain.tcpHeaderFlag import SYN, ACK, FIN

def __onTcpReceived(dstHost, srcHost, tcpPacket):
    if (tcpPacket['flag_ack'] == 1 and tcpPacket['flag_syn'] == 1):
        seq = tcpPacket['sequence'] + 1 
        ack = tcpPacket['ack'] + 1
        eUtils.sendeth(getTcpPacket(dstHost, srcHost, ACK, seqNumber=ack, ackNumber=seq), srcHost.interface, srcHost.port)
        return True
    else :
        return False

def doTcpConnectAttack(dstHost, srcHost):
    return doTcpAttack(dstHost, srcHost, tcpFlags=SYN, onPacketReceive=__onTcpReceived)
