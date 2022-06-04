from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from EnterGame import Stack_Widgets

class FullGame(QDialog):
    def __init__(self,isFull):
        super(FullGame, self).__init__()
        loadUi("fullGame.ui", self)
        self.isFull = isFull
        self.b6.clicked.connect(self.exit)
    def exit(self):
        self.isFull = True
        Stack_Widgets.widget