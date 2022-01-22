import socket
import sys
#import Task6_server
from PyQt5 import QtWidgets, QtCore,QtNetwork
from PyQt5.QtNetwork import *
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, \
     QGridLayout, QPushButton, QLineEdit, QSpinBox, QLabel, QPlainTextEdit


class TcpController(QObject):

    chatSig=pyqtSignal(str)

    def __init__(self):
        super (TcpController,self).__init__()
        self.TCP_HOST="127.0.0.1"
        self.TCP_SEND_TO_PORT = 8000
        self.chSocket = QtNetwork.QTcpSocket()
        
        self.chSocket.readyRead.connect(self.tcpReadData)

    def tcpUserMessage(self, msg):
    	print(msg)
    	self.tcpSendMessage(msg)

    def tcpSendMessage(self,msg):
        self.chSocket.connectToHost(self.TCP_HOST, self.TCP_SEND_TO_PORT)
        self.tcpTransmissionMessage(msg)

    def tcpTransmissionMessage(self, data):
        cmd = data.encode('utf-8')
        print("Message Sent:", cmd)
        self.chSocket.writeData(cmd)
        print("Transmitted")
        #self.chSocket.disconnectFromHost()

    def tcpReadData (self):
        print("Message Coming")
        data=self.chSocket.readAll()
        print("Client Message:", data)
        #print("Reading data:", data)
        self.chatSig.emit(str(data))


class ClientWindow(QDialog):
    
    def __init__(self):
        super(ClientWindow, self).__init__()
        self.setWindowTitle("Chat")

        self.le1 = QLineEdit()
        self.le2 = QLineEdit()

        self.lbs = QLabel()
        self.lbs.setText("Your message")

        self.lbs2 = QLabel()
        self.lbs2.setText("Server answer")

        self.pb = QPushButton()
        self.pb.setObjectName("Load message")
        self.pb.setText("Send message")

        self.meswindow = QPlainTextEdit()

        layout = QGridLayout()
        layout.addWidget(self.lbs)
        layout.addWidget(self.le1)
        layout.addWidget(self.pb)
        layout.addWidget(self.lbs2)
        layout.addWidget(self.le2)
        layout.addWidget(self.meswindow)
        self.setLayout(layout)
        self.tcp=TcpController()

        self.tcp.chatSig.connect(self.ser_answer)
        self.pb.clicked.connect(self.setup)

    def setup(self):
        msg=self.le1.text()
        self.tcp.tcpUserMessage(msg)
    def ser_answer(self, sermsg):
        sermsg=sermsg.replace("b","").replace("'","")
        self.le2.setText(sermsg)
        self.meswindow.insertPlainText(sermsg)
        self.meswindow.insertPlainText("\n")



if __name__ == '__main__':            
    app = QApplication(sys.argv)
    form = ClientWindow()
    form.show()
    app.exec_()
