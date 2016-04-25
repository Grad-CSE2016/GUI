
import cv2
import numpy as np
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QPushButton,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def cv2_to_qimage(self,cv_img):

        height, width, bytesPerComponent = cv_img.shape
        bgra = np.zeros([height, width, 4], dtype=np.uint8)
        bgra[:, :, 0:3] = cv_img
        return QImage(bgra.data, width, height, QImage.Format_RGB32)


    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.lbl = QLabel(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)
        hbox.addWidget(btn1)
        btn1.clicked.connect(self.buttonClicked)           

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()

    def changeim(self,src):
        pixmap = QPixmap(src)
        self.lbl.setPixmap(pixmap)
    def buttonClicked(self):
        img=cv2.imread("img2.bmp")
        src=self.cv2_to_qimage(img)
        self.changeim(src)

def cv2_to_qimage(cv_img):

    height, width, bytesPerComponent = cv_img.shape
    bgra = np.zeros([height, width, 4], dtype=np.uint8)
    bgra[:, :, 0:3] = cv_img
    return QImage(bgra.data, width, height, QImage.Format_RGB32)



if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    ex = Example()

    
    img=cv2.imread("img.bmp")
    
    src=cv2_to_qimage(img)
    ex.changeim(src)
    vid = cv2.VideoCapture("test.avi")
    while True:
        ret, frame = vid.read()
        src = cv2_to_qimage(frame)
        ex.changeim(src)
        cv2.imshow("frames",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




    sys.exit(app.exec_())
