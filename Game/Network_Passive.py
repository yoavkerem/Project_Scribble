import select
from PyQt5 import QtCore
from Game import Timer
from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
class Network:

    def __init__(self, client,pas,points):
        self.points=points
        self.minus=False
        self.client = client
        self.pas=pas
        self.timer=None
        self.startLoop=True

    def iterationBody(self):
        infds, outfds, errfds = select.select([self.client.my_socket], [], [], 0.1)
        if len(infds) != 0:
            data = self.client.handle_client_response()
            self.pas.lstDat = data.split(' ')
            if len(data) != 0:
                if self.pas.lstDat[0]=="done":
                    self.showDialog('Everybody Guessed', "Everybody guessed correctly!")
                    self.startLoop = False
                    self.timer.close()
                    self.pas.close()
                elif self.pas.lstDat[0]=="true":
                    #QMessageBox.information(self, "right guess!!!"," You have guessed right!\nWait for the other's guesses or time over")
                    self.showDialog('Right Guess',"Well done, your guess is correct! \n Wait for others to guess correctly or for the time to be over...")
                    self.pas.setDisabled(True)
                    self.points=int(self.pas.lstDat[1])
                elif self.pas.lstDat[0]=='minus':
                    self.minus = True
                elif self.pas.lstDat[0]=="starTime" :
                    self.timer=Timer.Timer()
                    self.timer.show()
                elif self.pas.lstDat[0]=="wrong":
                    self.showDialog('Wrong Guess','Wrong guess, try again!')
                elif self.pas.lstDat[0]=="clear":
                    self.clear()


    def loop(self):
        if self.startLoop==True:
            if self.timer!=None and self.timer.count==0:
                self.showDialog('Time Over', "The time is over...")
                self.timer.close()
                self.pas.close()
                self.startLoop=False
            self.iterationBody()
            QtCore.QTimer.singleShot(1, self.loop)

    def clear(self):
        self.pas.image.fill(Qt.white)
            # update
        self.pas.update()

    def showDialog(self,title,content):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(content)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()