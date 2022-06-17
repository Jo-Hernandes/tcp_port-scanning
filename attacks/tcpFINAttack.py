from attacks.defaultAttack import *
from domain.tcpHeaderFlag import FIN

def __onTcpReceived(_, __, tcpPacket):
    if tcpPacket['flag_rst'] == 1 :
       return False
    else :
        return True

def doFINAttack(dstHost, srcHost):
    return doTcpAttack(dstHost, srcHost, tcpFlags=FIN, reverse=True, onPacketReceive=__onTcpReceived)

