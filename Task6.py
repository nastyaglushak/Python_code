import sys
import socket
from PyQt5 import QtWidgets, QtCore, QtNetwork
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit,QVBoxLayout,QWidget,QPlainTextEdit
from PyQt5.QtNetwork import *
from PyQt5.QtCore import pyqtSignal

class Chat(QtCore.QObject):

    chatSig=pyqtSignal(str)

    def __init__(self):
        super (Chat,self).__init__()
        self.TCP_HOST="127.0.0.1"
        self.TCP_SEND_TO_PORT = 8000
        self.cSocket = QtNetwork.QTcpSocket()
        
        self.cSocket.readyRead.connect(self.funReadData)
        self.cSocket.connected.connect(self.on_connected)

        self.chatSig.connect(self.on_connected)
        
    def funSendMessage(self,msg):
        self.cSocket.connectToHost(self.TCP_HOST, self.TCP_SEND_TO_PORT)
        self.chatSig.emit(msg) 

    def on_connected(self, msg):
        cmd = msg.encode('utf-8')
        print("Command Sent:", cmd)
        self.cSocket.write(cmd)
        self.cSocket.flush()
        self.cSocket.disconnectFromHost()

    def funReadData (self):
        print("Reading data:", self.cSocket.readAll())


class Client(QtCore.QObject):
    def SetSocket(self, socket):
        self.socket = socket
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.readyRead.connect(self.on_readyRead)
        print( "Client Connected from IP %s" % self.socket.peerAddress().toString())

    def on_connected(self):
        print("Client Connected Event")

    def on_disconnected(self):
        print("Client Disconnected")

    def on_readyRead(self):
        msg = self.socket.readAll()
        print("Client Message:", msg)


class Server(QTcpServer):
    def __init__(self):
        QTcpServer.__init__(self)
        self.TCP_LISTEN_TO_PORT = 8000
        self.sersocket = QtNetwork.QTcpServer()
        self.sersocket.newConnection.connect(self.on_newConnection)

    def on_newConnection(self):
        while self.sersocket.hasPendingConnections():
            print("Incoming Connection...")
            self.client = Client(self)
            self.client.SetSocket(self.sersocket.nextPendingConnection())

    def StartServer(self):
        if self.sersocket.listen(QtNetwork.QHostAddress.Any, self.TCP_LISTEN_TO_PORT):
        	print("Server is listening on port: {}".format( self.TCP_LISTEN_TO_PORT))



class Data_exchenger(QtWidgets.QMainWindow):
    def __init__(self):
        super (Data_exchenger, self).__init__()
        self.setWindowTitle("TCP Data Server")
        self.resize(300, 300)

        self.pb=QPushButton()
        self.pb.setText("Send data")
        self.lb=QLabel()
        self.lb.setText("Not Connetion")
        self.le=QLineEdit()
        self.vd=QPlainTextEdit()

        self.layout=QVBoxLayout()
        self.layout.addWidget(self.lb)
        self.layout.addWidget(self.pb)
        self.layout.addWidget(self.le)
        self.layout.addWidget(self.vd)
        self.widget=QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.pb.clicked.connect(self.setup)

    def setup(self):
        self.vd.appendPlainText("Hello")
        msg=self.le.text()

        self.server = Server()
        self.server.StartServer()
        self.lb.setText("Connetion")

        self.tcp=Chat()
        self.tcp.funSendMessage(msg)



if __name__ == '__main__':            
    app = QApplication(sys.argv)
    form = Data_exchenger()
    form.show()
    app.exec_()