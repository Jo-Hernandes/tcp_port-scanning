import argparse
import subprocess
import sys
import ethernetUtils
import pScanner as ps


def setupArguments():
    parser = argparse.ArgumentParser(
        description='Program performa  port scanner on the host and offers different attacks')
    
    # attacked data
    parser.add_argument(
        '-i', '--ip', required=True, type=str, help='Attacked machine IP')
    parser.add_argument(
        '-m', '--mac', required=True, type=str, help='Attacked machine MAC')
    parser.add_argument(
        '-p', '--port', required=False, type=str, help='Current machine port', default='80')
    parser.add_argument(
        '-int', '--interface', required=False, type=str, help='Current machine interface', default='en0')
    parser.add_argument(
        '-o', '--OS', required=False, type=str, help='Current machine OS', default='macOS')

    return parser.parse_args()


if __name__ == "__main__":
    args = setupArguments()
    hostIp = args.ip
    hostMac = args.mac
    myPort = args.port
    int = args.interface
        
    try:
        subprocess.call('clear', shell=True)

        myMac = ethernetUtils.getMac(int)
        myIPv6 = ethernetUtils.getIPv6fromMac(myMac)

        print ("Scanning remote host", hostIp)
        
        for port in range (1,65535):
            ps.scanPort(hostIp, hostMac, port, myIPv6, myMac, myPort)      
                    
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()