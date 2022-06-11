
import socket
import sys
import tcpConnectAttack

def scanPort(destIp, destMac, dstPort, srcIp, srcMac, srcPort):
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.settimeout(10)

        result = sock.connect_ex((destIp, dstPort))
        if result == 0:
            sock.close()
            print ("Open Port Detected {}".format(dstPort))
            __startAttack(destIp, destMac, dstPort, srcIp, srcMac, srcPort)
        else :
            print ("Closed Port {}".format(dstPort))


    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        quit()

    except socket.gaierror:
        print ("Hostname could not be resolved. Exiting")
        quit()

    except socket.error:
        print ("Couldn't connect to server")
        quit()

        
def __startAttack(destIp, destMac, dstPort, srcIp, srcMac, srcPort):
    try:
        option = input ("1 -> TCP CONNECT \n" +
                        "0 -> Quit \n" +
                        "Select Attack : ")

        {
        '0': lambda a, b, c, x, y, z: sys.exit(),
        '1': lambda destIp, destMac, dstPort, srcIp, srcMac, srcPort: tcpConnectAttack.doTcpConnect(destIp, destMac, dstPort, srcIp, srcMac, srcPort) ,
        }[option](destIp, destMac, dstPort, srcIp, srcMac, srcPort)
    except SystemExit:
        print ("Quitting now")
        sys.exit()
    except Exception as e:
        print(e)
        print ("Invalid option. Quitting now")
        sys.exit()
        
