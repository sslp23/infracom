import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', 10000))

# List of servers registereds
servers_addresses = {}

def registerServer(address):
    serverSocket.sendto(bytes(1), address)
    print('Registering server: ' + str(address), end='')
    message, adr = serverSocket.recvfrom(1024)
    message = message.decode('utf-8')
    print(' as ' + message)
    if message in servers_addresses:
        # Alredy exists
        print("Sever alredy exists")
        
        serverSocket.sendto(bytes(5), adr)
    else:
        # Dosn't exist yet
        print("Server registered")
        servers_addresses[message] = adr
        
        serverSocket.sendto(bytes(1), adr)

def listServer(address):
    serverSocket.sendto(bytes(2), address)
    print('New client request: ' + str(address))

    message, adr = serverSocket.recvfrom(1024)
    message = message.decode('utf-8')
    if message in servers_addresses:
        serverSocket.sendto(bytes(servers_addresses[message][0], 'utf-8'), adr)
        serverSocket.sendto(bytes(str(servers_addresses[message][1]), 'utf-8'), adr)
    elif message == bytes(5):
        # Lost order
        print("Indetected messsage from client")
        return
    else:   
        serverSocket.sendto(bytes('', 'utf-8'), adr)
        serverSocket.sendto(bytes('0', 'utf-8'), adr)


if __name__ == "__main__":
    while True:
        message, address = serverSocket.recvfrom(1024)
        if message == bytes(1):
            # Server connection
            registerServer(address)
        elif message == bytes(2):
            # Client connection
            listServer(address)
            continue
