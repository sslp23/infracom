from socket import *

a = 1

class Dns():
    def __init__(self, dns_address):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.dns_address = dns_address

    def registerServerAs(self, url):
        self.sock.sendto(bytes(1), self.dns_address)
        message, address = self.sock.recvfrom(1024)
        if message == bytes(1):
            self.sock.sendto(bytes(url, 'utf-8'), self.dns_address)
        message, address = self.sock.recvfrom(1024)
        if message == bytes(1):
            return self.sock.getsockname()
        return ('', 0)
    
    def getIPFrom(self, url):
        self.sock.sendto(bytes(2), self.dns_address)
        message, address = self.sock.recvfrom(1024)
        if message == bytes(2):
            self.sock.sendto(bytes(url, 'utf-8'), self.dns_address)
        else:
            self.sock.sendto(bytes(5))
            return
        ip, adr = self.sock.recvfrom(1024)
        ip = ip.decode('utf-8')
        dor, adr = self.sock.recvfrom(1024)
        dor = int(dor.decode('utf-8'))
        return (ip, dor)

    def close(self):
        self.sock.close()