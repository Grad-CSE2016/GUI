import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit,QTableView)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import (Qt,QFile)
from PyQt5 import QtSql
import time
from datetime import datetime
import xlwt
import report
from io import StringIO,BytesIO
sys.path.append('./Abandoned-Object-Detection')
#from AbandonedObjectDetection import *
sys.path.append('./TrackingPeople')
from TrackingPeople import *

maxHeight=520;
maxWidth=600;

class Gui(QMainWindow):
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
        self.engine = Engine()
        self.logger = Logger()

    def initUI(self):
        """Initialize GUI user interface elements"""
        self.db_view = self.create_DB()
        self.sessionID=self.get_SessionId()
        global maxHeight
        global maxWidth
        self.maxHeight=maxHeight
        self.maxWidth=maxWidth
        show_logs = QPushButton("Open Database",self)
        show_logs.clicked.connect(lambda:self.show_logs(self.db_view))
        export_db = QPushButton("Export Database",self)
        export_db.clicked.connect(lambda:self.savefile())

        pixmap = QPixmap("back.jpg")
        pixmap=pixmap.scaledToHeight(self.maxHeight)

        self.lbl = QLabel(self)
        self.lbl.setFixedHeight(self.maxHeight)
        self.lbl.setPixmap(pixmap)

        hbox = QVBoxLayout(self)
        hbox.setAlignment(Qt.AlignCenter);
        hbox.addWidget(self.lbl)

        parentVideoBox=QWidget(self)
        parentVideoBox.setStyleSheet("background-color:#121A21");
        parentVideoBox.setLayout(hbox)

        vbox = QHBoxLayout(self)
        tracking = QCheckBox(self.tracking)
        luggage= QCheckBox(self.luggage)
        actions = QCheckBox(self.actions)
        falling = QCheckBox(self.falling)

        vbox.addWidget(tracking)
        vbox.addWidget(luggage)
        vbox.addWidget(actions)
        vbox.addWidget(falling)

        vbox.addWidget(show_logs)
        vbox.addWidget(export_db)

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
        openFile.triggered.connect(self.open_video)

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

    def show_logs(self,tableview):
        """Presents tableview as a pop up"""
        tableview.horizontalHeader().setStretchLastSection(True)
        tableview.setGeometry(300, 300, 1000, 1000)
        tableview.show()


    def create_DB(self):
        """Creates SQLite database or uses already created one"""
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
        tableview = QTableView()
        tableview.setModel(model)
        query = QtSql.QSqlQuery()
        query.exec_("create table logs(date text , time text ,sessionID number, log text ,stype text,svalue number)")
        return tableview

    def get_SessionId(self):
        """returns session ID from database"""
        query = QtSql.QSqlQuery()
        query.exec("SELECT sessionID FROM logs");
        if(query.last()):
            return(query.value(0)+1)
        else:
            return(1)

    def open_video(self):
        """Choose any video from dataset to be opened"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                self.changeFileSrc(fname[0],self.engine)

    def changeim(self,src):
        """Converts image and embeds it in PyQt interface"""
        pixmap = QPixmap(src)
        self.lbl.setPixmap(pixmap)

    def savefile(self):
        """Export database to an excel file"""
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add2(sheet)
        wbk.save("exportedDB.xls")

    def add2(self, sheet):
        """helper method for exporting database to an excel file"""
        for currentColumn in range(3):
            for currentRow in range(self.model.rowCount()):
                try:
                    teext = str(self.model.data(self.model.index(currentRow, currentColumn)))
                    sheet.write(currentRow, currentColumn, teext)
                except AttributeError:
                    pass

    def showReport(self):
        """displays report"""
        self.report=report.report(self.db_view)
        self.report.show()

    def changeFileSrc(self,src,engine):
        """calls engine to play the choosen video"""
        engine.play(src)

    def button_Pressed(self,btn):
        """triggers flags to set modules on/off,showing any actions in the logs 
        it's called when any checkbox is pressed"""
        if btn.isChecked() == True:
            log_msg = btn.text() + " Started ..."
            self.logger.save_log(log_msg)

            if btn.text() == self.tracking:
                self.tracking_flag = True
                pass
            elif btn.text() == self.luggage:
                self.luggage_flag = True
                pass
            elif btn.text() == self.actions:
                pass
            elif btn.text() == self.falling:
                pass
        else:
            log_msg = btn.text() + " Turned Off ..."
            self.logger.save_log(log_msg)
            if btn.text() == self.tracking:
                self.tracking_flag = False
                pass
            elif btn.text() == self.luggage:
                self.luggage_flag = False
                pass
            elif btn.text() == self.actions:
                pass
            elif btn.text() == self.falling:
                pass
                       
