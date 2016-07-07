import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit,QTableView,QTableWidget)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import (Qt,QThread,QFile)
from PyQt5 import QtSql
from datetime import datetime
import xlwt


from io import StringIO,BytesIO

sys.path.append('./Abandoned-Object-Detection')
from AbandonedObjectDetection import *

sys.path.append('./TrackingPeople')
from TrackingPeople import *

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
        db_view = self.create_DB()

        show_db = QPushButton("Open Database",self)
        show_db.clicked.connect(lambda:self.show_db(db_view))
        export_db = QPushButton("Export Database",self)
        export_db.clicked.connect(lambda:self.savefile())


        self.lbl = QLabel(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.lbl)

        vbox = QVBoxLayout(self)
        tracking = QCheckBox(self.tracking)
        luggage= QCheckBox(self.luggage)
        actions = QCheckBox(self.actions)
        falling = QCheckBox(self.falling)

        vbox.addWidget(tracking)
        vbox.addWidget(luggage)
        vbox.addWidget(actions)
        vbox.addWidget(falling)


        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.logs = QTextEdit(self)
        self.logs.setReadOnly(True)
        self.logs.setLineWrapMode(QTextEdit.NoWrap)
        self.logs.setMaximumHeight(200)

        vbox2 = QVBoxLayout(self)
        vbox2.addLayout(hbox)
        vbox2.addWidget(self.logs)
        vbox2.addWidget(show_db)
        vbox2.addWidget(export_db)


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

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('surveillance system')
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
        query.exec_("create table logs(date text , time text , log text )")
        return tableview

    def insert_DB(self,text):
        query = QtSql.QSqlQuery()
        #query.exec_("insert into logs values(date('now'),time('now'), ?)",(text))
        query.prepare("INSERT INTO logs(date,time,log) VALUES (?,?,?)")
        date = datetime.now().date()
        time = datetime.now().time()
        date = date.strftime('%m/%d/%Y')
        time = time.strftime('%H:%M:%S')

        query.addBindValue(date)
        query.addBindValue(time)
        query.addBindValue(text)

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

def cv2_to_qimage(cv_img):

    height, width, bytesPerComponent = cv_img.shape
    bgra = np.zeros([height, width, 4], dtype=np.uint8)
    bgra[:, :, 0:3] = cv_img
    return QImage(bgra.data, width, height, QImage.Format_RGB32)

def changeFileSrc(src):
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
colours = np.random.rand(32,3)
font = cv2.FONT_HERSHEY_SIMPLEX
maxID=0
lastCount=0
lastMax=0
def drawPedesterian(frame,track_bbs_ids,detections,count):
    global lastCount
    global lastMax
    global maxID
    reductFramSize=15
    for(tracker)in track_bbs_ids:
        x1,y1,x2,y2,n=int(tracker[0]),int(tracker[1]),int(tracker[2]),int(tracker[3]),int(tracker[4]),;
        #print(tracker)
        if(n>maxID):
            maxID=n
        color=colours[n%32,:]
        B=int(color[0]*255)
        R=int(color[1]*255)
        G=int(color[2]*255)
        cv2.putText(frame,str(n),(x1,y1), font, 1, (R,G,B), 2, cv2.LINE_AA)
        cv2.rectangle(frame,(x1+reductFramSize,y1+reductFramSize),(x2-reductFramSize, y2-reductFramSize),(R,G,B),2)
    cv2.putText(frame,str(count),(0,50), font, 2, (0,255,0), 2, cv2.LINE_AA)
    if(lastCount!=count):
        lastCount=count
        gui.logs.append("people count now "+str(count))
        gui.insert_DB("people count now "+str(count))
    if(lastMax!=maxID):
        lastMax=maxID
        gui.logs.append("people count from start "+str(maxID))
        gui.insert_DB("people count  from start "+str(maxID))
def play(src):
    vid = cv2.VideoCapture(src)
    BG = cv2.imread('./Abandoned-Object-Detection/bg.jpg')

    aod = AbandonedObjectDetection(vid, BG)

    thread1  = QThread()
    thread2  = QThread()
    while (1):
        ret, frame = vid.read()
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
        cv2.waitKey(1)

app = QApplication(sys.argv)
app.setStyle('Fusion')
tracker=TrackingPeople()
gui = Example()

sys.exit(app.exec_())
