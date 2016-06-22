import cv2
import sys, getopt
import numpy as np



class Tracking():
    def __init__(self):
        mog_er_w = 7
        mog_er_h = 7
        mog_di_w = 16
        mog_di_h = 26
        cv2.ocl.setUseOpenCL(False)
        self.bgs_mog = cv2.createBackgroundSubtractorMOG2()
        self.for_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(mog_er_w, mog_er_h))
        self.for_di = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(mog_di_w, mog_di_h))

    def get_frame(self,f):
        grey_image = self.bgs_mog.apply(f)
        thresh, im_bw = cv2.threshold(grey_image, 225, 255, cv2.THRESH_BINARY)
        im_er = cv2.erode(im_bw, self.for_er)
        im_dl = cv2.dilate(im_er, self.for_di)
        _, contours, hierarchy = cv2.findContours(im_dl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coordinates = []
        for cnt in contours:
            try:
                x,y,w,h = cv2.boundingRect(cnt)
                #cv2.rectangle(f, (x,y), (x+w, y+h), (255,0,0), 2)
                coordinates.append((x,y,w,h))
            except:
                print ("Bad Rect")
        #cv2.drawContours(f,contours,-1,(0,255,0),1)

        return coordinates
