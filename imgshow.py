
import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example(QWidget):


    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.lbl = QLabel(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()

    def changeim(self,src):
        pixmap = QPixmap(src)
        self.lbl.setPixmap(pixmap)


def cv2_to_qimage(cv_img):

    height, width, bytesPerComponent = cv_img.shape
    bgra = np.zeros([height, width, 4], dtype=np.uint8)
    bgra[:, :, 0:3] = cv_img
    return QImage(bgra.data, width, height, QImage.Format_RGB32)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()


    vid = cv2.VideoCapture("test.avi")
    while (vid.isOpened()):
        ret, frame = vid.read()
        if ret==False:
            break
        src = cv2_to_qimage(frame)
        ex.changeim(src)
        #cv2.imshow("frames",frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break




    sys.exit(app.exec_())
