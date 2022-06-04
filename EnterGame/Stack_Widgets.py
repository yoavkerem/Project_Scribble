from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets

App = QApplication(sys.argv)
global widget
widget=QtWidgets.QStackedWidget()



def widgetAddLog(login,reg,f,s):
    widget.setFixedHeight(591)
    widget.setFixedWidth(811)
    widget.addWidget(login)
    widget.addWidget(reg)
    widget.addWidget(f)
    widget.addWidget(s)
    widget.setCurrentIndex(3)
    widget.show()
    App.exec()

def widgetAddWait(w):
    widget.addWidget(w)
    widget.move(250, 70)
    widget.setFixedWidth(811)
    widget.setFixedHeight(591)
    widget.setCurrentIndex(4)
    widget.show()
    App.exec()