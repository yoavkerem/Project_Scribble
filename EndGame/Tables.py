from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

num=0
class Table(QDialog):
    def __init__(self,c,num_of_players):
        super(Table,self).__init__()
        loadUi("stats and results.ui",self)
        self.c=c
        print(33)

        self.num_of_players =num_of_players

        self.tableWidget.setColumnWidth(0,117)
        self.tableWidget.setColumnWidth(1, 117)
        self.tableWidget2.setColumnWidth(0, 70)
        self.tableWidget2.setColumnWidth(1, 70)
        self.tableWidget2.setColumnWidth(2, 152)
        self.loaddata()

    def loaddata(self):
        dataLst=[]
        for i in range(self.num_of_players):
            data=self.c.handle_client_response().split(' ')
            name=data[0]
            points=data[1]
            dataLst.append((name,points))
        data=self.c.handle_client_response().split(' ')
        tempLst=dataLst
        newLst=[]

        i=0
        while i<self.num_of_players:
            print(i)
            max=self.maxPlayer(tempLst)
            tempLst.remove(max)
            newLst.append(max)
            i+=1

        self.tableWidget.setRowCount(self.num_of_players)
        self.tableWidget2.setRowCount(1)
        row=0
        for person in newLst:
            self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(person[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person[1])))
            row+=1
        avg=float(int(data[0])/int(data[2]))
        self.tableWidget2.setItem(0, 0, QtWidgets.QTableWidgetItem(data[2]))
        self.tableWidget2.setItem(0, 1, QtWidgets.QTableWidgetItem(data[1]))
        avg=("%.2f" % avg)
        self.tableWidget2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(avg)))

    def maxPlayer(self,tempLst):
        max=tempLst[0]
        print(tempLst)
        for i in tempLst:
            if int(i[1])>int(max[1]):
                max=i
        print('max' +max[1])
        return max