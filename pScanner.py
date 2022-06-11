
import socket
import ethernetUtils as eUtils
import sys

def scanPort(host, port):
    try:
        sock = socket.socket()
        sock.settimeout(10)

        result = sock.connect_ex((host, port))
        if result == 0:
            sock.close()
            print ("Open Port Detected {}".format(port))
            print (eUtils.getMac())

            __startAttack(host, port)

    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        quit()

    except socket.gaierror:
        print ("Hostname could not be resolved. Exiting")
        quit()

    except socket.error:
        print ("Couldn't connect to server")
        quit()

        
def __startAttack(host, port):
    try:
        option = input ("1 -> TCP CONNECT \n" +
                        "0 -> Quit \n" +
                        "Select Attack : "
                        )

        {
        '0': lambda x, y : sys.exit(),
        '1': lambda host, port: print("PORT SCANNER: {} {}".format(host, port)) ,
        }[option](host, port)
    except SystemExit:
        print ("Quitting now")
        sys.exit()
    except :
        print ("Invalid option. Quitting now")
        sys.exit()