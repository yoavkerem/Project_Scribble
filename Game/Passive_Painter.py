from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Passive_Painter(QMainWindow):

    def __init__(self, c):
        self.c = c
        super().__init__()
        self.lstDat=[]
        self.setWindowTitle("Paint with PyQt5")
        self.coLst = [Qt.black, Qt.green, Qt.yellow, Qt.red, Qt.white,Qt.blue]
        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)
        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(100, 28)

        # Create a button in the window
        self.button = QPushButton('Enter', self)
        self.button.move(100, 0)
        self.button.clicked.connect(self.on_click)
        self.image.fill(Qt.white)
        self.painter=0

    def on_click(self):
        self.c.send_request_to_server(self.textbox.text())
        self.textbox.clear()

    def paintEvent(self, event):
        if self.lstDat != [] and self.lstDat!=["done"] and self.lstDat[0]!="true" and self.lstDat[0]!='minus' and self.lstDat[0]!="starTime" and self.lstDat[0]!="wrong" and self.lstDat[0]!="clear":
            # create a canvas
            canvasPainter = QPainter(self)
            # draw rectangle  on the canvas
            canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
            painter = QPainter(self.image)

            for i in self.coLst:
                if (self.lstDat[4] == str(i)):
                    col = i

            painter.setPen(QPen(col, int(self.lstDat[5])))
            painter.drawLine(int(self.lstDat[0]), int(self.lstDat[1]), int(self.lstDat[2]), int(self.lstDat[3]))
        else:
            canvasPainter = QPainter(self)
            # draw rectangle  on the canvas
            canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        self.update()