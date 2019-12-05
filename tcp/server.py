from socket import *
import _thread as thread

def remove(conexao):
    if conexao in clients:
        clients.remove(conexao)

def broadcast(msgb, conexao): #enviando para todos os clients
    for client in clients:
        if client != conexao:
            try:
                print(client)
                client.send(msgb)
            except:
                client.close()
                remove(client) #tirando o cliente com link quebrado

def lidaCliente(conexao, endereco, usr):
    conexao.send(b'Bem-vindo!')
    while True: 
        while True:
            data = conexao.recv(1024) #recebe o dado
            if data.decode() == 's':
                print("%s desconectou"%(usr))
                conexao.send(b'Tchau!')
                
                #avisando que o usuario saiu
                msg = usr + ' saiu do chat!' 
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

host = '' #string vazia = localhost
port = 5000

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(5) #recebe no maximo 5

clients = []

def main():
    while True:
        conexao, endereco = sock.accept()
        print('Servidor conectado por', endereco)

        clients.append(conexao)

        data = conexao.recv(1024)
        usr = data.decode("utf-8")
        print("%s conectou"%(data.decode("utf-8")))

        thread.start_new_thread(lidaCliente, (conexao,endereco,usr))
    
    conexao.close()
    sock.close()
if __name__ == '__main__':
    main()