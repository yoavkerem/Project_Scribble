from PyQt5.QtWidgets import *
import select
from PyQt5 import QtCore

class actNetwork():
    def __init__(self,client,painter):
        self.client = client
        self.painter = painter
        self.minus = False
        self.startLoop=True

    def iterationBody(self):
        global lstDat
        lstDat = []

        infds, outfds, errfds = select.select([self.client.my_socket], [], [], 0.00000000000001)
        if len(infds) != 0:
            data = self.client.handle_client_response()
            print(data)
            if len(data) != 0:
                if data == "done":
                    self.showDialog('Everybody Guessed', "Everybody guessed correctly!")
                    self.startLoop = False
                    self.painter.close()
                    self.painter.timer.close()
                elif data=='minus':
                    self.minus = True


    def loop(self):
        if self.startLoop == True:
            if self.painter.timer!= None and self.painter.timer.count==0:
                self.showDialog('Time Over', "The time is over...")
                self.startLoop = False
                self.painter.close()
                self.painter.timer.close()
            self.iterationBody()
            QtCore.QTimer.singleShot(1, self.loop)

    def showDialog(self,title,content):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(content)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()