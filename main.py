import argparse
import subprocess
import sys
import ethernetUtils
import pScanner as ps
import domain.setupParser as parser


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
            parser.loadData(args.settings)
        
                    
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()