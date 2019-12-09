from socket import *

host = ""
port = 5000
dest = (host, port)

def geraErro(mensagem, i):
    pkt = str(mensagem[i])+'0'+str(len(mensagem))
    return pkt

def geraPacote(mensagem, i):
    pkt = str(mensagem[i])+str(i)+str(len(mensagem))
    return pkt

def sendPkt(mensagem, conexao, endereco): #enviando o pacot
    i = 0
    ack = 0
    while i < len(mensagem):
        if i%7 == 0 and ack == 0:
            pkt = geraErro(mensagem, i)
            pkt = bytes(pkt, 'utf-8')
            conexao.sendto(pkt, endereco)
            #print('oi')
        else:
            pkt = str(mensagem[i])+str(i)+str(len(mensagem))
            pkt = bytes(pkt, 'utf-8')
            conexao.sendto(pkt, endereco)
            ack = 0

        #verificando se recebeu a mensagem correta:
        data, end = conexao.recvfrom(1024)
        if data.decode('utf-8') == 'ACK0':
            i = i+1
        else:
            ack = 1

def receiveMsg(server): #recebendo a mensagem
    data, endereco = server.recvfrom(1024)
    data = data.decode('utf-8')
    data = tuple(data)
    msg = data[0]
    
    if data[1] == '0':
        server.sendto(b'ACK0', endereco) #enviando ack0 se recebeu a mensagem correta
    else:
        server.sendto(b'ACK1', endereco)

    print(data) #recebendo os pacotes
    if len(data)< 3:
        tam = int(data[2])
    else:
        tam = ' '
        for i in range(2, len(data), 1):
            tam = tam+data[i] 
        tam = int(tam)
        #print(tam)
    
    i=1 #for manual (?)
    while i < tam:
        data, endereco = server.recvfrom(1024)
        data = data.decode('utf-8')
        data = tuple(data)

        x = str(i)
        x = len(x)
        nseq = data[1]
        if i >= 10:
            for j in range(2, x+1, 1):
                nseq = nseq+data[j]
        
        nseq = int(nseq)
        print(nseq)
        if nseq == i:
            print('ok')
            server.sendto(b'ACK0', endereco) #enviando ack0 se recebeu a mensagem correta
            i = i+1
            msg = msg+data[0]
        else:
            server.sendto(b'ACK1', endereco)
            print(i)

    return msg, endereco

def broadcast(endereco, enderecos, server, msg): #enviando para todos os clients
    for end in enderecos:
        if end != endereco:
            print(end)
            sendPkt(msg, server, end)

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
        data, endereco = receiveMsg(server)
        if not (endereco in enderecos):
            enderecos.append(endereco)
            usuarios.append(data) #salvando nome e endereco de quem entrou no chat

            print("%s conectou"%(data))
            sendPkt('Bem-vindo!', server, endereco) #avisando ao endereco que ele entrou
            
            msg = data + ' entrou do chat!'  #avisando que o usuario entrou no chat
            msgb = bytes(msg, 'utf-8')
            broadcast(endereco, enderecos, server, msg)
        else:
            if data == 's':
                x = enderecos.index(endereco)
                print("%s desconectou"%(usuarios[x]))
                sendPkt('Tchau!', server, endereco)
                
                #avisando que o usuario saiu
                msg = usuarios[x] + ' saiu do chat!' 
                msgb = bytes(msg, 'utf-8')
                broadcast(endereco, enderecos, server, msg)
                
                #removendo usuario
                remove(endereco, enderecos)
                remove(usuarios[x], usuarios)
            else:
                x = enderecos.index(endereco)
                msg = usuarios[x] + ': ' + data
                broadcast(endereco, enderecos, server, msg)

    # Fechamos o servidor
    server.close()
 
if __name__ == '__main__':
    main()
