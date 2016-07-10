from PyQt5.QtGui import QImage
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget,QGridLayout, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit,QTableView,QTableWidget)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import (Qt,QThread,QFile)
from PyQt5 import QtSql
import numpy as np
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random




class report(QWidget):
    def __init__(self,db_view):
        self.db_view=db_view
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 20, 700, 700)
        self.setWindowTitle('Daily Report')
        query = QtSql.QSqlQuery()
        query.exec("SELECT sessionID FROM logs");
        if(query.last()):
            self.sessionID=query.value(0)
        queryStr=("SELECT svalue FROM logs WHERE sessionID=%d AND stype='luggage' "%self.sessionID)
        query.exec(queryStr)
        luggageCount=query.size()

        queryStr=("SELECT svalue FROM logs WHERE sessionID=%d AND stype='actions' "%self.sessionID)
        query.exec(queryStr)
        actions=query.size()

        queryStr=("SELECT svalue FROM logs WHERE sessionID=%d AND stype='tracking' "%self.sessionID)
        query.exec(queryStr)
        if(query.last()):
            totalCount=query.value(0)
        queryStr=("SELECT svalue,date,time FROM logs WHERE sessionID=%d AND stype='count' "%self.sessionID)
        query.exec(queryStr)
        countingValues=[]

        while (query.next()):
            countingValues.append([query.value(2),query.value(0)])
        # print(countingValues)
        lbl = QLabel(self)
        text="<center><img src='logo.png' height=70>"
        text+="<h4> Total number of counts: <b style='color:red'>"+str(totalCount)+"</b></h4>"
        if(luggageCount==-1):
            luggageCount=0
        if(actions==-1):
            actions=0
        text+="<h4>Total number of Abandoned objects <b style='color:red'>"+str(luggageCount)+"<b></h4>"
        text+="<h4>Total number of Actions <b style='color:red'>"+str(actions)+"<b></h4>"
        data=np.asarray(countingValues)
        x=np.arange(len(data))
        fig, ax = plt.subplots()
        plt.xticks(x, data[:,0])
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 10))
        ax.plot(x, data[:,1])
        ax.grid(True)
        fig.autofmt_xdate()
        plt.savefig('report.jpg')
        text+="<h2><img src='report.jpg' width=700></center></h2>"
        # plt.show()
        lbl.setFixedWidth(700)
        lbl.setText(text)
        self.setStyleSheet("background-color:#FFF;");
