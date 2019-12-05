from socket import *
import threading 
from threading import Thread
import select
import sys
import time

ok = 0#semaforo

#defines
serverHost = 'localhost'
serverPort = 5000


def sendmsg(sock):
    global ok
    msg = ' '
    while msg != 's': #tratando o envio da mensagem    
        msg = input('-> ')
        msgb = bytes(msg, 'utf-8') #convertendo string pra byte
        sock.send(msgb) #reenvia a mensagem
    ok = 1
    print(ok)
    return

def rcvmsg(sock):
    global ok
    while True:
        try:
            data = sock.recv(1024) #recebe a mensagem do server de que teve uma mensagem recebida
            print(data.decode("utf-8"), '\n-> ', end='') 
            if ok == 1:
                return
        except OSError:
            break

class Cliente(threading.Thread):

    def __init__(self, c, usr, server, port):
        self.c = c #id do cliente
        self.usr = usr #nome de usuario
        self.server = server
        self.port = port

        threading.Thread.__init__(self)
    
    def run(self): #criar a conexao
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.server, self.port))
        
        msgb = bytes(self.usr, 'utf-8') #convertendo string pra byte
        sock.send(msgb) #reenvia a mensagem
        data = sock.recv(1024) #recebe a mensagem do server de que teve uma mensagem recebida
        print(data.decode("utf-8"))

        #tratando o recebimento e envio da mensagem
        s_msg = Thread(target = sendmsg, args = (sock,))
        s_msg.start()
        r_msg = Thread(target = rcvmsg, args = (sock,))
        r_msg.start()
        
        r_msg.join()
        s_msg.join()
        sock.close()

def main():
    usr = input('Digite o nome de usuario: ')
    c = int(input('Digite seu ID: '))
    cliente = Cliente(c, usr, serverHost, serverPort)
    cliente.run()

if __name__ == '__main__':
    main()