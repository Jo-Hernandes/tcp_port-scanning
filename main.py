import argparse
import subprocess
import sys
import domain.setupParser as parser

from attacks.tcpConnectAttack import doTcpConnectAttack
from attacks.tcpHalfOpenningAttack import doHalfOpenningAttack
from attacks.tcpFINAttack import doFINAttack
from attacks.tcpFPUAttack import doFPUAttack

def setupArguments():
    parser = argparse.ArgumentParser(
        description='Program performs port scanner on the host and offers different attacks',
        epilog="If first time running, please use -n to generate new settings file, else, run with -s")
    
    # attacked data
    parser.add_argument(
        '-s', '--settings', type=str, help='JSON settings file to accomplish attacks')

    parser.add_argument(
        '-n', '--new', action='store_const', const=True, help='Generate JSON settings')
    
    parser.add_argument(
        '-c', '--connect', action='store_const', const='CON', help='Use Connect Attack')

    parser.add_argument(
        '-ho', '--half-openning', action='store_const', const='HOP', help='Use Half Openning Attack')

    parser.add_argument(
        '-f', '--fin', action='store_const', const='FIN', help='Use FIN Attack')

    parser.add_argument(
        '-F', '--FPU', action='store_const', const='FPU', help='Use FIN/PSH/URG Attack')

    return parser.parse_args()

attacks = {
    'CON' : ('Tcp Connect Attack', lambda dstHost, srcHost : doTcpConnectAttack(dstHost, srcHost)),
    'HOP' : ('Half-Openning Attack', lambda dstHost, srcHost : doHalfOpenningAttack(dstHost, srcHost)),
    'FIN' : ('FIN Attack', lambda dstHost, srcHost : doFINAttack(dstHost, srcHost)),
    'FPU' : ('FIN/PSH/URG Attack', lambda dstHost, srcHost : doFPUAttack(dstHost, srcHost))
}

attackMessage = {
    True :  (1, '\N{hear-no-evil monkey} SUCCESS'),
    False : (0, '\N{see-no-evil monkey} FAILED')
}

portResult = {
    True :  '\N{ghost} PORT IS OPEN \N{ghost}',
    False : '\N{pile of poo} PORT IS CLOSED \N{pile of poo}'
}

if __name__ == "__main__":
    args = setupArguments()

    usingAttacks = [x for x in [args.connect, args.half_openning, args.fin, args.FPU] if x is not None]
        
    try:
        subprocess.call('clear', shell=True)
        if args.new:
            parser.generateFile()
            sys.exit()
        else:
            dst, src, portRange = parser.loadData(args.settings)
            for port in range(portRange.start, portRange.end):
                print('\N{smiling face with horns} Verifying port {} on {} \N{smiling face with horns}'.format(port, dst.ipv6))
                dst.port = port
                totalAttacks = 0
                for currentAttack in usingAttacks:
                    attackTitle, attackMethod = (attacks[currentAttack])
                    print('\N{alien monster} Initializing {} :'.format(attackTitle))
                    value, message = attackMessage[attackMethod(dst, src)]
                    totalAttacks = totalAttacks + value
                    print(' -- Attack Status : {}'.format(message))
                
                print('Result for {} : {} \n'.format(port, portResult[totalAttacks == len(usingAttacks)]))
                

                

                
                

    except TypeError as e:
        print("Incorred values in settings file: {}".format(e))
        sys.exit()    
                    
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()