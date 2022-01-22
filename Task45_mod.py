import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, \
     QGridLayout, QPushButton, QLineEdit, QSpinBox, QLabel
import pyqtgraph as pg


class DataController(QObject):
    dataReady = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.push_num = 0

    def pushed(self):
        
        self.push_num += 1
        self.dataReady.emit(str(self.push_num))
        pass


class DataLoader(QObject):
    data_load = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        wb_patch = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.InitFile(wb_patch)

    def InitFile(self, wb_patch):
        
        with open(wb_patch) as fp:
            self.text = fp.read()

        self.sing_string = []

        self.sing_string = self.text.split('\n')
        print (self.sing_string)

    def FindString(self, number):

        num = int(number)
        if (num == 0):
            self.line = str("Enter a number greater than 0")
        elif (num > len(self.sing_string)):
            self.line = str("Song ends")
        else:
            self.line = self.sing_string[num-1]
        self.data_load.emit(self.line)


class DataPreparing(QObject):
    string_data = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def DataConversion(self, data):
        self.letter_array = []
        self.list_line = list(data)
        for i in range(0, len(self.list_line)):
            self.letter_array.append(ord(self.list_line[i]))
        print(self.letter_array)
        self.string_data.emit(self.letter_array)


class DataViewer(QDialog):
    
    def __init__(self):
        super(DataViewer, self).__init__()

        self.view = view = pg.PlotWidget()
        self.curve = view.plot(pen=pg.mkPen('b', width=2))
        self.view.setBackground('w')
        self.view.setXRange(0, 60)
        self.view.setYRange(0, 150)
        self.view.enableAutoRange()
        self.view.setTitle('Numeric encoding of a line')
        self.view.setLabel('left', 'Symbol')
        self.view.setLabel('bottom', 'The number of the symbol in the string')

        self.le = QSpinBox()
        self.le2 = QLineEdit()

        self.lbs = QLabel()
        self.lbs.setText("Your string")

        self.pb = QPushButton()
        self.pb.setObjectName("Load String")
        self.pb.setText("Load Next String")

        layout = QGridLayout()
        layout.addWidget(self.lbs)
        layout.addWidget(self.le2)
        layout.addWidget(self.pb)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.setWindowTitle("String of Song")

        self.dataload = DataLoader()
        self.datacontrol = DataController()
        self.datapresentation = DataPreparing()

        self.datacontrol.dataReady.connect(self.dataload.FindString)
        self.dataload.data_load.connect(self.datapresentation.DataConversion)

        self.pb.clicked.connect(self.datacontrol.pushed)

        self.dataload.data_load.connect(self.ShowString)
        self.datapresentation.string_data.connect(self.PrintGraph)

    def ShowString(self, data):
        self.le2.setText(data)
        
    def PrintGraph(self, data):
        self.curve.setData(data)

if __name__ == '__main__':            
    app = QApplication(sys.argv)
    form = DataViewer()
    form.show()
    app.exec_()