class Logger:
    def save_log(self,text, stype='',svalue=0):
        """display text in the gui logs, and saves it offline"""
        gui.logs.append(text)
        self.insert_DB(text)

    def insert_DB(self,text,stype='',svalue=0):
        """creates a query to insert values to database"""
        query = QtSql.QSqlQuery()
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
        query.addBindValue(gui.sessionID)

        if not query.exec_():
            print(query.lastError().text())

class Drawer:
    def draw(self,frame,coordinates):
        """draws boxes around any abandoned luggage"""
        for coordinate in coordinates:
            if len(coordinate) == 4:
                x,y,w,h = coordinate
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            elif len(coordinate) == 5:
                x,y,w,h,_ = coordinate
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                if coordinate not in gui.luggage_coordinates:
                    gui.logs.append("Unattended Luggage Detected !")
                    gui.logger.insert_DB("Unattended Luggage Detected !","luggage")
                    gui.luggage_coordinates.append(coordinate)
 
    def drawPedesterian(self,frame,track_bbs_ids,detections,count):
        """draws boxes around people currently being tracked"""
        colours = np.array([[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0],[128,0,0],[0,128,0],[0,0,128],[128,128,0],[0,128,128],[128,0,128]])
        font = cv2.FONT_HERSHEY_SIMPLEX
        maxID=0
        lastCount=0
        lastMax=0
        global lastCount
        global lastMax
        global maxID
        reductFramSize=15

        for(tracker)in detections:
            x1,y1,x2,y2=int(tracker[0]),int(tracker[1]),int(tracker[2]),int(tracker[3]);

        for(tracker)in track_bbs_ids:
            x1,y1,x2,y2,n=int(tracker[0]),int(tracker[1]),int(tracker[2]),int(tracker[3]),int(tracker[4]),;
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
            gui.logger.insert_DB("people tracked now "+str(len(track_bbs_ids)),"count",str(len(track_bbs_ids)))
        if(lastMax!=maxID):
            lastMax=maxID
            gui.logs.append("people count from start "+str(count))
            gui.logger.insert_DB("people count from start "+str(count),"tracking",str(count))

    def cv2_to_qimage(self,cv_img):
        global maxWidth 
        global maxHeight
        height, width, bytesPerComponent = cv_img.shape
        bgra = np.zeros([height, width, 4], dtype=np.uint8)
        bgra[:, :, 0:3] = cv_img
        pixmap=QImage(bgra.data, width, height, QImage.Format_RGB32)
        pixmap = pixmap.scaledToHeight(maxHeight)
        return pixmap

class Engine:
    def play(self,src):
        """takes video path as an input, plays it, 
        calling any needed module to perform specific action on video frames during playing """
        vid = cv2.VideoCapture(src)
        BG = cv2.imread('./Abandoned-Object-Detection/bg.jpg')

        #aod = AbandonedObjectDetection(vid, BG)
        tracker=TrackingPeople()
        drawer = Drawer()

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
                drawer.drawPedesterian(frame,trackers,detections,peopleCount)

            if gui.luggage_flag == True:
                objs = aod.get_abandoned_objs(frame)
                drawer.draw(frame,objs)

            src = drawer.cv2_to_qimage(frame)
            gui.changeim(src)
            end_time = time.time()
            cv2.waitKey(1)

app = QApplication(sys.argv)
app.setStyle('Fusion')
gui = Gui()
sys.exit(app.exec_())
