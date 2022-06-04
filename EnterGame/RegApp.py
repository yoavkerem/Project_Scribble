from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.uic import loadUi

from EnterGame import Stack_Widgets

class RegApp(QDialog):
    def __init__(self,client):
        super(RegApp, self).__init__()
        self.client = client
        loadUi("pyQt5Signin.ui",self)
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)

    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()
        self.client.send_request_to_server('S'+un+' '+pw+' '+em)
        result = self.client.handle_client_response()
        self.tb3.setText("")
        self.tb4.setText("")
        self.tb5.setText("")
        print(result)
        if result=='empty':
            QMessageBox.information(self, "Login form", "username or password aren't valid")
        elif result=='not valid':
            QMessageBox.information(self, "Login form", "There was problem with the registration")
        else:
            QMessageBox.information(self, "Login form", "The user registered successfully, You can login now!")
            self.show_login()


    def show_login(self):
        Stack_Widgets.widget.setCurrentIndex(0)