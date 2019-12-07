#cada pacote vai lever um byte de dado (1 char)

from socket import *
from threading import Thread
import select
import sys
import time

ok = 0 #semaforo

serverHost = "localhost"
serverPort = 5000
server = (serverHost, serverPort)

def sendPkt(mensagem, conexao):
    for i in range(0, len(mensagem), 1):
        pkt = str(mensagem[i])+str(i)+str(len(mensagem))
        pkt = bytes(pkt, 'utf-8')
        conexao.sendto(pkt, server)

def receiveMsg(conexao): #recebendo a mensagem
    data, endereco = conexao.recvfrom(1024)
    data = data.decode('utf-8')
    data = tuple(data)
    msg = data[0]
    
    #print(data) #recebendo os pacotes
    if len(data)< 3:
        tam = int(data[2])
    else:
        tam = ' '
        for i in range(2, len(data), 1):
            tam = tam+data[i] 
        tam = int(tam)

    for i in range(1, tam, 1):
        data, endereco = conexao.recvfrom(1024)
        data = data.decode('utf-8')
        data = tuple(data)
        msg = msg+data[0]

    return msg, endereco

def sendmsg(conexao):
    global ok
    msg = ' '
    while msg != 's': #tratando o envio da mensagem    
        msg = input('-> ')
        
        sendPkt(msg, conexao)
    ok = 1
    return

def rcvmsg(conexao):
    global ok
    while True:
        try:
            data, endereco = receiveMsg(conexao) #recebe a mensagem do server de que teve uma mensagem recebida
            print(data, '\n-> ', end='') 
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
        #conexao.bind(server)

        sendPkt(self.usr, conexao)
        data, endereco = receiveMsg(conexao) #recebe a mensagem do server de que teve uma mensagem recebida
        print(data)

        #tratando o recebimento e envio da mensagem
        s_msg = Thread(target = sendmsg, args = (conexao,))
        s_msg.start()
        r_msg = Thread(target = rcvmsg, args = (conexao,))
        r_msg.start()
        
        r_msg.join()
        s_msg.join()
        conexao.close()

def main():
    usr = input('Digite o nome de usuario: ')
    c = int(input('Digite seu ID: '))
    cliente = Cliente(c, usr, serverHost, serverPort)
    cliente.run()
 
if __name__ == '__main__':
    main()