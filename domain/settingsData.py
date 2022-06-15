class HostData:
    def __init__(self, ipv6, mac, port):
        self.ipv6 = ipv6
        self.mac = mac
        self.port = port

    @classmethod
    def fromDict(cls, dict):
        return cls(dict['ipv6'],dict['mac'], dict['port'])
