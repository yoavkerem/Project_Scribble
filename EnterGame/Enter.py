import sys
from Client_pack import Client_oop
from EnterGame import RegApp
from EnterGame import LoginApp
from EnterGame import FullGame
from EnterGame import WaitingWind
from EnterGame import Stack_Widgets
from EnterGame import StartGame

class Enter:

    with open('datas.txt', 'r') as f:
        data_list = []
        for line in f:
             data_list.append(line.split(' ')[1][:-1])
    c = Client_oop.Client(str(data_list[0]),int(data_list[1]))
    # create pyqt5 app
    #App = QApplication(sys.argv)
    loginform = LoginApp.LoginApp(c)
    f = FullGame.FullGame(False)
    s = StartGame.StartGame()
    registrationform = RegApp.RegApp(c)
    Stack_Widgets.widgetAddLog(loginform,registrationform,f,s)

    if loginform.logged==False:
        sys.exit()
    if f.isFull==True:
        sys.exit()
    num_of_players = loginform.numPlyers
    rightNow=loginform.rigtNow
    w = WaitingWind.WaitingWind(c, num_of_players,rightNow)
    Stack_Widgets.widgetAddWait(w)
    if w.wait == False:
        sys.exit()


