from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from EnterGame import Stack_Widgets

class LoginApp(QDialog):
    def __init__(self,client):
        super(LoginApp, self).__init__()
        self.client=client
        self.logged=False
        self.numPlyers=0
        self.rigtNow=0
        loadUi("pyQt5Login.ui",self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)


    def login(self):
        un=self.tb1.text()
        pw=self.tb2.text()
        self.client.send_request_to_server("L"+ un + " "+pw)
        result=self.client.handle_client_response().split(' ')
        self.tb1.setText("")
        self.tb2.setText("")
        if result[0]=='suitability':

            self.numPlyers=result[1]
            self.rigtNow=result[2]
            self.logged = True
            QMessageBox.information(self,"Login Output", "Congrats! You login successfully!")
            Stack_Widgets.widget.close()
        elif result[0] =='unsuitability':
            QMessageBox.information(self, "Login Output", "Invalid User.. Register for new user!")

        else:
            Stack_Widgets.widget.setFixedHeight(591)
            Stack_Widgets.widget.setFixedWidth(811)
            Stack_Widgets.widget.setCurrentIndex(2)

    def show_reg(self):
        Stack_Widgets.widget.setCurrentIndex(1)
