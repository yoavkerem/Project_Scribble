from PyQt5.QtWidgets import QApplication
import sys
from EnterGame import Enter
from Game import Passive_Painter
from Game import Network_Passive
from Game import Active_Painter
from Game import Network_Active
class MainGame:
        App = QApplication(sys.argv)
        e=Enter.Enter()
        c=e.c
        num_of_players=e.num_of_players
        points = 0
        for i in range(int(num_of_players)):
            if (e.c.handle_client_response() == 'Not painter'):
                pas = Passive_Painter.Passive_Painter(c)
                network_handler = Network_Passive.Network(c, pas, points)
                pas.show()
                network_handler.loop()
                App.exec()
                points += network_handler.points
                if network_handler.minus == True:
                     num_of_players = str(int(num_of_players) - 1)
            else:
                words = c.handle_client_response()
                words = words.split('&')
                act = Active_Painter.Act_Painter(c, words)
                actNet = Network_Active.actNetwork(c, act)
                # showing the window
                act.show()
                # start the app
                actNet.loop()
                App.exec()
                if actNet.minus == True:
                    num_of_players = str(int(num_of_players) - 1)
            if i != int(num_of_players) - 1:
                c.send_request_to_server("Time over")
            else:
                break
