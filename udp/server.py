from socket import *

host = ""
port = 5000 

def main():
    server = socket(AF_INET, SOCK_DGRAM)
    print("Servidor iniciado")
    
    enderecos = [] #vetor que guarda os enderecos conectados no server

    while True:
        data, endereco = server.recvfrom(1024)
        if endereco not in enderecos:
            enderecos.append(endereco)
            usr = data.decode("utf-8")
            print("%s conectou"%(data.decode("utf-8")))

            server.sendto(b'Bem-vindo!', endereco) #avisando ao endereco que ele entrou
     
    # Fechamos o servidor
    server.close()
 
if __name__ == '__main__':
    main()