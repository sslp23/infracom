from socket import *
from models.Dns import Dns

serverHost = 'localhost'
serverPort = 5000

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((serverHost, serverPort))

nm_user = input('Digite seu nome de usuario: ')
msgb = bytes(nm_user, 'utf-8') #convertendo string pra byte
sock.send(msgb) #reenvia a mensagem
data = sock.recv(1024) #recebe a mensagem do server de que teve uma mensagem recebida
print('Seu nome de usuario eh: ', data.decode("utf-8"))

msg = ' '
while msg!= 's': 
    msg = input('-> ') #recebe a mensagem
    msgb = bytes(msg, 'utf-8') #convertendo string pra byte
    sock.send(msgb) #reenvia a mensagem
    data = sock.recv(1024) #recebe a mensagem do server de que teve uma mensagem recebida
    print('%s:'%(nm_user), data.decode("utf-8"))
 
sock.close()