from PyQt5.QtWidgets import QApplication
import sys
from Game import MainGame
from PyQt5 import QtWidgets
from EndGame import Tables

class EndGame:
    App = QApplication(sys.argv)
    mg=MainGame.MainGame()
    c=mg.c
    points=mg.points
    c.send_request_to_server("end " + str(points))
    num_of_players=mg.num_of_players
    t = Tables.Table(c, int(num_of_players))
    widget2 = QtWidgets.QStackedWidget()
    widget2.addWidget(t)
    widget2.setFixedWidth(800)
    widget2.setFixedHeight(581)
    widget2.show()
    App.exec()

