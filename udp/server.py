from socket import *

host = ""
port = 5000
dest = (host, port)

def broadcast(endereco, enderecos, server, msgb): #enviando para todos os clients
    for end in enderecos:
        if end != endereco:
            print(end)
            server.sendto(msgb, end)

def remove(endereco, enderecos):
    if endereco in enderecos:
        enderecos.remove(endereco)

def main():
    server = socket(AF_INET, SOCK_DGRAM)
    server.bind(dest)
    print("Servidor iniciado")
    
    enderecos = [] #vetor que guarda os enderecos conectados no server
    usuarios = [] #vetor que guarda o nome dos usuarios

    while True:
        data, endereco = server.recvfrom(1024)
        if not (endereco in enderecos):
            enderecos.append(endereco)
            usuarios.append(data.decode("utf-8")) #salvando nome e endereco de quem entrou no chat

            print("%s conectou"%(data.decode("utf-8")))
            server.sendto(b'Bem-vindo!', endereco) #avisando ao endereco que ele entrou
            
            msg = '\n' + data.decode("utf-8") + ' entrou do chat!'  #avisando que o usuario entrou no chat
            msgb = bytes(msg, 'utf-8')
            broadcast(endereco, enderecos, server, msgb)
        else:
            if data.decode("utf-8") == 's':
                x = enderecos.index(endereco)
                print("%s desconectou"%(usuarios[x]))
                server.sendto(b'Tchau!', endereco)
                
                #avisando que o usuario saiu
                msg = '\n' + usuarios[x] + ' saiu do chat!' 
                msgb = bytes(msg, 'utf-8')
                broadcast(endereco, enderecos, server, msgb)
                
                #removendo usuario
                remove(endereco, enderecos)
                remove(usuarios[x], usuarios)
            else:
                x = enderecos.index(endereco)
                msg = usuarios[x] + ': ' + data.decode("utf-8")
                msgb = bytes(msg, 'utf-8')
                broadcast(endereco, enderecos, server, msgb)

    # Fechamos o servidor
    server.close()
 
if __name__ == '__main__':
    main()