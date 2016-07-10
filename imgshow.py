import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget,QGridLayout, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit,QTableView,QTableWidget)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import (Qt,QThread,QFile)
from PyQt5 import QtSql
import time
from threading import Thread
from datetime import datetime
import xlwt
import report

from io import StringIO,BytesIO

sys.path.append('./Abandoned-Object-Detection')
from AbandonedObjectDetection import *

sys.path.append('./TrackingPeople')
from TrackingPeople import *
maxHeight=520;
maxWidth=600;
class Example(QMainWindow):
    tracking = "Tracking"
    luggage = "Luggage"
    actions = "Action Recognition"
    falling = "Falling"
    log_msg = ""
    tracking_flag = False
    luggage_flag = False
    luggage_coordinates = []


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.db_view = self.create_DB()
        self.sessionID=self.get_SessionId()
        global maxHeight
        global maxWidth
        self.maxHeight=maxHeight
        self.maxWidth=maxWidth
        show_db = QPushButton("Open Database",self)
        show_db.clicked.connect(lambda:self.show_db(self.db_view))
        export_db = QPushButton("Export Database",self)
        export_db.clicked.connect(lambda:self.savefile())

        pixmap = QPixmap("back.jpg")

        # pixmap= pixmap.scaled(self.maxWidth,self.maxHeight);
        pixmap=pixmap.scaledToHeight(self.maxHeight)
        self.lbl = QLabel(self)
        # self.lbl.setFixedWidth(self.maxWidth)
        self.lbl.setFixedHeight(self.maxHeight)
        self.lbl.setPixmap(pixmap)
        hbox = QVBoxLayout(self)
        hbox.setAlignment(Qt.AlignCenter);
        hbox.addWidget(self.lbl)

        parentVideoBox=QWidget(self)
        parentVideoBox.setStyleSheet("background-color:#121A21");
        parentVideoBox.setLayout(hbox)
        # parentVideoBox.setCentralWidget(self.lbl)

        vbox = QHBoxLayout(self)
        tracking = QCheckBox(self.tracking)
        luggage= QCheckBox(self.luggage)
        actions = QCheckBox(self.actions)
        falling = QCheckBox(self.falling)

        vbox.addWidget(tracking)
        vbox.addWidget(luggage)
        vbox.addWidget(actions)
        vbox.addWidget(falling)

        vbox.addWidget(show_db)
        vbox.addWidget(export_db)


        #hbox.addLayout(vbox)
        # hbox.addStretch(1)

        self.logs = QTextEdit(self)
        self.logs.setReadOnly(True)
        self.logs.setLineWrapMode(QTextEdit.NoWrap)
        self.logs.setMaximumHeight(200)

        vbox2 = QVBoxLayout(self)
        vbox2.addWidget(parentVideoBox)
        vbox2.addLayout(vbox)
        vbox2.addWidget(self.logs)




        parentBox=QWidget(self)
        parentBox.setLayout(vbox2)
        self.setCentralWidget(parentBox)
        tracking.stateChanged.connect(lambda:self.button_Pressed(tracking))
        luggage.stateChanged.connect(lambda:self.button_Pressed(luggage))
        actions.stateChanged.connect(lambda:self.button_Pressed(actions))
        falling.stateChanged.connect(lambda:self.button_Pressed(falling))

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)


        showReport = QAction(QIcon('open.png'), 'Report', self)
        showReport.setShortcut('Ctrl+R')
        showReport.setStatusTip('Show Report')
        showReport.triggered.connect(self.showReport)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(showReport)

        self.setGeometry(300, 20, 600, 700)
        self.setWindowTitle('Horas Surveillance System')
        self.show()
    def show_db(self,tableview):
        #self.w = MyPopup()
        #self.w.show()
        tableview.horizontalHeader().setStretchLastSection(True)
        tableview.setGeometry(300, 300, 1000, 1000)
        tableview.show()

    def create_DB(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("surveillance.db")
        db.open()
        if not db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
            QtGui.qApp.tr("Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information "
            "how to build it.\n\n" "Click Cancel to exit."),
            QtGui.QMessageBox.Cancel)
            return False

        model = QtSql.QSqlTableModel(self,db)
        model.setTable("logs")
        model.select()
        self.model = model


        #tableview = QTableWidget()
        tableview = QTableView()
        tableview.setModel(model)


        query = QtSql.QSqlQuery()
        query.exec_("create table logs(date text , time text ,sessionID number, log text ,stype text,svalue number)")
        return tableview
    def get_SessionId(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT sessionID FROM logs");
        if(query.last()):
            return(query.value(0)+1)
        else:
            return(1)
    def insert_DB(self,text,stype='',svalue=0):
        query = QtSql.QSqlQuery()
        #query.exec_("insert into logs values(date('now'),time('now'), ?)",(text))
        query.prepare("INSERT INTO logs(date,time,log,stype,svalue,sessionID) VALUES (?,?,?,?,?,?)")
        date = datetime.now().date()
        time = datetime.now().time()
        date = date.strftime('%m/%d/%Y')
        time = time.strftime('%H:%M:%S')

        query.addBindValue(date)
        query.addBindValue(time)
        query.addBindValue(text)
        query.addBindValue(stype)
        query.addBindValue(svalue)
        query.addBindValue(self.sessionID)


        if not query.exec_():
            print(query.lastError().text())

    def button_Pressed(self,btn):
        if btn.isChecked() == True:
            self.log_msg = btn.text() + " Started ..."
            self.logs.append(self.log_msg)
            if btn.text() == self.tracking:
                #call tracking file
                self.tracking_flag = True
                pass
            elif btn.text() == self.luggage:
                #call luggage file
                self.luggage_flag = True
                pass
            elif btn.text() == self.actions:
                #call action recognition file
                pass
            elif btn.text() == self.falling:
                #call falling file
                pass
        else:
            self.log_msg = btn.text() + " Turned Off ..."
            self.logs.append(self.log_msg)
            if btn.text() == self.tracking:
                #call tracking file
                self.tracking_flag = False
                pass
            elif btn.text() == self.luggage:
                #call luggage file
                self.luggage_flag = False
                pass
            elif btn.text() == self.actions:
                #call action recognition file
                pass
            elif btn.text() == self.falling:
                #call falling file
                pass
        self.insert_DB(self.log_msg)


    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                changeFileSrc(fname[0])
                #self.textEdit.setText(data)

    def changeim(self,src):
        pixmap = QPixmap(src)
        self.lbl.setPixmap(pixmap)

    def savefile(self):
        #filename = str(QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)"))
        #filename= str(QFileDialog.getSaveFileName(self,"saveFlle","",filter =".xls(*.xls)"))

        #f = QFile(filename);
        #f.open()



        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add2(sheet)
        wbk.save("exportedDB.xls")

    def add2(self, sheet):
        for currentColumn in range(3):
            for currentRow in range(self.model.rowCount()):
                try:
                    teext = str(self.model.data(self.model.index(currentRow, currentColumn)))
                    sheet.write(currentRow, currentColumn, teext)
                except AttributeError:
                    pass
    def showReport(self):
        self.report=report.report(self.db_view)
        self.report.show()

def cv2_to_qimage(cv_img):
    global maxWidth
    global maxHeight
    height, width, bytesPerComponent = cv_img.shape
    bgra = np.zeros([height, width, 4], dtype=np.uint8)
    bgra[:, :, 0:3] = cv_img
    pixmap=QImage(bgra.data, width, height, QImage.Format_RGB32)
    pixmap = pixmap.scaledToHeight(maxHeight)
    return pixmap

def changeFileSrc(src):
    #   t = Thread(target=play, args=(src,))
    #   t.start()
    play(src)

def draw(frame,coordinates):
    for coordinate in coordinates:
        if len(coordinate) == 4:
            x,y,w,h = coordinate
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        elif len(coordinate) == 5:
            x,y,w,h,_ = coordinate
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
            if coordinate not in gui.luggage_coordinates:
                gui.logs.append("Unattended Luggage Detected !")
                gui.insert_DB("Unattended Luggage Detected !")
                gui.luggage_coordinates.append(coordinate)
colours = np.array([[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0],[128,0,0],[0,128,0],[0,0,128],[128,128,0],[0,128,128],[128,0,128]])
font = cv2.FONT_HERSHEY_SIMPLEX
maxID=0
lastCount=0
lastMax=0
def drawPedesterian(frame,track_bbs_ids,detections,count):
    global lastCount
    global lastMax
    global maxID
    reductFramSize=15

    for(tracker)in detections:
        x1,y1,x2,y2=int(tracker[0]),int(tracker[1]),int(tracker[2]),int(tracker[3]);

        #cv2.rectangle(frame,(x1+reductFramSize,y1+reductFramSize),(x2-reductFramSize, y2-reductFramSize),(255,0,0),2)


    for(tracker)in track_bbs_ids:
        x1,y1,x2,y2,n=int(tracker[0]),int(tracker[1]),int(tracker[2]),int(tracker[3]),int(tracker[4]),;
        #print(tracker)
        if(n>maxID):
            maxID=n
        color=colours[n%len(colours),:]
        B=int(color[0])
        R=int(color[1])
        G=int(color[2])
        cv2.putText(frame,str(n),(x1,y1), font, 1, (R,G,B), 2, cv2.LINE_AA)
        cv2.rectangle(frame,(x1+reductFramSize,y1+reductFramSize),(x2-reductFramSize, y2-reductFramSize),(R,G,B),2)
    cv2.putText(frame,str(count),(0,50), font, 2, (0,255,0), 2, cv2.LINE_AA)
    cv2.putText(frame,str(len(track_bbs_ids)),(0,100), font, 2, (0,0,255), 2, cv2.LINE_AA)
    if(lastCount!=count):
        lastCount=count
        gui.logs.append("people tracked now "+str(len(track_bbs_ids)))
        gui.insert_DB("people tracked now "+str(len(track_bbs_ids)),"count",str(len(track_bbs_ids)))
    if(lastMax!=maxID):
        lastMax=maxID
        gui.logs.append("people count from start "+str(count))
        gui.insert_DB("people count from start "+str(count),"tracking",str(count))
def play(src):
    vid = cv2.VideoCapture(src)
    BG = cv2.imread('./Abandoned-Object-Detection/bg.jpg')

    aod = AbandonedObjectDetection(vid, BG)
    tracker=TrackingPeople()

    thread1  = QThread()
    thread2  = QThread()
    start_time = time.time()
    end_time = time.time()
    while (1):
        start_time = time.time()
        if(start_time-end_time<0.04):
            while(time.time()-end_time<0.04):
                x=1
        ret, frame = vid.read()
        if(not(ret)):return
        if gui.tracking_flag == True:
            trackers,detections,peopleCount=tracker.get_frame(frame)
            drawPedesterian(frame,trackers,detections,peopleCount)
            #draw(frame,detections)


            # tracker.moveToThread(thread1)
            #
            # tracker.get_frame(frame)
            #
            # tracker.calc_bounding.connect(draw)
            # thread1.start()



            #self.stopButton.clicked.connect(self.simulRunner.stop)

            # start the execution loop with the thread:
            #self.simulThread.started.connect(self.simulRunner.longRunning)

            #out = tracker.get_frame(frame)
            #frame = draw(frame,out)
        if gui.luggage_flag == True:
            objs = aod.get_abandoned_objs(frame)
            draw(frame,objs)


        #cv2.imshow("frames",frame)
        src = cv2_to_qimage(frame)
        gui.changeim(src)
        end_time = time.time()
        cv2.waitKey(1)

app = QApplication(sys.argv)
app.setStyle('Fusion')

gui = Example()

sys.exit(app.exec_())
