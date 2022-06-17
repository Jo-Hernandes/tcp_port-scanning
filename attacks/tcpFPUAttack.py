from attacks.defaultAttack import *
from domain.tcpHeaderFlag import FPU

def __onTcpReceived(_, __, tcpPacket):
    if tcpPacket['flag_rst'] == 1 :
       return False
    else :
        return True

def doFPUAttack(dstHost, srcHost):
    return doTcpAttack(dstHost, srcHost, tcpFlags=FPU, reverse=True, onPacketReceive=__onTcpReceived)

