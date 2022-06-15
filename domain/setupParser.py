

import json
import os

jsonFileName = 'settings.json'

settingsDefault = """
{

    "dst_host" : {
        "ipv6" : "",
        "mac" : "",
        "port" : null
    },

    "src_host" : {
        "ipv6" : "",
        "mac" : "",
        "port" : ""
    },

    "port_range" : {
        "start" : 0,
        "end" : 12345
    }

}
"""

class HostData:
    def __init__(self, ipv6, mac, port):
        self.ipv6 = ipv6
        self.mac = mac
        self.port = port

    @classmethod
    def fromDict(cls, dict):
        return cls(dict['ipv6'],dict['mac'], dict['port'])

class PortRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def fromDict(cls, dict):
        return cls(dict['start'],dict['end'])
    
def loadData(jsonFile):
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
        print(HostData.fromDict(dict = data['dst_host']))
        print(HostData.fromDict(dict = data['src_host']))
        print(PortRange.fromDict(data['port_range']))

def generateFile():
    if not os.path.exists(jsonFileName):
        with open(jsonFileName, 'w') as settings: 
            settings.write(settingsDefault)
            print("File generated. Please check {}".format(jsonFileName))
    else:
        print("File already exists. Please check {}".format(jsonFileName))