import argparse
import subprocess
import sys
import domain.setupParser as parser
from domain.settingsData import HostData, PortRange
from attacks.tcpConnectAttack import doTcpConnect

def setupArguments():
    parser = argparse.ArgumentParser(
        description='Program performa port scanner on the host and offers different attacks',
        epilog="OI")
    
    # attacked data
    parser.add_argument(
        '-s', '--settings', type=str, help='JSON settings file to accomplish attacks')

    parser.add_argument(
        '-n', '--new', action='store_const', const=True, help='Generate JSON settings')
    
    return parser.parse_args()


if __name__ == "__main__":
    args = setupArguments()
        
    try:
        subprocess.call('clear', shell=True)
        if args.new:
            parser.generateFile()
            sys.exit()
        else:
            dst, src, portRange = parser.loadData(args.settings)
            print(dst, src, portRange)
            for port in range(portRange.start, portRange.end):
                dst.port = port
                doTcpConnect(dst, src)
                

    except TypeError as e:
        print("Incorred values in settings file: {}".format(e))
        sys.exit()    
                    
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()