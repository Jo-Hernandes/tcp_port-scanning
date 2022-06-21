

import json
import os
from domain.settingsData import HostData, PortRange

jsonFileName = 'settings.json'

settingsDefault = """
{
    "dst_host" : {
        "ipv6" : "",
        "mac" : "",
        "interface": null,
        "port" : null
    },

    "src_host" : {
        "ipv6" : "",
        "mac" : "",
        "interface" : "",
        "port" : ""
    },

    "port_range" : {
        "start" : 0,
        "end" : 0
    }
}
"""
    
def loadData(jsonFile):
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
        return HostData.fromDict(dict = data['dst_host']), HostData.fromDict(dict = data['src_host']) , PortRange.fromDict(data['port_range'])

def generateFile():
    if not os.path.exists(jsonFileName):
        with open(jsonFileName, 'w') as settings: 
            settings.write(settingsDefault)
            print("File generated. Please check {}".format(jsonFileName))
    else:
        print("File already exists. Please check {}".format(jsonFileName))