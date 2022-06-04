from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from EnterGame import Stack_Widgets

class StartGame(QDialog):
    def __init__(self):
        super(StartGame, self).__init__()
        loadUi("startWindow.ui", self)
        self.b7.clicked.connect(self.login)
    def login(self):
        Stack_Widgets.widget.setFixedHeight(500)
        Stack_Widgets.widget.setFixedWidth(400)
        Stack_Widgets.widget.setGeometry(450, 100, 400, 500)
        Stack_Widgets.widget.setCurrentIndex(0)