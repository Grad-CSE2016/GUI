#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we dispay an image
on the window.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
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

    def changeim(self,pixmap):

        self.lbl.setPixmap(pixmap)


if __name__ == '__main__':
    img=cv2.imread("img.png")
    cv2.imshow("test",img   )


    app = QApplication(sys.argv)
    src="img.png"
    pixmap = QPixmap(src)
    ex = Example()
    ex.changeim(pixmap)
    sys.exit(app.exec_())
