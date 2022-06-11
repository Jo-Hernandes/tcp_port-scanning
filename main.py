import argparse
import socket
import subprocess
import pScanner as ps
import sys


def setupArguments():
    parser = argparse.ArgumentParser(
        description='Program performa  port scanner on the host and offers different attacks')
    parser.add_argument(
        '-i', '--ip', required=True, type=str, help='Attacked machine IP')
    parser.add_argument(
        '-m', '--mac', required=True, type=str, help='Attacked machine MAC')
    parser.add_argument(
        '-int', '--interface', required=False, type=str, help='Current machine interface', default='en0')
    parser.add_argument(
        '-o', '--OS', required=False, type=str, help='Current machine OS', default='macOS')

    return parser.parse_args()


if __name__ == "__main__":
    args = setupArguments()
    serverIp = args.ip
    serverMac = args.mac
    
    try:
        subprocess.call('clear', shell=True)
        remoteServerIP = socket.gethostbyname(serverIp)

        print ("Scanning remote host", remoteServerIP)
        for port in range (1,65535):
            ps.scanPort(remoteServerIP, port)      
                    
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()