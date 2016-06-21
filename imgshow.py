import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,QFileDialog,
    QLabel, QApplication,  QMainWindow, QAction, qApp)
from PyQt5.QtGui import QPixmap,QIcon

import Tracking


class Example(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.lbl = QLabel(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.lbl)
        parentBox=QWidget(self)
        parentBox.setLayout(hbox)
        self.setCentralWidget(parentBox)

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


def play(src):
    vid = cv2.VideoCapture("test.avi")
    ret, frame = vid.read()
    while (ret):
        out=tracker.get_frame(frame)
        src = cv2_to_qimage(out)
        ex.changeim(src)
        #cv2.imshow("frames",frame)
        ret, frame = vid.read()
        cv2.waitKey(1)


app = QApplication(sys.argv)
ex = Example()
tracker=Tracking.Tracking()
sys.exit(app.exec_())
