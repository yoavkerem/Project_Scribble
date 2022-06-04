from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Timer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Timer')
        self.setGeometry(900, 100, 0, 80)
        self.count = 300
        # start flag
        self.start = False

        # creating label to show the seconds
        self.label = QLabel("//TIMER//", self)

        # setting geometry of label
        self.label.setGeometry(0,0 , 160, 80)

        # setting border to the label
        self.label.setStyleSheet("border : 3px solid black")

        # setting font to the label
        self.label.setFont(QFont('Times', 15))

        # setting alignment ot the label
        self.label.setAlignment(Qt.AlignCenter)
        self.start_action()

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every tenth second
        timer.start(100)


    def showTime(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1

            # timer is completed

            if self.count == 0 :
                # making flag false
                self.start = False
                #QMessageBox.about(self, "Over", "Time is over")

                # setting text to the label

            if self.start:
                # getting text from count
                text = str(self.count / 10) + " s"

                # showing text
                self.label.setText(text)

    def start_action(self):
        # making flag true
        self.start = True
        # count = 0
        if self.count == 0:
            self.start = False
