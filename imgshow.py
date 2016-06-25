import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp,QVBoxLayout,QCheckBox,QTextEdit)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt

import Tracking


class Example(QMainWindow):
    tracking = "Tracking"
    luggage = "Luggage"
    actions = "Action Recognition"
    falling = "Falling"
    log_msg = ""
    tracking_flag = False
    luggage_flag = False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

    def button_Pressed(self,btn):
        if btn.isChecked() == True:
            #self.log_msg = self.log_msg  + btn.text()+ " Started ..."
            #self.logs.setText(self.log_msg)
            #self.logs.insertPlainText(self.log_msg)
            self.log_msg = btn.text() + " Started ..."
            self.logs.append(self.log_msg)
            if btn.text() == self.tracking:
                #call tracking file
                self.tracking_flag = True
                pass
            elif btn.text() == self.luggage:
                #call luggage file
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
                pass
            elif btn.text() == self.actions:
                #call action recognition file
                pass
            elif btn.text() == self.falling:
                #call falling file
                pass
            #self.log_msg = self.log_msg + "\n" + btn.text()+ " Turned off ..."
            #self.logs.setText(self.log_msg)

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


def cv2_to_qimage(cv_img):

    height, width, bytesPerComponent = cv_img.shape
    bgra = np.zeros([height, width, 4], dtype=np.uint8)
    bgra[:, :, 0:3] = cv_img
    return QImage(bgra.data, width, height, QImage.Format_RGB32)

def changeFileSrc(src):
    play(src)

def draw(frame,coordinates):
    for coordinate in coordinates:
        x,y,w,h = coordinate
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
    return frame

def play(src):
    vid = cv2.VideoCapture("test.avi")
    ret, frame = vid.read()
    while (ret):
        if gui.tracking_flag == True:
            out = tracker.get_frame(frame)
            frame = draw(frame,out)
        if gui.luggage_flag == False:
            pass

        #cv2.imshow("frames",frame)
        src = cv2_to_qimage(frame)
        gui.changeim(src)


        ret, frame = vid.read()
        cv2.waitKey(1)

app = QApplication(sys.argv)
gui = Example()
tracker=Tracking.Tracking()
sys.exit(app.exec_())
