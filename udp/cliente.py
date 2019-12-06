from socket import *
from threading import Thread
import select
import sys
import time

ok = 0 #semaforo

serverHost = "localhost"
serverPort = 5000
server = (serverHost, serverPort)

def sendmsg(conexao):
    global ok
    msg = ' '
    while msg != 's': #tratando o envio da mensagem    
        msg = input('-> ')
        msgb = bytes(msg, 'utf-8') #convertendo string pra byte
        conexao.sendto(msgb,server) #reenvia a mensagem
    ok = 1
    return

def rcvmsg(conexao):
    global ok
    while True:
        try:
            data, endereco = conexao.recvfrom(1024) #recebe a mensagem do server de que teve uma mensagem recebida
            print(data.decode("utf-8"), '\n-> ', end='') 
            if ok == 1:
                return
        except OSError:
            break

class Cliente(Thread):

    def __init__(self, c, usr, server, port):
        self.c = c #id do cliente
        self.usr = usr #nome de usuario
        self.server = server
        self.port = port
        Thread.__init__(self)
    
    def run(self):
        conexao = socket(AF_INET, SOCK_DGRAM)
        conexao.bind((serverHost, serverPort))

        msgb = bytes(self.usr, 'utf-8') #convertendo string pra byte
        conexao.sendto(msgb, server) #reenvia a mensagem
        data, endereco = conexao.recvfrom(1024) #recebe a mensagem do server de que teve uma mensagem recebida
        print(data.decode("utf-8"))

        #tratando o recebimento e envio da mensagem
        s_msg = Thread(target = sendmsg, args = (conexao,))
        s_msg.start()
        r_msg = Thread(target = rcvmsg, args = (conexao,))
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