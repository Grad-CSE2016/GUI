from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget,QGridLayout, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit,QTableView,QTableWidget)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import (Qt,QThread,QFile)
from PyQt5 import QtSql

class report(QWidget):
    def __init__(self,db_view):
        self.db_view=db_view
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 20, 250, 150)
        self.setWindowTitle('Daily Report')
        query = QtSql.QSqlQuery()
        query.exec("SELECT sessionID FROM logs");
        if(query.last()):
            self.sessionID=query.value(0)
        queryStr=("SELECT svalue FROM logs WHERE sessionID=%d AND stype='tracking' "%self.sessionID)
        query.exec(queryStr)
        if(query.last()):
            self.totalCount=query.value(0)
        queryStr=("SELECT svalue,date,time FROM logs WHERE sessionID=%d AND stype='count' "%self.sessionID)
        query.exec(queryStr)
        while (query.next()):
             print(query.value(0))
             print(query.value(1))
             print(query.value(2))
