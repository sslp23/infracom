from socket import *
import _thread as thread

def remove(conexao):
    if conexao in clients:
        clients.remove(conexao)

def broadcast(msgb, conexao): #enviando para todos os clients
    for i in range(0, clients.len(), 1):
        if clients[i] != conexao:
            try:
                print(clients[i])
                clients[i].sendto(msgb, endereco[i])
            except:
                clients[i].close()
                remove(client[i]) #tirando o cliente com link quebrado

def lidaCliente(conexao, endereco, usr):
    conexao.sendto(b'Bem-vindo!', endereco)
    while True: 
        while True:
            data, end = conexao.recvfrom(1024) #recebe o dado
            if data.decode() == 's':
                print("%s desconectou"%(usr))
                conexao.sendto(b'Tchau!', end)
                
                #avisando que o usuario saiu
                msg = '\n' + usr + ' saiu do chat!' 
                msgb = bytes(msg, 'utf-8')
                broadcast(msgb, conexao)
                
                #eliminando o usuario
                remove(conexao)
                break
            if not data:
                remove(conexao)
                break ##nao recebeu data, sai do loop
            msg = usr + ': ' + data.decode("utf-8")
            msgb = bytes(msg, 'utf-8')
            broadcast(msgb, conexao)
        
        conexao.close()

clients = []
enderecos = []

host = '' #string vazia = localhost
port = 5000

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

def main():
    while True:
        conexao, endereco = sock.accept()
        print('Servidor conectado por', endereco)

        clients.append(conexao)

        data, endereco = conexao.recvfrom(1024)
        enderecos.append(endereco)

        usr = data.decode("utf-8")
        print("%s conectou"%(data.decode("utf-8")))

        #avisando que o usr entrou
        msg = '\n' + usr + ' entrou do chat!' 
        msgb = bytes(msg, 'utf-8')
        broadcast(msgb, conexao)

        thread.start_new_thread(lidaCliente, (conexao,endereco,usr))
    
    conexao.close()
    sock.close()
if __name__ == '__main__':
    main()