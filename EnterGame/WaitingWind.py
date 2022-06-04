import select
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.uic import loadUi
from EnterGame import Stack_Widgets


class WaitingWind(QDialog):
    def __init__(self,c,numofPlayers,rightNow):
        super(WaitingWind, self).__init__()
        loadUi("WaitingWindow.ui",self)
        self.wait=False
        self.num_of_players=numofPlayers
        self.rightNow=rightNow
        self.c=c
        self.label = QLabel(self.rightNow+" / "+self.num_of_players, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(QFont('Ariel', 12))

        # setting geometry of label
        self.label.setGeometry(300, 200, 200, 60)

        # setting border to the label
        self.label.setStyleSheet("border : 3px solid black")
        self.b9=QPushButton("READY",self)
        self.b9.setGeometry(300, 450, 200, 60)
        self.stop=False
        self.b9.clicked.connect(self.logged)


    def start(self):

        infds, outfds, errfds = select.select([self.c.my_socket], [], [],0.1)
        if len(infds) != 0:

            data=self.c.handle_client_response().split(' ')
            print(data)
            if data[0]=="start":
                self.wait=True
                self.stop=True
                Stack_Widgets.widget.close()
            if data[0]=='plus':
                self.rightNow=str(int(self.rightNow)+1)
                text = str(self.rightNow+" / "+self.num_of_players)
                # showing text
                self.label.setText(text)

    def loop(self):
        if self.stop==False:
            self.b9.hide()
            self.start()
            QtCore.QTimer.singleShot(10,self.loop)

    def logged(self):
        self.c.send_request_to_server("logged in")
        self.loop()
