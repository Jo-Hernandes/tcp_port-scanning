class HostData:
    def __init__(self, ipv6, mac, interface, port):
        self.ipv6 = ipv6
        self.mac = mac
        self.interface = interface
        self.port = port
    
    def __str__(self):
        return 'IPv6 : {} | MAC : {} | Interface : {} | Port: {}'.format(self.ipv6, self.mac, self.interface, self.port)

    @classmethod
    def fromDict(cls, dict):
        return cls(dict['ipv6'],dict['mac'], dict['interface'], dict['port'])



class PortRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return 'Start : {} | End : {}'.format(self.start, self.end)

    @classmethod
    def fromDict(cls, dict):
        return cls(dict['start'],dict['end'])

