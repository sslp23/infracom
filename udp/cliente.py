#cada pacote vai lever um byte de dado (1 char)

from socket import *
from threading import Thread
import select
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
import functools

ok = 0 #semaforo
ok2 = 0 #outrosemaforo
ack = 0

serverHost = "localhost"
serverPort = 5000
server = (serverHost, serverPort)
flag = 0
MSG = ' '
DATA = ' '

@functools.lru_cache()
class GlobalObject(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._events = {}

    def addEventListener(self, name, func):
        if name not in self._events:
            self._events[name] = [func]
        else:
            self._events[name].append(func)

    def dispatchEvent(self, name):
        functions = self._events.get(name, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, func)

def geraErro(mensagem, i):
    pkt = str(mensagem[i])+'0'+str(len(mensagem))
    return pkt

def geraPacote(mensagem, i):
    pkt = str(mensagem[i])+str(i)+str(len(mensagem))
    return pkt

def sendPkt(mensagem, conexao):
    global ack
    global ok2

    i=0
    while i<len(mensagem):
        if i%7 == 0 and ack == 0: #gero um erro em todos os pacotes de numero de sequencia multiplos de 7
            pkt = geraErro(mensagem, i)
            pkt = bytes(pkt, 'utf-8')
            conexao.sendto(pkt, server)
        else:
            pkt = geraPacote(mensagem, i)
            pkt = bytes(pkt, 'utf-8')
            conexao.sendto(pkt, server)
            ack = 0
        
        while ok2 == 0:
            pass
            
        if ack == 1:
            ok2 = 0
        else:
            i = i+1
            ok2 = 0

def sendPktUsr(mensagem, conexao):
    global ack

    for i in range(0, len(mensagem), 1):
        pkt = str(mensagem[i])+str(i)+str(len(mensagem))
        pkt = bytes(pkt, 'utf-8')
        conexao.sendto(pkt, server)
        
        data, endereco = conexao.recvfrom(1024)
        if data.decode('utf-8') == 'ack1':
            ack = 1
        if ack == 1:
            conexao.sendto(pkt, server)
            i = i-1
            ack = 0

def receiveMsg(conexao): #recebendo a mensagem
    global ack
    global ok2

    data, endereco = conexao.recvfrom(1024)
    data = data.decode('utf-8')
    if data == 'ACK1':
        ack = 1
        msg = 'ack'
        ok2 = 1
    elif data == 'ACK0':
        msg = 'ack'
        ok2 = 1
        ack = 0
    else:    
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
    global flag
    global MSG
    msg = ' '
    while msg != 's': #tratando o envio da mensagem    
        if flag == 1:
            msg = MSG
            sendPkt(msg, conexao)
            flag = 0
    ok = 1
    return

def rcvmsg(conexao):
    global ok
    global DATA
    while True:
        try:
            data, endereco = receiveMsg(conexao) #recebe a mensagem do server de que teve uma mensagem recebida
            if data != 'ack':
                DATA = data
                GlobalObject().dispatchEvent("rcv")
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

        sendPktUsr(self.usr, conexao)
        data, endereco = receiveMsg(conexao) #recebe a mensagem do server de que teve uma mensagem recebida
        print(data)

        #tratando o recebimento e envio da mensagem
        s_msg = Thread(target = sendmsg, args = (conexao,))
        s_msg.start()
        r_msg = Thread(target = rcvmsg, args = (conexao,))
        r_msg.start()
        chat = Thread(target = main2, args = (self.usr,))
        chat.start()
        
        r_msg.join()
        s_msg.join()
        chat.join()
        conexao.close()

class App(QMainWindow):

    def __init__(self, usr):
        super().__init__()
        self.title = 'Chat do Uol'
        self.left = 500
        self.top = 300
        self.width = 420
        self.height = 480
        self.label = QLabel('Chat do Uol', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel(self)  
        self.label4 = QLabel(self)      
        self.label5 = QLabel(self)   
        self.label6 = QLabel(self)  
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)
        self.label9 = QLabel(self)
        self.textbox = QtWidgets.QTextEdit(self)
        self.button = QPushButton('Enviar', self)
        self.usr = usr
        self.temp_list = []
        self.i = 0
        self.j = 25
        for x in range (self.i, self.j):
            self.temp_list.append("\n ")
        
        self.initUI()
       
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.label.move(180,10)
        
        self.label2.move(40,60)
        self.label2.resize(360,350)

        self.label3.setPixmap(QPixmap('beibe shark.jpg'))
        self.label3.setGeometry(402,0,19,480)
        
        self.label4.setPixmap(QPixmap('beibe shark.jpg'))
        self.label4.setGeometry(0,0,19,480)

        self.label5.setPixmap(QPixmap('beibe shark.jpg'))
        self.label5.setGeometry(19,472,384,9)

        self.label6.setPixmap(QPixmap('beibe shark.jpg'))
        self.label6.setGeometry(19,0,384,18)

        self.label7.setPixmap(QPixmap('beibe shark.jpg'))
        self.label7.setGeometry(19,35,384,14)

        self.label8.setPixmap(QPixmap('beibe shark.jpg'))
        self.label8.setGeometry(19,18,155,20)

        self.label9.setPixmap(QPixmap('beibe shark.jpg'))
        self.label9.setGeometry(242,18,160,20)
        
        self.textbox.move(40,430)
        self.textbox.resize(220,30)
        self.textbox.textChanged.connect(self.check_enter)
        
        self.button.move(280,430)
        self.button.clicked.connect(self.send)

        GlobalObject().addEventListener("rcv", self.rcv)

    def paintEvent(self, event):
        global flag2
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.drawRect(20,50,380,420)

    def check_enter(self):
        text = self.textbox.document().toPlainText()
        if len(text) > 1:
            if text[-1] == '\n':
                self.textbox.setText(text[:-1])
                self.send()
        
    def send(self):
        global flag
        global MSG
        MSG = self.textbox.document().toPlainText()
        self.temp_list.append('\n'+self.usr+': '+MSG)
        self.i += 1
        self.j += 1
        text = ' '
        for x in range (self.i,self.j):
            text = text + self.temp_list[x]
            
        self.label2.setText(text)
        self.textbox.setText('')
        flag = 1

    def rcv(self):
        if DATA == "Tchau!":
            print ("desconectado")
            self.close()
        else:
            self.temp_list.append('\n'+DATA)
            self.i += 1
            self.j += 1
            text = ' '
            for x in range (self.i,self.j):
                text = text + self.temp_list[x]
                
            self.label2.setText(text)         
            
  
            

def main():
    usr = input('Digite o nome de usuario: ')
    c = int(input('Digite seu ID: '))
    cliente = Cliente(c, usr, serverHost, serverPort)
    cliente.run()
    
def main2(usr):
    app = QApplication(sys.argv)
    ex = App(usr)
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
